from django.shortcuts import render
from forecast.forms import CityForm
from forecast.utils import get_weather_data
from forecast.models import Weather


def weather_view(request):
    """
    Handles the main weather form and displays the weather data for the requested city.
    """
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            city_name = form.cleaned_data['name']
            weather_data = get_weather_data(city_name)

            # Check if the API returned valid data
            if weather_data and 'main' in weather_data:
                context = {
                    'city': city_name,
                    'temperature': weather_data['main']['temp'],
                    'humidity': weather_data['main']['humidity'],
                    'wind_speed': weather_data['wind']['speed'],
                    'weather_condition': weather_data['weather'][0]['description'],
                }
                return render(request, 'forecast/weather.html', context)
            else:
                error_message = "Unable to retrieve weather data. Please try again."
                return render(request, 'forecast/index.html', {'form': form, 'error': error_message})
    else:
        form = CityForm()

    return render(request, 'forecast/index.html', {'form': form})


def weather_data_view(request):
    """
    Displays the latest weather data saved in the database.
    """
    try:
        # Fetch the latest weather entry from the database
        weather_entry = Weather.objects.latest('timestamp')

        context = {
            'temperature': weather_entry.temperature,
            'humidity': weather_entry.humidity,
            'wind_speed': weather_entry.wind_speed,
            'weather_condition': weather_entry.weather_condition,
            'timestamp': weather_entry.timestamp,
        }

        return render(request, 'forecast/weather_data.html', context)

    except Weather.DoesNotExist:
        # Handle the case where there are no weather entries in the database
        error_message = "No weather data available in the database."
        return render(request, 'forecast/weather_data.html', {'error': error_message})
