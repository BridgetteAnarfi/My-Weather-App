from django.urls import path
from forecast import views

urlpatterns = [
    path('', views.weather_view, name='home'),  # Homepage of your app
    path('forecast/', views.get_weather_data, name='forecast'),  # Example endpoint
]
