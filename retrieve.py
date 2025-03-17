import json
from datetime import datetime
import matplotlib.pyplot as plt
from meteostat import Point, Daily
from geopy.geocoders import Nominatim
from pathlib import Path

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
  start = datetime(2024, 1, 1)
  end = datetime(2024, 12, 31)

  # Create Point for Vancouver, BC
  city = Point(lat, long, 70)

  # Get daily data for 2018
  data = Daily(city, start, end)
  data = data.fetch()

  # Plot line chart including average, minimum and maximum temperature
  data.plot(y=['tavg', 'tmin', 'tmax'])
  plt.show()

  #print(data)

get_coordinates("Norrköping", "Sweden")
get_weather_data(coordinates['latitude'], coordinates['longitude'])