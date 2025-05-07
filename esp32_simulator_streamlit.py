import streamlit as st
import pandas as pd

# بيانات وهمية للأجهزة
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

# -------------------------------
# 🖥️ الواجهة الرئيسية
# -------------------------------

st.set_page_config(page_title="Exam Room Monitor", layout="wide")
st.title("📡 Real-Time Device Monitor (Simulated)")

col1, col2, col3 = st.columns(3)
col1.metric("Bluetooth Devices", "05")
col2.metric("Wi-Fi Devices", "03")
col3.metric("High Risk Devices", "02")

st.markdown("---")

# جدول الأجهزة
df = pd.DataFrame(devices)[["IP", "Type", "Proximity", "Risk"]]
selected_index = st.radio("Select a device to inspect:", df["IP"])

selected_device = next(d for d in devices if d["IP"] == selected_index)

with st.expander("📋 Device Details"):
    for key, value in selected_device.items():
        if key not in ["Row", "Col"]:
            st.write(f"**{key}:** {value}")

# -------------------------------
# 🗺️ عرض الخريطة
# -------------------------------

st.markdown("---")
st.subheader("🗺️ Device Location Map (5x5 Grid)")

grid_size = 5
grid = [["⬜" for _ in range(grid_size)] for _ in range(grid_size)]

for device in devices:
    row, col = device["Row"], device["Col"]
    icon = "📱" if "phone" in device["Type"].lower() else "💻"
    grid[row][col] = icon

for row in grid:
    st.write(" ".join(row))
