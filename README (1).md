# Citizen Location-Based Hazard Alert System

A real-time platform that detects urban hazards and sends instant SMS alerts to nearby citizens — before accidents happen.

Submitted for **Graph-e-thon 3.0** | Tracks: SDG 11, SDG 7, SDG 9

---

## The Problem

Urban roads in India regularly have unmarked dangers — open construction pits, potholes, flooded excavations, and unbarricaded work zones. A tech professional died after his car fell into an unmarked water-filled pit in the Delhi–Noida region. A motorcyclist in Janakpuri, Delhi lost his life to an uncovered sewer pit. These are not freak incidents; they happen because people simply don't know the danger is ahead.

Current channels like news, social media, and manual signs are too slow, too broad, and not targeted to anyone actually approaching the hazard. There's no system that says *"there's a danger 500 metres ahead of you, right now"*.

---

## Solution

The system collects hazard reports from citizens, local authorities, and external APIs (weather, pollution), then cross-references each hazard's GPS coordinates against registered users in the surrounding area and fires off an SMS alert. No app required — if you have a phone number, you get the warning.

How it works:
1. A hazard is reported (by a citizen, authority, or automated data source)
2. The backend resolves the exact location and calculates a risk radius
3. Users within that radius are identified
4. An SMS is sent with the hazard type, location, and what to do

---

## Features

- **Citizen reporting** — submit a hazard with location, description, and an optional photo
- **Multi-source detection** — potholes, flooded roads, open pits, accidents, gas leaks, pollution, extreme weather
- **Location-based radius alerts** — only people near the hazard are notified
- **SMS delivery** — works on any mobile phone, no internet needed
- **Authority dashboard** — verify reports and coordinate responses
- **Hazard analytics** — spot recurring problem areas to inform urban planning

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React.js / HTML / CSS |
| Backend | Python (Flask/Django) or Node.js |
| Database | Firebase or PostgreSQL |
| SMS | Twilio or SMS Gateway |
| Maps | Google Maps API |
| Hosting | AWS / Firebase / Google Cloud |

---

## System Architecture

```
Citizens / Authorities / External APIs
                |
          Web Platform
                |
         Backend Server
        (hazard processing)
           /        \
      Database    Google Maps API
                  (radius detection)
                       |
                  SMS Gateway
              (alert dispatch)
```

---

## Getting Started

**Prerequisites**
- Python 3.8+ or Node.js 16+
- Google Maps API key
- Twilio account (or any SMS gateway)
- Firebase or PostgreSQL database

**Install**

```bash
git clone https://github.com/khushi-sharma2506/CITIZEN-LOCATION-BASED-HAZARD-ALERT-SYSTEM.git
cd CITIZEN-LOCATION-BASED-HAZARD-ALERT-SYSTEM

# Backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

**Environment variables** — create a `.env` file:

```
GOOGLE_MAPS_API_KEY=your_key
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_PHONE_NUMBER=your_number
DATABASE_URL=your_db_url
ALERT_RADIUS_KM=2
```

**Run**

```bash
python app.py        # backend
cd frontend && npm start   # frontend
```

App runs at `http://localhost:3000`

---

## Impact

Socially, the system gives people advance warning instead of after-the-fact news coverage. Economically, faster hazard identification means lower infrastructure maintenance costs and fewer accident-related losses. Environmentally, real-time pollution and flood alerts let both citizens and authorities respond before situations worsen.

The platform is built for citizens, municipal bodies, emergency teams, and urban planners alike.

---

## Team

Innovators_Knights — Graphic Era Deemed to be University, Dehradun

- Himanshu Butola
- Khushi Sharma
- Akhil Kotnala
- Anushreya Tomar

---

## References

1. Real-Time Accident Detection and Emergency Notification System
   https://goldncloudpublications.com/index.php/irjaem/article/view/730

2. Satellite-Based Automatic Road Accident Detection and Alert System

3. IoT-Enabled Highway Safety Pre-Warning System
   https://www.ijraset.com/research-paper/iot-enabled-highway-safety-pre-warning-system

4. Smart Roads for Autonomous Accident Detection and Warnings
   https://www.mdpi.com/1424-8220/22/6/2077

5. IoT-Enabled Accident Detection System for Smart Cities
   https://www.mdpi.com/1424-8220/19/9/2071
