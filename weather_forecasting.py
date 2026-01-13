from logging import root
import tkinter as tk
import requests
import json
import gzip

API_KEY = "fe9da8f5d9d066db32878cc17cdedee6"  # ضع الـ API Key بتاعك هنا
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# Loading cities from JSON file in a compressed format using gzip
filename = "city.list.json.gz"  # أو "city.list.json"
try:
    if filename.endswith(".gz"):
     with gzip.open(filename, "rt", encoding="utf-8") as file:
        cities = json.load(file)
    else:
     with open(filename, "r", encoding="utf-8") as file:
        cities = json.load(file)
except Exception as error:
    print(f"Error loading city list: {error}")
    exit()
    
# a list of (city name + country code)
city_names = [f"{city['name']}, {city['country']}" for city in cities]

# ----------- Helper Methods -----------



def search_city(event):
    """البحث في قائمة المدن عند كتابة 3 حروف أو أكثر"""
    query = entry.get().strip().lower()
    listbox.delete(0, tk.END)

    if len(query) >= 3:
        matches = [name for name in city_names if name.lower().startswith(query)]
        for name in matches:
            listbox.insert(tk.END, name)


def select_city(event):
    """Starting the search for the weather of a city from Single Click"""
    selection = listbox.curselection()
    if selection:
        city = listbox.get(selection[0])
        get_weather(city)

def select_all(event):
    """to select all the text in the box by pressing Ctrl + A"""
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

scrollbar = tk.Scrollbar(frame_2, orient="vertical", command=listbox.yview)
scrollbar.grid(row=1, column=1, sticky="ns")


listbox.config(yscrollcommand=scrollbar.set)
#listbox.bind("<ButtonRelease-1>", select_city)
#listbox.bind("<Return>", select_city)
listbox.bind("<<ListboxSelect>>", select_city)


# -------- Result label --------
result_label = tk.Label(window, text="Choose a city to know the weather",
                        justify="center", anchor="center" , fg="blue", font=("Arial", 12))
result_label.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

# -------- Main loop --------
window.mainloop()