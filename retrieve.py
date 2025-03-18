import json
from datetime import datetime
import matplotlib.pyplot as plt
from meteostat import Point, Daily, Hourly
from geopy.geocoders import Nominatim
from pathlib import Path

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
  # Set time period
  # Change another period here
  start = datetime(2024, 1, 1)
  end = datetime(2024, 12, 31)

  # Create Point for selected city
  city = Point(lat, long, 70)

  # Get daily data for certain year
  data = Daily(city, start, end)
  data = data.fetch()

  # Save to CSV file
  csv_file = "weather_data.csv"
  data.to_csv(csv_file, index=True)  # Index=True to keep the date column

  # Plot line chart including average, minimum and maximum temperature
  #data.plot(y=['tavg', 'tmin', 'tmax'])
  #plt.show()

  print(data.head())

get_coordinates(city, country)
get_weather_data(coordinates['latitude'], coordinates['longitude'])