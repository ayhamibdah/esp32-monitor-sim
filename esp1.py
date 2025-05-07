
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

# -------------------------
# Session state init
# -------------------------
if "flagged_devices" not in st.session_state:
    st.session_state.flagged_devices = []

# -------------------------
# UI Header
# -------------------------
st.set_page_config(page_title="ESP32 Monitor", layout="wide")
st.title("📡 Real-Time Device Monitor (Simulated)")

# Layout Top Stats
col1, col2, col3 = st.columns(3)
col1.metric("📶 Bluetooth Devices", "05")
col2.metric("🌐 Wi-Fi Devices", "03")
col3.metric("🚨 High Risk Devices", "02")

st.markdown("---")

# -------------------------
# Filter + Auto-refresh
# -------------------------
risk_filter = st.selectbox("📊 Filter by Risk Level:", ["All", "High", "Medium", "Low"])
st_autorefresh = st.empty()
st_autorefresh.markdown(f"⏳ Auto-refresh every 10s: `{time.strftime('%H:%M:%S')}`")
time.sleep(1)  # simulate delay (was 10 originally)

# -------------------------
# Device filtering
# -------------------------
filtered_devices = [
    d for d in devices if (risk_filter == "All" or d["Risk"] == risk_filter)
]

# -------------------------
# Display device cards
# -------------------------
for device in filtered_devices:
    is_flagged = device["IP"] in st.session_state.flagged_devices
    bg = "#ffe6e6" if is_flagged else "#f9f9f9"
    border_color = "red" if device["Risk"] == "High" or is_flagged else "green"

    with st.container():
        st.markdown(f"""
        <div style="padding:1.5rem;margin:10px 0;border-radius:10px;background-color:{bg};border-left:10px solid {border_color};box-shadow:2px 2px 8px #ccc;">
        <h4>{'🚩' if is_flagged else '📋'} Device: {device['IP']}</h4>
        <b>Type:</b> {device['Type']}<br>
        <b>Risk:</b> <span style="color:{border_color};">{device['Risk']}</span><br>
        <b>Proximity:</b> {device['Proximity']}<br>
        <b>MAC:</b> {device['MAC']}<br>
        <b>Seen:</b> {device['First Seen']} – {device['Last Seen']}<br>
        <b>Connection:</b> {device['Connection']}
        </div>
        """, unsafe_allow_html=True)

        if not is_flagged:
            if st.button(f"🚨 Flag {device['IP']}", key=device["IP"]):
                st.session_state.flagged_devices.append(device["IP"])

# -------------------------
# Grid Map View
# -------------------------
st.markdown("---")
st.subheader("🗺️ Device Location Map (5x5 Grid)")

grid_size = 5
grid = [["⬜" for _ in range(grid_size)] for _ in range(grid_size)]
icon_info = [["" for _ in range(grid_size)] for _ in range(grid_size)]

for device in devices:
    r, c = device["Row"], device["Col"]
    icon = "📱" if "phone" in device["Type"].lower() else "💻"
    if device["Risk"].lower() == "high":
        icon = "🔴"
    elif device["Risk"].lower() == "medium":
        icon = "🟡"
    else:
        icon = "🟢"

    grid[r][c] = icon
    icon_info[r][c] = f"{device['Type']} at Row {r}, Col {c} - Risk: {device['Risk']}"

col_labels = "    " + "  ".join([f"Col {i}" for i in range(grid_size)])
st.text(col_labels)

for i, row in enumerate(grid):
    row_label = f"Row {i}  " + "  ".join(row)
    st.text(row_label)

# Detailed map info
st.markdown("### 📋 Device Map Details")
for device in devices:
    r, c = device["Row"], device["Col"]
    st.write(f"🔹 **{device['Type']}** — Row {r}, Col {c}, Risk: **{device['Risk']}**, IP: `{device['IP']}`")
