from django.db import models


class City(models.Model):
    """
    Represents a city where weather data is being collected.
    """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Weather(models.Model):
    """
    Represents weather data for a city at a specific timestamp.
    """
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='weather_data')
    timestamp = models.DateTimeField(auto_now_add=True)
    temperature = models.FloatField()  # Temperature in Celsius or Fahrenheit
    humidity = models.FloatField()  # Humidity percentage
    wind_speed = models.FloatField()  # Wind speed in km/h or mph
    weather_condition = models.CharField(max_length=255)  # e.g., Clear, Rainy, Snowy

    class Meta:
        ordering = ['-timestamp']  # Order by latest weather data first

    def __str__(self):
        return f"{self.city.name} - {self.weather_condition} at {self.timestamp}"
