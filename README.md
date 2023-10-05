# Netatmo ePaper

## General information
This is a python application that displays data on a Waveshare 7.5" ePaper display.
The following data will be displayed:
* Date and time
* Data from Netatmo indoor and outdoor module
* Weather forecast from openweathermap.org


## How to install
coming soon

### For local development
Install dependencies:

```$ pip install -r requirements-base.txt```

Run the application:

```$ python netatmo-epaper/netatmo-epaper.py```

### On Raspberry Pi
```$ pip install -r requirements-base.txt -r requirements-pi.txt```


## Libraries used
The following libraries made this project much easier:
* [Waveshare ePaper libraries and examples](https://github.com/waveshare/e-Paper)
* [netatmo-api-python](https://github.com/philippelt/netatmo-api-python) for retrieving data from the Netatmo API
* [pyowm](https://github.com/csparpa/pyowm) for retreieving data from openweathermap.org
* [Pillow](https://github.com/python-pillow/Pillow) for image processing