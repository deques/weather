# Import Meteostat library and dependencies
from datetime import datetime
import matplotlib.pyplot as plt
from meteostat import Point, Daily

from geopy.geocoders import Nominatim

# Get coordinates for a city
def get_coordinates():
  global location
  geolocator = Nominatim(user_agent="geoapi")
  location = geolocator.geocode("Norrköping, Sweden")

def get_weather_data():
  # Set time period
  start = datetime(2024, 1, 1)
  end = datetime(2024, 12, 31)

  # Create Point for Vancouver, BC
  norrkoping = Point(58.594719, 16.183630, 70)

  # Get daily data for 2018
  data = Daily(norrkoping, start, end)
  data = data.fetch()

  # Plot line chart including average, minimum and maximum temperature
  # data.plot(y=['tavg', 'tmin', 'tmax'])
  # plt.show()

  print(data)
