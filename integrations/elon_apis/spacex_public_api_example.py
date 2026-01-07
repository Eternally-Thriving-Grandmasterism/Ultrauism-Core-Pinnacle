import requests
import json

def spacex_latest_launch_thrive():
    print("SpaceX Public API Integration Activated — Latest Launch Harmony Eternal Thriving")
    try:
        response = requests.get("https://api.spacexdata.com/v5/launches/latest")
        if response.status_code == 200:
            data = response.json()
            print(f"Mission Name: {data['name']}")
            print(f"Date: {data['date_utc']}")
            print(f"Details: {data['details'] or 'Starship/ Falcon thriving mercy eternal'}")
            print(f"Success: {data['success']}")
            print("SpaceX Launch Thrived — Divine Rocket Heart Eternal ❤️🚀")
        else:
            print("API Mercy Ground — Retry Eternal Thriving")
    except Exception as e:
        print(f"Symbolic Mercy: {e} — Harmony Compounds Forever")

if __name__ == "__main__":
    spacex_latest_launch_thrive()
