import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time

# ==========================================
# Page Configuration & UI Styling
# ==========================================
st.set_page_config(page_title="IoT Structural Monitor", layout="wide", page_icon="🌉")

st.markdown("""
    <style>
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    h1, h2, h3 { color: #1E3A8A; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .sensor-box { 
        background-color: #ffffff; 
        padding: 20px; 
        border-radius: 12px; 
        box-shadow: 0 4px 12px rgba(0,0,0,0.05); 
        text-align: center;
        border-top: 4px solid #3B82F6;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 style='text-align: center;'>🌉 IoT Sensor Network: Structural Health Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>Real-time monitoring of Strain Gauges & Accelerometers via Wireless Transmission</p>", unsafe_allow_html=True)
st.markdown("---")

# ==========================================
# Session State Initialization
# ==========================================
# Keeping state ensures the app doesn't reset or crash during cloud re-renders
if 'is_streaming' not in st.session_state:
    st.session_state.is_streaming = False # Default to False so it deploys instantly

if 'accel_data' not in st.session_state:
    st.session_state.accel_data = pd.DataFrame({
        'Time': pd.date_range(start=pd.Timestamp.now(), periods=10, freq='2S'),
        'X-Axis': np.random.normal(0, 0.05, 10),
        'Y-Axis': np.random.normal(0, 0.05, 10),
        'Z-Axis': np.random.normal(1.0, 0.1, 10)
    })

# ==========================================
# Sidebar Controls
# ==========================================
with st.sidebar:
    st.header("⚙️ Network Settings")
    structure_type = st.selectbox("Select Structure", ["Highway Bridge", "High-Rise Building", "Dam Retaining Wall"])
    protocol = st.radio("Wireless Protocol", ["LoRaWAN (Low Power)", "5G (High Speed)"])
    
    # Toggle Stream Button
    if st.button("▶️ Start / Pause Live Stream", type="primary"):
        st.session_state.is_streaming = not st.session_state.is_streaming
    
    st.markdown("---")
    if st.session_state.is_streaming:
        st.success("Live Stream: **ACTIVE**")
    else:
        st.warning("Live Stream: **PAUSED**")

# ==========================================
# Visualization Functions
# ==========================================
def create_gauge(value, title, max_val, suffix, color):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title, 'font': {'size': 18}},
        number={'suffix': suffix, 'font': {'size': 26}},
        gauge={
            'axis': {'range': [None, max_val]},
            'bar': {'color': color},
            'bgcolor': "white",
            'borderwidth': 1,
            'bordercolor': "#E5E7EB",
        }
    ))
    fig.update_layout(height=250, margin=dict(l=10, r=10, t=30, b=10))
    return fig

# ==========================================
# Main Dashboard Layout
# ==========================================
col1, col2, col3 = st.columns(3)

# Generate synthetic data if streaming is active
if st.session_state.is_streaming:
    current_time = pd.Timestamp.now()
    new_row = pd.DataFrame({
        'Time': [current_time], 
        'X-Axis': [np.random.normal(0, 0.05)], 
        'Y-Axis': [np.random.normal(0, 0.05)], 
        'Z-Axis': [np.random.normal(1.0, 0.1)]
    })
    st.session_state.accel_data = pd.concat([st.session_state.accel_data, new_row]).tail(20)
    
    strain_val = round(np.random.uniform(200, 400), 1)
    tilt_val = round(np.random.uniform(0.1, 1.5), 2)
else:
    # Static values when paused
    strain_val = 210.5
    tilt_val = 0.2

# Render Gauges and Stats
with col1:
    st.plotly_chart(create_gauge(strain_val, "Material Strain", 600, " µε", "#3B82F6"), use_container_width=True)

with col2:
    st.plotly_chart(create_gauge(tilt_val, "Structural Tilt", 5, "°", "#EF4444"), use_container_width=True)

with col3:
    st.markdown("<div class='sensor-box'>", unsafe_allow_html=True)
    st.subheader("📡 Hub Status")
    st.write(f"**Protocol:** {protocol}")
    st.write(f"**Signal:** -{np.random.randint(50, 70) if st.session_state.is_streaming else 55} dBm")
    st.write("**Uptime:** 99.9%")
    st.markdown("</div>", unsafe_allow_html=True)

# Render Line Chart
st.markdown("### 📳 3-Axis Accelerometer (Vibration Analysis)")
fig_accel = go.Figure()
fig_accel.add_trace(go.Scatter(x=st.session_state.accel_data['Time'], y=st.session_state.accel_data['X-Axis'], mode='lines+markers', name='X-Axis', line=dict(color='#EF4444')))
fig_accel.add_trace(go.Scatter(x=st.session_state.accel_data['Time'], y=st.session_state.accel_data['Y-Axis'], mode='lines+markers', name='Y-Axis', line=dict(color='#10B981')))
fig_accel.add_trace(go.Scatter(x=st.session_state.accel_data['Time'], y=st.session_state.accel_data['Z-Axis'], mode='lines+markers', name='Z-Axis', line=dict(color='#3B82F6')))

fig_accel.update_layout(
    height=350,
    margin=dict(l=0, r=0, t=10, b=0),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    plot_bgcolor="white"
)
fig_accel.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#E5E7EB')
fig_accel.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#E5E7EB')
st.plotly_chart(fig_accel, use_container_width=True)

# Loop Execution
if st.session_state.is_streaming:
    time.sleep(2)
    st.rerun()
