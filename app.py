import streamlit as st
from src.data_loader import load_data


# Page Configuration
st.set_page_config(
    page_title="InsightIQ",
    page_icon="📊",
    layout="wide"
)


# Main Title
st.title("📊 InsightIQ")

st.subheader("AI-Powered Business Intelligence Platform")

st.write(
    """
    InsightIQ transforms raw business data into meaningful insights 
    using data analysis, visualization, and intelligent recommendations.
    """
)


# Sidebar Navigation
st.sidebar.title("Navigation")

option = st.sidebar.selectbox(
    "Choose Module",
    [
        "Home",
        "Data Upload",
        "Data Cleaning",
        "Dashboard",
        "AI Insights"
    ]
)


# Home Module
if option == "Home":

    st.header("Welcome to InsightIQ 🚀")

    st.info(
        """
        Upload your business data and let InsightIQ help you discover:

        • Sales trends  
        • Business performance  
        • Data patterns  
        • Actionable insights
        """
    )


# Data Upload Module
elif option == "Data Upload":

    st.header("📂 Upload Your Dataset")

    uploaded_file = st.file_uploader(
        "Choose a CSV or Excel file",
        type=["csv", "xlsx", "xls"]
    )

    if uploaded_file is not None:

        df = load_data(uploaded_file)

        if df is not None:

            st.success("File uploaded successfully! 🎉")

            st.subheader("Dataset Preview")

            st.dataframe(df.head())


            st.subheader("Dataset Information")

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Number of Rows",
                    df.shape[0]
                )

            with col2:
                st.metric(
                    "Number of Columns",
                    df.shape[1]
                )


            st.subheader("Column Information")

            st.write(df.dtypes)


        else:

            st.error("Unable to read this file.")


# Other Modules (Coming Soon)
elif option == "Data Cleaning":

    st.header("🧹 Data Cleaning Module")
    st.warning("Coming Soon...")


elif option == "Dashboard":

    st.header("📊 Analytics Dashboard")
    st.warning("Coming Soon...")


elif option == "AI Insights":

    st.header("🤖 AI Insights Generator")
    st.warning("Coming Soon...")


# Footer
st.divider()

st.caption(
    "InsightIQ | Built using Python, Streamlit & Data Analytics"
)