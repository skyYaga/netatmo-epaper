import logging
import time
import lnetatmo
from drawing import DisplayDrawer, DateTimeModel, NetatmoIndoorModel, NetatmoOutdoorModel
from PIL import Image
from weather import Weather
import yaml

#
# Remember to put credentials into ~/.netatmo.credentials
#


logging.basicConfig(
    format='%(asctime)s %(name)s: %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

#
# READ SETTINGS BLOCK
#
with open('config.yaml', 'r') as file:
    config_file = yaml.safe_load(file)

# Dev Mode
dev_mode = config_file["devMode"]
logger.debug("Dev Mode: %s" % dev_mode)

# Netatmo
home_name = config_file["netatmo"]["homeName"]
indoor_name = config_file["netatmo"]["indoorName"]
outdoor_name = config_file["netatmo"]["outdoorName"]
client_id = config_file["netatmo"]["oauth"]["clientId"]
client_secret = config_file["netatmo"]["oauth"]["clientSecret"]
refresh_token = config_file["netatmo"]["oauth"]["refreshToken"]

logger.debug("Netatmo homeName: %s" % home_name)
logger.debug("Netatmo indoorName: %s" % indoor_name)
logger.debug("Netatmo outdoorName: %s" % outdoor_name)
logger.debug("Netatmo clientId: %s" % client_id)
logger.debug("Netatmo clientSecret: %s" % client_secret)
logger.debug("Netatmo refreshToken: %s" % refresh_token)

# OWM
owm_api_token = config_file["owm"]["apiToken"]
lat = config_file["owm"]["lat"]
lon = config_file["owm"]["lon"]

logger.debug("OWM apiToken: %s" % owm_api_token)
logger.debug("OWM lat: %s" % lat)
logger.debug("OWM lon: %s" % lon)

#
# END SETTINGS BLOCK
#

if not dev_mode:
    from display import Epd


def log_indoor_info(data):
    """ Print sensor data for indoor module """
    logger.debug("Current data (inside):")
    logger.debug("Temperature (min/max) %s°C (%s°C / %s°C)" %
                 (data['Temperature'],
                  data.get('min_temp', ''), data.get('max_temp', ''))
                 )
    logger.debug("Temperature trend: %s" % (data.get('temp_trend', '')))
    logger.debug("CO2 / Humidity: %s ppm / %s %%" %
                 (data['CO2'], data['Humidity']))


def log_outoor_info(data):
    """ Print sensor data for outdoor module """
    logger.debug("Current data (outside):")
    logger.debug("Temperature (min/max) %s°C (%s°C / %s°C)" %
                 (data['Temperature'],
                  data.get('min_temp', ''), data.get('max_temp', ''))
                 )
    logger.debug("Temperature trend: %s" % (data.get('temp_trend', '')))
    logger.debug("Humidity: %s %%" % (data['Humidity']))


def set_indoor_model(model, data):
    """ set sensor data for indoor module into model"""

    set_outdoor_model(model, data)
    model.co2 = data.get('CO2', '')


def set_outdoor_model(model, data):
    """ set sensor data for outdoor module into model"""

    model.temp = data.get('Temperature', '')
    model.min_temp = data.get('min_temp', '')
    model.max_temp = data.get('max_temp', '')
    model.trend = data.get('temp_trend', '')
    model.humidity = data.get('Humidity', '')


# Init variables
current_time = ""
current_hour = ""
drawer = DisplayDrawer()
dt_model = DateTimeModel()
indoor_model = NetatmoIndoorModel()
outdoor_model = NetatmoOutdoorModel()
weather = Weather(owm_api_token)
forecast = []
weather_data = ""
if not dev_mode:
    epd = Epd()

# Authenticate
authorization = lnetatmo.ClientAuth(clientId=client_id, clientSecret=client_secret, refreshToken=refresh_token)

while True:
    current_local_time = time.localtime()

    if current_time != time.strftime("%H:%M", current_local_time):

        # time handling
        current_date = time.strftime("%d.%m.%Y", current_local_time)
        current_time = time.strftime("%H:%M", current_local_time)
        logger.debug(current_date)
        logger.debug(current_time)
        dt_model.date = current_date
        dt_model.time = current_time

        # weather handling
        logger.debug("Retrieving weather data from netatmo")
        try:
            weather_data = lnetatmo.WeatherStationData(
                authorization, home=home_name)
        except Exception as e:
            logger.error("Error getting Netatmo data: %s" % str(e))
            logger.info("Continue with old data")

        indoor_data = weather_data.lastData()[indoor_name]
        set_indoor_model(indoor_model, indoor_data)
        log_indoor_info(indoor_data)

        outdoor_data = weather_data.lastData()[outdoor_name]
        set_outdoor_model(outdoor_model, outdoor_data)
        log_outoor_info(outdoor_data)

        # weather forecast
        if current_hour != time.strftime("%H", current_local_time):
            try:
                forecast = weather.get_weather(lat=lat, lon=lon)
                current_hour = time.strftime("%H", current_local_time)
            except Exception as e:
                logger.error(
                    "Error getting weather forecast data: %s" % str(e))
                logger.info("Continue with old data")

        img = drawer.draw_image(dt_model, indoor_model,
                                outdoor_model, forecast)

        if dev_mode:
            # show image
            img.show()
        else:
            # draw image
            epd.draw(img)
    else:
        time.sleep(1)
        current_local_time = time.localtime()
