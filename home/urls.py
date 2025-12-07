from django.urls import path
from .views import esp32_api
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('home/', views.home_view, name='home'),
    # path('dashboard/', views.dashboard, name='dashboard'),
    path('api/iot/', views.iot_api_view, name='iot_api'),
    path('logout/', views.logout_view, name='logout'),
    path("login/", views.user_login, name="login"),
    path('about/', views.about, name='about'),
    path('privacy/', views.privacy, name='privacy'),
    path('help/', views.help_page, name='help'),
    path('contact/', views.contact, name='contact'),
    path("weather/", views.weather_iot, name="weather_iot"),
    path('weather/', views.weather_iot, name='weather'),
    path("sensors/", views.sensors, name="sensors"),
    path('controls/', views.controls, name='controls'),
    path("report/", views.report, name="report"),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path("api/update-sensors/", views.update_sensors, name="update_sensors"),
    path('contact/', views.contact, name='contact'),
    path('api/esp32/', views.esp32_api, name='esp32_api'),



    path('reset_password/<int:uid>/', views.reset_password, name='reset_password'),
    path('resend_otp/', views.resend_otp, name='resend_otp'),

    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('api/esp32/', views.sensors_api, name='sensors_api'),
     path('api/esp32/', views.esp32_api, name='esp32_api'),

    path("sensors/", views.sensors_page, name="sensors"),  # HTML page
    path("api/esp32/", views.sensors_api, name="sensors_api"),

     path('api/esp32/', views.esp32_api, name='esp32_api'),   # POST from ESP32
    path('api/esp32/sensors/', views.sensors_api, name='sensors_api'),  # GET for web

   path('api/esp32/', views.esp32_api, name='esp32_api'),
    path('sensors/', views.sensors_page, name='sensors_page'),


]


