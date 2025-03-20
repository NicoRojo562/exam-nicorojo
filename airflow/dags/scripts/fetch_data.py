import requests
import os
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

# access api key
API_KEY = os.getenv("AVIATIONSTACK_API_KEY")
URL = "https://api.aviationstack.com/v1/flights"

def fetch_flights():
    params = {
        "access_key": API_KEY,
        "flight_status": "active",
        "limit": 100
    }

    try:
        response = requests.get(URL, params=params, timeout=10)
        response.raise_for_status() 
    except requests.RequestException as e:
        print(f" Error en la API: {e}")
        return pd.DataFrame()

    
    data = response.json().get("data", [])
    
    #Extraction of relevant fields and transformations applied
    flights = [
        {
            "flight_date": flight.get("flight_date"),
            "flight_status": flight.get("flight_status"),
            "departure_airport": (flight.get("departure") or {}).get("airport", ""),
            "departure_timezone": (flight.get("departure") or {}).get("timezone", "").replace("/", " - "),
            "arrival_airport": (flight.get("arrival") or {}).get("airport", ""),
            "arrival_timezone": (lambda tz: tz.replace("/", " - ") if tz is not None else "")((flight.get("arrival") or {}).get("timezone")),
            "arrival_terminal": (flight.get("arrival") or {}).get("terminal", ""),
            "airline_name": (flight.get("airline") or {}).get("name", ""),
            "flight_number": (flight.get("flight") or {}).get("number", ""),
        }
        for flight in data if flight
    ]

    df = pd.DataFrame(flights)
    print(f" {len(df)} flights extracted from API")
    return df

if __name__ == "__main__":
    df = fetch_flights()
    print(df.head())
