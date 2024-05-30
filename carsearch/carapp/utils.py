from .models import Advert
from statistics import mean

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