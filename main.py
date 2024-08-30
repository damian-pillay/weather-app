from twilio.rest import Client
from dotenv import load_dotenv
import requests
import os

load_dotenv()

API_KEY = os.environ["WEATHER_API_KEY"]
API_ENDPOINT = os.environ["WEATHER_ENDPOINT"]
LAT = -29.858681
LONG = 31.021839

account_sid = os.environ["TWILIO_SID"]
auth_token = os.environ["TWILIO_TOKEN"]
twilio_number = os.environ["TWILIO_NUMBER"]
my_number = os.environ["MY_NUMBER"]

weather_params = {
    "lat": LAT,
    "lon": LONG,
    "appid": API_KEY,
    "cnt": 4
}

response = requests.get(url=API_ENDPOINT, params=weather_params)
response.raise_for_status()

weather = response.json()["list"]

forecasts = [forecast["weather"][0]["id"] for forecast in weather]

will_rain = False

for forecast in forecasts:
    if forecast < 700:
        will_rain = True

if will_rain:
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_=twilio_number,
        body = "It's going to rain today. Remember to bring an Umbrella!",
        to=my_number
    )