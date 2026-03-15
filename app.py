"""
app.py — CitizenGuard AI | Streamlit Dashboard
-----------------------------------------------
Run: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import json
import os
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
from hazards_data import (
    generate_training_data, generate_sample_hazards,
    HAZARD_TYPES, SEVERITY_LABELS, LOCATIONS
)

# ── Page Config ───────────────────────────────────────────────
st.set_page_config(
    page_title="CitizenGuard AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CSS ───────────────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background-color: #0d1117; color: #e6edf3; }
    section[data-testid="stSidebar"] { background: #161b22; border-right: 1px solid #21262d; }
    div[data-testid="metric-container"] {
        background: #161b22; border: 1px solid #21262d;
        border-radius: 12px; padding: 16px;
    }
    div[data-testid="metric-container"] label { color: #8b949e !important; font-size: 0.72rem !important; text-transform: uppercase; letter-spacing: 1px; }
    div[data-testid="metric-container"] div[data-testid="stMetricValue"] { font-size: 1.8rem !important; font-weight: 800 !important; }
    .stButton > button {
        background: #238636; color: #fff; font-weight: 700;
        border: none; border-radius: 8px; width: 100%; padding: 10px;
    }
    .stButton > button:hover { background: #2ea043; }
    .alert-critical { background: rgba(248,81,73,0.12); border: 1px solid rgba(248,81,73,0.4); border-radius: 10px; padding: 14px; }
    .alert-high     { background: rgba(255,140,0,0.12); border: 1px solid rgba(255,140,0,0.4);  border-radius: 10px; padding: 14px; }
    .alert-medium   { background: rgba(255,193,7,0.12); border: 1px solid rgba(255,193,7,0.4);  border-radius: 10px; padding: 14px; }
    .alert-low      { background: rgba(63,185,80,0.12); border: 1px solid rgba(63,185,80,0.4);  border-radius: 10px; padding: 14px; }
    .sms-box { background: #161b22; border: 1px solid #238636; border-radius: 12px; padding: 16px; font-family: monospace; }
</style>
""", unsafe_allow_html=True)

# ── Severity Colors ───────────────────────────────────────────
SEV_COLOR = {"Low": "#3fb950", "Medium": "#ffc107", "High": "#ff8c00", "Critical": "#f85149"}
SEV_EMOJI = {"Low": "🟢", "Medium": "🟡", "High": "🟠", "Critical": "🔴"}
STATUS_COLOR = {"Active": "#f85149", "Resolved": "#3fb950", "Under Review": "#ffc107"}

