from .models import Advert
from statistics import mean

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