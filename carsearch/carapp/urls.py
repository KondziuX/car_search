"""carsearch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.contrib.auth import views as auth_views
from .forms import CustomLoginForm, CaptchaPasswordResetForm
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import generate_ics, compare_ads, check_car_value


urlpatterns = [
    # path('login/', views.user_login, name="login"),

    # login/logout urls
    path('login/', auth_views.LoginView.as_view(authentication_form=CustomLoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard', views.dashboard, name='dashboard'),

    # change password urls
    path('password-change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    # reset password urls
    path('password-reset/', auth_views.PasswordResetView.as_view(form_class=CaptchaPasswordResetForm), name='password_reset'),
    path('password-reset/done', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # register urls
    path('register/', views.registerUser, name="register"),
    path('deleting/', views.deleteAccount, name='delete-account'),

    # profile urls
    path('profile/<str:pk>/', views.profile, name="profile"),
    path('account/', views.userAccount, name="account"),
    path('edit-account/', views.editAccount, name="edit-account"),

    # adverts urls
    path('create-advert/', views.create_advert, name="advert_form"),
    path('update-advert/<str:pk>/', views.updateAdvert, name="update_advert_form"),
    path('delete-advert/<str:pk>/', views.delete_advert, name="delete_advert"),
    path('contact_advert/<str:pk>/', views.contact_advert, name="contact_advert"),
    path('price-reminder/<str:pk>/', views.price_reminder, name="price_reminder"),
    path('adverts/', views.adverts_view, name="adverts"),
    path('advert/<str:pk>/', views.advert_view, name="single-advert"),
    path('my-advert/', views.myAdverts, name="my-adverts"),
    path('user-advert/<str:pk>', views.other_user_adverts, name="other-adverts"),
    path('add-to-favorite/<str:pk>/', views.add_to_favorite, name="add_to_favorite"),
    path('opinion/<str:pk>/', views.add_opinion, name="opinion"),
    path('generate_ics/', generate_ics, name='generate_ics'),
    path('compare-ads/', compare_ads, name='compare-ads'),
    path('check_car_value/', check_car_value, name='check_car_value'),

    # other urls
    path('', views.index, name="main-site"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
