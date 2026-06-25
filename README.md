# Weather-App-CLI
# ⛅ CLI Weather Application
```
**CodTech IT Solutions — Python Programming Internship**  
Task Name  : Weather App (CLI)  
Intern Name: B.SHAM  
Intern ID  : CITS5427  
Domain     : Python Programming  
Duration   : 22 June 2026 – 20 July 2026  
```

## 📌 Project Overview

The **CLI Weather Application** is a Python command-line tool that fetches **real-time weather data** for any city in the world using the **OpenWeatherMap API**. It displays current conditions and an optional **5-day forecast** directly in the terminal — no GUI needed.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🌡️ Current Weather | Temperature, feels-like, min/max for the day |
| 💧 Atmosphere | Humidity, pressure, visibility |
| 💨 Wind | Speed (km/h), direction (N/S/E/W), degrees |
| 🌅 Sun Times | Sunrise and sunset in local time |
| 📅 5-Day Forecast | Daily high/low for the next 5 days |
| 🌍 Any City | Works for any city worldwide |
| 🌡️ Unit Toggle | Choose Celsius or Fahrenheit at startup |
| ♾️ Multi-Search | Search multiple cities in one session |
| 🛡️ Error Handling | Handles invalid city, bad API key, no internet |
| 🎨 Emoji Icons | Condition-matched weather emojis in terminal |

---

## 🛠️ Technologies Used

| Tool | Purpose |
|------|---------|
| Python 3.x | Core programming language |
| `requests` | HTTP calls to OpenWeatherMap API |
| `datetime` | Time formatting and date calculations |
| `sys` | Clean exit on import failure |
| OpenWeatherMap API | Free real-time weather data source |

---

## 📂 Project Structure

```
weather-app-cli/
│
├── weather_app.py     ← Main Python script
└── README.md          ← Project documentation
```

---

## 🚀 Getting Started

### Step 1 — Get a Free API Key

1. Go to [https://openweathermap.org/api](https://openweathermap.org/api)
2. Sign up for a free account
3. Go to **"My API Keys"** and copy your key
4. The free tier gives you 60 calls/minute — more than enough

### Step 2 — Clone the Repository

```bash
git clone https://github.com/your-username/weather-app-cli.git
cd weather-app-cli
```

### Step 3 — Install Dependencies

```bash
pip install requests
```

### Step 4 — Add Your API Key

Open `weather_app.py` and replace line 27:

```python
API_KEY = "YOUR_API_KEY_HERE"   # ← paste your key here
```

### Step 5 — Run the App

```bash
python weather_app.py
```

---
## 🔧 How It Works (Step-by-Step)  
Step 1  →  User selects Celsius or Fahrenheit  
           ↓  
Step 2  →  User types a city name  
           ↓  
Step 3  →  Script calls OpenWeatherMap /weather endpoint  
           ↓  
Step 4  →  JSON response is parsed for temp, humidity,
           wind, pressure, sunrise/sunset, etc.  
           ↓  
Step 5  →  Data is formatted and printed with emojis  
           ↓  
Step 6  →  User optionally requests a 5-day forecast  
           ↓  
Step 7  →  Script calls /forecast endpoint, groups
           readings by date, computes daily min/max  
           ↓  
Step 8  →  Forecast table is displayed  
           ↓  
Step 9  →  User can search another city or type 'quit'  
```

```
## ⚠️ Error Handling
| Scenario | Response |
|----------|---------|
| City not found | `❌ City 'xyz' not found. Please check the spelling.` |
| Invalid API key | `❌ Invalid API Key. Please update API_KEY in the script.` |
| No internet | `❌ No internet connection. Please check your network.` |
| Request timeout | `❌ Request timed out. Try again later.` |
| Empty input | `⚠️ Please enter a city name.` |
```
```
**Conclusion:**  
This project successfully demonstrates the use of Python and API integration to fetch and display real-time weather information through a user-friendly command-line interface. It enhances practical skills in API handling, data processing, error management, and CLI application development.  
```

