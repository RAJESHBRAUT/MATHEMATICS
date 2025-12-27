import streamlit as st
import pandas as pd
import numpy as np

# Set page to mobile-friendly wide mode
st.set_page_config(page_title="Stats for Students", layout="centered")

st.title("📊 Descriptive Statistics Lab")
st.write("Enter numbers separated by commas to see the math in action.")

# User Input
data_str = st.text_input("Input Data (e.g., 175, 172, 165):", "175, 172, 165")

if data_str:
    try:
        # Convert string to list of numbers
        nums = [float(x.strip()) for x in data_str.split(",")]
        df = pd.DataFrame(nums, columns=["Value"])

        # Display Statistics in "Metric Cards" (Looks great on phones)
        col1, col2, col3 = st.columns(3)
        col1.metric("Mean", round(np.mean(nums), 2))
        col2.metric("Median", np.median(nums))
        col3.metric("SD", round(np.std(nums), 2))

        # Show Table
        st.subheader("Raw Data Summary")
        st.table(df.describe().T)

        # Plotting
        st.subheader("Visualizations")
        st.bar_chart(df)
        st.line_chart(df)

    except ValueError:
        st.error("Please ensure you only enter numbers and commas.")
