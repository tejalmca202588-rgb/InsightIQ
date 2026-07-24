import streamlit as st

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

# Sidebar
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

# Home Page
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

# Footer
st.divider()

st.caption(
    "InsightIQ | Built using Python, Streamlit & Data Analytics"
)