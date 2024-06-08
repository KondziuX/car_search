from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import LoginForm, CustomUserCreationForm, \
                   ProfileForm, ProfileFormEditable, \
                   AdvertForm, EmailPriceForm, EmailPriceReminderForm, CommentForm
from .models import Profile, Advert, PriceReminderConnection
# from .utils import searchAdverts
from django.core.mail import send_mail
from django.core.paginator import Paginator
from .utils import evaluate_economy, evaluate_price, evaluate_eco_friendly, geocode_address, generate_map_link

from .forms import FilterForm

def adverts_view(request):
    adverts = Advert.objects.all()

    # Filtrowanie
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
        elif sort_by == 'doors_high':
            adverts = adverts.order_by('-num_of_doors')
        elif sort_by == 'doors_low':
            adverts = adverts.order_by('num_of_doors')
        else:
            adverts = adverts.order_by('-created')

    # Ocena ceny i ekonomii
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

    context = {'adverts': adverts, 'form': form}
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
    adverts = Advert.objects.all()
    num = len(adverts)
    context = {'num': num, 'adverts': adverts}
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

    context = {'profile': profile,
               'form': form,
               'adverts': adverts,
               'username': username}

    return render(request, 'carapp/profile.html', context)


@login_required(login_url="login")
def editAccount(request):
    profile = request.user.profile
    form = ProfileFormEditable(instance=profile)
    username = profile.username
    if request.method == 'POST':
        form = ProfileFormEditable(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')

    context = {'form': form, 'profile': profile, 'username': username}
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
        {'label': 'Typ nadwozia:', 'value': advert.variant.title()},
        {'label': 'Rok produkcji:', 'value': advert.first_registration},
        {'label': 'Pojemność skokowa:', 'value': f"{advert.engine_capacity} cm³"},
        {'label': 'Moc:', 'value': f"{advert.power} KM"},
        {'label': 'Przebieg:', 'value': f"{advert.mileage} km"},
        {'label': 'Rodzaj paliwa:', 'value': advert.fuel_type},
        {'label': 'Bezwypadkowy:', 'value': advert.no_crashed},
        {'label': 'Model:', 'value': advert.model} if advert.model else None,
        {'label': 'Czy posiada numer rejestracyjny:', 'value': advert.has_registration_number} if advert.has_registration_number else None,
        {'label': 'Zarejestrowany w Polsce:', 'value': advert.registered_in_poland} if advert.registered_in_poland else None,
        {'label': 'Zarejestrowany jako zabytek:', 'value': advert.registered_as_antique} if advert.registered_as_antique else None,
        {'label': 'Pierwszy właściciel:', 'value': advert.first_owner} if advert.first_owner else None,
        {'label': 'Serwisowany w ASO:', 'value': advert.serviced_in_aso} if advert.serviced_in_aso else None,
        {'label': 'Stan:', 'value': advert.condition} if advert.condition else None,
        {'label': 'Uszkodzony:', 'value': advert.damaged} if advert.damaged else None,
        {'label': 'Importowany:', 'value': advert.imported} if advert.imported else None,
        {'label': 'Skrzynia biegów:', 'value': advert.transmission} if advert.transmission else None,
        {'label': 'Prawostronny:', 'value': advert.right_hand_drive} if advert.right_hand_drive else None,
        {'label': 'Napęd:', 'value': advert.drive} if advert.drive else None,
        {'label': 'Homologacja ciężarowa:', 'value': advert.truck_approval} if advert.truck_approval else None,
        {'label': 'Kraj pochodzenia:', 'value': advert.country_of_origin} if advert.country_of_origin else None,
        {'label': 'Spalanie w mieście:', 'value': f"{advert.city_fuel_consumption} L/100km"},
        {'label': 'Spalanie poza miastem:', 'value': f"{advert.highway_fuel_consumption} L/100km"},
        {'label': 'Spalanie cykl mieszany:', 'value': f"{advert.combined_fuel_consumption} L/100km"},
        {'label': 'Emisja CO2:', 'value': f"{advert.co2_emission} g/km"},
        {'label': 'Klasa emisji spalin:', 'value': advert.emission_class},
        {'label': 'Ekoplakietka:', 'value': advert.eco_sticker},
        {'label': 'Kolor:', 'value': advert.color.title()},
        {'label': 'Liczba drzwi:', 'value': advert.num_of_doors},
        {'label': 'Typ koloru:', 'value': advert.color_type.title()},
    ]

    # Remove None values from the list
    details = [detail for detail in details if detail is not None]

    # Split the details into two columns
    middle_index = (len(details) + 1) // 2
    left_column = details[:middle_index]
    right_column = details[middle_index:]

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
    # adverts = Advert.objects.all()
    adverts = profile.advert_set.all()
    context = {'adverts': adverts, 'profile': profile}
    return render(request, 'carapp/myAdverts.html', context)

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
    profile = request.user.profile  # aktualnie zalogowany użytkownik
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
