#!/usr/bin/env python3
"""
CodTech Internship Task-1: API Integration + Data Visualization

Fetches 5-day / 3-hour forecast data from OpenWeatherMap and builds a simple
"dashboard" with multiple charts using matplotlib.

Requirements:
  pip install requests matplotlib

How to run:
  1) Create an API key at https://openweathermap.org/api
  2) Set your key as an environment variable:
       - macOS/Linux:
           export OWM_API_KEY="YOUR_KEY"
       - Windows PowerShell:
           setx OWM_API_KEY "YOUR_KEY"
  3) Run:
       python weather_dashboard.py --city "Hyderabad" --country "IN"
"""

import os
import sys
import argparse
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict, Any, Optional

import requests
import matplotlib.pyplot as plt


@dataclass
class ForecastPoint:
    dt: datetime
    temp_c: float
    feels_like_c: float
    humidity: int
    wind_ms: float
    rain_mm_3h: float
    pressure_hpa: int
    desc: str


class OpenWeatherClient:
    BASE_URL = "https://api.openweathermap.org/data/2.5/forecast"

    def __init__(self, api_key: str, timeout: int = 15):
        self.api_key = api_key
        self.timeout = timeout

    def fetch_forecast(self, city: str, country: Optional[str] = None) -> Dict[str, Any]:
        q = f"{city},{country}" if country else city
        params = {
            "q": q,
            "appid": self.api_key,
            "units": "metric",  # Celsius
        }
        resp = requests.get(self.BASE_URL, params=params, timeout=self.timeout)
        if resp.status_code != 200:
            # Try to print a helpful message from API if present
            try:
                msg = resp.json()
            except Exception:
                msg = resp.text
            raise RuntimeError(f"OpenWeatherMap API error {resp.status_code}: {msg}")
        return resp.json()


class WeatherDashboard:
    def __init__(self, out_png: str = "weather_dashboard.png"):
        self.out_png = out_png

    @staticmethod
    def parse_points(payload: Dict[str, Any]) -> List[ForecastPoint]:
        points: List[ForecastPoint] = []
        for item in payload.get("list", []):
            dt = datetime.fromtimestamp(item["dt"])
            main = item.get("main", {})
            wind = item.get("wind", {})
            weather_list = item.get("weather", [])
            desc = weather_list[0].get("description", "") if weather_list else ""

            rain_mm_3h = 0.0
            if "rain" in item and isinstance(item["rain"], dict):
                # OpenWeatherMap may provide "3h" field
                rain_mm_3h = float(item["rain"].get("3h", 0.0) or 0.0)

            points.append(
                ForecastPoint(
                    dt=dt,
                    temp_c=float(main.get("temp", 0.0)),
                    feels_like_c=float(main.get("feels_like", 0.0)),
                    humidity=int(main.get("humidity", 0) or 0),
                    wind_ms=float(wind.get("speed", 0.0) or 0.0),
                    rain_mm_3h=rain_mm_3h,
                    pressure_hpa=int(main.get("pressure", 0) or 0),
                    desc=desc,
                )
            )
        if not points:
            raise ValueError("No forecast points found in API response.")
        return points

    @staticmethod
    def _top_conditions(points: List[ForecastPoint], top_n: int = 6):
        counts: Dict[str, int] = {}
        for p in points:
            key = p.desc.strip().lower() or "unknown"
            counts[key] = counts.get(key, 0) + 1
        # Sort by frequency
        items = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)[:top_n]
        labels = [k for k, _ in items]
        values = [v for _, v in items]
        return labels, values

    def plot(self, points: List[ForecastPoint], title: str):
        x = [p.dt for p in points]
        temps = [p.temp_c for p in points]
        feels = [p.feels_like_c for p in points]
        humidity = [p.humidity for p in points]
        wind = [p.wind_ms for p in points]
        rain = [p.rain_mm_3h for p in points]

        # A simple "dashboard" layout: 2 rows x 2 cols
        fig, axes = plt.subplots(2, 2, figsize=(14, 8))
        fig.suptitle(title, fontsize=16)

        # (1) Temperature line chart
        ax = axes[0][0]
        ax.plot(x, temps, label="Temp (°C)")
        ax.plot(x, feels, label="Feels like (°C)")
        ax.set_title("Temperature Forecast")
        ax.set_ylabel("°C")
        ax.tick_params(axis="x", rotation=25)
        ax.grid(True, linestyle="--", alpha=0.4)
        ax.legend()

        # (2) Humidity + Wind (two lines)
        ax = axes[0][1]
        ax.plot(x, humidity, label="Humidity (%)")
        ax.plot(x, wind, label="Wind (m/s)")
        ax.set_title("Humidity & Wind")
        ax.set_ylabel("Value")
        ax.tick_params(axis="x", rotation=25)
        ax.grid(True, linestyle="--", alpha=0.4)
        ax.legend()

        # (3) Rain bar chart
        ax = axes[1][0]
        ax.bar(x, rain)
        ax.set_title("Rain (mm per 3h)")
        ax.set_ylabel("mm")
        ax.tick_params(axis="x", rotation=25)
        ax.grid(True, axis="y", linestyle="--", alpha=0.4)

        # (4) Top weather conditions (bar chart)
        ax = axes[1][1]
        labels, values = self._top_conditions(points, top_n=6)
        ax.bar(labels, values)
        ax.set_title("Most Frequent Conditions")
        ax.set_ylabel("Count")
        ax.tick_params(axis="x", rotation=25)
        ax.grid(True, axis="y", linestyle="--", alpha=0.4)

        plt.tight_layout(rect=[0, 0.02, 1, 0.95])
        plt.savefig(self.out_png, dpi=200)
        plt.show()


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Fetch weather forecast and create a matplotlib dashboard.")
    p.add_argument("--city", required=True, help="City name, e.g., Hyderabad")
    p.add_argument("--country", default=None, help="Optional country code, e.g., IN")
    p.add_argument("--out", default="weather_dashboard.png", help="Output dashboard image filename")
    return p


def main() -> int:
    args = build_arg_parser().parse_args()
    api_key = os.getenv("OWM_API_KEY")

    if not api_key:
        print("ERROR: Please set environment variable OWM_API_KEY to your OpenWeatherMap API key.", file=sys.stderr)
        print('Example: export OWM_API_KEY="304320b61f5800a64f24b78babc1d7da"', file=sys.stderr)
        return 2

    client = OpenWeatherClient(api_key=api_key)
    dashboard = WeatherDashboard(out_png=args.out)

    payload = client.fetch_forecast(city=args.city, country=args.country)
    points = dashboard.parse_points(payload)

    city_name = payload.get("city", {}).get("name", args.city)
    country = payload.get("city", {}).get("country", args.country or "")
    title = f"Weather Dashboard: {city_name} {('(' + country + ')') if country else ''} | Next 5 Days (3h intervals)"

    dashboard.plot(points, title=title)
    print(f"Saved dashboard image to: {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

