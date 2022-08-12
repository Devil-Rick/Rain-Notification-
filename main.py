from geopy.geocoders import Nominatim
import config
import requests as req
from twilio.rest import Client

# ------------------- Getting Lat and Long --------------------- #
loc = Nominatim(user_agent="GetLoc")  # calling the Nominatim tool

getLoc = loc.geocode("Siuri")  # entering the location name
latitude = getLoc.latitude
longitude = getLoc.longitude
print(getLoc.address)

# ------------------- Working With API --------------------- #

params = {
    "lat": latitude,
    "lon": longitude,
    "appid": config.OW_api_key,
    "units": "metric",
    "exclude": "current,minutely,daily"
}
response = req.get(url=config.OW_api_id, params=params)
response.raise_for_status()
weather_data = response.json()
hourly_weather = weather_data["hourly"][:12]

will_rain = False

for hour_data in hourly_weather:
    data = hour_data["weather"][0]
    data_id = data["id"]
    data_main = data["main"]
    if data_id < 700:
        will_rain = True

# ------------------- Setting up twilio API --------------------- #


if will_rain:
    client = Client(config.TW_auth_sid, config.TW_auth_token)
    message = client.messages.create(
        body="Take an Umbrella with you. It's gonna rain today.☔☔☔☔",
        from_='+13149123008',
        to='+918016323773'
    )
    print(message.status)
