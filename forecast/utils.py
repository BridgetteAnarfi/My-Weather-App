import requests
import psycopg2
from psycopg2 import sql
from datetime import datetime


# Function to fetch weather data from OpenWeatherMap API
def get_weather_data(city):
    """
    Fetch weather data for a given city from OpenWeatherMap API.

    Args:
        city (str): Name of the city.

    Returns:
        dict: JSON response from the OpenWeatherMap API or None if an error occurs.
    """
    api_key = '95fc0f494496a94141ad8cee0a3d0b69'  # Replace with your actual API key
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}'



    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from OpenWeatherMap API: {e}")
        return None


# Function to establish a database connection
def get_db_connection():
    """
    Create a database connection to PostgreSQL.

    Returns:
        psycopg2.connection: A connection object for PostgreSQL.
    """
    try:
        conn = psycopg2.connect(
            dbname="WeatherAppDB",
            user="postgres",
            password="Horseman246",  # Replace with your credentials
            host="127.0.0.1",
            port="5432"
        )
        return conn
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
        return None


# Function to save weather data to the database
def save_weather_to_db(conn, temperature, humidity, wind_speed, weather_condition):
    """
    Save weather data to the PostgreSQL database.

    Args:
        conn (psycopg2.connection): Active database connection.
        temperature (float): Temperature value in Celsius.
        humidity (int): Humidity percentage.
        wind_speed (float): Wind speed in m/s.
        weather_condition (str): Description of the weather condition.
    """
    try:
        with conn.cursor() as cursor:
            query = sql.SQL("""
                INSERT INTO weather_data (timestamp, temperature, humidity, wind_speed, weather_condition)
                VALUES (%s, %s, %s, %s, %s)
            """)
            cursor.execute(query, (datetime.now(), temperature, humidity, wind_speed, weather_condition))
            conn.commit()
            print("Weather data saved successfully.")
    except psycopg2.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()


# Main function to fetch and save weather data
def main(city):
    """
    Fetch weather data and save it to the database for a specified city.

    Args:
        city (str): Name of the city to fetch weather data for.
    """
    # Fetch weather data
    weather_data = get_weather_data(city)
    if weather_data:
        try:
            temperature = weather_data['main']['temp']
            humidity = weather_data['main']['humidity']
            wind_speed = weather_data['wind']['speed']
            weather_condition = weather_data['weather'][0]['description']

            # Connect to the database
            conn = get_db_connection()
            if conn:
                save_weather_to_db(conn, temperature, humidity, wind_speed, weather_condition)
        except KeyError as e:
            print(f"Error parsing weather data: {e}")
    else:
        print("Failed to fetch weather data. Please check your API key or city name.")


if __name__ == "__main__":
    city_name = input("Enter the name of the city: ")
    main(city_name)
