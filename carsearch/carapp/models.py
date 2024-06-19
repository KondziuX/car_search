from django.db import models
from django.contrib.auth.models import User
import uuid
from django.core.validators import MaxValueValidator, MinValueValidator
from django.urls import reverse
from datetime import timedelta
from django.utils import timezone



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
    featured_image4 = models.ImageField(null=True, blank=True, default='bmwcs.jpg')
    featured_image5 = models.ImageField(null=True, blank=True, default='bmwcs.jpg')
    featured_image6 = models.ImageField(null=True, blank=True, default='bmwcs.jpg')
    featured_image7 = models.ImageField(null=True, blank=True, default='bmwcs.jpg')
    featured_image8 = models.ImageField(null=True, blank=True, default='bmwcs.jpg')
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
    truck_approval = models.CharField(max_length=200, choices=YES_OR_NO, null=True, blank=True)
    country_of_origin = models.CharField(max_length=200, choices=COUNTRY_CHOICES, null=True, blank=True)

    # Audio i multimedia
    apple_carplay = models.BooleanField(default=False)
    android_auto = models.BooleanField(default=False)
    bluetooth_interface = models.BooleanField(default=False)
    radio = models.BooleanField(default=False)
    handsfree_kit = models.BooleanField(default=False)
    usb_socket = models.BooleanField(default=False)
    wireless_charging = models.BooleanField(default=False)
    navigation_system = models.BooleanField(default=False)
    sound_system = models.BooleanField(default=False)
    head_up_display = models.BooleanField(default=False)
    touchscreen = models.BooleanField(default=False)
    voice_control = models.BooleanField(default=False)
    internet_access = models.BooleanField(default=False)

    # Komfort
    air_conditioning = models.BooleanField(default=False)
    rear_passenger_air_conditioning = models.BooleanField(default=False)
    folding_roof = models.BooleanField(default=False)
    sunshade = models.BooleanField(default=False)
    openable_roof = models.BooleanField(default=False)
    electric_driver_seat = models.BooleanField(default=False)
    electric_passenger_seat = models.BooleanField(default=False)
    heated_driver_seat = models.BooleanField(default=False)
    heated_passenger_seat = models.BooleanField(default=False)
    lumbar_support_driver = models.BooleanField(default=False)
    lumbar_support_passenger = models.BooleanField(default=False)
    ventilated_front_seats = models.BooleanField(default=False)
    massage_front_seats = models.BooleanField(default=False)
    seat_memory = models.BooleanField(default=False)
    sport_front_seats = models.BooleanField(default=False)
    heated_rear_seats = models.BooleanField(default=False)
    ventilated_rear_seats = models.BooleanField(default=False)
    massage_rear_seats = models.BooleanField(default=False)
    front_armrest = models.BooleanField(default=False)
    rear_armrest = models.BooleanField(default=False)
    leather_steering_wheel = models.BooleanField(default=False)
    sport_steering_wheel = models.BooleanField(default=False)
    steering_wheel_radio_controls = models.BooleanField(default=False)
    electric_steering_column = models.BooleanField(default=False)
    multifunction_steering_wheel = models.BooleanField(default=False)
    heated_steering_wheel = models.BooleanField(default=False)
    paddle_shifters = models.BooleanField(default=False)
    leather_gear_knob = models.BooleanField(default=False)
    digital_key = models.BooleanField(default=False)
    keyless_entry = models.BooleanField(default=False)
    keyless_go = models.BooleanField(default=False)
    engine_start_without_key = models.BooleanField(default=False)
    automatic_climate_control = models.BooleanField(default=False)
    heated_front_windshield = models.BooleanField(default=False)
    electric_front_windows = models.BooleanField(default=False)
    tinted_rear_windows = models.BooleanField(default=False)
    remote_openable_roof = models.BooleanField(default=False)
    parking_heater = models.BooleanField(default=False)
    rain_sensor = models.BooleanField(default=False)
    wipers = models.BooleanField(default=False)
    electric_rear_windows = models.BooleanField(default=False)
    electric_roof = models.BooleanField(default=False)
    tow_hook = models.BooleanField(default=False)

    # Samochody elektryczne
    energy_recovery_system = models.BooleanField(default=False)
    fast_charging_function = models.BooleanField(default=False)
    charging_cable = models.BooleanField(default=False)

    # Systemy wspomagania kierownicy
    cruise_control = models.BooleanField(default=False)
    park_assist = models.BooleanField(default=False)
    rear_distance_control = models.BooleanField(default=False)
    panoramic_camera_360 = models.BooleanField(default=False)
    electric_vehicle_presence_control = models.BooleanField(default=False)
    side_mirror_memory = models.BooleanField(default=False)
    side_mirror_camera = models.BooleanField(default=False)
    automatic_parking_assistant = models.BooleanField(default=False)
    heated_side_mirrors = models.BooleanField(default=False)
    lane_assist = models.BooleanField(default=False)
    active_lane_change_assistant = models.BooleanField(default=False)
    speed_limiter = models.BooleanField(default=False)
    brake_assist = models.BooleanField(default=False)
    hill_holder_automatic_occupancy_control = models.BooleanField(default=False)
    hill_holder_assistance = models.BooleanField(default=False)
    active_speed_limit_sign_recognition = models.BooleanField(default=False)
    uphill_start_assistance = models.BooleanField(default=False)
    high_beam_assistant = models.BooleanField(default=False)
    cornering_lights = models.BooleanField(default=False)
    adaptive_lighting = models.BooleanField(default=False)
    dynamic_cornering_lights = models.BooleanField(default=False)
    dusk_sensor = models.BooleanField(default=False)
    headlight_washers = models.BooleanField(default=False)
    daytime_running_lights = models.BooleanField(default=False)
    led_daytime_running_lights = models.BooleanField(default=False)
    fog_lights = models.BooleanField(default=False)
    led_fog_lights = models.BooleanField(default=False)
    led_rear_lights = models.BooleanField(default=False)
    home_lighting = models.BooleanField(default=False)
    led_interior_lighting = models.BooleanField(default=False)
    start_stop_system = models.BooleanField(default=False)
    electronic_tire_pressure_control = models.BooleanField(default=False)
    electric_parking_brake = models.BooleanField(default=False)
    power_steering = models.BooleanField(default=False)
    differential_lock = models.BooleanField(default=False)
    adjustable_central_differential = models.BooleanField(default=False)
    traffic_jam_assistant = models.BooleanField(default=False)

    # Performance and Tuning
    runflat_tires = models.BooleanField(default=False)
    comfort_suspension = models.BooleanField(default=False)
    electronic_suspension_control = models.BooleanField(default=False)
    sport_suspension = models.BooleanField(default=False)
    adjustable_suspension = models.BooleanField(default=False)
    pneumatic_suspension = models.BooleanField(default=False)
    hydropneumatic_suspension = models.BooleanField(default=False)
    ceramic_composite_brakes = models.BooleanField(default=False)
    particulate_filter = models.BooleanField(default=False)

    # Safety
    abs = models.BooleanField(default=False)
    electronic_brake_distribution = models.BooleanField(default=False)
    emergency_brake_assist = models.BooleanField(default=False)
    active_city_brake_assist = models.BooleanField(default=False)
    driver_fatigue_warning = models.BooleanField(default=False)
    collision_warning = models.BooleanField(default=False)
    side_impact_protection = models.BooleanField(default=False)
    rear_impact_protection = models.BooleanField(default=False)
    engine_sound_elimination = models.BooleanField(default=False)
    rear_cross_traffic_alert = models.BooleanField(default=False)
    lane_keeping_assist = models.BooleanField(default=False)
    obstacle_detection_assist = models.BooleanField(default=False)
    cornering_stability_assist = models.BooleanField(default=False)
    rear_collision_mitigation = models.BooleanField(default=False)
    central_airbag = models.BooleanField(default=False)
    driver_side_airbag = models.BooleanField(default=False)
    front_side_airbags = models.BooleanField(default=False)
    rear_side_airbags = models.BooleanField(default=False)
    rear_curtain_airbags = models.BooleanField(default=False)
    passenger_airbag = models.BooleanField(default=False)
    isofix = models.BooleanField(default=False)
    rollover_protection = models.BooleanField(default=False)


    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    expiry_date = models.DateTimeField(default=timezone.now() + timedelta(days=30))

    def save(self, *args, **kwargs):
        if not self.id:
            # Ogłoszenie jest tworzone
            self.expiry_date = self.created + timedelta(days=30)
        super().save(*args, **kwargs)

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