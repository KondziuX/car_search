from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, CustomUserCreationForm, \
                   ProfileForm, ProfileFormEditable, \
                   AdvertForm, EmailPriceForm, EmailPriceReminderForm, CommentForm
from .models import Profile, Advert, PriceReminderConnection, Notification
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import requests
from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .utils import evaluate_economy, evaluate_price, evaluate_eco_friendly, geocode_address, generate_map_link, save_search_criteria, load_search_criteria, clear_search_criteria, estimate_car_value
from django.utils import timezone
from django.http import HttpResponse
from ics import Calendar, Event
from datetime import datetime
from random import sample, shuffle
import pytz
from django.conf import settings
from .forms import FilterForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from carapp.templatetags.custom_filters import currency
from django.db.models import Q

def check_car_value(request):
    if request.method == 'POST':
        year = int(request.POST.get('year'))
        brand = request.POST.get('brand')
        model = request.POST.get('model')
        body_type = request.POST.get('body_type')
        mileage = int(request.POST.get('mileage'))
        power = int(request.POST.get('power'))

        estimated_value = estimate_car_value(year, brand, model, body_type, mileage, power)

        if estimated_value:
            min_price, max_price = estimated_value
            return JsonResponse({
                'status': 'success',
                'min_price': str(min_price),
                'max_price': str(max_price),
                'brand': brand,
                'model': model,
                'mileage': str(mileage),
                'year': str(year),
            })
        else:
            return JsonResponse({'status': 'error', 'message': 'Nie znaleziono podobnych pojazdów w bazie danych.'})
    return JsonResponse({'status': 'error', 'message': 'Nieprawidłowe żądanie.'})

