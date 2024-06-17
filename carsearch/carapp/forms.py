from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, UserCreationForm
from .models import User, Profile, Advert, Comment
from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm
from django.forms import TextInput, Textarea

BODY_TYPE_CHOICES = [
    ('Coupe', 'Coupe'),
    ('Kabriolet', 'Kabriolet'),
    ('Kombi', 'Kombi'),
    ('Kompakt', 'Kompakt'),
    ('Sedan', 'Sedan'),
    ('SUV', 'SUV'),
]

BRAND_CHOICES = [
    ('Fiat', 'Fiat'),
    ('KIA', 'KIA'),
    ('BMW', 'BMW'),
    ('Opel', 'Opel'),
    ('Audi', 'Audi'),
    ('Renault', 'Renault'),
]

PRICE_CHOICES = [
    (3000, '3000 PLN'),
    (5000, '5000 PLN'),
    (10000, '10 000 PLN'),
    (15000, '15 000 PLN'),
    (20000, '20 000 PLN'),
    (25000, '25 000 PLN'),
    (30000, '30 000 PLN'),
    (35000, '35 000 PLN'),
    (40000, '40 000 PLN'),
    (50000, '50 000 PLN'),
    (65000, '65 000 PLN'),
    (80000, '80 000 PLN'),
    (100000, '100 000 PLN'),
    (200000, '200 000 PLN'),
    (500000, '500 000 PLN'),
    (1000000, '1 000 000 PLN'),
    (7500000, '7 500 000 PLN'),
]

MILEAGE_CHOICES = [
    (20000, '20 000 km'),
    (35000, '35 000 km'),
    (50000, '50 000 km'),
    (75000, '75 000 km'),
    (100000, '100 000 km'),
    (125000, '125 000 km'),
    (150000, '150 000 km'),
    (200000, '200 000 km'),
    (250000, '250 000 km'),
]

CAPACITY_CHOICES = [
    (900, '900 cm3'),
    (1000, '1000 cm3'),
    (1250, '1250 cm3'),
    (1500, '1500 cm3'),
    (2000, '2000 cm3'),
    (2500, '2500 cm3'),
    (3000, '3000 cm3'),
    (4000, '4000 cm3'),
    (5000, '5000 cm3'),
    (6000, '6000 cm3'),
]

POWER_CHOICES = [
    (50, '50 KM'),
    (80, '80 KM'),
    (120, '120 KM'),
    (150, '150 KM'),
    (200, '200 KM'),
    (300, '300 KM'),
    (500, '500 KM'),
]

YEAR_CHOICES = [(year, year) for year in range(2022, 2004, -1)]

NO_CRASHED = [
    ('Tak', 'Tak'),
    ('Nie', 'Nie'),
]

CONSUMPTION_CHOICES = [
    ('Niskie', 'Niskie'),
    ('Średnie', 'Średnie'),
    ('Wysokie', 'Wysokie'),
]


class FilterForm(forms.Form):
    variant = forms.MultipleChoiceField(choices=BODY_TYPE_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)
    price_min = forms.ChoiceField(choices=[('', 'od')] + PRICE_CHOICES, required=False)
    price_max = forms.ChoiceField(choices=[('', 'do')] + PRICE_CHOICES, required=False)
    mileage_min = forms.ChoiceField(choices=[('', 'od')] + MILEAGE_CHOICES, required=False)
    mileage_max = forms.ChoiceField(choices=[('', 'do')] + MILEAGE_CHOICES, required=False)
    year_min = forms.ChoiceField(choices=[('', 'od')] + YEAR_CHOICES, required=False)
    year_max = forms.ChoiceField(choices=[('', 'do')] + YEAR_CHOICES, required=False)
    engine_capacity_min = forms.ChoiceField(choices=[('', 'od')] + CAPACITY_CHOICES, required=False)
    engine_capacity_max = forms.ChoiceField(choices=[('', 'do')] + CAPACITY_CHOICES, required=False)
    power_min = forms.ChoiceField(choices=[('', 'od')] + POWER_CHOICES, required=False)
    power_max = forms.ChoiceField(choices=[('', 'do')] + POWER_CHOICES, required=False)
    no_crashed = forms.ChoiceField(choices=[('', 'Czy bezwypadkowe?')] + NO_CRASHED, required=False)
    brand = forms.MultipleChoiceField(choices=BRAND_CHOICES, widget=forms.CheckboxSelectMultiple, required=False)
    consumption = forms.MultipleChoiceField(choices=CONSUMPTION_CHOICES, widget=forms.CheckboxSelectMultiple,required=False)
    only_eco = forms.BooleanField(required=False)

    # def __init__(self, *args, **kwargs):
    #     super(FilterForm, self).__init__(*args, **kwargs)
    #     # self.fields['brand'].choices = [(brand, brand) for brand in Advert.objects.values_list('brand', flat=True).distinct()]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'body', 'comment_image1', 'comment_image2', 'comment_image3']
        labels = {
            'name': 'Imię',
            'body': 'Treść',
        }
        widgets = {
            'name': TextInput(attrs={'placeholder': 'Twoje imię', 'class': 'bg-light form-control fw-light'}),
            'body': Textarea(attrs={'placeholder': 'Co chcesz powiedzieć?', 'class': 'bg-light form-control fw-light'}),
        }

