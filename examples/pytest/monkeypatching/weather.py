import requests

def get_weather(city):
    """
    Makes a GET request to a weather API and returns the temperature.
    """
    response = requests.get(f"https://api.example.com/weather?city={city}")
    data = response.json()
    return data["temp"]
