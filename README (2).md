# Citizen Location-Based Hazard Alert System

<p align="center">
  <img src="https://img.shields.io/badge/Hackathon-Graph--e--thon%203.0-red?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Team-Innovators__Knights-blue?style=for-the-badge" />
  <img src="https://img.shields.io/badge/SDG-11%20%7C%207%20%7C%209-green?style=for-the-badge" />
</p>

> A real-time, location-based hazard alert platform that warns citizens about nearby urban dangers via instant SMS — before accidents happen.

---

## Table of Contents

- [Problem Statement](#problem-statement)
- [Proposed Solution](#proposed-solution)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [System Architecture](#system-architecture)
- [Impact & Benefits](#impact--benefits)
- [Getting Started](#getting-started)
- [Team](#team)
- [Research & References](#research--references)

---

## Problem Statement

Urban roads in India often contain hidden hazards — potholes, flooded construction pits, and poorly barricaded work zones. Real incidents highlight the fatal consequences:

- A tech professional lost his life after his car fell into an **unmarked, water-filled construction pit** in the Delhi–Noida region.
- A motorcyclist in **Janakpuri, Delhi** died after his bike fell into an uncovered sewer pit on the road.

These tragedies are preventable. The core issue is that citizens receive **no real-time, location-targeted warnings** before entering danger zones.

### Why existing channels fail

| Limitation | Description |
|---|---|
| Delayed communication | Alerts arrive only after an incident has occurred |
| Limited reach | Only followers of specific platforms receive updates |
| No location targeting | Alerts are not directed to people near the hazard |
| Poor coordination | Authorities lack a centralized system for instant notifications |

Common urban hazards that go unreported in real-time:
- Large potholes that damage vehicles and cause accidents
- Open construction pits without proper barricades or warning signs
- Flooded streets or excavation sites during heavy rainfall
- Sudden road closures or construction zones without clear alerts
- Traffic accidents creating dangerous road conditions

---

## Proposed Solution

The **Citizen Location-Based Hazard Alert System** provides real-time safety alerts to citizens based on their geographic location. The system:

1. **Accepts hazard reports** from citizens via a web platform, local authorities, or external data sources (weather APIs, environmental monitoring)
2. **Processes the exact geographic coordinates** of each reported hazard
3. **Identifies users within a defined risk radius** around the hazard zone
4. **Dispatches instant SMS alerts** — accessible even without smartphones or internet

Each alert clearly communicates the **type of hazard**, its **location**, and **recommended safety precautions**, enabling commuters to make safer travel decisions before they reach the danger zone.

---

## Key Features

| Feature | Description |
|---|---|
| **Multi-Source Hazard Detection** | Detects potholes, flooded roads, open pits, accidents, gas leaks, extreme weather, and pollution hazards |
| **Citizen Hazard Reporting** | Users submit location, description, and optional image to report hazards in real time |
| **External API Integration** | Integrates weather APIs and pollution monitoring systems for environmental risk detection |
| **Location-Based Risk Radius** | GPS data identifies users approaching a hazard zone within a defined distance |
| **Instant SMS Alerts** | Automated SMS warnings sent to nearby citizens — no smartphone required |
| **Authority Dashboard** | Monitoring panel for local authorities to track, verify, and respond to hazard reports |
| **Data Insights** | Aggregated hazard data identifies accident-prone areas to support urban planning |

---

## Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | React.js / HTML / CSS / JavaScript |
| **Backend** | Python (Flask / Django) or Node.js |
| **Database** | Firebase or PostgreSQL |
| **SMS Alerts** | Twilio or SMS Gateway |
| **Maps & Location** | Google Maps API |
| **Cloud Hosting** | AWS / Firebase / Google Cloud |

**Hardware Requirements** — No specialized hardware needed. The system runs on standard mobile phones for citizen reporting and SMS receipt, and cloud servers for application hosting and data processing.

---

## System Architecture

```
Citizens / Authorities / External APIs
            │
            ▼
    ┌───────────────────┐
    │   Web Platform    │  ← Hazard reporting (location + description + image)
    └────────┬──────────┘
             │
             ▼
    ┌───────────────────┐
    │   Backend Server  │  ← Processes hazard data, resolves GPS coordinates
    │  (Python/Node.js) │
    └────────┬──────────┘
             │
     ┌───────┴────────┐
     ▼                ▼
┌─────────┐    ┌──────────────┐
│   DB    │    │ Google Maps  │  ← Identifies users within risk radius
│Firebase/│    │     API      │
│Postgres │    └──────┬───────┘
└─────────┘           │
                       ▼
              ┌────────────────┐
              │  SMS Gateway   │  ← Sends real-time alerts to nearby citizens
              │    (Twilio)    │
              └────────────────┘
```

---

## Impact & Benefits

### Social Impact
- Warns citizens about nearby hazards before accidents occur
- Enables faster communication between authorities and the public during emergencies
- Encourages community participation in safety monitoring
- Increases awareness of local risks — floods, accidents, dangerous road conditions

### Economic Impact
- Reduces economic losses caused by accidents and infrastructure damage
- Helps authorities identify and fix hazard-prone areas faster, lowering maintenance costs
- Improves city efficiency by preventing traffic disruptions
- Supports smart city development to attract investment

### Environmental Impact
- Alerts citizens to avoid polluted or hazardous areas
- Supports better environmental monitoring via weather and pollution API integration
- Encourages faster authority response to flooding, waterlogging, and extreme weather events

### Target Audience
- Citizens and daily commuters
- Local government & municipal bodies
- Emergency response teams
- Urban planners & smart city initiatives

---

## Getting Started

**Prerequisites**
- Node.js >= 16 or Python >= 3.8
- Google Maps API key
- Twilio account (or compatible SMS gateway)
- Firebase project or PostgreSQL database

**Installation**

```bash
# Clone the repository
git clone https://github.com/khushi-sharma2506/CITIZEN-LOCATION-BASED-HAZARD-ALERT-SYSTEM.git
cd CITIZEN-LOCATION-BASED-HAZARD-ALERT-SYSTEM

# Install backend dependencies
pip install -r requirements.txt

# Install frontend dependencies
cd frontend
npm install

# Configure environment variables
cp .env.example .env
```

**Environment Variables**

```env
GOOGLE_MAPS_API_KEY=your_google_maps_api_key
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=your_twilio_number
DATABASE_URL=your_database_connection_string
ALERT_RADIUS_KM=2
```

**Run**

```bash
# Backend
python app.py

# Frontend (new terminal)
cd frontend
npm start
```

App runs at `http://localhost:3000`

---

## Team

**Innovators_Knights** — Graphic Era Deemed to be University, Dehradun, India

- Himanshu Butola
- Khushi Sharma
- Akhil Kotnala
- Anushreya Tomar

---

## Research & References

1. **Real-Time Accident Detection and Emergency Notification System**
   https://goldncloudpublications.com/index.php/irjaem/article/view/730

2. **Satellite-Based Automatic Road Accident Detection and Alert System**

3. **IoT-Enabled Highway Safety Pre-Warning System**
   https://www.ijraset.com/research-paper/iot-enabled-highway-safety-pre-warning-system

4. **Smart Roads for Autonomous Accident Detection and Warnings**
   https://www.mdpi.com/1424-8220/22/6/2077

5. **IoT-Enabled Accident Detection System for Smart Cities**
   https://www.mdpi.com/1424-8220/19/9/2071

---

*Graph-e-thon 3.0 submission — All rights reserved by Team Innovators_Knights*
