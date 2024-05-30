from .models import Advert
from statistics import mean

def evaluate_price(advert):
    similar_adverts = Advert.objects.filter(
        brand=advert.brand,
        variant=advert.variant,
        first_registration=advert.first_registration,
    )
    
    if not similar_adverts.exists():
        return "Brak danych porównawczych"

    prices = [a.price for a in similar_adverts]
    avg_price = mean(prices)

    if advert.price < avg_price * 0.9:
        return "poniżej średniej"
    elif avg_price * 0.9 <= advert.price <= avg_price * 1.1:
        return "w granicach średniej"
    else:
        return "powyżej średniej"