"""
hazards_data.py
---------------
Generates synthetic hazard dataset for training the AI classifier
and populating the dashboard with sample data.
"""

import numpy as np
import pandas as pd
import json
import os

HAZARD_TYPES = [
    "Pothole", "Open Construction Pit", "Flooded Road",
    "Fallen Tree", "Gas Leak", "Power Line Down",
    "Road Collapse", "Broken Bridge", "Chemical Spill", "Fire"
]

LOCATIONS = [
    {"name": "Connaught Place, Delhi",       "lat": 28.6315, "lng": 77.2167},
    {"name": "Noida Sector 18",              "lat": 28.5672, "lng": 77.3210},
    {"name": "Dehradun Clock Tower",         "lat": 30.3165, "lng": 78.0322},
    {"name": "Haridwar Har Ki Pauri",        "lat": 29.9457, "lng": 78.1642},
    {"name": "Gurgaon Cyber City",           "lat": 28.4950, "lng": 77.0890},
    {"name": "Lajpat Nagar, Delhi",          "lat": 28.5677, "lng": 77.2433},
    {"name": "Rohini Sector 3, Delhi",       "lat": 28.7041, "lng": 77.1025},
    {"name": "Greater Noida West",           "lat": 28.5921, "lng": 77.4239},
    {"name": "Saket, Delhi",                 "lat": 28.5245, "lng": 77.2066},
    {"name": "Dwarka Sector 10, Delhi",      "lat": 28.5823, "lng": 77.0500},
]

SEVERITY_LABELS = ["Low", "Medium", "High", "Critical"]

DESCRIPTIONS = [
    "Large pothole in the middle of the road causing vehicles to swerve",
    "Open construction pit without any barricade or warning sign",
    "Road completely flooded, water level above knee height",
    "Fallen tree blocking both lanes of the road",
    "Strong smell of gas near residential area, possible leak",
    "Live power line fallen on road after storm",
    "Road has collapsed, large sinkhole visible",
    "Bridge structure appears damaged, cracks visible",
    "Unknown chemical spill on highway, hazardous fumes",
    "Fire spreading near market area, smoke visible",
    "Small pothole on side of road, minor inconvenience",
    "Construction work ongoing but properly barricaded",
    "Minor waterlogging after rain, passable with caution",
    "Broken tree branch on footpath, not blocking road",
    "Temporary gas smell, workers already notified",
]


def generate_training_data(n_samples=2000):
    """Generate synthetic training data for severity classifier."""
    np.random.seed(42)
    data = []

    for _ in range(n_samples):
        hazard_type  = np.random.choice(HAZARD_TYPES)
        hour         = np.random.randint(0, 24)
        reports      = np.random.randint(1, 50)
        area_density = np.random.uniform(0, 1)   # population density
        near_hospital= np.random.randint(0, 2)
        near_school  = np.random.randint(0, 2)
        weather_bad  = np.random.randint(0, 2)
        size_score   = np.random.uniform(0, 10)

        # Rule-based severity for training labels
        score = 0
        if hazard_type in ["Fire", "Chemical Spill", "Gas Leak", "Power Line Down"]: score += 4
        elif hazard_type in ["Road Collapse", "Open Construction Pit", "Broken Bridge"]: score += 3
        elif hazard_type in ["Flooded Road", "Fallen Tree"]: score += 2
        else: score += 1

        score += reports * 0.1
        score += area_density * 2
        score += near_hospital * 1.5
        score += near_school * 1.5
        score += weather_bad * 1
        score += size_score * 0.3
        if hour >= 22 or hour <= 5: score += 1  # night = more dangerous

        if score < 3:    severity = 0  # Low
        elif score < 6:  severity = 1  # Medium
        elif score < 9:  severity = 2  # High
        else:            severity = 3  # Critical

        data.append({
            "hazard_type"   : hazard_type,
            "hour"          : hour,
            "reports_count" : reports,
            "area_density"  : round(area_density, 3),
            "near_hospital" : near_hospital,
            "near_school"   : near_school,
            "weather_bad"   : weather_bad,
            "size_score"    : round(size_score, 2),
            "severity"      : severity
        })

    return pd.DataFrame(data)


def generate_sample_hazards(n=30):
    """Generate sample hazards for dashboard display."""
    np.random.seed(7)
    hazards = []

    for i in range(n):
        loc      = LOCATIONS[i % len(LOCATIONS)]
        htype    = np.random.choice(HAZARD_TYPES)
        severity = np.random.choice(SEVERITY_LABELS, p=[0.3, 0.35, 0.25, 0.1])
        status   = np.random.choice(["Active", "Resolved", "Under Review"], p=[0.5, 0.3, 0.2])

        # Add small random offset to coordinates
        lat = loc["lat"] + np.random.uniform(-0.02, 0.02)
        lng = loc["lng"] + np.random.uniform(-0.02, 0.02)

        hazards.append({
            "id"          : f"HZD-{1000+i}",
            "type"        : htype,
            "location"    : loc["name"],
            "lat"         : round(lat, 6),
            "lng"         : round(lng, 6),
            "severity"    : severity,
            "status"      : status,
            "reports"     : int(np.random.randint(1, 45)),
            "description" : np.random.choice(DESCRIPTIONS),
            "time"        : f"{np.random.randint(0,23):02d}:{np.random.randint(0,59):02d}",
            "alerts_sent" : int(np.random.randint(10, 500)),
        })

    return hazards


if __name__ == "__main__":
    df = generate_training_data()
    print(f"Generated {len(df)} training samples")
    print(df['severity'].value_counts())
