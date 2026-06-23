import streamlit as st
import requests
import numpy as np
from datetime import datetime
import folium
from streamlit_folium import st_folium

# ---------- Page config ----------
st.set_page_config(
    page_title="NYC Taxi Trip Duration Predictor",
    page_icon="🚕",
    layout="centered"
)

# ---------- Global Custom CSS (Uber-style: white/black/green) ----------
st.markdown("""
<style>
    /* Overall app background - subtle off-white gradient */
    .stApp {
        background: linear-gradient(135deg, #FAFAFA 0%, #F0F2F5 50%, #E8EBEF 100%);
    }   
    [data-testid="stHeader"] {
        background-color: #FFFFFF;
    }

    /* Base font size bump for the whole app */
    html, body, [class*="css"] {
        font-size: 18px !important;
    }
    /* Force larger font on all text content blocks */
    .stMarkdown, .stMarkdown p, [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] {
        font-size: 1.5rem !important;
    }
    .stMarkdown, .stMarkdown p, [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] {
        font-size: 1.5rem !important;
        color: #000000 !important;
    }

    /* Subheader text size (Pickup Address, Trip Details, etc.) */
    .stMarkdown h3 {
        font-size: 2.2rem !important;
    }

    /* Input field text itself (what user types) */
    input {
        font-size: 1.5rem !important;
    }

    /* Selectbox selected value text */
    [data-baseweb="select"] span {
        font-size: 1.4rem !important;
    }

    /* Form submit button text */
    div.stButton > button p, button[kind="formSubmit"] p {
        font-size: 1.6rem !important;
    }

    /* Caption / footer text - slightly bigger than before */
    [data-testid="stCaptionContainer"] p {
        font-size: 1.2rem !important;
    }

    /* Input field text itself (what user types) */
    input {
        font-size: 1.3rem !important;
    }

    /* Selectbox selected value text */
    [data-baseweb="select"] span {
        font-size: 1.2rem !important;
    }

    /* Form submit button text */
    div.stButton > button p, button[kind="formSubmit"] p {
        font-size: 1.4rem !important;
    }

    /* Caption / footer text - slightly bigger than before */
    [data-testid="stCaptionContainer"] p {
        font-size: 1.05rem !important;
    }

    /* Main title */
    .main-title {
        font-size: 3.5rem;
        font-weight: 900;
        color: #000000;
        margin-bottom: 0;
    }
    .subtitle {
        color: #4A4A4A;
        font-size: 1.5rem;
        margin-bottom: 1.5rem;
    }

    /* Section subheaders (Pickup Address, Trip Details, etc.) */
    h3 {
        color: #000000 !important;
        font-size: 1.6rem !important;
        font-weight: 800 !important;
    }

    /* Labels above input fields */
    label, .stTextInput label, .stSlider label, .stDateInput label, .stSelectbox label {
        color: #000000 !important;
        font-size: 1.15rem !important;
        font-weight: 600 !important;
    }

    /* Text input & date input boxes */
    .stTextInput input, .stDateInput input {
        background-color: #F5F5F5 !important;
        color: #000000 !important;
        border: 2px solid #06C167 !important;
        border-radius: 8px !important;
        font-size: 1.15rem !important;
        padding: 10px !important;
    }

    /* Selectbox - target every nested layer */
    .stSelectbox div[data-baseweb="select"],
    .stSelectbox div[data-baseweb="select"] > div,
    .stSelectbox div[data-baseweb="select"] div[role="button"] {
        background-color: #F5F5F5 !important;
        border: 2px solid #06C167 !important;
        border-radius: 8px !important;
        font-size: 1.2rem !important;
    }
    .stSelectbox div[data-baseweb="select"] * {
        color: #000000 !important;
        background-color: transparent !important;
    }

    /* Dropdown menu (the popup list when you click it) */
    div[data-baseweb="popover"] ul,
    div[data-baseweb="popover"] li {
        background-color: #F5F5F5 !important;
        color: #000000 !important;
        font-size: 1.15rem !important;
    }

    /* Slider track and labels */
    .stSlider [data-testid="stTickBarMin"],
    .stSlider [data-testid="stTickBarMax"] {
        color: #000000 !important;
        font-size: 1rem !important;
    }
    .stSlider div[data-baseweb="slider"] > div > div {
        background-color: #06C167 !important;
    }

    /* Form container box */
    div[data-testid="stForm"] {
        background-color: #FAFAFA;
        border: 2px solid #E0E0E0;
        border-radius: 16px;
        padding: 24px;
    }

    /* Submit button */
    div.stButton > button, button[kind="formSubmit"], button[kind="secondaryFormSubmit"] {
        background-color: #06C167 !important;
        color: #FFFFFF !important;
        font-weight: 800 !important;
        font-size: 1.3rem !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 14px !important;
    }
    div.stButton > button:hover, button[kind="formSubmit"]:hover {
        background-color: #04A157 !important;
    }

    /* Result card */
    .result-card {
        background-color: #000000;
        border-radius: 16px;
        padding: 32px;
        text-align: center;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
        margin: 20px 0;
    }
    .result-card .label {
        color: #06C167;
        font-size: 1.2rem;
        font-weight: 700;
        letter-spacing: 1px;
    }
    .result-card h1 {
        color: #FFFFFF;
        font-size: 3.8rem;
        margin: 8px 0;
        font-weight: 900;
    }
    .fare-pill {
        display: inline-block;
        background-color: #06C167;
        color: #FFFFFF;
        padding: 10px 26px;
        border-radius: 999px;
        font-weight: 800;
        margin-top: 14px;
        font-size: 1.3rem;
    }

    /* Expander */
    .streamlit-expanderHeader {
        font-size: 1.2rem !important;
        font-weight: 700 !important;
        color: #000000 !important;
    }

    /* Metric labels and values inside expander */
    [data-testid="stMetricLabel"] {
        font-size: 1.05rem !important;
        color: #4A4A4A !important;
    }
    [data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
        color: #000000 !important;
        font-weight: 800 !important;
    }

    /* Caption at bottom */
    .stCaption, [data-testid="stCaptionContainer"] {
        font-size: 1rem !important;
        color: #888888 !important;
    }
</style>
""", unsafe_allow_html=True)