# ── Auto Train ────────────────────────────────────────────────
def auto_train():
    from sklearn.ensemble import GradientBoostingClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import LabelEncoder, StandardScaler
    from sklearn.metrics import accuracy_score, confusion_matrix

    df = generate_training_data(n_samples=3000)
    le_hazard = LabelEncoder()
    df['hazard_encoded'] = le_hazard.fit_transform(df['hazard_type'])

    features = ['hazard_encoded', 'hour', 'reports_count', 'area_density',
                'near_hospital', 'near_school', 'weather_bad', 'size_score']
    X = df[features].values
    y = df['severity'].values

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42, stratify=y)

    model = GradientBoostingClassifier(n_estimators=200, max_depth=5, learning_rate=0.1, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    acc    = accuracy_score(y_test, y_pred)
    cm     = confusion_matrix(y_test, y_pred)
    importances = model.feature_importances_
    feat_imp = sorted(zip(features, importances), key=lambda x: x[1], reverse=True)

    with open("severity_model.pkl", "wb") as f: pickle.dump(model, f)
    with open("severity_scaler.pkl", "wb") as f: pickle.dump(scaler, f)
    with open("hazard_encoder.pkl", "wb") as f: pickle.dump(le_hazard, f)

    meta = {
        "accuracy": round(acc * 100, 2), "features": features,
        "hazard_types": list(le_hazard.classes_), "severity_labels": SEVERITY_LABELS,
        "confusion_matrix": cm.tolist(),
        "feature_importance": [{"feature": f, "importance": round(i, 4)} for f, i in feat_imp]
    }
    with open("model_meta.json", "w") as f: json.dump(meta, f, indent=2)

@st.cache_resource
def load_model():
    if not os.path.exists("severity_model.pkl"):
        with st.spinner("⏳ First launch — training AI model (~30 seconds)..."):
            auto_train()
    with open("severity_model.pkl", "rb") as f: model = pickle.load(f)
    with open("severity_scaler.pkl", "rb") as f: scaler = pickle.load(f)
    with open("hazard_encoder.pkl", "rb") as f: le = pickle.load(f)
    return model, scaler, le

@st.cache_data
def load_meta():
    if not os.path.exists("model_meta.json"): return None
    with open("model_meta.json") as f: return json.load(f)

@st.cache_data
def get_hazards():
    return generate_sample_hazards(30)

model, scaler, le_hazard = load_model()
meta    = load_meta()
hazards = get_hazards()
df_haz  = pd.DataFrame(hazards)

# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🛡️ CitizenGuard AI")
    st.markdown("*Real-time urban hazard alert system*")
    st.divider()

    page = st.radio("Navigate", [
        "🏠 Dashboard",
        "📍 Report Hazard",
        "🗺️ Hazard Map",
        "🤖 AI Classifier",
        "📊 Admin Panel"
    ])

    st.divider()
    active   = len(df_haz[df_haz['status'] == 'Active'])
    critical = len(df_haz[df_haz['severity'] == 'Critical'])
    st.markdown("**Live Status**")
    st.error(f"🔴 {critical} Critical alerts")
    st.warning(f"⚠️ {active} Active hazards")
    if meta: st.success(f"🤖 AI Accuracy: {meta['accuracy']}%")
    st.divider()
    st.caption("Inspired by real Delhi-Noida accidents")
    st.caption("Built by Khushi Sharma | B.Tech AIML")


# ══════════════════════════════════════════════════════════════
# PAGE 1 — DASHBOARD
# ══════════════════════════════════════════════════════════════
if page == "🏠 Dashboard":
    st.title("🏠 CitizenGuard AI Dashboard")
    st.caption(f"Last updated: {datetime.now().strftime('%d %b %Y, %H:%M')} | Protecting citizens across India")
    st.divider()

    # KPIs
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Hazards",    str(len(df_haz)),  "+3 today")
    c2.metric("Active Alerts",    str(active),        delta=f"{active} need attention", delta_color="inverse")
    c3.metric("Critical",         str(critical),      delta="Immediate action", delta_color="inverse")
    c4.metric("Resolved Today",   str(len(df_haz[df_haz['status']=='Resolved'])))
    c5.metric("SMS Alerts Sent",  f"{df_haz['alerts_sent'].sum():,}")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📊 Hazards by Type")
        type_counts = df_haz['type'].value_counts()
        fig = go.Figure(go.Bar(
            x=type_counts.values, y=type_counts.index,
            orientation='h',
            marker=dict(color=type_counts.values, colorscale='Reds', showscale=False)
        ))
        fig.update_layout(plot_bgcolor='#161b22', paper_bgcolor='#161b22',
                          font_color='#e6edf3', height=320, margin=dict(l=0,r=0,t=10,b=0))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("🎯 Severity Distribution")
        sev_counts = df_haz['severity'].value_counts()
        fig2 = go.Figure(go.Pie(
            labels=sev_counts.index, values=sev_counts.values,
            hole=0.6,
            marker_colors=[SEV_COLOR.get(s, '#888') for s in sev_counts.index]
        ))
        fig2.update_layout(plot_bgcolor='#161b22', paper_bgcolor='#161b22',
                           font_color='#e6edf3', height=320, margin=dict(l=0,r=0,t=10,b=0))
        st.plotly_chart(fig2, use_container_width=True)

    st.divider()
    st.subheader("🚨 Recent Active Hazards")

    active_df = df_haz[df_haz['status'] == 'Active'].head(8)
    for _, row in active_df.iterrows():
        sev = row['severity']
        col_a, col_b, col_c, col_d = st.columns([3, 2, 2, 2])
        col_a.markdown(f"**{SEV_EMOJI[sev]} {row['type']}** — {row['location']}")
        col_b.markdown(f"Severity: **{sev}**")
        col_c.markdown(f"Reports: **{row['reports']}**")
        col_d.markdown(f"📱 {row['alerts_sent']} alerts sent")
        st.divider()


# ══════════════════════════════════════════════════════════════
# PAGE 2 — REPORT HAZARD
# ══════════════════════════════════════════════════════════════
elif page == "📍 Report Hazard":
    st.title("📍 Report a Hazard")
    st.markdown("Help keep your city safe by reporting hazards near you.")
    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Hazard Details")
        hazard_type = st.selectbox("Type of Hazard", HAZARD_TYPES)
        description = st.text_area("Describe the hazard", placeholder="e.g. Large open pit without any barricade near the main road...")
        severity_guess = st.select_slider("How severe does it look?", options=["Low", "Medium", "High", "Critical"])

        st.subheader("Your Location")
        location_name = st.text_input("Area / Landmark", placeholder="e.g. Sector 18 Noida, near Metro Station")
        loc_preset = st.selectbox("Or select from known locations", ["Select..."] + [l['name'] for l in LOCATIONS])

        lat_val = 28.6139
        lng_val = 77.2090
        if loc_preset != "Select...":
            sel = next(l for l in LOCATIONS if l['name'] == loc_preset)
            lat_val, lng_val = sel['lat'], sel['lng']

        col_lat, col_lng = st.columns(2)
        lat = col_lat.number_input("Latitude",  value=lat_val, format="%.6f")
        lng = col_lng.number_input("Longitude", value=lng_val, format="%.6f")

    with col2:
        st.subheader("Additional Info")
        near_hospital = st.checkbox("Near a hospital")
        near_school   = st.checkbox("Near a school / college")
        weather_bad   = st.checkbox("Bad weather conditions")
        hour          = st.slider("Current hour", 0, 23, datetime.now().hour)
        reporter_phone= st.text_input("Your phone number (for updates)", placeholder="+91 XXXXXXXXXX")
        reporter_name = st.text_input("Your name (optional)")

        st.divider()
        st.info("🤖 After submitting, our AI will classify the severity and alert nearby citizens via SMS simulation.")

    st.divider()
    if st.button("🚨 Submit Hazard Report"):
        # Run AI prediction
        hazard_encoded = list(le_hazard.classes_).index(hazard_type) if hazard_type in le_hazard.classes_ else 0
        features_input = np.array([[
            hazard_encoded, hour, 1, 0.5,
            int(near_hospital), int(near_school), int(weather_bad), 5.0
        ]])
        scaled_input = scaler.transform(features_input)
        pred     = model.predict(scaled_input)[0]
        proba    = model.predict_proba(scaled_input)[0]
        sev_pred = SEVERITY_LABELS[pred]
        conf     = proba[pred] * 100

        st.divider()
        sev_col = SEV_COLOR[sev_pred]
        st.markdown(f"""
        <div class="alert-{sev_pred.lower()}">
            <h2 style="color:{sev_col};margin:0">{SEV_EMOJI[sev_pred]} AI Severity Assessment: {sev_pred}</h2>
            <p style="margin-top:8px">Confidence: <strong>{conf:.1f}%</strong> | Hazard: <strong>{hazard_type}</strong></p>
        </div>
        """, unsafe_allow_html=True)

        st.success(f"✅ Report submitted! ID: HZD-{np.random.randint(2000,9999)}")

        # SMS simulation
        st.divider()
        st.subheader("📱 SMS Alert Simulation")
        sim_users = np.random.randint(50, 300)
        st.markdown(f"""
        <div class="sms-box">
            <p style="color:#8b949e;font-size:0.75rem">CITIZENGUARD AI ALERT — Sending to {sim_users} users within 2km radius</p>
            <p style="color:#3fb950;margin:8px 0">📨 MESSAGE:</p>
            <p style="color:#e6edf3">⚠️ HAZARD ALERT — {sev_pred.upper()} SEVERITY<br>
            {hazard_type} reported near {location_name or loc_preset}.<br>
            Please avoid this area and take alternate route.<br>
            Stay safe. — CitizenGuard AI</p>
            <p style="color:#8b949e;font-size:0.75rem;margin-top:12px">✅ {sim_users} SMS alerts dispatched successfully</p>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
# PAGE 3 — HAZARD MAP
# ══════════════════════════════════════════════════════════════
elif page == "🗺️ Hazard Map":
    st.title("🗺️ Live Hazard Map")
    st.markdown("Interactive map showing all reported hazards across cities.")
    st.divider()

    # Filters
    col1, col2, col3 = st.columns(3)
    filter_sev    = col1.multiselect("Filter by Severity", SEVERITY_LABELS, default=SEVERITY_LABELS)
    filter_status = col2.multiselect("Filter by Status", ["Active","Resolved","Under Review"], default=["Active","Under Review"])
    filter_type   = col3.multiselect("Filter by Type", HAZARD_TYPES, default=HAZARD_TYPES)

    filtered = df_haz[
        df_haz['severity'].isin(filter_sev) &
        df_haz['status'].isin(filter_status) &
        df_haz['type'].isin(filter_type)
    ]

    st.caption(f"Showing {len(filtered)} hazards")

    # Plotly map
    if len(filtered) > 0:
        fig_map = go.Figure()

        for sev in SEVERITY_LABELS:
            subset = filtered[filtered['severity'] == sev]
            if len(subset) == 0: continue
            fig_map.add_trace(go.Scattermapbox(
                lat=subset['lat'], lon=subset['lng'],
                mode='markers',
                marker=dict(size=14, color=SEV_COLOR[sev], opacity=0.85),
                text=subset.apply(lambda r: f"<b>{r['type']}</b><br>Severity: {r['severity']}<br>Reports: {r['reports']}<br>Status: {r['status']}<br>{r['description'][:60]}...", axis=1),
                hoverinfo='text',
                name=f"{SEV_EMOJI[sev]} {sev}"
            ))

        fig_map.update_layout(
            mapbox=dict(style="carto-darkmatter", center=dict(lat=28.6, lon=77.2), zoom=9),
            margin=dict(l=0, r=0, t=0, b=0),
            height=520,
            paper_bgcolor='#0d1117',
            legend=dict(bgcolor='#161b22', bordercolor='#21262d', font_color='#e6edf3')
        )
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.warning("No hazards match your filters.")

    st.divider()
    st.subheader("📋 Hazard Table")
    display_cols = ['id', 'type', 'location', 'severity', 'status', 'reports', 'alerts_sent', 'time']
    st.dataframe(filtered[display_cols], use_container_width=True, hide_index=True)


# ══════════════════════════════════════════════════════════════
# PAGE 4 — AI CLASSIFIER
# ══════════════════════════════════════════════════════════════
elif page == "🤖 AI Classifier":
    st.title("🤖 AI Hazard Severity Classifier")
    st.markdown("Enter hazard details — the AI will predict severity level instantly.")
    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Input Features")
        hazard_type  = st.selectbox("Hazard Type", HAZARD_TYPES)
        hour         = st.slider("Time of Report (hour)", 0, 23, 14)
        reports      = st.slider("Number of Reports", 1, 50, 5)
        density      = st.slider("Area Population Density", 0.0, 1.0, 0.5)
        near_hosp    = st.checkbox("Near Hospital")
        near_sch     = st.checkbox("Near School/College")
        bad_weather  = st.checkbox("Bad Weather")
        size         = st.slider("Hazard Size Score", 0.0, 10.0, 5.0)

    with col2:
        st.subheader("How AI Decides")
        st.markdown("""
        The AI model looks at **8 features** to predict severity:

        | Feature | Impact |
        |---|---|
        | Hazard Type | Highest — Fire/Gas = Critical |
        | Reports Count | More reports = more severe |
        | Near Hospital/School | Increases severity |
        | Time of Day | Night = more dangerous |
        | Weather | Bad weather = higher risk |
        | Population Density | Crowded = more people at risk |
        | Size Score | Larger hazard = higher severity |

        **Algorithm:** Gradient Boosting Classifier  
        **Accuracy:** {acc}%  
        **Classes:** Low → Medium → High → Critical
        """.format(acc=meta['accuracy'] if meta else "N/A"))

    st.divider()

    if st.button("⚡ Classify Severity"):
        hazard_enc = list(le_hazard.classes_).index(hazard_type) if hazard_type in le_hazard.classes_ else 0
        inp = np.array([[hazard_enc, hour, reports, density,
                         int(near_hosp), int(near_sch), int(bad_weather), size]])
        inp_scaled = scaler.transform(inp)
        pred   = model.predict(inp_scaled)[0]
        proba  = model.predict_proba(inp_scaled)[0]
        sev    = SEVERITY_LABELS[pred]
        conf   = proba[pred] * 100

        st.divider()
        res1, res2 = st.columns(2)

        with res1:
            sev_col = SEV_COLOR[sev]
            st.markdown(f"""
            <div class="alert-{sev.lower()}">
                <h1 style="color:{sev_col};margin:0;font-size:2.5rem">{SEV_EMOJI[sev]}</h1>
                <h2 style="color:{sev_col};margin:4px 0">{sev} Severity</h2>
                <p style="color:#e6edf3">Confidence: <strong>{conf:.1f}%</strong></p>
                <p style="color:#8b949e;font-size:0.85rem">
                {"🚨 Immediate action required! Alert all nearby citizens." if sev == "Critical"
                 else "⚠️ High priority. Notify authorities and nearby residents." if sev == "High"
                 else "📋 Moderate risk. Monitor and inform local residents." if sev == "Medium"
                 else "ℹ️ Low risk. Log report and schedule maintenance."}
                </p>
            </div>
            """, unsafe_allow_html=True)

        with res2:
            fig_conf = go.Figure(go.Bar(
                x=SEVERITY_LABELS,
                y=[p * 100 for p in proba],
                marker_color=[SEV_COLOR[s] for s in SEVERITY_LABELS],
                text=[f"{p*100:.1f}%" for p in proba],
                textposition='outside'
            ))
            fig_conf.update_layout(
                title="Confidence per Class",
                plot_bgcolor='#161b22', paper_bgcolor='#161b22',
                font_color='#e6edf3', height=280,
                yaxis=dict(range=[0, 115]),
                margin=dict(l=0, r=0, t=30, b=0)
            )
            st.plotly_chart(fig_conf, use_container_width=True)

        # Estimated impact
        est_users = int(reports * density * 500 + np.random.randint(50, 200))
        st.info(f"📱 Estimated users to alert: **{est_users:,}** within 2km radius")


# ══════════════════════════════════════════════════════════════
# PAGE 5 — ADMIN PANEL
# ══════════════════════════════════════════════════════════════
elif page == "📊 Admin Panel":
    st.title("📊 Admin Panel")
    st.markdown("Manage hazard reports, send alerts, and monitor system performance.")
    st.divider()

    # Admin KPIs
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Reports",    str(len(df_haz)))
    c2.metric("SMS Sent Today",   f"{df_haz['alerts_sent'].sum():,}")
    c3.metric("Resolved",         str(len(df_haz[df_haz['status']=='Resolved'])))
    c4.metric("AI Accuracy",      f"{meta['accuracy']}%" if meta else "N/A")

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📈 Alerts Sent by Severity")
        sev_alerts = df_haz.groupby('severity')['alerts_sent'].sum().reset_index()
        fig = go.Figure(go.Bar(
            x=sev_alerts['severity'],
            y=sev_alerts['alerts_sent'],
            marker_color=[SEV_COLOR[s] for s in sev_alerts['severity']]
        ))
        fig.update_layout(plot_bgcolor='#161b22', paper_bgcolor='#161b22',
                          font_color='#e6edf3', height=280, margin=dict(l=0,r=0,t=10,b=0))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        if meta:
            st.subheader("🤖 Model Confusion Matrix")
            cm = meta['confusion_matrix']
            fig_cm = go.Figure(go.Heatmap(
                z=cm,
                x=["Low","Med","High","Crit"],
                y=["Low","Med","High","Crit"],
                colorscale=[[0,'#161b22'],[1,'#238636']],
                text=[[str(v) for v in row] for row in cm],
                texttemplate="%{text}", textfont={"size":14},
                showscale=False
            ))
            fig_cm.update_layout(plot_bgcolor='#161b22', paper_bgcolor='#161b22',
                                 font_color='#e6edf3', height=280, margin=dict(l=0,r=0,t=10,b=0))
            st.plotly_chart(fig_cm, use_container_width=True)

    st.divider()
    st.subheader("📋 Manage All Reports")

    status_filter = st.multiselect("Filter by status", ["Active","Resolved","Under Review"], default=["Active"])
    mgmt_df = df_haz[df_haz['status'].isin(status_filter)][
        ['id','type','location','severity','status','reports','alerts_sent','time']
    ]
    st.dataframe(mgmt_df, use_container_width=True, hide_index=True)

    st.divider()
    st.subheader("📱 Send Broadcast Alert")
    broadcast_msg  = st.text_area("Alert message", value="⚠️ CITIZENGUARD ALERT: Please be cautious of reported hazards in your area. Stay safe!")
    target_area    = st.selectbox("Target area", [l['name'] for l in LOCATIONS])
    target_radius  = st.slider("Radius (km)", 1, 10, 3)

    if st.button("📨 Send Broadcast SMS"):
        sim_count = np.random.randint(200, 2000)
        st.success(f"✅ Broadcast sent to **{sim_count:,} users** within {target_radius}km of {target_area}")
        st.markdown(f"""
        <div class="sms-box">
            <p style="color:#8b949e;font-size:0.75rem">BROADCAST TO {sim_count:,} USERS — {target_area} ({target_radius}km radius)</p>
            <p style="color:#e6edf3;margin-top:8px">{broadcast_msg}</p>
            <p style="color:#3fb950;font-size:0.75rem;margin-top:8px">✅ Delivered successfully</p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    if meta:
        st.subheader("🌲 Feature Importance")
        fi = meta['feature_importance']
        fig_fi = go.Figure(go.Bar(
            x=[f['importance'] for f in fi][::-1],
            y=[f['feature'] for f in fi][::-1],
            orientation='h', marker_color='#238636'
        ))
        fig_fi.update_layout(plot_bgcolor='#161b22', paper_bgcolor='#161b22',
                             font_color='#e6edf3', height=320, margin=dict(l=0,r=0,t=10,b=0))
        st.plotly_chart(fig_fi, use_container_width=True)
