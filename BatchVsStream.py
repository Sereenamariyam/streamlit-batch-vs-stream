import streamlit as st
import pandas as pd
import time
import random
from datetime import datetime
import altair as alt

# Session state for orders
if "orders" not in st.session_state:
    st.session_state.orders = pd.DataFrame(columns=["Order ID", "Customer", "Amount", "Time"])

# Function to simulate an order
def generate_order():
    return {
        "Order ID": f"O{random.randint(1000, 9999)}",
        "Customer": random.choice(["Alice", "Bob", "Charlie", "Diana","Mahi","Lalitha","Sandhya"]),
        "Amount": round(random.uniform(50, 500), 2),
        "Time": datetime.now().strftime("%H:%M:%S")
    }

# Page title
st.title("📊 Real-Time Stream vs Batch Processing")

# Sidebar to add a new order (stream simulation)
with st.sidebar:
    st.header("🛒 Simulate Orders")
    if st.button("Add New Order"):
        new_order = generate_order()
        st.session_state.orders = pd.concat(
            [st.session_state.orders, pd.DataFrame([new_order])],
            ignore_index=True
        )
        st.success(f"🟢 New Order Added: {new_order['Customer']} - ₹{new_order['Amount']}")

# Display current orders
st.markdown("### 📦 Current Orders")
st.dataframe(st.session_state.orders, use_container_width=True)

# Batch processing logic
if st.button("Run Batch Processing"):
    with st.spinner("Running batch job..."):
        time.sleep(2)
        summary = st.session_state.orders.groupby("Customer")["Amount"].sum().reset_index()
        st.success("✅ Batch job complete!")
        st.markdown("### 📊 Batch Summary")
        st.dataframe(summary)

# Stream processing simulation with real-time chart
if st.button("Enable Stream Processing (with chart updates)"):
    st.markdown("📡 Simulating live stream... (5 events)")

    chart_placeholder = st.empty()
    table_placeholder = st.empty()

    for i in range(10):
        # Simulate 1 new order every second
        time.sleep(1)
        new_order = generate_order()
        st.session_state.orders = pd.concat(
            [st.session_state.orders, pd.DataFrame([new_order])],
            ignore_index=True
        )
        st.toast(f"🟢 Streamed: {new_order['Customer']} spent ₹{new_order['Amount']}")

        # Update chart in real-time
        summary = st.session_state.orders.groupby("Customer")["Amount"].sum().reset_index()
        chart = alt.Chart(summary).mark_bar().encode(
            x=alt.X("Customer", sort="-y"),
            y="Amount",
            color="Customer"
        ).properties(
            title="Live Sales by Customer",
            width=600,
            height=300
        )
        chart_placeholder.altair_chart(chart, use_container_width=True)
        table_placeholder.dataframe(summary)

