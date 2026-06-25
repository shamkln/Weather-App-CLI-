import sys
import datetime

# ── Try importing required library ────────────────────────────────────
try:
    import requests
except ImportError:
    print("\n[ERROR] 'requests' library not found.")
    print("  Install it by running:  pip install requests\n")
    sys.exit(1)

# ─────────────────────────────────────────────────────────────────────
# CONFIGURATION
# Replace the value below with your own free API key from:
#   https://openweathermap.org/api  →  "Current Weather Data" (Free)
# ─────────────────────────────────────────────────────────────────────
API_KEY  = "YOUR_API_KEY_HERE"          # <-- paste your key here
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"

# ─────────────────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────────────────

def weather_emoji(condition: str) -> str:
    """Return an emoji that matches the weather condition."""
    condition = condition.lower()
    mapping = {
        "clear":        "☀️",
        "clouds":       "☁️",
        "rain":         "🌧️",
        "drizzle":      "🌦️",
        "thunderstorm": "⛈️",
        "snow":         "❄️",
        "mist":         "🌫️",
        "fog":          "🌫️",
        "haze":         "🌫️",
        "smoke":        "🌫️",
        "dust":         "💨",
        "tornado":      "🌪️",
    }
    for key, emoji in mapping.items():
        if key in condition:
            return emoji
    return "🌡️"


def celsius_to_fahrenheit(c: float) -> float:
    return round(c * 9 / 5 + 32, 1)


def mps_to_kmph(mps: float) -> float:
    return round(mps * 3.6, 1)


def format_time(unix_ts: int, offset_sec: int) -> str:
    """Convert Unix timestamp + UTC offset to local HH:MM."""
    local_time = datetime.datetime.utcfromtimestamp(unix_ts + offset_sec)
    return local_time.strftime("%I:%M %p")


def get_wind_direction(degrees: int) -> str:
    directions = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    return directions[round(degrees / 45) % 8]


def get_uv_label(uv: float) -> str:
    if uv < 3:   return "Low"
    if uv < 6:   return "Moderate"
    if uv < 8:   return "High"
    if uv < 11:  return "Very High"
    return "Extreme"


def divider(char="─", width=56):
    print(char * width)


# ─────────────────────────────────────────────────────────────────────
# CURRENT WEATHER
# ─────────────────────────────────────────────────────────────────────

def fetch_current_weather(city: str, unit: str = "metric") -> dict | None:
    """Fetch current weather data from OpenWeatherMap."""
    params = {
        "q":     city,
        "appid": API_KEY,
        "units": unit,
    }
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 404:
            print(f"\n  ❌ City '{city}' not found. Please check the spelling.\n")
        elif response.status_code == 401:
            print("\n  ❌ Invalid API Key. Please update API_KEY in the script.\n")
        else:
            print(f"\n  ❌ Error {response.status_code}: {response.json().get('message', 'Unknown error')}\n")
    except requests.exceptions.ConnectionError:
        print("\n  ❌ No internet connection. Please check your network.\n")
    except requests.exceptions.Timeout:
        print("\n  ❌ Request timed out. Try again later.\n")
    return None


def display_current_weather(data: dict, unit: str):
    """Print current weather in a formatted CLI layout."""
    temp_sym = "°C" if unit == "metric" else "°F"

    city        = data["name"]
    country     = data["sys"]["country"]
    condition   = data["weather"][0]["main"]
    description = data["weather"][0]["description"].title()
    emoji       = weather_emoji(condition)

    temp        = data["main"]["temp"]
    feels_like  = data["main"]["feels_like"]
    temp_min    = data["main"]["temp_min"]
    temp_max    = data["main"]["temp_max"]
    humidity    = data["main"]["humidity"]
    pressure    = data["main"]["pressure"]
    visibility  = data.get("visibility", 0) / 1000  # metres → km

    wind_speed  = mps_to_kmph(data["wind"]["speed"])
    wind_deg    = data["wind"].get("deg", 0)
    wind_dir    = get_wind_direction(wind_deg)

    sunrise     = format_time(data["sys"]["sunrise"], data["timezone"])
    sunset      = format_time(data["sys"]["sunset"],  data["timezone"])

    now         = datetime.datetime.now().strftime("%A, %d %B %Y  |  %I:%M %p")

    print()
    divider("═")
    print(f"  {emoji}  WEATHER IN {city.upper()}, {country}")
    print(f"     {now}")
    divider("═")
    print(f"  Condition   :  {description}")
    print(f"  Temperature :  {temp}{temp_sym}  (feels like {feels_like}{temp_sym})")
    print(f"  Range       :  ↓ {temp_min}{temp_sym}   ↑ {temp_max}{temp_sym}")
    divider()
    print(f"  Humidity    :  {humidity}%")
    print(f"  Pressure    :  {pressure} hPa")
    print(f"  Visibility  :  {visibility} km")
    print(f"  Wind        :  {wind_speed} km/h  {wind_dir}  ({wind_deg}°)")
    divider()
    print(f"  Sunrise     :  {sunrise}")
    print(f"  Sunset      :  {sunset}")
    divider("═")
    print()