class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
                                'class': 'bg-light form-control',
                                'placeholder': 'Enter your username'})
        self.fields['password'].widget.attrs.update({
                                'id': 'password',
                                'class': 'form-control bg-light',
                                'placeholder': 'Enter your password'})


class CaptchaPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'bg-light form-control', 'placeholder': 'Enter your email'})


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
                                    'id': 'email',
                                    'class': 'bg-light form-control',
                                    'placeholder': 'Enter your email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
                                    'id': 'password',
                                    'class': 'bg-light form-control',
                                    'placeholder': 'Enter password'}))


class CustomUserCreationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
                                'id': 'password1',
                                'class': 'bg-light form-control',
                                'placeholder': 'Wprowadź hasło'})
        self.fields['password2'].widget.attrs.update({
                                'id': 'password2',
                                'class': 'bg-light form-control',
                                'placeholder': 'Powtórz hasło'})

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

        widgets = {
            'username': forms.TextInput(attrs={
                                    'id': 'username',
                                    'class': 'bg-light form-control',
                                    'placeholder': 'Wprowadź nazwę użytkownika'}),
            'email': forms.EmailInput(attrs={
                                    'id': 'email',
                                    'class': 'bg-light form-control',
                                    'placeholder': 'Wprowadź adres e-mail'}),
            # 'password1' : forms.PasswordInput(attrs={
            #                         'id': 'password1',
            #                         'class': 'form-control bg-light',
            #                         'placeholder': 'Enter password'}),
            # 'password2' : forms.PasswordInput(attrs={
            #                         'id': 'password2',
            #                         'class': 'form-control bg-light',
            #                         'placeholder': 'Repeat password'}),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'surname', 'email', 'username', 'location_city', 'location_country', 'seller', 'phone_number',
                  'bio', 'profile_image']
        labels = {
            'name':   _('Full Name'),
        }

        widgets = {
            'name': forms.TextInput(attrs={
                                'id': 'name',
                                'class': 'bg-light form-control',
                                'disabled': 'disabled'}),
            'surname': forms.TextInput(attrs={
                                'id': 'name',
                                'class': 'bg-light form-control',
                                'disabled': 'disabled'}),
            'email': forms.TextInput(attrs={
                                'id': 'eMail',
                                'class': 'bg-light form-control',
                                'disabled': 'disabled'}),
            'username': forms.TextInput(attrs={
                                'id': 'username',
                                'class': 'bg-light form-control',
                                'disabled': 'disabled'}),
            'location_city': forms.TextInput(attrs={
                                'id': 'locationCity',
                                'class': 'bg-light form-control',
                                'disabled': 'disabled'}),
            'location_country': forms.TextInput(attrs={
                                'id': 'locationCountry',
                                'class': 'bg-light form-control',
                                'disabled': 'disabled'}),
            'seller': forms.Select(attrs={
                                'id': 'seller',
                                'class': 'bg-light form-control',
                                'disabled': 'disabled'}),
            'phone_number': forms.TextInput(attrs={
                                'id': 'shortIntro',
                                'class': 'bg-light form-control',
                                'disabled': 'disabled'}),
            'bio': forms.Textarea(attrs={
                                'id': 'bio',
                                'class': 'bg-light form-control',
                                'rows': '7',
                                'maxlength': '300',
                                'minlength': '20',
                                'disabled': 'disabled'}),
            'profile_image': forms.FileInput(attrs={
                                'id': 'imageProfile',
                                'class': 'edit-photo rounded-circle img-fluid border border-dark',
                                'disabled': 'disabled'}),
        }


