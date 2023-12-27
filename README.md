# Netatmo ePaper

## General information

This is a python application that displays data on a Waveshare 7.5" ePaper display.
The following data will be displayed:

- Date and time
- Data from Netatmo indoor and outdoor module
- Weather forecast from openweathermap.org

Example screenshot:

![Display Screenshot](docs/epaper.png)

Real life example:

![Display Screenshot](docs/epaper_real.png)

## Prerequisites

1. Create a netatmo developer account (https://dev.netatmo.com)
1. Create an app in the portal (-> client ID, client secret)
1. Create a token with `read_station` scope (-> refresh token)

## How to install

### For local development

1. Checkout this repo
1. Create Virtual env (see https://docs.python.org/3/library/venv.html)
1. Install dependencies:
   ```shell
   $ pip install -r requirements-base.txt
   ```
1. Create `~/.netatmo.credentials` with the following content (filling in your netatmo API credentials):
   ```json
   {
     "CLIENT_ID": "xxx",
     "CLIENT_SECRET": "xxx",
     "REFRESH_TOKEN" : "xxx"
   }
   ```
1. Copy `example.yaml` to `config.yaml` and update the file accordingly.
1. Run the application:
   ```shell
   $ python netatmo-epaper/netatmo-epaper.py
   ```

### On Raspberry Pi

1. Checkout this repo
1. Create and activate Virtual env (see https://docs.python.org/3/library/venv.html)
   ```shell
   $ cd netatmo-epaper
   $ python3 -m venv .venv
   $ source .venv/bin/activate
   ```
1. Install dependencies:
   ```shell
   $ pip3 install -r requirements-base.txt -r requirements-pi.txt
   ```
1. Create `~/.netatmo.credentials` with the following content:
   ```json
   {
     "CLIENT_ID": "xxx",
     "CLIENT_SECRET": "xxx",
     "REFRESH_TOKEN" : "xxx"
   }
   ```
1. Copy `example.yaml` to `config.yaml` and update the file accordingly.
1. Run the application:
   ```shell
   $ python3 netatmo-epaper/netatmo-epaper.py
   ```
1. Optional: (re)start automatically, e.g. using pm2:
   ```shell
   $ pm2 start /home/pi/netatmo-epaper/netatmo-epaper/netatmo-epaper.py --name "netatmo-epaper.py" --interpreter "/home/pi/netatmo-epaper/.venv/bin/python"
   $ pm2 save
   ```

## Libraries used

The following libraries made this project much easier:

- [Waveshare ePaper libraries and examples](https://github.com/waveshare/e-Paper)
- [netatmo-api-python](https://github.com/philippelt/netatmo-api-python) for retrieving data from the Netatmo API
- [pyowm](https://github.com/csparpa/pyowm) for retreieving data from openweathermap.org
- [Pillow](https://github.com/python-pillow/Pillow) for image processing