# ─────────────────────────────────────────────────────────────────────
# 5-DAY FORECAST
# ─────────────────────────────────────────────────────────────────────

def fetch_forecast(city: str, unit: str = "metric") -> dict | None:
    params = {
        "q":     city,
        "appid": API_KEY,
        "units": unit,
        "cnt":   40,           # 5 days × 8 readings per day
    }
    try:
        response = requests.get(FORECAST_URL, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass
    return None


def display_forecast(data: dict, unit: str):
    """Print a concise 5-day daily forecast."""
    temp_sym = "°C" if unit == "metric" else "°F"

    # Group readings by date and pick min/max
    daily: dict[str, dict] = {}
    for item in data["list"]:
        date = item["dt_txt"].split(" ")[0]
        temp = item["main"]["temp"]
        cond = item["weather"][0]["main"]
        if date not in daily:
            daily[date] = {"min": temp, "max": temp, "cond": cond}
        else:
            daily[date]["min"] = min(daily[date]["min"], temp)
            daily[date]["max"] = max(daily[date]["max"], temp)

    print()
    divider("═")
    print("  📅  5-DAY FORECAST")
    divider("═")
    for i, (date, info) in enumerate(list(daily.items())[:5]):
        day_name = datetime.datetime.strptime(date, "%Y-%m-%d").strftime("%a %d %b")
        emoji    = weather_emoji(info["cond"])
        lo       = round(info["min"], 1)
        hi       = round(info["max"], 1)
        print(f"  {emoji}  {day_name:<12}  ↓ {lo}{temp_sym:<8}  ↑ {hi}{temp_sym}")
    divider("═")
    print()


# ─────────────────────────────────────────────────────────────────────
# MAIN MENU
# ─────────────────────────────────────────────────────────────────────

def print_banner():
    print()
    divider("═")
    print("  ⛅  CLI WEATHER APPLICATION")
    print("       CodTech IT Solutions — Python Internship")
    divider("═")
    print()


def select_units() -> tuple[str, str]:
    print("  Select temperature unit:")
    print("    [1] Celsius  (metric)")
    print("    [2] Fahrenheit (imperial)")
    choice = input("\n  Enter choice (default = 1): ").strip()
    if choice == "2":
        return "imperial", "°F"
    return "metric", "°C"


def main():
    print_banner()
    unit, sym = select_units()

    while True:
        print()
        divider()
        city = input("  🔍 Enter city name (or 'quit' to exit): ").strip()

        if city.lower() in ("quit", "exit", "q"):
            print("\n  👋  Thank you for using the Weather App!\n")
            break

        if not city:
            print("  ⚠️  Please enter a city name.")
            continue

        # ── Current weather ───────────────────────────────────────
        data = fetch_current_weather(city, unit)
        if data:
            display_current_weather(data, unit)

            # ── Forecast option ───────────────────────────────────
            show_fc = input("  📅 Show 5-day forecast? (y/n): ").strip().lower()
            if show_fc == "y":
                fc_data = fetch_forecast(city, unit)
                if fc_data:
                    display_forecast(fc_data, unit)
                else:
                    print("  ⚠️  Could not fetch forecast data.\n")


if __name__ == "__main__":
    main()