class ProfileFormEditable(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'surname', 'email', 'username', 'location_city', 'location_country', 'seller', 'phone_number',
                  'bio', 'profile_image']
        labels = {
            'name':   _('Full Name'),
        }

        widgets = {
            'name': forms.TextInput(attrs={
                                'id': 'name',
                                'class': 'bg-light form-control'}),
            'surname': forms.TextInput(attrs={
                                'id': 'name',
                                'class': 'bg-light form-control'}),
            'email': forms.TextInput(attrs={
                                'id': 'eMail',
                                'class': 'bg-light form-control'}),
            'username': forms.TextInput(attrs={
                                'id': 'username',
                                'class': 'bg-light form-control'}),
            'location_city': forms.TextInput(attrs={
                                'id': 'locationCity',
                                'class': 'bg-light form-control'}),
            'location_country': forms.TextInput(attrs={
                                'id': 'locationCountry',
                                'class': 'bg-light form-control'}),
            'seller': forms.Select(attrs={
                                'id': 'seller',
                                'class': 'bg-light form-control'}),
            'phone_number': forms.TextInput(attrs={
                                'id': 'shortIntro',
                                'class': 'bg-light form-control'}),
            'bio': forms.Textarea(attrs={
                                'id': 'bio',
                                'class': 'bg-light form-control',
                                'rows': '7',
                                'maxlength': '300',
                                'minlength': '20'}),
            'profile_image': forms.FileInput(attrs={
                                'id': 'imageProfile'}),
        }




