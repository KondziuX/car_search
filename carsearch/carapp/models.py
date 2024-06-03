from django.db import models
from django.contrib.auth.models import User
import uuid
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse




class Profile(models.Model):

    SELLER = [
        ('Dealer', 'Dealer'),
        ('Osoba Prywatna', 'Osoba Prywatna'),
    ]
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    surname = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(max_length=500, blank=True, null=True)
    username = models.CharField(max_length=200, null=True, blank=True)
    location_city = models.CharField(max_length=50, null=True, blank=False)
    location_country = models.CharField(max_length=50, null=True, blank=False)
    phone_number = models.CharField(max_length=200, null=True, blank=True)
    seller = models.CharField(max_length=200, null=True, blank=False, choices=SELLER)
    bio = models.TextField(null=True, blank=True)
    profile_image = models.ImageField(
        null=True, blank=True, upload_to='profiles/', default='profiles/user.png')
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return str(self.username)


class Advert(models.Model):

    YES_OR_NO = [
        ('Tak', 'Tak'),
        ('Nie', 'Nie'),
    ]

    BRAND_CHOICES = [
    ('Fiat', 'Fiat'),
    ('KIA', 'KIA'),
    ('BMW', 'BMW'),
    ('Opel', 'Opel'),
    ('Audi', 'Audi'),
    ('Renault', 'Renault'),
    ]

    CONDITION_CHOICES = [
        ('Używane', 'Używane'),
        ('Nowe', 'Nowe'),
        ('Poleasingowy', 'Poleasingowy')
    ]

    TRANSMISSION_CHOICES = [
        ('Automatyczna', 'Automatyczna'),
        ('Manualna', 'Manualna'),
    ]

    DRIVE_CHOICES = [
        ('4x4 (dołączany automatycznie)', '4x4 (dołączany automatycznie)'),
        ('4x4 (dołączany ręcznie)', '4x4 (dołączany ręcznie)'),
        ('4x4 (stały)', '4x4 (stały)'),
        ('Na przednie koła', 'Na przednie koła'),
        ('Na tylne koła', 'Na tylne koła'),
    ]

    EMISSION_CLASS_CHOICES = [
        ('Euro 1', 'Euro 1'),
        ('Euro 2', 'Euro 2'),
        ('Euro 3', 'Euro 3'),
        ('Euro 4', 'Euro 4'),
        ('Euro 5', 'Euro 5'),
        ('Euro 6', 'Euro 6'),
    ]

    COLOR_TYPE_CHOICES = [
        ('Matowy', 'Matowy'),
        ('Metalik', 'Metalik'),
        ('Perłowy', 'Perłowy'),
    ]

    SEAT_NUMBER_CHOICES = [
        (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'),
    ]

    COUNTRY_CHOICES = [
        ('Austria', 'Austria'),
        ('Belgia', 'Belgia'),
        ('Białoruś', 'Białoruś'),
        ('Bułgaria', 'Bułgaria'),
        ('Chorwacja', 'Chorwacja'),
        ('Czechy', 'Czechy'),
        ('Dania', 'Dania'),
        ('Estonia', 'Estonia'),
        ('Finlandia', 'Finlandia'),
        ('Francja', 'Francja'),
        ('Grecja', 'Grecja'),
        ('Hiszpania', 'Hiszpania'),
        ('Holandia', 'Holandia'),
        ('Inny', 'Inny'),
        ('Irlandia', 'Irlandia'),
        ('Islandia', 'Islandia'),
        ('Japonia', 'Japonia'),
        ('Kanada', 'Kanada'),
        ('Korea', 'Korea'),
        ('Liechtenstein', 'Liechtenstein'),
        ('Litwa', 'Litwa'),
        ('Luksemburg', 'Luksemburg'),
        ('Łotwa', 'Łotwa'),
        ('Monako', 'Monako'),
        ('Niemcy', 'Niemcy'),
        ('Norwegia', 'Norwegia'),
        ('Polska', 'Polska'),
        ('Rosja', 'Rosja'),
        ('Rumunia', 'Rumunia'),
        ('Słowacja', 'Słowacja'),
        ('Słowenia', 'Słowenia'),
        ('USA', 'USA'),
        ('Szwajcaria', 'Szwajcaria'),
        ('Szwecja', 'Szwecja'),
        ('Turcja', 'Turcja'),
        ('Ukraina', 'Ukraina'),
        ('Węgry', 'Węgry'),
        ('Wielka Brytania', 'Wielka Brytania'),
        ('Włochy', 'Włochy'),
    ]

    owner = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=200)
    price = models.IntegerField(null=True, blank=False, validators=[MaxValueValidator(9999999), MinValueValidator(1000)])
    variant = models.CharField(max_length=200, null=True, blank=False)
    brand = models.CharField(max_length=200, null=True, blank=False, choices=BRAND_CHOICES)
    phone = models.CharField(max_length=15, null=True, blank=False)
    description = models.TextField(max_length=3500, null=True, blank=False)
    featured_image1 = models.ImageField(null=True, blank=True, default='bmwcs.jpg')
    featured_image2 = models.ImageField(null=True, blank=True, default='bmwcs.jpg')
    featured_image3 = models.ImageField(null=True, blank=True, default='bmwcs.jpg')
    fuel_type = models.ForeignKey('Fuel', null=True, on_delete=models.DO_NOTHING)
    engine_capacity = models.IntegerField(null=True, blank=False, validators=[MaxValueValidator(9999), MinValueValidator(300)])
    power = models.IntegerField(null=True, blank=False, validators=[MaxValueValidator(5000), MinValueValidator(40)])
    mileage = models.IntegerField(null=True, blank=False, validators=[MaxValueValidator(500000), MinValueValidator(100)])
    no_crashed = models.CharField(max_length=200, null=True, blank=False, choices=YES_OR_NO)
    first_registration = models.IntegerField(null=True, blank=False)
    color = models.CharField(max_length=200, null=True, blank=False)
    num_of_doors = models.IntegerField(choices=SEAT_NUMBER_CHOICES, null=True, blank=False)
    color_type = models.CharField(max_length=200, choices=COLOR_TYPE_CHOICES, null=True, blank=False)
    street = models.CharField(max_length=100, null=True, blank=False)
    postal_code = models.CharField(max_length=20, null=True, blank=False)
    city = models.CharField(max_length=100, null=True, blank=False)
    city_fuel_consumption = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0)])
    highway_fuel_consumption = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0)])
    combined_fuel_consumption = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0)])
    co2_emission = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0)])
    emission_class = models.CharField(max_length=50, choices=EMISSION_CLASS_CHOICES, null=True, blank=True)
    eco_sticker = models.CharField(max_length=50, null=True, blank=True)
    economy = models.CharField(max_length=50, null=True, blank=True)

    #Nowe pola
    model = models.CharField(max_length=200, null=True, blank=True)
    registration_number = models.CharField(max_length=200, null=True, blank=True)
    has_registration_number = models.CharField(max_length=200, choices=YES_OR_NO, null=True, blank=True)
    registered_in_poland = models.CharField(max_length=200, choices=YES_OR_NO, null=True, blank=True)
    registered_as_antique = models.CharField(max_length=200, choices=YES_OR_NO, null=True, blank=True)
    first_owner = models.CharField(max_length=200, choices=YES_OR_NO, null=True, blank=True)
    serviced_in_aso = models.CharField(max_length=200, choices=YES_OR_NO, null=True, blank=True)
    condition = models.CharField(max_length=200, choices=CONDITION_CHOICES, null=True, blank=True)
    damaged = models.CharField(max_length=200, choices=YES_OR_NO, null=True, blank=True)
    imported = models.CharField(max_length=200, choices=YES_OR_NO, null=True, blank=True)
    transmission = models.CharField(max_length=200, choices=TRANSMISSION_CHOICES, null=True, blank=True)
    right_hand_drive = models.CharField(max_length=200, choices=YES_OR_NO, null=True, blank=True)
    drive = models.CharField(max_length=200, choices=DRIVE_CHOICES, null=True, blank=True)
    tuning = models.CharField(max_length=200, choices=YES_OR_NO, null=True, blank=True)
    truck_approval = models.CharField(max_length=200, choices=YES_OR_NO, null=True, blank=True)
    country_of_origin = models.CharField(max_length=200, choices=COUNTRY_CHOICES, null=True, blank=True)


    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('single-advert', kwargs={'id': str(self.id)})

    @property
    def get_photo_url(self):
        if self.featured_image1 and hasattr(self.featured_image1, 'url'):
            return self.featured_image1.url
        else:
            return "/static/images/bmwcs.jpg"


# class Brand(models.Model):
#     name = models.CharField(max_length=200)
#     created = models.DateTimeField(auto_now_add=True)
#     id = models.UUIDField(default=uuid.uuid4, unique=True,
#                           primary_key=True, editable=False)

#     def __str__(self):
#         return self.name


class Fuel(models.Model):
    name = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.name


class PriceReminderConnection(models.Model):
    user_address = models.EmailField(max_length=200)
    id_of_advert = models.CharField(max_length=50)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self):
        return self.user_address

class Comment(models.Model):
    advert = models.ForeignKey(Advert,
                             on_delete=models.CASCADE,
                             related_name='comments')
    name = models.CharField(max_length=30)
    body = models.TextField()
    comment_image1 = models.ImageField(null=True, blank=True)
    comment_image2 = models.ImageField(null=True, blank=True)
    comment_image3 = models.ImageField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['created']
        indexes = [
            models.Index(fields=['created']),
        ]

    def __str__(self):
        return f"Comment by {self.name}"

    @property
    def get_photo_url(self):
        if self.comment_image1 and hasattr(self.comment_image1, 'url'):
            return self.comment_image1.url
        else:
            return "/static/images/bmwcs.jpg"