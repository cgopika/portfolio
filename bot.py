# Pulse - Daily Summary Bot

import requests
import smtplib
import os
from email.message import EmailMessage
from datetime import date
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

CITY = "palakkad"


def get_weather_alert():
    api_key = os.getenv("OPENWEATHER_API_KEY")

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={CITY}&appid={api_key}&units=metric"
    )

    response = requests.get(url)
    data = response.json()
    

    temp = data["main"]["temp"]
    weather = data["weather"][0]["main"]

    print(f"Temperature: {temp}°C")
    print(f"Weather: {weather}")

    if temp > 35:
        return f"⚠ HIGH TEMPERATURE ALERT\n\nTemperature: {temp}°C in {CITY.title()}"

    if weather.lower() in ["rain", "drizzle", "thunderstorm"]:
        return f"☔ RAIN ALERT\n\nRain predicted in {CITY.title()}"

    return None

def get_weather(city=CITY):
    url = f"https://wttr.in/{city}?format=3&m"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text.strip()

    except Exception as e:
        return f"Weather unavailable ({e})"


def get_quote():
    try:
        response = requests.get(
            "https://zenquotes.io/api/random",
            timeout=20,
            verify=False
        )

        data = response.json()

        quote = data[0]["q"]
        author = data[0]["a"]

        return f'"{quote}" - {author}'

    except Exception as e:
        return f"Quote unavailable ({e})"

def send_email(summary):
    sender = "moaname032@gmail.com"
    receiver = "moaname032@gmail.com"

    password = os.getenv("EMAIL_PASSWORD")

    msg = EmailMessage()
    msg["Subject"] = f"Pulse Daily Summary - {date.today()}"
    msg["From"] = sender
    msg["To"] = receiver

    msg.set_content(summary)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender, password)
        smtp.send_message(msg)

    print("Email sent successfully!")
# today = date.today()

# summary = f"""
# PULSE DAILY SUMMARY
# Date: {today}

# Weather:
# {get_weather()}

# Quote:
# {get_quote()}
# """
today = date.today()

summary = f"""

         PULSE DAILY SUMMARY        


📅  {today}


🌦️  WEATHER
{get_weather()}


💡  QUOTE OF THE DAY
{get_quote()}
"""

with open("daily_summary.txt", "w", encoding="utf-8") as file:
    file.write(summary)

print("Daily summary saved to daily_summary.txt")

alert = get_weather_alert()

if alert:
    send_email(alert)
    print("Alert email sent")
else:
    print("No alert needed today")