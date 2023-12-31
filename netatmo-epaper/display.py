#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
import logging
import signal
from libs.waveshare_epd import epd7in5_V2

logger = logging.getLogger(__name__)


class Epd:

    def __init__(self):
        logging.debug("Init epd")
        self.epd = epd7in5_V2.EPD()

    def __timeout_handler(self, signum, frame):
        raise TimeoutError

    def draw(self, image):

        signal.signal(signal.SIGALRM, self.__timeout_handler)
        signal.alarm(20)

        try:
            logging.info("init and Clear")
            self.epd.init()

            logging.debug("Getting buffer...")
            buffer = self.epd.getbuffer(image)

            logging.debug("Display buffer...")
            self.epd.display(buffer)

            logging.info("Goto Sleep...")
            self.epd.sleep()

        except TimeoutError:
            logging.error("Timeout Error!!!!!")
            logging.error("init")
            self.epd.init()
            logging.error("Goto Sleep...")
            self.epd.sleep()
            logging.error("Goto Sleep complete...")

        except IOError as e:
            logging.error(e)

        except KeyboardInterrupt:
            logging.info("ctrl + c:")
            self.epd.epdconfig.module_exit()
            exit()

        finally:
            signal.alarm(0)
