#!/usr/bin/env python3

import hashlib
from datetime import datetime, timezone
from pathlib import Path

import requests
from icalendar import Calendar, Event

SOURCE = "https://donnees.solutions.hydroquebec.com/donnees-ouvertes/data/json/pointeshivernales.json"


def ical_file(offer, year, output_dir):
    return Path(output_dir, offer, f"{year}.ics")


def add_event(event: Event, path: Path):
    cal = Calendar.from_ical(path.read_text())

    for e in cal.events:
        if e["uid"] == event["uid"]:
            return

    cal.add_component(event)
    path.write_bytes(cal.to_ical())


# Ensure a icalendar exists at path
def ensure_calendar(path: Path):
    if path.exists():
        return

    # Create parent directories if needed
    path.parent.mkdir(parents=True, exist_ok=True)

    cal = Calendar()
    cal.add("prodid", "github.com/jlaffaye/hydroquebec-peak-events-ical")
    cal.add("version", "2.0")
    cal.add("calscale", "GREGORIAN")

    path.write_bytes(cal.to_ical())


def fetch_and_generate_files(output_dir="./data"):
    r = requests.get(SOURCE)
    data = r.json()
    generate_files(data, output_dir)


def generate_files(data: dict, output_dir):
    now = datetime.now()
    years = [now.year]

    if now.month == 12 and now.day == 31:
        years.append(now.year + 1)

    for offer in data["offresDisponibles"]:
        for year in years:
            ical_file_path = ical_file(offer, year, output_dir)
            ensure_calendar(ical_file_path)

    for event in data["evenements"]:
        offer = event["offre"]
        startDate = datetime.fromisoformat(event["dateDebut"])
        endDate = datetime.fromisoformat(event["dateFin"])

        year = startDate.year

        ical_file_path = ical_file(offer, year, output_dir)
        uid = hashlib.md5(f"{offer}-{startDate.timestamp()}".encode()).hexdigest()
        event = Event()
        event.start = startDate.astimezone(timezone.utc)
        event.end = endDate.astimezone(timezone.utc)
        event.add("summary", "Peak Event")
        event.add("uid", uid)

        add_event(event, ical_file_path)


fetch_and_generate_files()
