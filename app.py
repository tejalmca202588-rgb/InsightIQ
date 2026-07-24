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
from src.charts import (
    create_bar_chart,
    create_line_chart,
    create_scatter_chart,
    create_histogram,
    create_box_plot,
    create_pie_chart,
)
from src.ai_insights import generate_insights

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

    st.header("📊 Interactive Dashboard")

    if st.session_state.df is None:

        st.warning("Please upload a dataset first.")

    else:

        df = st.session_state.df

        numeric_columns = df.select_dtypes(include=["number"]).columns.tolist()
        categorical_columns = df.select_dtypes(exclude=["number"]).columns.tolist()

        st.subheader("📌 Dashboard Summary")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Rows", df.shape[0])

        with col2:
            st.metric("Columns", df.shape[1])

        with col3:
            st.metric("Numeric Columns", len(numeric_columns))

        with col4:
            st.metric("Categorical Columns", len(categorical_columns))

        st.divider()

        chart_type = st.selectbox(
            "Select Chart",
            [
                "Bar Chart",
                "Line Chart",
                "Scatter Plot",
                "Histogram",
                "Box Plot",
                "Pie Chart",
            ]
        )

        if chart_type in ["Bar Chart", "Line Chart", "Scatter Plot"]:

            if len(numeric_columns) == 0:
                st.warning("No numeric columns available.")
            else:

                x_col = st.selectbox("Select X-axis", df.columns)

                y_col = st.selectbox("Select Y-axis", numeric_columns)

                if chart_type == "Bar Chart":
                    fig = create_bar_chart(df, x_col, y_col)

                elif chart_type == "Line Chart":
                    fig = create_line_chart(df, x_col, y_col)

                else:
                    fig = create_scatter_chart(df, x_col, y_col)

                st.plotly_chart(fig, use_container_width=True)

        elif chart_type in ["Histogram", "Box Plot"]:

            if len(numeric_columns) == 0:
                st.warning("No numeric columns available.")
            else:

                column = st.selectbox(
                    "Select Numeric Column",
                    numeric_columns
                )

                if chart_type == "Histogram":
                    fig = create_histogram(df, column)

                else:
                    fig = create_box_plot(df, column)

                st.plotly_chart(fig, use_container_width=True)

        elif chart_type == "Pie Chart":

            if len(categorical_columns) == 0:
                st.warning("No categorical columns available.")
            else:

                column = st.selectbox(
                    "Select Category",
                    categorical_columns
                )

                fig = create_pie_chart(df, column)

                st.plotly_chart(fig, use_container_width=True)
# -----------------------------
# AI Insights
# -----------------------------
elif option == "AI Insights":

    st.header("🤖 AI Business Insights")

    if st.session_state.df is None:

        st.warning("Please upload a dataset first.")

    else:

        df = st.session_state.df

        insights = generate_insights(df)

        st.subheader("Generated Insights")

        for insight in insights:
            st.success(insight)
# -----------------------------
# Footer
# -----------------------------
st.divider()

st.caption(
    "InsightIQ | Built using Python, Streamlit & Data Analytics"
)