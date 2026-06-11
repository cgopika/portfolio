# Pulse - Daily Summary Bot

import requests
from datetime import date

def get_weather(city="Thiruvananthapuram"):
    url = f"https://wttr.in/{city}?format=3"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text.strip()

    except Exception as e:
        return f"Weather unavailable ({e})"


def get_quote():
    url = "https://zenquotes.io/api/random"

    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()

        data = response.json()
        quote = data[0]["q"]
        author = data[0]["a"]

        return f'"{quote}" - {author}'

    except Exception as e:
        return f"Quote unavailable ({e})"


today = date.today()

summary = f"""
PULSE DAILY SUMMARY
Date: {today}

Weather:
{get_weather()}

Quote:
{get_quote()}
"""

with open("daily_summary.txt", "w", encoding="utf-8") as file:
    file.write(summary)

print("Daily summary saved to daily_summary.txt")