class AdvertForm(ModelForm):
    class Meta:
        model = Advert
        fields = ['title', 'price', 'variant', 'brand',
                  'phone', 'street', 'postal_code', 'city', 'description',
                  'featured_image1', 'featured_image2', 'featured_image3',
                  'featured_image4', 'featured_image5', 'featured_image6',
                  'featured_image7', 'featured_image8',
                  'fuel_type', 'engine_capacity', 'power', 'mileage',
                  'no_crashed', 'first_registration', 'color', 'num_of_doors',
                  'color_type', 'city_fuel_consumption', 'highway_fuel_consumption',
                  'combined_fuel_consumption', 'co2_emission', 'emission_class',
                  'eco_sticker', 'model', 'has_registration_number',
                  'registered_in_poland', 'registered_as_antique', 'first_owner', 'serviced_in_aso', 
                  'condition', 'damaged', 'imported', 'transmission', 'right_hand_drive', 
                  'drive', 'truck_approval', 'country_of_origin',
                  'apple_carplay', 'android_auto', 'bluetooth_interface', 'radio', 'handsfree_kit', 'usb_socket',
                  'wireless_charging', 'navigation_system', 'sound_system', 'head_up_display', 'touchscreen',
                  'voice_control', 'internet_access', 'air_conditioning', 'rear_passenger_air_conditioning', 'folding_roof',
                  'sunshade', 'openable_roof', 'electric_driver_seat', 'electric_passenger_seat', 'heated_driver_seat',
                  'heated_passenger_seat', 'lumbar_support_driver', 'lumbar_support_passenger', 'ventilated_front_seats',
                  'massage_front_seats', 'seat_memory', 'sport_front_seats', 'heated_rear_seats', 'ventilated_rear_seats',
                  'massage_rear_seats', 'front_armrest', 'rear_armrest', 'leather_steering_wheel', 'sport_steering_wheel',
                  'steering_wheel_radio_controls', 'electric_steering_column', 'multifunction_steering_wheel', 'heated_steering_wheel',
                  'paddle_shifters', 'leather_gear_knob', 'digital_key', 'keyless_entry', 'keyless_go', 'engine_start_without_key',
                  'automatic_climate_control', 'heated_front_windshield', 'electric_front_windows', 'tinted_rear_windows',
                  'remote_openable_roof', 'parking_heater', 'rain_sensor', 'wipers', 'electric_rear_windows', 'electric_roof', 'tow_hook',
                  'energy_recovery_system', 'fast_charging_function', 'charging_cable', 'cruise_control', 'park_assist', 'rear_distance_control',
                  'panoramic_camera_360', 'electric_vehicle_presence_control', 'side_mirror_memory', 'side_mirror_camera', 'automatic_parking_assistant',
                  'heated_side_mirrors', 'lane_assist', 'active_lane_change_assistant', 'speed_limiter', 'brake_assist', 'hill_holder_automatic_occupancy_control',
                  'hill_holder_assistance', 'active_speed_limit_sign_recognition', 'uphill_start_assistance', 'high_beam_assistant', 'cornering_lights',
                  'adaptive_lighting', 'dynamic_cornering_lights', 'dusk_sensor', 'headlight_washers', 'daytime_running_lights', 'led_daytime_running_lights',
                  'fog_lights', 'led_fog_lights', 'led_rear_lights', 'home_lighting', 'led_interior_lighting', 'start_stop_system', 'electronic_tire_pressure_control',
                  'electric_parking_brake', 'power_steering', 'differential_lock', 'adjustable_central_differential', 'traffic_jam_assistant',
                  'runflat_tires', 'comfort_suspension', 'electronic_suspension_control',
                  'sport_suspension', 'adjustable_suspension', 'pneumatic_suspension',
                  'hydropneumatic_suspension', 'ceramic_composite_brakes', 'particulate_filter',
                  'abs', 'electronic_brake_distribution', 'emergency_brake_assist', 'active_city_brake_assist',
                  'driver_fatigue_warning', 'collision_warning', 'side_impact_protection', 'rear_impact_protection',
                  'engine_sound_elimination', 'rear_cross_traffic_alert', 'lane_keeping_assist',
                  'obstacle_detection_assist', 'cornering_stability_assist', 'rear_collision_mitigation',
                  'central_airbag', 'driver_side_airbag', 'front_side_airbags', 'rear_side_airbags',
                  'rear_curtain_airbags', 'passenger_airbag', 'isofix', 'rollover_protection']

        widgets = {
            'title': forms.TextInput(
                attrs={'id': 'title', 'class': 'bg-light form-control', 'placeholder': 'Tytuł ogłoszenia'}),
            'price': forms.NumberInput(attrs={'id': 'price', 'class': 'bg-light form-control', 'placeholder': 'Cena w złotych:'}),
            'variant': forms.TextInput(
                attrs={'id': 'variant', 'class': 'bg-light form-control', 'placeholder': 'Podaj wariant'}),
            'brand': forms.Select(attrs={'id': 'brand', 'class': 'bg-light form-control'}),
            'phone': forms.TextInput(
                attrs={'id': 'phone', 'class': 'bg-light form-control', 'placeholder': '"123-123-123"',
                       'pattern': "[0-9]{3}-[0-9]{3}-[0-9]{3}"}),
            'description': forms.Textarea(
                attrs={'id': 'description', 'class': 'bg-light form-control', 'placeholder': 'Max 5000 znaków'}),
            'featured_image1': forms.FileInput(attrs={'id': 'featured_image1', 'class': 'form-control-file'}),
            'featured_image2': forms.FileInput(attrs={'id': 'featured_image2', 'class': 'form-control-file'}),
            'featured_image3': forms.FileInput(attrs={'id': 'featured_image3', 'class': 'form-control-file'}),
            'featured_image4': forms.FileInput(attrs={'id': 'featured_image4', 'class': 'form-control-file'}),
            'featured_image5': forms.FileInput(attrs={'id': 'featured_image5', 'class': 'form-control-file'}),
            'featured_image6': forms.FileInput(attrs={'id': 'featured_image6', 'class': 'form-control-file'}),
            'featured_image7': forms.FileInput(attrs={'id': 'featured_image7', 'class': 'form-control-file'}),
            'featured_image8': forms.FileInput(attrs={'id': 'featured_image8', 'class': 'form-control-file'}),
            'fuel_type': forms.Select(attrs={'id': 'fuel_type', 'class': 'bg-light form-control'}),
            'engine_capacity': forms.NumberInput(attrs={'id': 'engine_capacity', 'class': 'bg-light form-control', 'placeholder': 'np. 1989'}),
            'power': forms.NumberInput(attrs={'id': 'power', 'class': 'bg-light form-control', 'placeholder': 'KM'}),
            'mileage': forms.NumberInput(attrs={'id': 'mileage', 'class': 'bg-light form-control', 'placeholder': 'np. 62500'}),
            'no_crashed': forms.Select(attrs={'id': 'no_crashed', 'class': 'form-control'}),
            'first_registration': forms.NumberInput(
                attrs={'id': 'first_registration', 'class': 'bg-light form-control', 'placeholder': 'np. 2015'}),
            'color': forms.TextInput(attrs={'id': 'color', 'class': 'form-control', 'placeholder': 'np. czerwony'}),
            'num_of_doors': forms.Select(attrs={'id': 'num_of_doors', 'class': 'form-control'}),
            'color_type': forms.Select(attrs={'id': 'color_type', 'class': 'form-control'}),
            'city_fuel_consumption': forms.NumberInput(attrs={'id': 'city_fuel_consumption', 'class': 'form-control', 'placeholder': 'L/100km'}),
            'highway_fuel_consumption': forms.NumberInput(attrs={'id': 'highway_fuel_consumption', 'class': 'form-control', 'placeholder': 'L/100km'}),
            'combined_fuel_consumption': forms.NumberInput(attrs={'id': 'combined_fuel_consumption', 'class': 'form-control', 'placeholder': 'L/100km'}),
            'co2_emission': forms.NumberInput(attrs={'id': 'co2_emission', 'class': 'form-control', 'placeholder': 'g/km'}),
            'emission_class': forms.Select(attrs={'id': 'emission_class', 'class': 'form-control'}),
            'eco_sticker': forms.TextInput(attrs={'id': 'eco_sticker', 'class': 'form-control', 'placeholder': 'np. 4 (Zielona)'}),
            'street': forms.TextInput(attrs={'id': 'street', 'class': 'bg-light form-control', 'placeholder': 'Ulica'}),
            'postal_code': forms.TextInput(attrs={'id': 'postal_code', 'class': 'bg-light form-control', 'placeholder': 'Kod pocztowy'}),
            'city': forms.TextInput(attrs={'id': 'city', 'class': 'bg-light form-control', 'placeholder': 'Miasto'}),
            'model': forms.TextInput(attrs={'class': 'form-control', 'required': False}),
            'has_registration_number': forms.Select(attrs={'class': 'form-control', 'required': False}),
            'registered_in_poland': forms.Select(attrs={'class': 'form-control', 'required': False}),
            'registered_as_antique': forms.Select(attrs={'class': 'form-control', 'required': False}),
            'first_owner': forms.Select(attrs={'class': 'form-control', 'required': False}),
            'serviced_in_aso': forms.Select(attrs={'class': 'form-control', 'required': False}),
            'condition': forms.Select(attrs={'class': 'form-control', 'required': False}),
            'damaged': forms.Select(attrs={'class': 'form-control', 'required': False}),
            'imported': forms.Select(attrs={'class': 'form-control', 'required': False}),
            'transmission': forms.Select(attrs={'class': 'form-control', 'required': False}),
            'right_hand_drive': forms.Select(attrs={'class': 'form-control', 'required': False}),
            'drive': forms.Select(attrs={'class': 'form-control', 'required': False}),
            'truck_approval': forms.Select(attrs={'class': 'form-control', 'required': False}),
            'country_of_origin': forms.Select(attrs={'class': 'form-control', 'required': False}),
            'apple_carplay': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'android_auto': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'bluetooth_interface': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'radio': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'handsfree_kit': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'usb_socket': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'wireless_charging': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'navigation_system': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'sound_system': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'head_up_display': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'touchscreen': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'voice_control': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'internet_access': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'air_conditioning': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'rear_passenger_air_conditioning': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'folding_roof': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'sunshade': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'openable_roof': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'electric_driver_seat': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'electric_passenger_seat': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'heated_driver_seat': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'heated_passenger_seat': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'lumbar_support_driver': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'lumbar_support_passenger': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'ventilated_front_seats': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'massage_front_seats': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'seat_memory': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'sport_front_seats': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'heated_rear_seats': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'ventilated_rear_seats': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'massage_rear_seats': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'front_armrest': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'rear_armrest': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'leather_steering_wheel': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'sport_steering_wheel': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'steering_wheel_radio_controls': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'electric_steering_column': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'multifunction_steering_wheel': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'heated_steering_wheel': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'paddle_shifters': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'leather_gear_knob': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'digital_key': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'keyless_entry': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'keyless_go': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'engine_start_without_key': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'automatic_climate_control': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'heated_front_windshield': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'electric_front_windows': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'tinted_rear_windows': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'remote_openable_roof': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'parking_heater': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'rain_sensor': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'wipers': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'electric_rear_windows': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'electric_roof': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'tow_hook': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'energy_recovery_system': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'fast_charging_function': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'charging_cable': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'cruise_control': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'park_assist': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'rear_distance_control': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'panoramic_camera_360': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'electric_vehicle_presence_control': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'side_mirror_memory': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'side_mirror_camera': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'automatic_parking_assistant': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'heated_side_mirrors': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'lane_assist': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'active_lane_change_assistant': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'speed_limiter': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'brake_assist': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'hill_holder_automatic_occupancy_control': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'hill_holder_assistance': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'active_speed_limit_sign_recognition': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'uphill_start_assistance': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'high_beam_assistant': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'cornering_lights': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'adaptive_lighting': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'dynamic_cornering_lights': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'dusk_sensor': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'headlight_washers': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'daytime_running_lights': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'led_daytime_running_lights': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'fog_lights': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'led_fog_lights': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'led_rear_lights': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'home_lighting': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'led_interior_lighting': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'start_stop_system': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'electronic_tire_pressure_control': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'electric_parking_brake': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'power_steering': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'differential_lock': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'adjustable_central_differential': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'traffic_jam_assistant': forms.CheckboxInput(attrs={'class': 'form-check-input', 'required': False}),
            'runflat_tires': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'comfort_suspension': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'electronic_suspension_control': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'sport_suspension': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'adjustable_suspension': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'pneumatic_suspension': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'hydropneumatic_suspension': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'ceramic_composite_brakes': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'particulate_filter': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'abs': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'electronic_brake_distribution': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'emergency_brake_assist': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'active_city_brake_assist': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'driver_fatigue_warning': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'collision_warning': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'side_impact_protection': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'rear_impact_protection': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'engine_sound_elimination': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'rear_cross_traffic_alert': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'lane_keeping_assist': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'obstacle_detection_assist': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'cornering_stability_assist': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'rear_collision_mitigation': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'central_airbag': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'driver_side_airbag': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'front_side_airbags': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'rear_side_airbags': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'rear_curtain_airbags': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'passenger_airbag': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'isofix': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'rollover_protection': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        

        
class EmailPriceForm(forms.Form):

    name = forms.CharField(max_length=25)
    your_address = forms.EmailField()
    your_phone = forms.CharField()
    comments = forms.CharField(required=False, widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({
                            'class': 'bg-light form-control',
                            'placeholder': 'Wprowadź swoje imie i nazwisko'})
        self.fields['name'].label = "Imię i Nazwisko:"
        self.fields['your_address'].widget.attrs.update({
                            'class': 'bg-light form-control',
                            'placeholder': 'Podaj swój adres e-mail'})
        self.fields['your_address'].label = "Twój e-mail:"
        self.fields['your_phone'].widget.attrs.update({
                            'class': 'bg-light form-control',
                            'pattern': '[0-9]{3}-[0-9]{3}-[0-9]{3}',
                            'placeholder': 'Podaj swój numer telefonu np. 777-888-999'})
        self.fields['your_phone'].label = "Numer telefonu:"
        self.fields['comments'].widget.attrs.update({
                            'class': 'bg-light form-control',
                            'placeholder': 'Dodaj wiadomość do sprzedawcy (opcjonalne)'})
        self.fields['comments'].label = "Komentarz:"


class EmailPriceReminderForm(forms.Form):

    your_address = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['your_address'].widget.attrs.update({
                                'class': 'bg-light form-control',
                                'placeholder': 'Podaj swój adres e-mail'})
        self.fields['your_address'].label = "Twój e-mail:"