# ---------- Title ----------
st.markdown('<p class="main-title">🚕 NYC Taxi Trip Duration Predictor</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Enter your pickup and dropoff address and find out how long your taxi ride will take!</p>', unsafe_allow_html=True)

# ---------- Geocoding function (Address -> Lat/Long) ----------
@st.cache_data(show_spinner=False)
def geocode_address(address: str):
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": address, "format": "json", "limit": 1}
    headers = {"User-Agent": "nyc-taxi-duration-app"}

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        data = response.json()
        if len(data) == 0:
            return None
        return {
            "lat": float(data[0]["lat"]),
            "lon": float(data[0]["lon"]),
            "display_name": data[0]["display_name"]
        }
    except Exception:
        return None

# ---------- Distance calculation helpers ----------
def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2.0) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2.0) ** 2
    c = 2 * np.arcsin(np.sqrt(a))
    return R * c

def manhattan_distance(lat1, lon1, lat2, lon2):
    a = haversine_distance(lat1, lon1, lat1, lon2)
    b = haversine_distance(lat1, lon1, lat2, lon1)
    return a + b

def euclidean_distance(lat1, lon1, lat2, lon2):
    return np.sqrt((lat2 - lat1) ** 2 + (lon2 - lon1) ** 2)

def estimate_fare(distance_km, duration_min, vendor_id):
    """A simple illustrative NYC-style fare formula (not the real metered fare)."""
    base_fare = 2.50
    per_km_rate = 1.75 if vendor_id == 1 else 1.85
    per_min_rate = 0.35
    fare = base_fare + (distance_km * per_km_rate) + (duration_min * per_min_rate)
    return round(fare, 2)

# ---------- Input form ----------
with st.form("trip_form"):
    st.subheader("📍 Pickup Address")
    pickup_address = st.text_input("Where are you being picked up from?", value="Times Square, New York")

    st.subheader("📍 Dropoff Address")
    dropoff_address = st.text_input("Where do you want to go?", value="Central Park, New York")

    st.subheader("🕒 Trip Details")
    col5, col6 = st.columns(2)
    with col5:
        pickup_date_input = st.date_input("Pickup Date", value=datetime(2016, 6, 15))
        passenger_count = st.slider("Passenger Count", min_value=1, max_value=6, value=1)
    with col6:
        pickup_hour = st.slider("Pickup Hour (24h)", min_value=0, max_value=23, value=14)
        vendor_id = st.selectbox("Vendor ID", options=[1, 2])

    submitted = st.form_submit_button("🚀 Predict Trip Duration", use_container_width=True)

