import json
from datetime import datetime
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim
from pathlib import Path

import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry

city = "Paris"
country = "France"

# Read json file
def get_from_json(file):
  words_data = Path(file)

  # Read the file
  with open(words_data, "r") as file:
    data = json.load(file)

  return data

# Get coordinates for a city
def get_coordinates(city, country):
  global coordinates
  file = "coordinates.json"
  if not Path(file).is_file():
    geolocator = Nominatim(user_agent="geoapi")
    location = geolocator.geocode(city + ", " + country)

    # Save to json file
    data = {
      "city": city,
      "latitude": location.latitude,
      "longitude": location.longitude
    }

    with open("coordinates.json", "w") as json_file:
      json.dump(data, json_file, indent=4)

    coordinates = {
      "latitude": location.latitude,
      "longitude": location.longitude
    }
  else:
    location = get_from_json(file)
    coordinates = {
      "latitude": location['latitude'],
      "longitude": location['longitude']
    }
    

def get_weather_data(lat, long):
  # Setup the Open-Meteo API client with cache and retry on error
  cache_session = requests_cache.CachedSession('.cache', expire_after = -1)
  retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
  openmeteo = openmeteo_requests.Client(session = retry_session)

  # Make sure all required weather variables are listed here
  # The order of variables in hourly or daily is important to assign them correctly below
  url = "https://archive-api.open-meteo.com/v1/archive"
  params = {
    "latitude": lat,
    "longitude": long,
    "start_date": "2024-01-01",
    "end_date": "2024-12-31",
    "daily": ["temperature_2m_max", "temperature_2m_min", "weather_code", "precipitation_sum", "temperature_2m_mean"]
  }
  responses = openmeteo.weather_api(url, params=params)

  # Process first location. Add a for-loop for multiple locations or weather models
  response = responses[0]
  print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
  print(f"Elevation {response.Elevation()} m asl")
  print(f"Timezone {response.Timezone()}{response.TimezoneAbbreviation()}")
  print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

                # Process daily data. The order of variables needs to be the same as requested.
  daily = response.Daily()
  daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
  daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()
  daily_weather_code = daily.Variables(2).ValuesAsNumpy()
  daily_precipitation_sum = daily.Variables(3).ValuesAsNumpy()
  daily_temperature_2m_mean = daily.Variables(4).ValuesAsNumpy()

  daily_data = {"date": pd.date_range(
    start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
    end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
    freq = pd.Timedelta(seconds = daily.Interval()),
    inclusive = "left"
  )}

  daily_data["temperature_2m_max"] = daily_temperature_2m_max
  daily_data["temperature_2m_min"] = daily_temperature_2m_min
  daily_data["weather_code"] = daily_weather_code
  daily_data["precipitation_sum"] = daily_precipitation_sum
  daily_data["temperature_2m_mean"] = daily_temperature_2m_mean

  daily_dataframe = pd.DataFrame(data = daily_data)

  # Plot line chart including average, minimum and maximum temperature
  daily_dataframe.plot(y=['temperature_2m_min', 'temperature_2m_max'])
  plt.show()

get_coordinates(city, country)
get_weather_data(coordinates['latitude'], coordinates['longitude'])