@csrf_exempt
def compare_ads(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        ad_ids = data.get('ad_ids', [])
        adverts = Advert.objects.filter(id__in=ad_ids)
        ads_data = []
        for ad in adverts:
            equipment_list = get_equipment(ad)
            ads_data.append({
                'title': ad.title,
                'featured_image1': ad.featured_image1.url,
                'price': currency(ad.price),
                'brand': ad.brand,
                'model': ad.model if ad.model else "Brak danych",
                'variant': ad.variant,
                'first_registration': ad.first_registration,
                'engine_capacity': f"{ad.engine_capacity} cm³",
                'power': f"{ad.power} KM",
                'mileage': f"{ad.mileage} km",
                'fuel_type': ad.fuel_type.name,
                'city_fuel_consumption': f"{ad.city_fuel_consumption} L/100km",
                'highway_fuel_consumption':f"{ad.highway_fuel_consumption} L/100km",
                'combined_fuel_consumption': f"{ad.combined_fuel_consumption} L/100km",
                'co2_emission': f"{ad.co2_emission} g/km",
                'emission_class': ad.emission_class,
                'transmission': ad.transmission if ad.transmission else "Brak danych",
                'drive': ad.drive if ad.drive else "Brak danych",
                'eco_sticker': ad.eco_sticker,
                'no_crashed': ad.no_crashed,
                'damaged': ad.damaged if ad.damaged else "Brak danych",
                'condition': ad.condition if ad.condition else "Brak danych",
                'has_registration_number': ad.has_registration_number if ad.has_registration_number else "Brak danych",
                'registered_in_poland': ad.registered_in_poland if ad.registered_in_poland else "Brak danych",
                'registered_as_antique': ad.registered_as_antique if ad.registered_as_antique else "Brak danych",
                'first_owner': ad.first_owner if ad.first_owner else "Brak danych",
                'serviced_in_aso': ad.serviced_in_aso if ad.serviced_in_aso else "Brak danych",
                'imported': ad.imported if ad.imported else "Brak danych",
                'right_hand_drive': ad.right_hand_drive if ad.right_hand_drive else "Brak danych",
                'truck_approval': ad.truck_approval if ad.truck_approval else "Brak danych",
                'color': ad.color.title(),
                'color_type': ad.color_type.title(),
                'num_of_doors': ad.num_of_doors,
                'country_of_origin': ad.country_of_origin if ad.country_of_origin else "Brak danych",
                'equipment': equipment_list,
            })
        return JsonResponse(ads_data, safe=False)
    return JsonResponse({'error': 'Invalid request'}, status=400)


def get_recommended_adverts(request, exclude_ids=None, model=None):
    if exclude_ids is None:
        exclude_ids = []
    
    # Pobierz ostatnio przeglądane marki i modele przez użytkownika z sesji
    recently_viewed = request.session.get('recently_viewed', [])
    recently_viewed_brands_models = [(advert.brand, advert.model) for advert in Advert.objects.filter(id__in=recently_viewed)]
    
    # Filtruj ogłoszenia, aby pasowały do marki i modelu (jeśli podano) i nie były już wyświetlane
    query = {'brand__in': [brand for brand, model in recently_viewed_brands_models]}
    if model:
        query['model'] = model
    matching_adverts = Advert.objects.filter(**query).exclude(id__in=exclude_ids)
    
    available_adverts = list(matching_adverts)
    
    # Uzupełnij losowymi ofertami tylko jeśli jest mniej niż trzy dostępne auta
    # i tylko jeśli liczba dostępnych losowych ogłoszeń jest wystarczająca
    if len(available_adverts) < 3:
        random_adverts = Advert.objects.exclude(id__in=exclude_ids + [advert.id for advert in available_adverts])
        if model:
            random_adverts = random_adverts.filter(model=model)
        random_adverts = list(random_adverts)
        num_additional_adverts = min(3 - len(available_adverts), len(random_adverts))
        
        if num_additional_adverts > 0:
            additional_adverts = sample(random_adverts, num_additional_adverts)
            available_adverts.extend(additional_adverts)
    
    # Przetasuj i zwróć pierwsze trzy
    shuffle(available_adverts)
    return available_adverts[:3]

def generate_ics(request):
    date_str = request.GET.get('date')
    time_str = request.GET.get('time')

    if date_str and time_str:
        date_time_str = f"{date_str} {time_str}"
        viewing_datetime = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M").replace(tzinfo=pytz.utc)

        c = Calendar()
        e = Event()
        e.name = "Oglądanie pojazdu"
        e.begin = viewing_datetime
        e.duration = {'hours': 1}  # Zakładamy, że oglądanie trwa godzinę
        e.location = f"{request.GET.get('city')}, {request.GET.get('country')}"
        e.description = "Oglądanie pojazdu z ogłoszenia ID: " + request.GET.get('advert_id')

        c.events.add(e)
        ics_content = str(c)

        response = HttpResponse(ics_content, content_type='text/calendar')
        response['Content-Disposition'] = 'attachment; filename="ogladanie_pojazdu.ics"'
        return response
    else:
        return HttpResponse(status=400)

def filter_adverts(request, adverts):
    if 'load_search' in request.GET:
        search_criteria = load_search_criteria(request)
        form = FilterForm(search_criteria)
    else:
        form = FilterForm(request.GET)
    if form.is_valid():
        if form.cleaned_data['variant']:
            adverts = adverts.filter(variant__in=form.cleaned_data['variant'])
        if form.cleaned_data['brand']:
            adverts = adverts.filter(brand__in=form.cleaned_data['brand'])
        if form.cleaned_data['price_min']:
            adverts = adverts.filter(price__gte=form.cleaned_data['price_min'])
        if form.cleaned_data['price_max']:
            adverts = adverts.filter(price__lte=form.cleaned_data['price_max'])
        if form.cleaned_data['mileage_min']:
            adverts = adverts.filter(mileage__gte=form.cleaned_data['mileage_min'])
        if form.cleaned_data['mileage_max']:
            adverts = adverts.filter(mileage__lte=form.cleaned_data['mileage_max'])
        if form.cleaned_data['year_min']:
            adverts = adverts.filter(first_registration__gte=form.cleaned_data['year_min'])
        if form.cleaned_data['year_max']:
            adverts = adverts.filter(first_registration__lte=form.cleaned_data['year_max'])
        if form.cleaned_data['engine_capacity_min']:
            adverts = adverts.filter(engine_capacity__gte=form.cleaned_data['engine_capacity_min'])
        if form.cleaned_data['engine_capacity_max']:
            adverts = adverts.filter(engine_capacity__lte=form.cleaned_data['engine_capacity_max'])
        if form.cleaned_data['power_min']:
            adverts = adverts.filter(power__gte=form.cleaned_data['power_min'])
        if form.cleaned_data['power_max']:
            adverts = adverts.filter(power__lte=form.cleaned_data['power_max'])
        if form.cleaned_data['no_crashed']:
            adverts = adverts.filter(no_crashed__lte=form.cleaned_data['no_crashed'])       
        
        # Filtrowanie według spalania
        if form.cleaned_data['consumption']:
            filtered_adverts = []
            for advert in adverts:
                economy = evaluate_economy(
                    advert.city_fuel_consumption,
                    advert.highway_fuel_consumption,
                    advert.combined_fuel_consumption
                )
                if economy in form.cleaned_data['consumption']:
                    filtered_adverts.append(advert.id)
            adverts = adverts.filter(id__in=filtered_adverts)
        
        # Filtrowanie według emisji spalin (tylko eko)
        if form.cleaned_data.get('only_eco'):
            eco_adverts = []
            for advert in adverts:
                eco_friendly, _ = evaluate_eco_friendly(
                    advert.co2_emission,
                    advert.emission_class
                )
                if eco_friendly == "Eko":
                    eco_adverts.append(advert.id)
            adverts = adverts.filter(id__in=eco_adverts)

        # Filtrowanie tagów
        if form.cleaned_data.get('tags'):
            tags = form.cleaned_data['tags']
            tag_filters = Q()
            for tag in tags:
                tag_filters |= Q(**{tag: True})
            adverts = adverts.filter(tag_filters) 

    return adverts, form

def evaluate_adverts(adverts):
    for advert in adverts:
        advert.price_evaluation, advert.price_icon = evaluate_price(advert)
        advert.economy = evaluate_economy(
            advert.city_fuel_consumption,
            advert.highway_fuel_consumption,
            advert.combined_fuel_consumption
        )
        advert.eco_friendly, advert.eco_icon = evaluate_eco_friendly(
            advert.co2_emission,
            advert.emission_class
        )


def adverts_view(request):
    current_date = timezone.now()
    adverts = Advert.objects.filter(expiry_date__gte=current_date)

    if 'save_search' in request.GET:
        return save_search_criteria(request)
    if 'clear_search' in request.GET:
        return clear_search_criteria(request)

    # Filtrowanie
    adverts, form = filter_adverts(request, adverts)

    # Sortowanie
    sort_by = request.GET.get('sort')
    if sort_by == 'new':
        adverts = adverts.order_by('-created')
    elif sort_by == 'old':
        adverts = adverts.order_by('created')
    elif sort_by == 'price_low':
        adverts = adverts.order_by('price')
    elif sort_by == 'price_high':
        adverts = adverts.order_by('-price')
    elif sort_by == 'mileage_low':
        adverts = adverts.order_by('mileage')
    elif sort_by == 'mileage_high':
        adverts = adverts.order_by('-mileage')
    elif sort_by == 'engine_capacity_low':
        adverts = adverts.order_by('engine_capacity')
    elif sort_by == 'engine_capacity_high':
        adverts = adverts.order_by('-engine_capacity')
    elif sort_by == 'first_registration_low':
        adverts = adverts.order_by('-first_registration')
    elif sort_by == 'first_registration_high':
        adverts = adverts.order_by('first_registration')
    elif sort_by == 'consumption_low':
        adverts = adverts.order_by('combined_fuel_consumption')
    elif sort_by == 'consumption_high':
        adverts = adverts.order_by('-combined_fuel_consumption')
    elif sort_by == 'doors_high':
        adverts = adverts.order_by('-num_of_doors')
    elif sort_by == 'doors_low':
        adverts = adverts.order_by('num_of_doors')
    else:
        adverts = adverts.order_by('-created')

    evaluate_adverts(adverts)

    paginator = Paginator(adverts, 9)
    page_number = request.GET.get('page')
    try:
        adverts = paginator.page(page_number)
    except PageNotAnInteger:
        adverts = paginator.page(1)
    except EmptyPage:
        adverts = paginator.page(paginator.num_pages)

    context = {'adverts': adverts, 'form': form, 'paginator': paginator}
    return render(request, 'carapp/advertsView.html', context)


reminder_list = {}


@login_required
def dashboard(request):
    return render(request,
                  'carapp/dashboard.html',
                  {'section': 'dashboard'})


@login_required
def add_opinion(request, pk):

    advert = Advert.objects.get(id=pk)
    comments = advert.comments.filter(active=True).order_by('-created')
    form = CommentForm()
    if request.method == "POST":
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.advert = advert
            comment.save()
            comment = CommentForm()
            return redirect('single-advert', pk)

    return render(request,
                  'carapp/opinion.html',
                  {'comments': comments,
                  'form': form})

def user_login(request):
    form = LoginForm(request.POST)

    if request.method == 'POST':
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('main-site')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
        else:
            form = LoginForm()

    context = {'form': form}
    return render(request, 'registration/login.html', context)


def index(request):
    current_date = timezone.now()
    adverts = Advert.objects.filter(expiry_date__gte=current_date)
    adverts, form = filter_adverts(request, adverts)
    num = len(adverts)

    evaluate_adverts(adverts)

    recently_viewed_ids = request.session.get('recently_viewed', [])
    recently_viewed = Advert.objects.filter(id__in=recently_viewed_ids)

    evaluate_adverts(recently_viewed)
    recently_viewed_ids = request.session.get('recently_viewed', [])
    recommended_for_you = get_recommended_adverts(request, exclude_ids=recently_viewed_ids)
    evaluate_adverts(recommended_for_you)


    context = {'num': num, 'adverts': adverts, 'recently_viewed': recently_viewed, 'recommended_for_you': recommended_for_you, 'form': form}
    return render(request, 'carapp/index.html', context)


def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            profile = Profile.objects.create(user=user)
            profile.save()

            messages.success(request, "User account was created!")

            login(request, user)
            return redirect('edit-account')

        else:
            return HttpResponse('Error')

    context = {'page': page, 'form': form}
    return render(request, 'registration/register.html', context)


def forgot(request):
    return render(request, 'carapp/forgot.html')


def profile(request, pk):
    page = 'profile'
    profile = Profile.objects.get(id=pk)

    adverts = profile.advert_set.all()

    context = {'profile': profile,
               'page': page,
               'adverts': adverts,
               }
    return render(request, 'carapp/profile.html', context)


@login_required(login_url="login")
def userAccount(request):
    profile = request.user.profile
    username = profile.username
    form = ProfileForm(instance=profile)
    adverts = profile.advert_set.all()
    new_notifications_count = Notification.objects.filter(user=request.user, is_read=False).count()

    context = {'profile': profile,
               'form': form,
               'adverts': adverts,
               'username': username,
               'new_notifications_count': new_notifications_count
               }

    return render(request, 'carapp/profile.html', context)


@login_required(login_url="login")
def editAccount(request):
    profile = request.user.profile
    form = ProfileFormEditable(instance=profile)
    # Liczba nowych powiadomień
    new_notifications_count = Notification.objects.filter(user=request.user, is_read=False).count()
    username = profile.username
    if request.method == 'POST':
        form = ProfileFormEditable(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {'form': form, 'profile': profile, 'username': username, 'new_notifications_count': new_notifications_count}
    return render(request, 'carapp/edit_profile.html', context)


@login_required(login_url="login")
def deleteAccount(request):
    if request.method == "POST":
        profile = request.user.profile
        profile.delete()
        messages.success(request, "User account was deleted!")
        return render(request, 'registration/deleted.html')


# def adverts_view(request):
#     search_query = ""
#     adverts = Advert.objects.all()

#     # searching
#     if request.GET.get('search_query'):
#         adverts, search_query = searchAdverts(request)
#     elif request.GET.get('first-registration-min'):
#         filter_by_year = request.GET.get('first-registration-min')

#         if filter_by_year == '2022':
#             adverts = Advert.objects.filter(first_registration__gte=2022)
#         elif filter_by_year == '2021':
#             adverts = Advert.objects.filter(first_registration__gte=2021)
#         elif filter_by_year == '2020':
#             adverts = Advert.objects.filter(first_registration__gte=2020)
#         elif filter_by_year == '2019':
#             adverts = Advert.objects.filter(first_registration__gte=2019)
#         elif filter_by_year == '2018':
#             adverts = Advert.objects.filter(first_registration__gte=2018)
#         elif filter_by_year == '2017':
#             adverts = Advert.objects.filter(first_registration__gte=2017)
#         elif filter_by_year == '2016':
#             adverts = Advert.objects.filter(first_registration__gte=2016)
#         elif filter_by_year == '2015':
#             adverts = Advert.objects.filter(first_registration__gte=2015)
#         elif filter_by_year == '2014':
#             adverts = Advert.objects.filter(first_registration__gte=2014)
#         elif filter_by_year == '2013':
#             adverts = Advert.objects.filter(first_registration__gte=2013)
#         elif filter_by_year == '2012':
#             adverts = Advert.objects.filter(first_registration__gte=2012)
#         elif filter_by_year == '2011':
#             adverts = Advert.objects.filter(first_registration__gte=2011)
#         elif filter_by_year == '2010':
#             adverts = Advert.objects.filter(first_registration__gte=2010)
#         elif filter_by_year == '2009':
#             adverts = Advert.objects.filter(first_registration__gte=2009)
#         elif filter_by_year == '2008':
#             adverts = Advert.objects.filter(first_registration__gte=2008)
#         elif filter_by_year == '2007':
#             adverts = Advert.objects.filter(first_registration__gte=2007)
#         elif filter_by_year == '2006':
#             adverts = Advert.objects.filter(first_registration__gte=2006)
#         elif filter_by_year == '2005':
#             adverts = Advert.objects.filter(first_registration__gte=2005)
#     elif request.GET.get('first-registration-max'):
#         filter_by_year_max = request.GET.get('first-registration-max')

#         if filter_by_year_max == '2022':
#             adverts = Advert.objects.filter(first_registration__lte=2022)
#         elif filter_by_year_max == '2021':
#             adverts = Advert.objects.filter(first_registration__lte=2021)
#         elif filter_by_year_max == '2020':
#             adverts = Advert.objects.filter(first_registration__lte=2020)
#         elif filter_by_year_max == '2019':
#             adverts = Advert.objects.filter(first_registration__lte=2019)
#         elif filter_by_year_max == '2018':
#             adverts = Advert.objects.filter(first_registration__lte=2018)
#         elif filter_by_year_max == '2017':
#             adverts = Advert.objects.filter(first_registration__lte=2017)
#         elif filter_by_year_max == '2016':
#             adverts = Advert.objects.filter(first_registration__lte=2016)
#         elif filter_by_year_max == '2015':
#             adverts = Advert.objects.filter(first_registration__lte=2015)
#         elif filter_by_year_max == '2014':
#             adverts = Advert.objects.filter(first_registration__lte=2014)
#         elif filter_by_year_max == '2013':
#             adverts = Advert.objects.filter(first_registration__lte=2013)
#         elif filter_by_year_max == '2012':
#             adverts = Advert.objects.filter(first_registration__lte=2012)
#         elif filter_by_year_max == '2011':
#             adverts = Advert.objects.filter(first_registration__lte=2011)
#         elif filter_by_year_max == '2010':
#             adverts = Advert.objects.filter(first_registration__lte=2010)
#         elif filter_by_year_max == '2009':
#             adverts = Advert.objects.filter(first_registration__lte=2009)
#         elif filter_by_year_max == '2008':
#             adverts = Advert.objects.filter(first_registration__lte=2008)
#         elif filter_by_year_max == '2007':
#             adverts = Advert.objects.filter(first_registration__lte=2007)
#         elif filter_by_year_max == '2006':
#             adverts = Advert.objects.filter(first_registration__lte=2006)
#         elif filter_by_year_max == '2005':
#             adverts = Advert.objects.filter(first_registration__lte=2005)
#     elif request.GET.get('distance-min'):
#         filter_by_mileage_min = request.GET.get('distance-min')
#         if filter_by_mileage_min == '20000':
#             adverts = Advert.objects.filter(mileage__gte=20000)
#         elif filter_by_mileage_min == '35000':
#             adverts = Advert.objects.filter(mileage__gte=35000)
#         elif filter_by_mileage_min == '50000':
#             adverts = Advert.objects.filter(mileage__gte=50000)
#         elif filter_by_mileage_min == '75000':
#             adverts = Advert.objects.filter(mileage__gte=75000)
#         elif filter_by_mileage_min == '100000':
#             adverts = Advert.objects.filter(mileage__gte=100000)
#         elif filter_by_mileage_min == '125000':
#             adverts = Advert.objects.filter(mileage__gte=125000)
#         elif filter_by_mileage_min == '150000':
#             adverts = Advert.objects.filter(mileage__gte=150000)
#         elif filter_by_mileage_min == '200000':
#             adverts = Advert.objects.filter(mileage__gte=200000)
#         elif filter_by_mileage_min == '250000':
#             adverts = Advert.objects.filter(mileage__gte=250000)
#     elif request.GET.get('distance-max'):
#         filter_by_mileage_max = request.GET.get('distance-max')
#         if filter_by_mileage_max == '20000':
#             adverts = Advert.objects.filter(mileage__lte=20000)
#         elif filter_by_mileage_max == '35000':
#             adverts = Advert.objects.filter(mileage__lte=35000)
#         elif filter_by_mileage_max == '50000':
#             adverts = Advert.objects.filter(mileage__lte=50000)
#         elif filter_by_mileage_max == '75000':
#             adverts = Advert.objects.filter(mileage__lte=75000)
#         elif filter_by_mileage_max == '100000':
#             adverts = Advert.objects.filter(mileage__lte=100000)
#         elif filter_by_mileage_max == '125000':
#             adverts = Advert.objects.filter(mileage__lte=125000)
#         elif filter_by_mileage_max == '150000':
#             adverts = Advert.objects.filter(mileage__lte=150000)
#         elif filter_by_mileage_max == '200000':
#             adverts = Advert.objects.filter(mileage__lte=200000)
#         elif filter_by_mileage_max == '250000':
#             adverts = Advert.objects.filter(mileage__lte=250000)

#     num = len(adverts)
#     context = {'adverts': adverts, 'search_query': search_query, 'num':num}
#     return render(request, 'carapp/advertsView.html', context)

def get_equipment(advert):
    categories = {
        "Audio i multimedia": {
            'apple_carplay': 'Apple CarPlay',
            'android_auto': 'Android Auto',
            'bluetooth_interface': 'Interfejs Bluetooth',
            'radio': 'Radio',
            'handsfree_kit': 'Zestaw głośnomówiący',
            'usb_socket': 'Gniazdo USB',
            'wireless_charging': 'Ładowanie bezprzewodowe',
            'navigation_system': 'System nawigacji',
            'sound_system': 'System dźwiękowy',
            'head_up_display': 'Wyświetlacz przezierny',
            'touchscreen': 'Ekran dotykowy',
            'voice_control': 'Sterowanie głosowe',
            'internet_access': 'Dostęp do internetu'
        },
        "Komfort": {
            'air_conditioning': 'Klimatyzacja',
            'rear_passenger_air_conditioning': 'Klimatyzacja dla pasażerów z tyłu',
            'folding_roof': 'Składany dach',
            'sunshade': 'Roleta przeciwsłoneczna',
            'openable_roof': 'Otwierany dach',
            'electric_driver_seat': 'Elektryczny fotel kierowcy',
            'electric_passenger_seat': 'Elektryczny fotel pasażera',
            'heated_driver_seat': 'Podgrzewany fotel kierowcy',
            'heated_passenger_seat': 'Podgrzewany fotel pasażera',
            'lumbar_support_driver': 'Podparcie lędźwiowe kierowcy',
            'lumbar_support_passenger': 'Podparcie lędźwiowe pasażera',
            'ventilated_front_seats': 'Wentylowane przednie siedzenia',
            'massage_front_seats': 'Masujące przednie siedzenia',
            'seat_memory': 'Pamięć ustawień siedzeń',
            'sport_front_seats': 'Sportowe przednie siedzenia',
            'heated_rear_seats': 'Podgrzewane tylne siedzenia',
            'ventilated_rear_seats': 'Wentylowane tylne siedzenia',
            'massage_rear_seats': 'Masujące tylne siedzenia',
            'front_armrest': 'Podłokietnik przedni',
            'rear_armrest': 'Podłokietnik tylny',
            'leather_steering_wheel': 'Skórzana kierownica',
            'sport_steering_wheel': 'Sportowa kierownica',
            'steering_wheel_radio_controls': 'Sterowanie radiem w kierownicy',
            'electric_steering_column': 'Elektryczna kolumna kierownicy',
            'multifunction_steering_wheel': 'Wielofunkcyjna kierownica',
            'heated_steering_wheel': 'Podgrzewana kierownica',
            'paddle_shifters': 'Łopatki zmiany biegów',
            'leather_gear_knob': 'Skórzana gałka zmiany biegów',
            'digital_key': 'Cyfrowy klucz',
            'keyless_entry': 'Bezkluczykowy dostęp',
            'keyless_go': 'Bezkluczykowy start',
            'engine_start_without_key': 'Start silnika bez kluczyka',
            'automatic_climate_control': 'Automatyczna klimatyzacja',
            'heated_front_windshield': 'Podgrzewana przednia szyba',
            'electric_front_windows': 'Elektryczne przednie szyby',
            'tinted_rear_windows': 'Przyciemniane tylne szyby',
            'remote_openable_roof': 'Zdalnie otwierany dach',
            'parking_heater': 'Ogrzewanie postojowe',
            'rain_sensor': 'Czujnik deszczu',
            'wipers': 'Wycieraczki',
            'electric_rear_windows': 'Elektryczne tylne szyby',
            'electric_roof': 'Elektryczny dach',
            'tow_hook': 'Hak holowniczy'
        },
        "Samochody elektryczne": {
            'energy_recovery_system': 'System odzyskiwania energii',
            'fast_charging_function': 'Funkcja szybkiego ładowania',
            'charging_cable': 'Kabel do ładowania'
        },
        "Systemy wspomagania kierownicy": {
            'cruise_control': 'Tempomat',
            'park_assist': 'Asystent parkowania',
            'rear_distance_control': 'Kontrola odległości z tyłu',
            'panoramic_camera_360': 'Panoramiczna kamera 360',
            'electric_vehicle_presence_control': 'Kontrola obecności pojazdu elektrycznego',
            'side_mirror_memory': 'Pamięć lusterek bocznych',
            'side_mirror_camera': 'Kamera w lusterkach bocznych',
            'automatic_parking_assistant': 'Asystent automatycznego parkowania',
            'heated_side_mirrors': 'Podgrzewane lusterka boczne',
            'lane_assist': 'Asystent pasa ruchu',
            'active_lane_change_assistant': 'Aktywny asystent zmiany pasa ruchu',
            'speed_limiter': 'Ogranicznik prędkości',
            'brake_assist': 'Asystent hamowania',
            'hill_holder_automatic_occupancy_control': 'Automatyczna kontrola zajętości górki',
            'hill_holder_assistance': 'Asystent podjazdu',
            'active_speed_limit_sign_recognition': 'Aktywne rozpoznawanie znaków ograniczenia prędkości',
            'uphill_start_assistance': 'Asystent startu na wzniesieniu',
            'high_beam_assistant': 'Asystent świateł drogowych',
            'cornering_lights': 'Światła doświetlające zakręty',
            'adaptive_lighting': 'Oświetlenie adaptacyjne',
            'dynamic_cornering_lights': 'Dynamiczne światła doświetlające zakręty',
            'dusk_sensor': 'Czujnik zmierzchu',
            'headlight_washers': 'Spryskiwacze reflektorów',
            'daytime_running_lights': 'Światła do jazdy dziennej',
            'led_daytime_running_lights': 'LED-owe światła do jazdy dziennej',
            'fog_lights': 'Światła przeciwmgielne',
            'led_fog_lights': 'LED-owe światła przeciwmgielne',
            'led_rear_lights': 'LED-owe tylne światła',
            'home_lighting': 'Oświetlenie domowe',
            'led_interior_lighting': 'LED-owe oświetlenie wnętrza',
            'start_stop_system': 'System start-stop',
            'electronic_tire_pressure_control': 'Elektroniczna kontrola ciśnienia w oponach',
            'electric_parking_brake': 'Elektryczny hamulec postojowy',
            'power_steering': 'Wspomaganie kierownicy',
            'differential_lock': 'Blokada mechanizmu różnicowego',
            'adjustable_central_differential': 'Regulowany centralny mechanizm różnicowy',
            'traffic_jam_assistant': 'Asystent korków'
        },
        "Osiągi i tuning": {
            'runflat_tires': 'Opony runflat',
            'comfort_suspension': 'Zawieszenie komfortowe',
            'electronic_suspension_control': 'Elektroniczna kontrola zawieszenia',
            'sport_suspension': 'Zawieszenie sportowe',
            'adjustable_suspension': 'Regulowane zawieszenie',
            'pneumatic_suspension': 'Zawieszenie pneumatyczne',
            'hydropneumatic_suspension': 'Zawieszenie hydropneumatyczne',
            'ceramic_composite_brakes': 'Ceramiczne hamulce kompozytowe',
            'particulate_filter': 'Filtr cząstek stałych'
        },
        "Bezpieczeństwo": {
            'abs': 'ABS',
            'electronic_brake_distribution': 'Elektroniczny rozdział sił hamowania',
            'emergency_brake_assist': 'Asystent hamowania awaryjnego',
            'active_city_brake_assist': 'Aktywny asystent hamowania w mieście',
            'driver_fatigue_warning': 'Ostrzeżenie o zmęczeniu kierowcy',
            'collision_warning': 'Ostrzeżenie przed kolizją',
            'side_impact_protection': 'Ochrona przed uderzeniem bocznym',
            'rear_impact_protection': 'Ochrona przed uderzeniem tylnym',
            'engine_sound_elimination': 'Eliminacja dźwięku silnika',
            'rear_cross_traffic_alert': 'Ostrzeżenie o ruchu poprzecznym z tyłu',
            'lane_keeping_assist': 'Asystent utrzymania pasa ruchu',
            'obstacle_detection_assist': 'Asystent wykrywania przeszkód',
            'cornering_stability_assist': 'Asystent stabilności na zakrętach',
            'rear_collision_mitigation': 'Łagodzenie skutków kolizji tylnej',
            'central_airbag': 'Centralna poduszka powietrzna',
            'driver_side_airbag': 'Poduszka powietrzna po stronie kierowcy',
            'front_side_airbags': 'Przednie poduszki powietrzne boczne',
            'rear_side_airbags': 'Tylne poduszki powietrzne boczne',
            'rear_curtain_airbags': 'Tylne kurtyny powietrzne',
            'passenger_airbag': 'Poduszka powietrzna pasażera',
            'isofix': 'Isofix',
            'rollover_protection': 'Ochrona przed przewróceniem'
        }
    }
    
    equipment = {}
    for category, fields in categories.items():
        selected_features = []
        for field in fields:
            if getattr(advert, field):
                selected_features.append(fields[field])
        if selected_features:
            equipment[category] = selected_features
    
    return equipment


def advert_view(request, pk):
    page = 'advert'
    advert = Advert.objects.get(id=pk)

    recently_viewed = request.session.get('recently_viewed', [])
    if pk not in recently_viewed:
        recently_viewed.insert(0, pk)
        if len(recently_viewed) > 3:
            recently_viewed.pop()
    request.session['recently_viewed'] = recently_viewed

    comments = advert.comments.filter(active=True).order_by('-created')
    comments_count = comments.count()  # Get the count of active comments

    # Paginacja: 3 komentarze na stronę
    paginator = Paginator(comments, 3)
    page_number = request.GET.get('page')
    comments = paginator.get_page(page_number)

    # Pobranie danych adresowych z ogłoszenia
    street = advert.street
    postal_code = advert.postal_code
    city = advert.city

    # Geokodowanie adresu
    latitude, longitude = geocode_address(street, postal_code, city)

    # Generowanie linku do mapy
    map_link = generate_map_link(latitude, longitude) if latitude and longitude else None

    # Zakres zdjęć do ogłoszenia
    image_indices = range(1, 9)

    profile = Profile.objects.all()

    equipment = get_equipment(advert)

    # Szczegóły ogłoszenia do podziału na dwie kolumny
    details = [
        {'label': 'Marka:', 'value': advert.brand.title()},
        {'label': 'Model:', 'value': advert.model} if advert.model else None,
        {'label': 'Typ nadwozia:', 'value': advert.variant.title()},
        {'label': 'Rok produkcji:', 'value': advert.first_registration},
        {'label': 'Pojemność skokowa:', 'value': f"{advert.engine_capacity} cm³"},
        {'label': 'Moc:', 'value': f"{advert.power} KM"},
        {'label': 'Przebieg:', 'value': f"{advert.mileage} km"},
        {'label': 'Rodzaj paliwa:', 'value': advert.fuel_type},
        {'label': 'Spalanie w mieście:', 'value': f"{advert.city_fuel_consumption} L/100km"},
        {'label': 'Spalanie poza miastem:', 'value': f"{advert.highway_fuel_consumption} L/100km"},
        {'label': 'Spalanie cykl mieszany:', 'value': f"{advert.combined_fuel_consumption} L/100km"},
        {'label': 'Emisja CO2:', 'value': f"{advert.co2_emission} g/km"},
        {'label': 'Klasa emisji spalin:', 'value': advert.emission_class},
        {'label': 'Ekoplakietka:', 'value': advert.eco_sticker},
        {'label': 'Skrzynia biegów:', 'value': advert.transmission} if advert.transmission else None,
        {'label': 'Napęd:', 'value': advert.drive} if advert.drive else None,
        {'label': 'Bezwypadkowy:', 'value': advert.no_crashed},
        {'label': 'Uszkodzony:', 'value': advert.damaged} if advert.damaged else None,
        {'label': 'Stan:', 'value': advert.condition} if advert.condition else None,
        {'label': 'Czy posiada numer rejestracyjny:', 'value': advert.has_registration_number} if advert.has_registration_number else None,
        {'label': 'Zarejestrowany w Polsce:', 'value': advert.registered_in_poland} if advert.registered_in_poland else None,
        {'label': 'Zarejestrowany jako zabytek:', 'value': advert.registered_as_antique} if advert.registered_as_antique else None,
        {'label': 'Pierwszy właściciel:', 'value': advert.first_owner} if advert.first_owner else None,
        {'label': 'Serwisowany w ASO:', 'value': advert.serviced_in_aso} if advert.serviced_in_aso else None,
        {'label': 'Importowany:', 'value': advert.imported} if advert.imported else None,
        {'label': 'Prawostronny:', 'value': advert.right_hand_drive} if advert.right_hand_drive else None,
        {'label': 'Homologacja ciężarowa:', 'value': advert.truck_approval} if advert.truck_approval else None,
        {'label': 'Kolor:', 'value': advert.color.title()},
        {'label': 'Typ koloru:', 'value': advert.color_type.title()},
        {'label': 'Liczba drzwi:', 'value': advert.num_of_doors},
        {'label': 'Kraj pochodzenia:', 'value': advert.country_of_origin} if advert.country_of_origin else None,
    ]

    # Remove None values from the list
    details = [detail for detail in details if detail is not None]

    # Split the details into two columns
    middle_index = (len(details) + 1) // 2
    left_column = details[:middle_index]
    right_column = details[middle_index:]

    recently_viewed_ids = request.session.get('recently_viewed', [])
    recommended_for_you = get_recommended_adverts(request, exclude_ids=recently_viewed_ids)

    active_tags = advert.get_active_tags()

    context = {
        'advert': advert,
        'image_indices': image_indices,
        'map_link': map_link,
        'profile': profile, 
        'page': page, 
        'comments': comments, 
        'comments_count': comments_count,  # Pass the count to the template
        'paginator': paginator,
        'equipment': equipment,
        'left_column': left_column,
        'right_column': right_column,
        'recommended_for_you': recommended_for_you,
        'active_tags': active_tags
    }
    return render(request, 'carapp/detailsAdvert.html', context)

@login_required(login_url="login")
def add_to_favorite(request, pk):
    profile = request.user.profile
    advert = Advert.objects.get(id=pk)

    
    context = {'advert': advert, 'profile': profile}
    return render(request, 'carapp/detailsAdvert.html', context)


@login_required(login_url="login")
def myAdverts(request):
    profile = request.user.profile
    current_date = timezone.now()
    # Pobierz i posortuj aktywne i nieaktywne ogłoszenia
    active_adverts = profile.advert_set.filter(expiry_date__gte=current_date).order_by('-created')
    inactive_adverts = profile.advert_set.filter(expiry_date__lt=current_date).order_by('-created')
     # Dodaj paginację
    active_paginator = Paginator(active_adverts, 10)
    inactive_paginator = Paginator(inactive_adverts, 10)
    
    # Pobierz numer strony z GET requestu
    active_page_number = request.GET.get('active_page')
    inactive_page_number = request.GET.get('inactive_page')
    
    # Pobierz odpowiednie strony
    active_page_obj = active_paginator.get_page(active_page_number)
    inactive_page_obj = inactive_paginator.get_page(inactive_page_number)
    adverts = profile.advert_set.all()
    active_count = active_adverts.count()
    inactive_count = inactive_adverts.count()
    # Liczba nowych powiadomień
    new_notifications_count = Notification.objects.filter(user=request.user, is_read=False).count()
    context = {
        'adverts': adverts,
        'profile': profile, 
        'active_adverts': active_adverts, 
        'inactive_adverts': inactive_adverts,
        'active_page_obj': active_page_obj, 
        'inactive_page_obj': inactive_page_obj,
        'active_count': active_count,
        'inactive_count': inactive_count,
        'new_notifications_count': new_notifications_count
        }
    return render(request, 'carapp/myAdverts.html', context)

@login_required(login_url="login")
def restore_advert(request, pk):
    advert = Advert.objects.get(id=pk)
    advert.created = timezone.now()  # Ustawiamy nową datę utworzenia na bieżącą
    advert.expiry_date = advert.created + timezone.timedelta(days=30)  # Ustawiamy nową datę wygaśnięcia
    advert.save()
    messages.success(request, f"Ogłoszenie '{advert.title}' zostało przywrócone.")
    return redirect('my-adverts')  # Przekierowanie z powrotem do widoku 'myAdverts'

@login_required(login_url="login")
def notifications(request):
    profile = request.user.profile
    adverts = profile.advert_set.all()
    # Notification.objects.all().delete()
    notifications_list = Notification.objects.filter(user=request.user).order_by('-created')
    paginator = Paginator(notifications_list, 20)  # 20 powiadomień na stronę
    # Pobierz numer aktualnej strony z GET requesta
    page_number = request.GET.get('page')
    # Pobierz powiadomienia dla aktualnej strony
    notifications = paginator.get_page(page_number)
    notifications_deleted = request.session.pop('notifications_deleted', False)  # Pobierz wartość i usuń z sesji
    context = {'profile': profile, 'adverts': adverts, 'notifications': notifications, 'total_notifications': notifications_list.count(), 'notifications_deleted': notifications_deleted}
    return render(request, 'carapp/notifications.html', context)


def delete_selected_notifications(request):
    if request.method == 'POST':
        notification_ids = request.POST.getlist('selected_notifications')
        notifications_to_delete = Notification.objects.filter(id__in=notification_ids)
        notifications_to_delete.delete()
        messages.success(request, 'Zaznaczone powiadomienia zostały pomyślnie usunięte.')
        request.session['notifications_deleted'] = True  # Ustawienie sesji
    
    return redirect('notifications')

@login_required(login_url="login")
def delete_advert(request, pk):
    profile = request.user.profile
    advert = Advert.objects.get(id=pk)
    advert.delete()
    context = {'advert': advert, 'profile': profile}
    return render(request, 'carapp/myAdverts.html', context)


def contact_advert(request, pk):
    advert = Advert.objects.get(id=pk)
    sent = False
    if request.method == 'POST':
        # form was submitted
        form = EmailPriceForm(request.POST)
        if form.is_valid():
            # form fields passed validation
            cd = form.cleaned_data
            # send email
            subject = f"{cd['name']} prosi o kontakt. Ogłoszenie: {advert.title}, {advert.created}"
            if cd['comments']:
                message = f"Adres e-mail do kontaktu: {cd['your_address']}\nNumer telefonu: {cd['your_phone']}\n\nLink do ogłoszenia: localhost:8000/advert/{advert.id}\n" \
                          f"Komentarze do kontaktu: \n {cd['comments']}"
            else:
                message = f"Adres e-mail do kontaktu: {cd['your_address']}\nNumer telefonu: {cd['your_phone']}\n\nLink do ogłoszenia: localhost:8000/advert/{advert.id}\n" \
                          f"Uzytkownik nie dodal komentarza."
            send_mail(subject, message, 'marczak01@o2.pl', [cd['your_address'], advert.owner.email])
            sent = True
        else:
            print('form not valid')
    else:
        print('no post method')
        form = EmailPriceForm()

    context = {'advert': advert, 'form': form, 'sent': sent}
    return render(request, 'carapp/contact_seller.html', context)


@login_required(login_url="login")
def price_reminder(request, pk):
    profile = request.user.profile
    advert = Advert.objects.get(id=pk)
    sent = False
    on_the_list = False

    if request.method == 'POST':
        form = EmailPriceReminderForm(request.POST, profile)
        if form.is_valid():
            # we're cleaning data from form and saving it in 'cd' variable
            cd = form.cleaned_data
            subject = f"Ustawienie powiadomienia przebieglo pomyslnie."
            message = f"Dziękujemy za ustawienie powiadomienia. Gdy tylko cena ogloszenia ulegnie zmianie powiadomimy Ciebie o tym drogą mailową"
            send_mail(subject, message, 'marczak01@o2.pl', [cd['your_address']])
            sent = True

            if sent:
                list_of_emails = PriceReminderConnection.objects.filter(user_address=cd['your_address'], id_of_advert=advert.id)
                print(list_of_emails)
                if list_of_emails:
                    on_the_list = True
                    print('on the list')
                else:
                    price_reminder_list = PriceReminderConnection(user_address=cd['your_address'], id_of_advert=advert.id)
                    price_reminder_list.save()
                    on_the_list = False
                    print(f"Dodano email oraz id ogloszenia do bazy danych {cd['your_address']} oraz id {advert.id}")
        else:
            print('form not valid')
    else:
        form = EmailPriceReminderForm()


    context = {'advert': advert, 'form': form, 'sent': sent, 'profile': profile, 'on_the_list': on_the_list}
    return render(request, 'carapp/price_reminder.html', context)


def other_user_adverts(request, pk):
    profile = Profile.objects.get(id=pk)

    adverts = profile.advert_set.all()
    context = {'adverts': adverts, 'profile': profile}
    return render(request, 'carapp/otherUserAdverts.html', context)


@login_required(login_url="login")
def create_advert(request):
    profile = request.user.profile
    form = AdvertForm()
    created = False
    if request.method == "POST":
        form = AdvertForm(request.POST, request.FILES)
        if form.is_valid():
            advert = form.save(commit=False)
            advert.owner = profile
            advert.save()
            form.save_m2m()
            created = True
            return redirect('adverts')
        else:
            form = AdvertForm(request.POST)

    step = int(request.GET.get('step', '1'))
    progress = (step - 1) * (75 / 4)
    context = {'form': form, 'created': created, 'progress': progress}
    return render(request, 'carapp/addAdvert.html', context)

@login_required(login_url="login")
def autocomplete_address(request):
    street = request.GET.get('street', '')
    postal_code = request.GET.get('postal_code', '')
    city = request.GET.get('city', '')

    if not (street and city):
        return JsonResponse({'results': []})

    query = f"{street}, {postal_code} {city}, Poland"
    url = "https://nominatim.openstreetmap.org/search"

    params = {
        'q': query,
        'format': 'json',
        'addressdetails': 1,
        'limit': 10,

    }

    headers = {
        'User-Agent': 'carapp/1.0 (ktrybus15@gmail.com)'  # Zastąp 'your_email@example.com' swoim adresem email
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        # Logowanie błędu
        print(f"Request error: {e}")
        return JsonResponse({'results': []})
    except ValueError as e:
        # Logowanie błędu parsowania JSON
        print(f"JSON decode error: {e}")
        return JsonResponse({'results': []})

    results = []
    for result in data:
        results.append({
            'formatted': result['display_name'],
            'components': {
                'road': result['address'].get('road', ''),
                'postcode': result['address'].get('postcode', ''),
                'city': result['address'].get('city', result['address'].get('town', ''))
            }
        })

    return JsonResponse({'results': results})


@login_required(login_url="login")
def updateAdvert(request, pk):
    profile = request.user.profile
    advert = profile.advert_set.get(id=pk)
    form = AdvertForm(instance=advert)
    # we're taking actual price before changes
    advert_price = advert.price
    print(f"{advert_price} było")
    if request.method == "POST":
        form = AdvertForm(request.POST, request.FILES, instance=advert)
        if form.is_valid():
            form.save()
            print(f"{advert.price} jest")
            # after we see any price changes in advert
            # then we send a reminder to all addresses connected with this advert
            if advert_price != advert.price:
                print('cena sie zmienila')
                list_of_emails = PriceReminderConnection.objects.filter(id_of_advert=str(advert.id))
                print(list_of_emails)

                subject = f"Uwaga nastąpiła zmiana ceny dla ogłoszenia: {advert.title}"
                message = f"Informujemy, ze cena ogłoszenia uległa zmianie.\n " \
                          f"Poprzenia cena: {advert_price}PLN \nAktualna cena: {advert.price}PLN"
                for i in list_of_emails:
                    send_mail(subject, message, 'marczak01@o2.pl', [i])

            return redirect('adverts')

    context = {'form': form}
    return render(request, 'carapp/addAdvert.html', context)




# @login_required(login_url="login")
# def deleteAdvert(request, pk):
#     profile = request.user.profile
#     advert = profile.advert_set.get(id=pk)
#     if request.method == 'POST':
#         advert.delete()
#         return redirect('adverts')
#     context = {'object': advert}
#     return render(request, 'adverts/delete_template.html', context)
