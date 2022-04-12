from twilio.rest import Client
import requests


OWMapi = "YOUR OpenWeatherMap API HERE"
TWILIO_ACCOUNT_SID = "Put your Twilio Account SID Here"
TWILIO_AUTH_TOKEN = "Put your Twilio Auth Token Here"
TO = "NUMBER TO SEND TO"
FROM = "YOUR TWILIO NUMBER TO SEND FROM"
LAT = "YOUR LOCATIONS LATTITUDE"
LONG = "YOUR LOCATIONS LONGITUDE"


def get_codes_12hrs():
    # Function that takes in 12-hour weather_data slice and returns a list of codes
    codes_12hr = []
    for data_hour in weather_slice:
        codes_12hr.append(data_hour["weather"][0]["id"])

    return codes_12hr


def check_for_rain():
    # Function that takes in 12-hour weather_data slice and returns a bool of whether it will rain
    will_rain = False
    codes = get_codes_12hrs()
    for code in codes:
        if int(code) < 700:
            will_rain = True
    if will_rain:
        print("Bring an umbrella!")

    return will_rain


def get_location_data():
    user_loc = UserLocation()
    user_location = {
        "ip": user_loc.get_ip(),
        "place": user_loc.get_location(),
        "coordinates": user_loc.get_coord()
    }
    return user_location


def get_temp_range():
    temp_list = []
    for i in range(12):
        temp_list.append(weather_slice[i]["temp"])
    low_of_day = min(temp_list)
    high_of_day = max(temp_list)

    return low_of_day, high_of_day


def get_temp():
    low, high = get_temp_range()
    return f"__temp__" \
           f"\n\tlow:  {low}°" \
           f"\n\thigh: {high}°"


def inform_me():
    intro = "\n\tDAILY BRIEFING:\n"
    if check_for_rain():
        client = Client(account_sid, auth_token)
        message = client.messages \
            .create(
                body=f"{intro}\tIt's going to rain today. Remember to bring an ☂\n{get_temp()}",
                to=TO,
                from_=FROM
            )

        return message.status
    else:
        client = Client(account_sid, auth_token)
        message = client.messages \
            .create(
                body=f"{intro}Should be dry today. No rain.\n{get_temp()}",
                to=TO,
                from_=FROM
            )

        return message.status


# ------------ TWILIO API ------------- #
account_sid = TWILIO_ACCOUNT_SID
auth_token = TWILIO_AUTH_TOKEN

# ------------ GET DATA FROM OPEN WEATHER MAP ------------- #
# OpenWeatherMap endpoint
OWM_Endpoint = "https://api.openweathermap.org/data/2.5/onecall"
# My location
lat = LAT
long = LONG
my_coordinates = (lat, long)
# My OpenWeatherMap API Key
api_key = OWMapi

weather_params = {
    "lat": lat,
    "lon": long,
    "units": "imperial",
    "appid": api_key,
    "exclude": "current,minutely,daily"
}

# Getting data from OWM using endpoint and proper parameters
response = requests.get(OWM_Endpoint, params=weather_params)
response.raise_for_status()

#  Get weather data in json format
weather_data = response.json()
# List of weather conditions for the next 12 hours
weather_slice = weather_data["hourly"][:12]

msg_status = inform_me()
print(f"Status: {msg_status}")
