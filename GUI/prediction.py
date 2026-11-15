
import requests
import pandas as pd

# Choose your location
LATITUDE = 49.6
LONGITUDE = 6.2

START_DATE = "2024-01-01"
END_DATE = "2025-12-31"

URL = "https://archive-api.open-meteo.com/v1/archive"

params = {
    "latitude": LATITUDE,
    "longitude": LONGITUDE,
    "start_date": START_DATE,
    "end_date": END_DATE,
    "hourly": [
        "temperature_2m",
        "relative_humidity_2m",
        "dew_point_2m",
        "precipitation",
        "rain",
        "snowfall",
        "weather_code",
        "pressure_msl",
        "surface_pressure",
        "cloud_cover",
        "wind_speed_10m",
        "wind_gusts_10m",
        "wind_direction_10m"
    ],
    "timezone": "Europe/Luxembourg"
}

print("Downloading historical weather...")

response = requests.get(URL, params=params, timeout=120)
response.raise_for_status()

weather = response.json()

df = pd.DataFrame(weather["hourly"])

df["time"] = pd.to_datetime(df["time"])

# Sort chronological data
df = df.sort_values("time").reset_index(drop=True)

# Create future weather labels
# Each row predicts conditions one hour later.

df["rain_next_60m"] = (
    df["rain"].shift(-1) > 0.1
).astype("float")

df["snow_next_60m"] = (
    df["snowfall"].shift(-1) > 0
).astype("float")

# Example configurable heavy-rain threshold.
# This is a project threshold, not an official warning threshold.
df["heavy_rain_next_60m"] = (
    df["precipitation"].shift(-1) >= 7.5
).astype("float")

# Thunderstorm weather codes:
# 95 = thunderstorm
# 96 = thunderstorm with hail
# 99 = thunderstorm with heavy hail
#
# Treat this label as provisional: reanalysis
# weather codes are not reliable thunderstorm
# observations.

df["thunder_next_60m"] = (
    df["weather_code"].shift(-1).isin([95, 96, 99])
).astype("float")

# Remove final row because its future hour is unknown
df = df.iloc[:-1].copy()

df.to_csv("weather_training.csv", index=False)

print("\nDownload completed!")
print("Records:", len(df))
print("File: weather_training.csv")

print("\nRain events:", int(df["rain_next_60m"].sum()))
print("Snow events:", int(df["snow_next_60m"].sum()))
print("Heavy rain events:", int(
    df["heavy_rain_next_60m"].sum()
))
print("Thunder events:", int(
    df["thunder_next_60m"].sum()
))
