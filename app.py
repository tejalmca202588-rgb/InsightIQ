import streamlit as st
from src.data_loader import load_data
from src.data_cleaner import (
    get_missing_values,
    get_duplicate_count,
    remove_duplicates,
    fill_missing_values,
)
from src.eda import (
    dataset_summary,
    numerical_summary,
    missing_values,
    data_types,
)

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="InsightIQ",
    page_icon="📊",
    layout="wide"
)

# -----------------------------
# Session State
# -----------------------------
if "df" not in st.session_state:
    st.session_state.df = None

# -----------------------------
# Title
# -----------------------------
st.title("📊 InsightIQ")
st.subheader("AI-Powered Business Intelligence Platform")

st.write("""
InsightIQ transforms raw business data into meaningful insights
using data analysis, visualization, and intelligent recommendations.
""")

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("Navigation")

option = st.sidebar.selectbox(
    "Choose Module",
    [
    "Home",
    "Data Upload",
    "Data Cleaning",
    "EDA",
    "Dashboard",
    "AI Insights"
    ]
)

# -----------------------------
# Home
# -----------------------------
if option == "Home":

    st.header("🏠 Welcome to InsightIQ")

    st.info("""
Upload your CSV or Excel dataset to begin analysis.

Current Features:
- 📂 Upload CSV & Excel files
- 🧹 Clean datasets
- 📊 Dashboard (Coming Soon)
- 🤖 AI Insights (Coming Soon)
""")

# -----------------------------
# Data Upload
# -----------------------------
elif option == "Data Upload":

    st.header("📂 Upload Dataset")

    uploaded_file = st.file_uploader(
        "Choose CSV or Excel File",
        type=["csv", "xlsx", "xls"]
    )

    if uploaded_file is not None:

        df = load_data(uploaded_file)

        if df is not None:

            st.session_state.df = df

            st.success("Dataset uploaded successfully ✅")

            st.subheader("Preview")

            st.dataframe(df.head())

            col1, col2 = st.columns(2)

            with col1:
                st.metric("Rows", df.shape[0])

            with col2:
                st.metric("Columns", df.shape[1])

            st.subheader("Column Data Types")

            st.dataframe(df.dtypes.astype(str))

        else:
            st.error("Unable to read file.")

# -----------------------------
# Data Cleaning
# -----------------------------
elif option == "Data Cleaning":

    st.header("🧹 Data Cleaning")

    if st.session_state.df is None:

        st.warning("Please upload a dataset first.")

    else:

        df = st.session_state.df

        st.subheader("Missing Values")

        missing = get_missing_values(df)

        st.dataframe(missing)

        duplicate_count = get_duplicate_count(df)

        st.metric(
            "Duplicate Rows",
            duplicate_count
        )

        st.divider()

        if st.button("Remove Duplicates"):

            df = remove_duplicates(df)

            st.session_state.df = df

            st.success("Duplicate rows removed.")

        if st.button("Fill Missing Values"):

            df = fill_missing_values(df)

            st.session_state.df = df

            st.success("Missing values filled.")

        st.subheader("Cleaned Dataset")

        st.dataframe(st.session_state.df.head())

        csv = st.session_state.df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="⬇ Download Cleaned Dataset",
            data=csv,
            file_name="cleaned_dataset.csv",
            mime="text/csv"
        )

elif option == "EDA":

    st.header("📊 Exploratory Data Analysis")

    if st.session_state.df is None:

        st.warning("Please upload a dataset first.")

    else:

        df = st.session_state.df

        # -----------------------
        # Dataset Summary
        # -----------------------

        st.subheader("📋 Dataset Summary")

        summary = dataset_summary(df)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Rows", summary["Rows"])
            st.metric("Missing Values", summary["Missing Values"])

        with col2:
            st.metric("Columns", summary["Columns"])
            st.metric("Duplicate Rows", summary["Duplicate Rows"])

        with col3:
            st.metric("Memory (KB)", summary["Memory Usage (KB)"])

        st.divider()

        # -----------------------
        # Numerical Statistics
        # -----------------------

        st.subheader("📈 Numerical Statistics")

        st.dataframe(numerical_summary(df))

        st.divider()

        # -----------------------
        # Missing Values
        # -----------------------

        st.subheader("🚨 Missing Values")

        st.dataframe(missing_values(df))

        st.divider()

        # -----------------------
        # Data Types
        # -----------------------

        st.subheader("🏷 Data Types")

        st.dataframe(data_types(df))
# -----------------------------
# Dashboard
# -----------------------------
elif option == "Dashboard":

    st.header("📊 Dashboard")
    st.info("Coming Soon...")

# -----------------------------
# AI Insights
# -----------------------------
elif option == "AI Insights":

    st.header("🤖 AI Insights")
    st.info("Coming Soon...")

# -----------------------------
# Footer
# -----------------------------
st.divider()

st.caption(
    "InsightIQ | Built using Python, Streamlit & Data Analytics"
)