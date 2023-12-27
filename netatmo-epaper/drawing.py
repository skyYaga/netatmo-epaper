import fontawesome as fa
from PIL import Image, ImageDraw, ImageFont
import logging
import sys
import os
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
import weathericons as wi

logger = logging.getLogger(__name__)


class DateTimeModel():
    time = "00:00"
    date = "01.01.0000"


class NetatmoIndoorModel():
    temp = "0.0"
    min_temp = "0.0"
    max_temp = "0.0"
    trend = "none"
    co2 = "0"
    humidity = "0"


class NetatmoOutdoorModel():
    temp = "0.0"
    min_temp = "0.0"
    max_temp = "0.0"
    trend = "none"
    humidity = "0"


class NetatmoRainModel():
    rain = "0.0"
    sum_rain_1 = "0.0"
    sum_rain_24 = "0.0"


class DisplayDrawer():

    """ This class draws the image for the epaper display """

    def __init__(self):
        logger.debug("Initializing DisplayDrawer")
        fonts_path = os.path.join(os.path.dirname(os.path.dirname(
            os.path.realpath(__file__))), 'fonts')
        self.font_path = os.path.join(fonts_path,
                                      "OpenSans-Regular.ttf")
        self.fa_path = os.path.join(fonts_path,
                                    "fa-regular-400.ttf")
        self.fas_path = os.path.join(fonts_path,
                                     "fa-solid-900.ttf")
        self.wi_path = os.path.join(fonts_path,
                                    "weathericons-regular-webfont.ttf")
        self.font12 = ImageFont.truetype(self.font_path, 12)
        self.font18 = ImageFont.truetype(self.font_path, 18)
        self.font24 = ImageFont.truetype(self.font_path, 24)
        self.font48 = ImageFont.truetype(self.font_path, 48)
        self.font64 = ImageFont.truetype(self.font_path, 64)
        self.fa24 = ImageFont.truetype(self.fa_path, 24)
        self.fa48 = ImageFont.truetype(self.fa_path, 48)
        self.fas24 = ImageFont.truetype(self.fas_path, 24)
        self.fas48 = ImageFont.truetype(self.fas_path, 48)
        self.wi48 = ImageFont.truetype(self.wi_path, 48)

    def __get_icon_prefix(self, icon_name):
        if icon_name.endswith("d"):
            return "wi_owm_day_"
        if icon_name.endswith("n"):
            return "wi_owm_night_"
        return "wi_owm_"

    def __draw_indoor_data(self, draw, indoor_model):
        logger.debug("Drawing indoor data")
        draw.text((10, 100), 'Innen', font=self.font18, fill=0)
        draw.text((10, 120),
                  '%s °' % (indoor_model.temp), font=self.font64, fill=0)

        if indoor_model.trend == "up":
            draw.text(
                (280, 140), fa.icons['chevron-up'], font=self.fas48, fill=0)
        if indoor_model.trend == "down":
            draw.text(
                (280, 140), fa.icons['chevron-down'], font=self.fas48, fill=0)

        draw.text((350, 110), 'Min', font=self.font12, fill=0)
        draw.text((350, 120),
                  '%s °C' % (indoor_model.min_temp), font=self.font24, fill=0)
        draw.text((350, 160), 'Max', font=self.font12, fill=0)
        draw.text((350, 170),
                  '%s °C' % (indoor_model.max_temp), font=self.font24, fill=0)

        draw.text((10, 210), 'CO2 (ppm)', font=self.font18, fill=0)
        draw.text((10, 225), str(indoor_model.co2), font=self.font48, fill=0)

        if indoor_model.co2 < 1000:
            draw.text((150, 230), fa.icons['smile'], font=self.fa48, fill=0)

        if indoor_model.co2 >= 1000 & indoor_model.co2 < 2000:
            draw.text((150, 230), fa.icons['meh'], font=self.fa48, fill=0)
        else:
            draw.text((150, 230), fa.icons['frown'], font=self.fa48, fill=0)

        draw.text((280, 210), 'Luftfeuchtigkeit', font=self.font18, fill=0)
        draw.text((280, 225),
                  '%s %%' % (indoor_model.humidity),
                  font=self.font48, fill=0)

    def __draw_outdoor_data(self, draw, outdoor_model, rain_model, forecast):
        rain_shift = 0
        if rain_model:
            rain_shift = 80

        logger.debug("Drawing indoor data")
        draw.text((10, 320), 'Außen', font=self.font18, fill=0)
        draw.text((10, 340), '%s °' %
                  (outdoor_model.temp), font=self.font64, fill=0)

        if outdoor_model.trend == "up":
            draw.text(
                (280 - rain_shift, 360), fa.icons['chevron-up'], font=self.fas48, fill=0)
        if outdoor_model.trend == "down":
            draw.text(
                (280 - rain_shift, 360), fa.icons['chevron-down'], font=self.fas48, fill=0)

        draw.text((350 - rain_shift, 330), 'Min', font=self.font12, fill=0)
        draw.text((350 - rain_shift, 340), '%s °C' %
                  (outdoor_model.min_temp), font=self.font24, fill=0)
        draw.text((350 - rain_shift, 380), 'Max', font=self.font12, fill=0)
        draw.text((350 - rain_shift, 390), '%s °C' %
                  (outdoor_model.max_temp), font=self.font24, fill=0)

        draw.text(
            (20, 445), fa.icons['sun'], font=self.fa24, fill=0)
        draw.text(
            (50, 445), fa.icons['caret-up'], font=self.fas24, fill=0)
        draw.text((90, 440), '%s' %
                  (forecast.sunrise), font=self.font24, fill=0)
        draw.text(
            (20, 485), fa.icons['sun'], font=self.fa24, fill=0)
        draw.text(
            (50, 485), fa.icons['caret-down'], font=self.fas24, fill=0)
        draw.text((90, 480), '%s' %
                  (forecast.sunset), font=self.font24, fill=0)

        draw.text((280 - rain_shift, 430), 'Luftfeuchtigkeit',
                  font=self.font18, fill=0)
        draw.text((280 - rain_shift, 445), '%s %%' %
                  (outdoor_model.humidity), font=self.font48, fill=0)

        if rain_model:
            draw.line((350, 320, 350, 500), fill=0)
            
            draw.text((360, 320), 'Regen', font=self.font18, fill=0)

            draw.text((360, 360), 'Letzte Stunde', font=self.font12, fill=0)
            draw.text((360, 370), '%s mm/h' %
                      (rain_model.sum_rain_1), font=self.font24, fill=0)
            draw.text((360, 420), 'Kumulativ', font=self.font12, fill=0)
            draw.text((360, 430), '%s mm' %
                      (rain_model.sum_rain_24), font=self.font24, fill=0)
            draw.text((360, 470), 'Prognostiziert', font=self.font12, fill=0)
            draw.text((360, 480), '%s mm' %
                  (rain_model.rain), font=self.font24, fill=0)

    def __draw_forecast(self, draw, forecast):
        logger.debug("Drawing forecast")

        draw.line((10, 675, 470, 675), fill=0)

        for idx, day in enumerate(forecast):
            if idx == 0:
                # Draw hourly forecast
                draw.text((10, 530), "Vorhersage heute",
                          font=self.font18, fill=0)
                for hour_idx, hour in enumerate(day.hours):
                    draw.text((10 + hour_idx * 100, 560), "%s Uhr" %
                              hour.hour,
                              font=self.font12, fill=0)
                    draw.text((15 + hour_idx * 100, 575),
                              wi.icons[
                                  self.__get_icon_prefix(hour.icon_name)
                                  + str(hour.weather_code)],
                              font=self.wi48, fill=0)
                    draw.text((30 + hour_idx * 100, 640), "%s °C" %
                              hour.temp,
                              font=self.font12, fill=0)

            # Draw Daily Forecast
            draw.text((15 + idx * 100, 690),
                      forecast[idx].day, font=self.font12, fill=0)
            draw.text((15 + idx * 100, 705),
                      wi.icons[
                self.__get_icon_prefix(
                    forecast[idx].icon_name)
                + str(forecast[idx].weather_code)],
                font=self.wi48, fill=0)
            draw.text((10 + idx * 100, 770), "%s °C / %s °C" %
                      (forecast[idx].min_temp, forecast[idx].max_temp),
                      font=self.font12, fill=0)

    def draw_image(self,
                   dt_model=DateTimeModel(),
                   indoor_model=NetatmoIndoorModel(),
                   outdoor_model=NetatmoOutdoorModel(),
                   rain_model=None,
                   forecast=None):
        """ This acutally draws the image """

        if forecast is None:
            forecast = []
        logger.debug("Drawing new image")

        with Image.new('1', (480, 800), 255) as im:

            draw = ImageDraw.Draw(im)

            # Time + Date
            draw.text((10, 0), dt_model.time, font=self.font64, fill=0)
            draw.text((220, 10), dt_model.date, font=self.font48, fill=0)

            draw.line((10, 90, 470, 90), fill=0)

            # indoor data
            self.__draw_indoor_data(draw, indoor_model)

            draw.line((10, 300, 470, 300), fill=0)

            # outdoor data
            self.__draw_outdoor_data(
                draw, outdoor_model, rain_model, forecast[0])

            draw.line((10, 520, 470, 520), fill=0)

            self.__draw_forecast(draw, forecast)

            # rotate image by 180 degrees
            return im.rotate(180)
