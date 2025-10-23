#!/usr/bin/env python3
import requests
import argparse

# You need an OpenWeatherMap API key if you want live data
OWM_API_KEY = 'YOUR_OPENWEATHERMAP_KEY'

def get_weather(city, country_code='IN'):
    q = f"{city},{country_code}"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={q}&appid={OWM_API_KEY}&units=metric"
    r = requests.get(url, timeout=10)
    if r.status_code != 200:
        raise Exception("Weather API error: " + r.text)
    data = r.json()
    return {
        "temp": data['main']['temp'],
        "humidity": data['main']['humidity'],
        "desc": data['weather'][0]['description'],
        "wind": data['wind'].get('speed',0),
        "rain": data.get('rain',{}).get('1h',0)
    }

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--city', required=True)
    args = parser.parse_args()
    try:
        res = get_weather(args.city)
        print("Weather:", res)
    except Exception as e:
        print("Error getting weather:", e)
