from pyowm import OWM
from datetime import datetime


class Day:
    day = ""
    min_temp = ""
    max_temp = ""
    sunrise = ""
    sunset = ""
    weather_code = ""
    icon_name = ""
    rain_forecast = ""


class Hour():
    hour = ""
    temp = ""
    weather_code = ""
    icon_name = ""


def to_weekday_string(day):
    switch = {
        0: "Montag",
        1: "Dienstag",
        2: "Mittwoch",
        3: "Donnerstag",
        4: "Freitag",
        5: "Samstag",
        6: "Sonntag",
    }
    return switch.get(day, "Unknown")


def get_weather_hourly(observation):
    hour_forecast = []
    for hour_num in [0, 3, 6, 9, 12]:
        forecast = observation.forecast_hourly[hour_num]
        hour = Hour()
        hour.hour = datetime.fromtimestamp(
            forecast.ref_time).strftime("%H:%M")
        hour.temp = int(round(forecast.temp['temp']))
        hour.weather_code = forecast.weather_code
        hour.icon_name = forecast.weather_icon_name
        hour_forecast.append(hour)
    return hour_forecast


class Weather:

    def __init__(self, api_token):
        owm = OWM(api_token)
        self.mgr = owm.weather_manager()

    def get_weather(self, lat=0, lon=0):
        # Search for current weather and get details
        observation = self.mgr.one_call(lat=lat, lon=lon, units='metric')
        complete_forecast = []

        for day_num in range(5):
            forecast = observation.forecast_daily[day_num]
            day = Day()
            day.day = to_weekday_string(datetime.fromtimestamp(
                forecast.ref_time).weekday())
            day.max_temp = int(round(forecast.temp['max']))
            day.min_temp = int(round(forecast.temp['min']))
            day.sunrise = datetime.fromtimestamp(
                forecast.srise_time).strftime("%H:%M")
            day.sunset = datetime.fromtimestamp(
                forecast.sset_time).strftime("%H:%M")
            day.weather_code = forecast.weather_code
            day.icon_name = forecast.weather_icon_name

            if day_num == 0:
                day.hours = get_weather_hourly(observation)
                if (hasattr(forecast.rain, 'all')):
                    day.rain_forecast = round(forecast.rain['all'], 1)
                else:
                    day.rain_forecast = 0

            complete_forecast.append(day)

        return complete_forecast
