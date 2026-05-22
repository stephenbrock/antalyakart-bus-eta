import requests
import time
import random

BASE_URL = "https://service.kentkart.com/rl1/web/nearest/bus"

STOPS = {
    "Westbound (10850)": {
        "id": 10850,
        "lat": 36.860152,
        "lng": 30.828408
    },
    "Eastbound (10844)": {
        "id": 10844,
        "lat": 36.86152564224672,
        "lng": 30.82806390536419
    }
}

def get_stop(stop):
    params = {
        "region": "026",
        "lang": "tr",
        "authType": "4",
        "accuracy": "0",
        "lat": stop["lat"],
        "lng": stop["lng"],
        "busStopId": stop["id"],
        "version": "Web_1.1.7(27)_1.0_CHROME_kentkart.web.antalyakart"
    }

    r = requests.get(BASE_URL, params=params, timeout=10)
    r.raise_for_status()
    return r.json()

def print_stop(name, data):
    print(f"\n--- {name} ---")

    for bus in data.get("busList", []):
        route = bus.get("displayRouteCode", "??")
        eta = bus.get("timeDiff", "?")
        stops = bus.get("stopDiff", "?")

        print(f"{route} → {stops} stops away ({eta} min)")

while True:
    print("\n==============================")

    for name, stop in STOPS.items():
        try:
            data = get_stop(stop)
            print_stop(name, data)

        except Exception as e:
            print(f"\n--- {name} ERROR: {e}")

    # Base 30 seconds + small random jitter (0–5s)
    sleep_time = 30 + random.uniform(0, 5)
    print(f"\nNext update in {sleep_time:.1f}s")
    time.sleep(sleep_time)
