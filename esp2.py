import streamlit as st
import pandas as pd
import time

# -------------------------
# Sample device data
# -------------------------
devices = [
    {
        "IP": "192.168.1.45",
        "Type": "Smartphone",
        "RSSI": -48,
        "Proximity": "Close",
        "Risk": "High",
        "Row": 3,
        "Col": 2,
        "MAC": "F4:5C:89:AB:23:76",
        "First Seen": "10:13:22 AM",
        "Last Seen": "10:15:04 AM",
        "Connection": "Wi-Fi + Bluetooth"
    },
    {
        "IP": "192.168.1.102",
        "Type": "Laptop",
        "RSSI": -68,
        "Proximity": "Medium",
        "Risk": "Medium",
        "Row": 1,
        "Col": 4,
        "MAC": "3C:7A:8A:10:99:B1",
        "First Seen": "10:14:00 AM",
        "Last Seen": "10:15:10 AM",
        "Connection": "Wi-Fi"
    }
]

if "flagged_devices" not in st.session_state:
    st.session_state.flagged_devices = []
if "event_log" not in st.session_state:
    st.session_state.event_log = []

# -------------------------
# Page Config
# -------------------------
st.set_page_config(page_title="ESP32 Monitor (Dark)", layout="wide", initial_sidebar_state="expanded")

# Custom dark styling
st.markdown("""
    <style>
    body {
        background-color: #1e1e1e;
        color: white;
    }
    .block-container {
        background-color: #1e1e1e;
    }
    h1, h2, h3, h4, h5, h6 {
        color: white !important;
    }
    .stMarkdown {
        color: white;
    }
    .stTable td {
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------
# Header
# -------------------------
st.image("https://i.imgur.com/UbOXYAU.png", width=80)
st.title("🌙 ESP32 Exam Room Monitor (Dark Mode)")

col1, col2, col3 = st.columns(3)
col1.metric("📶 Bluetooth Devices", "05")
col2.metric("🌐 Wi-Fi Devices", "03")
col3.metric("🚨 High Risk Devices", sum(1 for d in devices if d["Risk"] == "High"))

st.sidebar.header("🎛️ Filters")
risk_filter = st.sidebar.selectbox("Risk Level", ["All", "High", "Medium", "Low"])
type_filter = st.sidebar.selectbox("Device Type", ["All", "Smartphone", "Laptop"])

# Filter devices
filtered_devices = [d for d in devices if
                    (risk_filter == "All" or d["Risk"] == risk_filter) and
                    (type_filter == "All" or d["Type"] == type_filter)]

st.markdown("---")
st.subheader("📋 Device Overview")

# -------------------------
# Device Cards
# -------------------------
for device in filtered_devices:
    is_flagged = device["IP"] in st.session_state.flagged_devices
    bg = "#331212" if is_flagged else "#2b2b2b"
    border = "red" if device["Risk"] == "High" or is_flagged else "#44ff44"

    with st.container():
        st.markdown(f"""
        <div style="padding:1rem;border-left:8px solid {border};margin-bottom:10px;background-color:{bg};border-radius:10px;">
        <strong>{'🚩 FLAGGED' if is_flagged else '📡 DEVICE'}</strong><br>
        <b>IP:</b> {device['IP']} | <b>Type:</b> {device['Type']} | <b>Risk:</b> <span style="color:{border};">{device['Risk']}</span><br>
        <b>MAC:</b> {device['MAC']} | <b>RSSI:</b> {device['RSSI']} | <b>Proximity:</b> {device['Proximity']}<br>
        <b>Seen:</b> {device['First Seen']} - {device['Last Seen']} | <b>Connection:</b> {device['Connection']}
        </div>
        """, unsafe_allow_html=True)

        if not is_flagged:
            if st.button(f"🚨 Flag {device['IP']}", key=device["IP"]):
                st.session_state.flagged_devices.append(device["IP"])
                st.session_state.event_log.append({
                    "IP": device["IP"],
                    "Time": time.strftime("%H:%M:%S"),
                    "Risk": device["Risk"],
                    "Type": device["Type"]
                })

# -------------------------
# Room Grid Map
# -------------------------
st.markdown("---")
st.subheader("🗺️ Room Layout Map")

grid_size = 5
grid = [["⬛" for _ in range(grid_size)] for _ in range(grid_size)]
for device in devices:
    r, c = device["Row"], device["Col"]
    icon = "🔴" if device["Risk"] == "High" else "🟡" if device["Risk"] == "Medium" else "🟢"
    grid[r][c] = icon

col_labels = "     " + "   ".join([f"Col {i}" for i in range(grid_size)])
st.text(col_labels)
for i, row in enumerate(grid):
    st.text(f"Row {i}  " + "   ".join(row))

# -------------------------
# Flag Log
# -------------------------
st.markdown("---")
st.subheader("📝 Flagged Devices Log")
if st.session_state.event_log:
    df_log = pd.DataFrame(st.session_state.event_log)
    st.table(df_log)
else:
    st.info("No devices have been flagged yet.")
