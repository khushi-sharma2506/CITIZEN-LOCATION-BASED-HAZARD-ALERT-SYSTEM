"""
train_model.py
--------------
Trains the AI Hazard Severity Classifier.
Run once before launching app:
    python train_model.py
"""

import numpy as np
import pandas as pd
import pickle
import json
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from hazards_data import generate_training_data, HAZARD_TYPES, SEVERITY_LABELS

print("=" * 55)
print("  🤖 CitizenGuard AI — Model Training")
print("=" * 55)

# ── 1. Generate Data ──────────────────────────────────────────
print("\n📊 Generating training data...")
df = generate_training_data(n_samples=3000)
print(f"   Samples     : {len(df):,}")
print(f"   Features    : {df.shape[1]-1}")
print(f"\n   Severity distribution:")
for i, label in enumerate(SEVERITY_LABELS):
    count = (df['severity'] == i).sum()
    pct   = count / len(df) * 100
    bar   = "█" * int(pct / 2)
    print(f"   {label:<10} {bar} {count} ({pct:.1f}%)")

# ── 2. Encode & Preprocess ────────────────────────────────────
le_hazard = LabelEncoder()
df['hazard_encoded'] = le_hazard.fit_transform(df['hazard_type'])

features = ['hazard_encoded', 'hour', 'reports_count', 'area_density',
            'near_hospital', 'near_school', 'weather_bad', 'size_score']

X = df[features].values
y = df['severity'].values

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y
)

# ── 3. Train Model ────────────────────────────────────────────
print("\n🌲 Training Gradient Boosting Classifier...")
model = GradientBoostingClassifier(
    n_estimators=200, max_depth=5,
    learning_rate=0.1, random_state=42
)
model.fit(X_train, y_train)
print("✅ Training complete!")

# ── 4. Evaluate ───────────────────────────────────────────────
y_pred = model.predict(X_test)
acc    = accuracy_score(y_test, y_pred)
cm     = confusion_matrix(y_test, y_pred)

print(f"\n{'='*55}")
print(f"  📈 MODEL PERFORMANCE")
print(f"{'='*55}")
print(f"  Accuracy : {acc*100:.2f}%")
print()
print(classification_report(y_test, y_pred,
      target_names=SEVERITY_LABELS))

# Feature importance
importances = model.feature_importances_
feat_imp = sorted(zip(features, importances), key=lambda x: x[1], reverse=True)
print("Top Features:")
for feat, imp in feat_imp:
    bar = "█" * int(imp * 100)
    print(f"  {feat:<20} {bar} {imp:.4f}")

# ── 5. Save ───────────────────────────────────────────────────
with open("severity_model.pkl", "wb") as f: pickle.dump(model, f)
with open("severity_scaler.pkl", "wb") as f: pickle.dump(scaler, f)
with open("hazard_encoder.pkl", "wb") as f: pickle.dump(le_hazard, f)

model_meta = {
    "accuracy"      : round(acc * 100, 2),
    "features"      : features,
    "hazard_types"  : list(le_hazard.classes_),
    "severity_labels": SEVERITY_LABELS,
    "confusion_matrix": cm.tolist(),
    "feature_importance": [{"feature": f, "importance": round(i, 4)} for f, i in feat_imp]
}
with open("model_meta.json", "w") as f: json.dump(model_meta, f, indent=2)

print(f"\n{'='*55}")
print("  💾 Saved Files:")
print("     severity_model.pkl   — trained classifier")
print("     severity_scaler.pkl  — fitted scaler")
print("     hazard_encoder.pkl   — label encoder")
print("     model_meta.json      — model metadata")
print(f"{'='*55}")
print("\n🚀 Now run:  streamlit run app.py")