# ---------- On submit ----------
if submitted:
    with st.spinner("🔍 Finding your pickup and dropoff points..."):
        pickup_geo = geocode_address(pickup_address)
        dropoff_geo = geocode_address(dropoff_address)

    if pickup_geo is None:
        st.error(f"⚠️ Couldn't find location for pickup address: '{pickup_address}'. Try being more specific (e.g. add city/state).")
    elif dropoff_geo is None:
        st.error(f"⚠️ Couldn't find location for dropoff address: '{dropoff_address}'. Try being more specific (e.g. add city/state).")
    else:
        pickup_latitude = pickup_geo["lat"]
        pickup_longitude = pickup_geo["lon"]
        dropoff_latitude = dropoff_geo["lat"]
        dropoff_longitude = dropoff_geo["lon"]

        pickup_day = pickup_date_input.weekday()
        pickup_date = pickup_date_input.day
        pickup_month = pickup_date_input.month
        is_weekend = 1 if pickup_day >= 5 else 0

        h_dist = haversine_distance(pickup_latitude, pickup_longitude, dropoff_latitude, dropoff_longitude)
        e_dist = euclidean_distance(pickup_latitude, pickup_longitude, dropoff_latitude, dropoff_longitude)
        m_dist = manhattan_distance(pickup_latitude, pickup_longitude, dropoff_latitude, dropoff_longitude)

        payload = {
            "vendor_id": vendor_id,
            "passenger_count": passenger_count,
            "pickup_longitude": pickup_longitude,
            "pickup_latitude": pickup_latitude,
            "dropoff_longitude": dropoff_longitude,
            "dropoff_latitude": dropoff_latitude,
            "pickup_hour": pickup_hour,
            "pickup_date": pickup_date,
            "pickup_month": pickup_month,
            "pickup_day": pickup_day,
            "is_weekend": is_weekend,
            "haversine_distance": h_dist,
            "euclidean_distance": e_dist,
            "manhattan_distance": m_dist
        }

        try:
            with st.spinner("🚦 Calculating your trip duration..."):
                response = requests.post("http://127.0.0.1:8000/predictions", json=payload, timeout=10)

            if response.status_code == 200:
                result_text = response.json()
                try:
                    duration_value = float(result_text.split("is")[1].strip().split(" ")[0])
                except Exception:
                    duration_value = None

                fare = estimate_fare(h_dist, duration_value, vendor_id) if duration_value else None

                # ---------- Attractive result card ----------
                if duration_value is not None:
                    fare_html = f'<div class="fare-pill">💵 Estimated Fare: ${fare}</div>' if fare else ""
                    st.markdown(f"""
                    <div class="result-card">
                        <div class="label">ESTIMATED TRIP DURATION</div>
                        <h1>{duration_value:.1f} min</h1>
                        {fare_html}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.success(result_text)

                # ---------- Map ----------
                st.subheader("🗺️ Route Preview")
                mid_lat = (pickup_latitude + dropoff_latitude) / 2
                mid_lon = (pickup_longitude + dropoff_longitude) / 2

                m = folium.Map(location=[mid_lat, mid_lon], tiles="CartoDB positron")

                folium.Marker(
                    [pickup_latitude, pickup_longitude],
                    tooltip="Pickup",
                    popup=pickup_geo["display_name"],
                    icon=folium.Icon(color="green", icon="play")
                ).add_to(m)

                folium.Marker(
                    [dropoff_latitude, dropoff_longitude],
                    tooltip="Dropoff",
                    popup=dropoff_geo["display_name"],
                    icon=folium.Icon(color="black", icon="stop")
                ).add_to(m)

                folium.PolyLine(
                    locations=[[pickup_latitude, pickup_longitude], [dropoff_latitude, dropoff_longitude]],
                    color="#06C167",
                    weight=5,
                    dash_array="8"
                ).add_to(m)
                m.fit_bounds(
                   [[pickup_latitude, pickup_longitude], [dropoff_latitude, dropoff_longitude]],
                   padding=(40, 40)
                )
                st_folium(m, width=700, height=400, returned_objects=[])

                # ---------- Extra details ----------
                with st.expander("📋 See trip calculation details"):
                    col_a, col_b = st.columns(2)
                    with col_a:
                        st.metric("Distance (Haversine)", f"{h_dist:.2f} km")
                        st.metric("Distance (Manhattan)", f"{m_dist:.2f} km")
                    with col_b:
                        st.metric("Day of week", ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"][pickup_day])
                        st.metric("Weekend trip?", "Yes" if is_weekend else "No")
                    st.write(f"**Pickup resolved to:** {pickup_geo['display_name']}")
                    st.write(f"**Dropoff resolved to:** {dropoff_geo['display_name']}")

            else:
                st.error(f"❌ Something went wrong. Status code: {response.status_code}")
                st.code(response.text)

        except requests.exceptions.ConnectionError:
            st.error("⚠️ Could not connect to the prediction API. Make sure the FastAPI server (app.py) is running on http://127.0.0.1:8000")
        except Exception as e:
            st.error(f"⚠️ Unexpected error: {e}")

st.divider()
st.caption("Built with FastAPI (backend) + Streamlit (frontend) | NYC Taxi Trip Duration MLOps Project")