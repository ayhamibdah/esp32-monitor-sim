import streamlit as st
import pandas as pd
import time

# Sample device data with extended types
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
    },
    {
        "IP": "192.168.1.50",
        "Type": "Smartwatch",
        "RSSI": -60,
        "Proximity": "Medium",
        "Risk": "Medium",
        "Row": 0,
        "Col": 1,
        "MAC": "D1:55:FA:44:AB:CD",
        "First Seen": "10:12:00 AM",
        "Last Seen": "10:14:30 AM",
        "Connection": "Bluetooth"
    },
    {
        "IP": "192.168.1.60",
        "Type": "Earbuds",
        "RSSI": -70,
        "Proximity": "Medium",
        "Risk": "Medium",
        "Row": 4,
        "Col": 3,
        "MAC": "A0:BB:CC:DD:EE:11",
        "First Seen": "10:11:00 AM",
        "Last Seen": "10:13:45 AM",
        "Connection": "Bluetooth"
    }
]

# Initialize Streamlit UI
st.set_page_config(page_title="Exam Room Monitor", layout="wide")
st.title("🧑‍🏫 Exam Room Monitor - Simulation")

col1, col2, col3 = st.columns(3)
col1.metric("Bluetooth Devices", "07")
col2.metric("Wi-Fi Devices", "05")
col3.metric("High Risk Devices", "01")

st.sidebar.header("🔍 Filter Devices")
risk_filter = st.sidebar.selectbox("Risk Level", ["All", "High", "Medium", "Low"])
type_filter = st.sidebar.selectbox("Device Type", ["All", "Smartphone", "Laptop", "Smartwatch", "Earbuds"])

filtered_devices = [d for d in devices if
                    (risk_filter == "All" or d["Risk"] == risk_filter) and
                    (type_filter == "All" or d["Type"] == type_filter)]

st.markdown("---")
st.subheader("📋 Detected Devices")

for device in filtered_devices:
    icon = "📱" if "phone" in device["Type"].lower() else "💻" if "laptop" in device["Type"].lower() else "⌚" if "watch" in device["Type"].lower() else "🎧"
    color = "#f9f9f9" if device["Risk"] == "Low" else "#fffbe6" if device["Risk"] == "Medium" else "#ffe6e6"

    with st.container():
        st.markdown(f"""
        <div style='padding:1rem;margin-bottom:10px;border-radius:10px;background-color:{color};box-shadow:2px 2px 8px #ccc;'>
        <h4>{icon} {device['Type']} — {device['Risk']} Risk</h4>
        <b>IP:</b> {device['IP']}<br>
        <b>MAC:</b> {device['MAC']}<br>
        <b>Proximity:</b> {device['Proximity']}<br>
        <b>Signal Strength:</b> {device['RSSI']} dBm<br>
        <b>Connection:</b> {device['Connection']}<br>
        <b>Seen:</b> {device['First Seen']} – {device['Last Seen']}<br>
        <b>Location:</b> Row {device['Row']}, Column {device['Col']}
        </div>
        """, unsafe_allow_html=True)

        st.button(f"🚩 Flag {device['IP']}", key=device["IP"])

st.markdown("---")
st.subheader("🗺️ Room Map (5x5 Grid)")

grid_size = 5
grid = [["⬜" for _ in range(grid_size)] for _ in range(grid_size)]

for device in devices:
    icon = "📱" if "phone" in device["Type"].lower() else "💻" if "laptop" in device["Type"].lower() else "⌚" if "watch" in device["Type"].lower() else "🎧"
    grid[device["Row"]][device["Col"]] = icon

st.text("    " + "   ".join([f"Col {i}" for i in range(grid_size)]))
for i, row in enumerate(grid):
    st.text(f"Row {i}  " + "   ".join(row))
