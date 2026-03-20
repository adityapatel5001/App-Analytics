import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Analytics Dashboard")

uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.write("### Data Preview")
    st.dataframe(df)

    st.write("### Summary")
    st.write(df.describe())

    column = st.selectbox("Select column for chart", df.columns)

    fig, ax = plt.subplots()
    df[column].value_counts().plot(kind='bar', ax=ax)

    st.pyplot(fig)
