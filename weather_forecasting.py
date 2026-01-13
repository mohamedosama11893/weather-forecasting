"""
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
"""


from logging import root
import tkinter as tk
import requests
import json
import gzip

# ===================== CONFIGURATION =====================

API_KEY = "fe9da8f5d9d066db32878cc17cdedee6"  
# 🔑 Replace this with your own OpenWeatherMap API Key

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
# 🌍 OpenWeatherMap base URL for current weather data

# ===================== LOAD CITY DATA =====================

# City list file (can be .json or compressed .json.gz)
filename = "city.list.json.gz"

try:
    # If file is compressed (.gz), open with gzip
    if filename.endswith(".gz"):
        with gzip.open(filename, "rt", encoding="utf-8") as file:
            cities = json.load(file)
    else:
        with open(filename, "r", encoding="utf-8") as file:
            cities = json.load(file)
except Exception as error:
    print(f"Error loading city list: {error}")
    exit()

# Create a list of "City, Country" strings for searching
city_names = [f"{city['name']}, {city['country']}" for city in cities]

# ----------- Helper Methods -----------

def get_weather(city_entry):
    """
    Fetch weather data for a given city and update the result label.

    Args:
        city_entry (str): City name with country code (e.g., "Cairo, EG").

    API Response includes:
        - Coordinates (lat, lon)
        - Weather description
        - Temperature (°C)
        - Humidity (%)
        - Pressure (hPa)
        - Wind speed (converted to km/h)
        - Rain probability (estimated from rain volume)
    """
    try:
        # Split input into city name and country code
        city_name, country_code = city_entry.split(", ")
        
        # API parameters
        params = {"q": f"{city_name},{country_code}",
                  "appid": API_KEY,
                  "units": "metric"}      # Celsius instead of Kelvin
        
        # Send GET request
        response = requests.get(BASE_URL, params=params)
        
        # Check response status
        if response.status_code == 200:
            data = response.json()

             # Extract weather information  
            city = data.get("name", "N/A")
            lat = data["coord"]["lat"]
            lon = data["coord"]["lon"]
            description = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            pressure = data["main"]["pressure"]
            wind_speed = round(data["wind"]["speed"] * 3.6 , 2)  # m/s → km/h

            # Estimate rain probability
            rain_mm = data.get("rain", {}).get("1h", 0.0)
            rain_chance = min(int((rain_mm / 7) * 100), 100)

            # Prepare output string
            output = (
                f"🌍 City: {city}, {country_code}\n"
                f"\n📍 Lat: {lat}, Lon: {lon}\n"
                f"\n🌤 Weather: {description}\n"
                f"\n🌞 Temp: {temp}°C\n"
                f"\n💧 Humidity: {humidity}%\n"
                f"\n💨 Wind: {wind_speed} km/h\n"
                f"\n🌡 Pressure: {pressure} hPa\n"
                f"\n☔Rain Probability: {rain_chance}%\n"
            )
            
            # Display weather info
            result_label.config(text=output, fg="black")
            

        elif response.status_code == 404:
            result_label.config(text="❌ City not found", fg="red")
        elif response.status_code == 401:
            result_label.config(text="❌ Wrong API Key", fg="red")
        else:
            result_label.config(text=f"⚠️ Unexpected Error: {response.status_code}", fg="orange")

    except requests.exceptions.RequestException as e:
        result_label.config(text=f"⚠️ Connection Problem: {e}", fg="orange")

def search_city(event):
    """
    Filter and display matching cities in the listbox
    when the user types 3 or more characters in the search entry.
    """
    query = entry.get().strip().lower()
    listbox.delete(0, tk.END)

    if len(query) >= 3:
        # Find all cities starting with user input
        matches = [name for name in city_names if name.lower().startswith(query)]
        for name in matches:
            listbox.insert(tk.END, name)


def select_city(event):
    """
    Fetch and display weather info when a city is selected from the listbox.
    Triggered by single click or selection event.
    """
    selection = listbox.curselection()
    if selection:
        city = listbox.get(selection[0])
        get_weather(city)

def select_all(event):
    """
    Select all text inside the entry box when pressing Ctrl+A.
    Prevents the default behavior of tkinter entry.
    """
    entry.select_range(0, tk.END)
    entry.icursor(tk.END)
    return 'break'  # to prevent the default behavior

# ----------- GUI -----------

window = tk.Tk()
window.title("Weather Forecasting")

# -------- Frame 1 (label + entry) --------
frame_1 = tk.Frame(window)
frame_1.grid(row=0, column=0, padx=10, pady=10, sticky="w")

label = tk.Label(frame_1, text="Search : ", font=("Arial", 12))
label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

entry = tk.Entry(frame_1, font=("Arial", 12))
entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
entry.focus_set()
entry.bind("<KeyRelease>", search_city)
entry.bind("<Control-a>", select_all)  
entry.bind("<Control-A>", select_all)

# -------- Frame 2 (listbox + scrollbar) --------
frame_2 = tk.Frame(window)
frame_2.grid(row=1, column=0, padx=10, pady=10, sticky="w")

listbox = tk.Listbox(frame_2, width=30, height=10, font=("Arial", 12))
listbox.grid(row=1, column=0, sticky="nsew")

# Scrollbar for city list
scrollbar = tk.Scrollbar(frame_2, orient="vertical", command=listbox.yview)
scrollbar.grid(row=1, column=1, sticky="ns")


listbox.config(yscrollcommand=scrollbar.set)

# Bind selection event
listbox.bind("<<ListboxSelect>>", select_city)


# -------- Result label --------
result_label = tk.Label(window,
                        text="Choose a city to know the weather",
                        justify="center",
                        anchor="center" ,
                        fg="blue",
                        font=("Arial", 12)
)
result_label.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

# -------- Main loop --------
# Start the Tkinter event loop
window.mainloop()