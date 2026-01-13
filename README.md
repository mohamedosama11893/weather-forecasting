===========================================================
 Weather Forecasting App - Documentation
===========================================================

Overview:
    This Python application provides a GUI (Graphical User Interface)
    to fetch and display real-time weather data from OpenWeatherMap API.
    The user can search for a city, select it from a list, and view
    weather details such as temperature, humidity, wind speed, pressure,
    and rain probability.

Requirements:
    - Python 3.x
    - requests library (install via: pip install requests)
    - tkinter (comes with Python by default)
    - city.list.json OR city.list.json.gz (download from OpenWeatherMap)

Features:
    - Search-as-you-type (filter cities when typing 3+ characters)
    - City selection from listbox
    - Displays:
        * City & Country
        * Coordinates (Lat, Lon)
        * Weather description
        * Temperature (°C)
        * Humidity (%)
        * Wind speed (km/h)
        * Pressure (hPa)
        * Rain probability (%)

Usage:
    1. Replace API_KEY with your OpenWeatherMap API key.
    2. Place city.list.json.gz (or city.list.json) in the same directory.
    3. Run the script:
       python weather_app.py
