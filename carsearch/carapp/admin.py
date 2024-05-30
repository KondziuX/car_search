from django.contrib import admin
from .models import Profile, Advert, Fuel, PriceReminderConnection, Comment
# Register your models here.

admin.site.register(Profile)
admin.site.register(Advert)
admin.site.register(Fuel)
admin.site.register(PriceReminderConnection)
admin.site.register(Comment)

