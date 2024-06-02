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
                  'address', 'phone', 'description',
                  'featured_image1', 'featured_image2', 'featured_image3',
                  'fuel_type', 'engine_capacity', 'power', 'mileage',
                  'no_crashed', 'first_registration', 'color', 'num_of_doors',
                  'color_type', 'city_fuel_consumption', 'highway_fuel_consumption',
                  'combined_fuel_consumption', 'co2_emission', 'emission_class',
                  'eco_sticker']

        widgets = {
            'title': forms.TextInput(
                attrs={'id': 'title', 'class': 'bg-light form-control', 'placeholder': 'Tytuł ogłoszenia'}),
            'price': forms.NumberInput(attrs={'id': 'price', 'class': 'bg-light form-control', 'placeholder': 'Cena w złotych:'}),
            'variant': forms.TextInput(
                attrs={'id': 'variant', 'class': 'bg-light form-control', 'placeholder': 'Podaj wariant'}),
            'brand': forms.Select(attrs={'id': 'brand', 'class': 'bg-light form-control'}),
            'address': forms.TextInput(
                attrs={'id': 'address', 'class': 'bg-light form-control', 'placeholder': 'np. Koszalin, Młyńska 10'}),
            'phone': forms.TextInput(
                attrs={'id': 'phone', 'class': 'bg-light form-control', 'placeholder': '"123-123-123"',
                       'pattern': "[0-9]{3}-[0-9]{3}-[0-9]{3}"}),
            'description': forms.Textarea(
                attrs={'id': 'description', 'class': 'bg-light form-control', 'placeholder': 'Max 5000 znaków'}),
            'featured_image1': forms.FileInput(attrs={'id': 'featured_image1', 'class': 'form-control-file'}),
            'featured_image2': forms.FileInput(attrs={'id': 'featured_image2', 'class': 'form-control-file'}),
            'featured_image3': forms.FileInput(attrs={'id': 'featured_image3', 'class': 'form-control-file'}),
            'fuel_type': forms.Select(attrs={'id': 'fuel_type', 'class': 'bg-light form-control'}),
            'engine_capacity': forms.NumberInput(attrs={'id': 'engine_capacity', 'class': 'bg-light form-control', 'placeholder': 'np. 1989'}),
            'power': forms.NumberInput(attrs={'id': 'power', 'class': 'bg-light form-control', 'placeholder': 'KM'}),
            'mileage': forms.NumberInput(attrs={'id': 'mileage', 'class': 'bg-light form-control', 'placeholder': 'np. 62500'}),
            'no_crashed': forms.Select(attrs={'id': 'no_crashed', 'class': 'form-control'}),
            'first_registration': forms.NumberInput(
                attrs={'id': 'first_registration', 'class': 'bg-light form-control', 'placeholder': 'np. 2015'}),
            'color': forms.TextInput(attrs={'id': 'color', 'class': 'form-control', 'placeholder': 'np. czerwony'}),
            'num_of_doors': forms.NumberInput(attrs={'id': 'num_of_doors', 'class': 'form-control', 'placeholder': 'np. 5'}),
            'color_type': forms.TextInput(attrs={'id': 'color_type', 'class': 'form-control', 'placeholder': 'np. metaliczny'}),
            'city_fuel_consumption': forms.NumberInput(attrs={'id': 'city_fuel_consumption', 'class': 'form-control', 'placeholder': 'L/100km'}),
            'highway_fuel_consumption': forms.NumberInput(attrs={'id': 'highway_fuel_consumption', 'class': 'form-control', 'placeholder': 'L/100km'}),
            'combined_fuel_consumption': forms.NumberInput(attrs={'id': 'combined_fuel_consumption', 'class': 'form-control', 'placeholder': 'L/100km'}),
            'co2_emission': forms.NumberInput(attrs={'id': 'co2_emission', 'class': 'form-control', 'placeholder': 'g/km'}),
            'emission_class': forms.Select(attrs={'id': 'emission_class', 'class': 'form-control'}),
            'eco_sticker': forms.TextInput(attrs={'id': 'eco_sticker', 'class': 'form-control', 'placeholder': 'np. 4 (Zielona)'}),
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
