import streamlit as st
import pandas as pd
import numpy as np
import time

import time
import RPi.GPO as gp


clk = 26  #37
miso = 19 #35
mosi = 13 #33
cs = 6	  #31

mcp = Adafruit_MCP3008.MCP3008(clk=clk, cs=cs, miso=miso, mosi=mosi)
read_analog = mcp.read_adc

light = 10
fan = 8

gp.setmode(gp.BOARD)
gp.setup(light,gp.OUT)
gp.setup(fan, gp.OUT)

# Simulate data for temperature, brightness, and air pollution levels
def generate_data(num_points=100):
    time_series = pd.date_range(start="2023-01-01", periods=num_points, freq='H')
    temperature = np.random.normal(loc=22, scale=2, size=num_points)  # Simulate around 22°C
    brightness = np.random.normal(loc=300, scale=50, size=num_points)  # Simulate around 300 lux
    air_pollution = np.random.normal(loc=50, scale=10, size=num_points)  # Simulate around 50 AQI

    data = pd.DataFrame({
        'Time': time_series,
        'Temperature': temperature,
        'Brightness': brightness,
        'Air Pollution': air_pollution
    })

    return data

# Generate the data
data = generate_data()

# Streamlit UI
st.title("Smart Laboratory Energy Management System")

st.write("## Environmental Monitoring Dashboard")

# Create a sidebar for user controls
st.sidebar.title("Controls")
num_points = st.sidebar.slider("Number of Data Points", min_value=10, max_value=500, value=100, step=10)

# Update the data based on user selection
data = generate_data(num_points)

# Display the data
st.write("### Data")
st.dataframe(data)

# Buttons for controlling electrical appliances
st.write("### Control Electrical Appliances")

if st.button('Turn On Air Conditioner'):
    st.write("Air Conditioner is ON")

if st.button('Turn Off Air Conditioner'):
    st.write("Air Conditioner is OFF")

if st.button('Turn On Lights'):
    st.write("Lights are ON")

if st.button('Turn Off Lights'):
    st.write("Lights are OFF")

if st.button('Turn On Air Purifier'):
    st.write("Air Purifier is ON")

if st.button('Turn Off Air Purifier'):
    st.write("Air Purifier is OFF")

# Data input fields
st.write("### Input Data Fields")
temperature_input = st.number_input('Set Desired Temperature (°C)', min_value=16, max_value=30, value=22)
brightness_input = st.number_input('Set Desired Brightness (lux)', min_value=100, max_value=1000, value=300)
air_pollution_input = st.number_input('Set Desired Air Pollution Level (AQI)', min_value=0, max_value=200, value=50)

# Plotting the data
st.write("### Temperature Over Time")
st.line_chart(data.set_index('Time')['Temperature'])

st.write("### Brightness Over Time")
st.line_chart(data.set_index('Time')['Brightness'])

st.write("### Air Pollution Over Time")
st.line_chart(data.set_index('Time')['Air Pollution'])

# Real-time simulation
st.write("### Real-Time Data Simulation")
placeholder = st.empty()

for _ in range(10):  # Simulate 10 iterations of real-time data updates
    new_data = generate_data(1)
    data = pd.concat([data, new_data]).tail(num_points)  # Keep only the latest num_points rows

    with placeholder.container():
        st.write("#### Updated Data")
        st.line_chart(data.set_index('Time')['Temperature'])
        st.line_chart(data.set_index('Time')['Brightness'])
        st.line_chart(data.set_index('Time')['Air Pollution'])
    
    time.sleep(2)  # Pause for 2 seconds to simulate real-time update
