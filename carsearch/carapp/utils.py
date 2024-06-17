from .models import Advert
from statistics import mean
from geopy.geocoders import Nominatim
import time
from geopy.exc import GeocoderTimedOut
import json
from django.http import JsonResponse

def save_search_criteria(request):
    search_criteria = {key: request.GET.getlist(key) if len(request.GET.getlist(key)) > 1 else request.GET.getlist(key)[0]
                       for key in request.GET.keys()}
    response = JsonResponse({"message": "Search criteria saved."})
    response.set_cookie('saved_search', json.dumps(search_criteria), max_age=30*24*60*60)  # 30 days
    return response

def load_search_criteria(request):
    saved_search = request.COOKIES.get('saved_search')
    if saved_search:
        search_criteria = json.loads(saved_search)
    else:
        search_criteria = {}
    return search_criteria

def clear_search_criteria(request):
    response = JsonResponse({"message": "Search criteria cleared."})
    response.delete_cookie('saved_search')
    return response

def evaluate_economy(city_consumption, highway_consumption, combined_consumption):
    if city_consumption is None or highway_consumption is None or combined_consumption is None:
        return "Brak wystarczających danych"
    
    if city_consumption < 7 and highway_consumption < 5.5 and combined_consumption < 6:
        return "Niskie"
    elif 7 < city_consumption <= 10 and 5.5 < highway_consumption < 8 and 6 <= combined_consumption < 7.5:
        return "Średnie"
    elif city_consumption > 10 or highway_consumption > 8 or combined_consumption > 7.5:
        return "Wysokie"
    else:
        return "Średnie"  # Możemy uznać średnie spalanie jako domyślną ocenę

def evaluate_eco_friendly(co2_emission, emission_class):
    if co2_emission is None or emission_class is None:
        return "Nieokreślone", "bi bi-question-circle"
    
    if co2_emission < 100 and emission_class in ["Euro 5", "Euro 6"]:
        return "Eko", "bi bi-circle-fill text-success"
    elif co2_emission < 150 and emission_class in ["Euro 4", "Euro 5", "Euro 6"]:
        return "Średnia", "bi bi-circle-fill text-warning"
    else:
        return "Wysoka", "bi bi-exclamation-triangle text-danger"

def evaluate_price(advert):
    similar_adverts = Advert.objects.filter(
        brand=advert.brand,
        variant=advert.variant,
        first_registration=advert.first_registration,
    )
    
    if not similar_adverts.exists():
        return "Brak danych porównawczych", "bi bi-question-circle"

    prices = [a.price for a in similar_adverts]
    avg_price = mean(prices)

    if advert.price < avg_price * 0.9:
        return "poniżej średniej", "bi bi-arrow-down-circle text-success"
    elif avg_price * 0.9 <= advert.price <= avg_price * 1.1:
        return "w granicach średniej", "bi bi-dash-circle text-warning"
    else:
        return "powyżej średniej", "bi bi-arrow-up-circle text-danger"

# Funkcja geokodowania z obsługą błędów
def geocode_address(street, postal_code, city):
    try:
        # Pełny adres
        address = f"{street}, {postal_code} {city}"
        
        # Użycie geokodera Nominatim
        geolocator = Nominatim(user_agent="carapp")
        location = geolocator.geocode(address)
        
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except GeocoderTimedOut:
        print("Przekroczono limit czasu geokodera, odczekaj 30 sekund przed ponowną próbą.")
        time.sleep(30)  # Odczekaj 30 sekund przed ponowną próbą
        return geocode_address(street, postal_code, city)  # Rekurencyjnie wywołaj funkcję ponownie
    except Exception as e:
        print(f"Wystąpił błąd geokodowania: {e}")
        return None, None  # Zwróć None, jeśli wystąpi inny błąd

# Funkcja generująca link HTML do mapy
def generate_map_link(latitude, longitude):
    return f'<iframe width="425" height="350" src="https://www.openstreetmap.org/export/embed.html?bbox={longitude-0.0025}%2C{latitude-0.001}%2C{longitude+0.0025}%2C{latitude+0.001}&amp;layer=mapnik&amp;marker={latitude}%2C{longitude}" style="border: 1px solid black"></iframe><br/><small><a href="https://www.openstreetmap.org/?mlat={latitude}&amp;mlon={longitude}#map=19/{latitude}/{longitude}">Wyświetl wskazówki dojazdu</a></small>'

# Przykładowy adres
# street = "Rogowo 52"
# postal_code = "78-200"
# city = "Białogard"

# latitude, longitude = geocode_address(street, postal_code, city)
# print(f"Szerokość geograficzna: {latitude}, Długość geograficzna: {longitude}")

# Generowanie linku do mapy na podstawie współrzędnych
# map_link = generate_map_link(latitude, longitude)
# print(map_link)
