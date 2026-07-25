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
from src.business_metrics import get_business_metrics
from src.filters import apply_filters

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="InsightIQ",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# -----------------------------
# Session State
# -----------------------------
if "df" not in st.session_state:
    st.session_state.df = None


# -----------------------------
# Sidebar
# -----------------------------

st.sidebar.title("📊 InsightIQ")

st.sidebar.markdown(
    """
    ---
    **AI-Powered Business Intelligence Platform**

    Transform your data into insights.
    ---
    """
)


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

    st.title("📊 InsightIQ")
    st.subheader("AI-Powered Business Intelligence Platform")

    st.write(
        """
        InsightIQ transforms raw business data into meaningful insights
        using data analysis, visualization, and intelligent recommendations.
        """
    )


    st.header("🏠 Welcome to InsightIQ 🚀")


    st.write(
        """
        ### AI-Powered Business Intelligence Platform

        InsightIQ transforms raw business data into meaningful insights
        using data cleaning, exploratory analysis, interactive visualization,
        and intelligent recommendations.
        """
    )


    st.subheader("✨ Current Features")


    col1, col2, col3 = st.columns(3)


    with col1:

        st.success(
            """
            📂 Data Upload

            ✔ CSV Support
            ✔ Excel Support
            ✔ Dataset Preview
            """
        )


    with col2:

        st.success(
            """
            🧹 Data Cleaning

            ✔ Missing Values
            ✔ Duplicate Detection
            ✔ Clean Dataset Download
            """
        )


    with col3:

        st.success(
            """
            📊 Analytics

            ✔ EDA
            ✔ Dashboard
            ✔ AI Insights
            """
        )


    st.divider()


    st.info(
        """
        🚀 Upload your dataset and let InsightIQ help you discover
        patterns, trends, and actionable business insights.
        """
    )



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

        st.dataframe(get_missing_values(df))


        duplicate_count = get_duplicate_count(df)


        st.metric(
            "Duplicate Rows",
            duplicate_count
        )


        if st.button("Remove Duplicates"):

            st.session_state.df = remove_duplicates(df)

            st.success("Duplicates removed")


        if st.button("Fill Missing Values"):

            st.session_state.df = fill_missing_values(df)

            st.success("Missing values filled")


        st.subheader("Cleaned Dataset")

        st.dataframe(st.session_state.df.head())



# -----------------------------
# EDA
# -----------------------------

elif option == "EDA":

    st.header("📊 Exploratory Data Analysis")


    if st.session_state.df is None:

        st.warning("Please upload a dataset first.")


    else:

        df = st.session_state.df


        st.subheader("📋 Dataset Summary")

        st.dataframe(dataset_summary(df))


        st.subheader("📈 Statistics")

        st.dataframe(numerical_summary(df))


        st.subheader("🚨 Missing Values")

        st.dataframe(missing_values(df))


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

        df = apply_filters(st.session_state.df)
        # -----------------------------
        # Business Metrics
        # -----------------------------

        st.subheader("📈 Business Metrics")

        metrics = get_business_metrics(df)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("📦 Total Records", metrics["Total Records"])
            st.metric("📊 Total Columns", metrics["Total Columns"])

        with col2:
            if "Numeric Column" in metrics:
                st.metric(
                    f"💰 Total ({metrics['Numeric Column']})",
                    metrics["Total"]
                )
                st.metric(
                    f"📈 Average ({metrics['Numeric Column']})",
                    metrics["Average"]
                )

        with col3:
            if "Numeric Column" in metrics:
                st.metric(
                    f"🔺 Maximum ({metrics['Numeric Column']})",
                    metrics["Maximum"]
                )
                st.metric(
                    f"🔻 Minimum ({metrics['Numeric Column']})",
                    metrics["Minimum"]
                )

        st.divider()

        # -----------------------------
        # Charts
        # -----------------------------

        numeric_columns = df.select_dtypes(include="number").columns.tolist()
        categorical_columns = df.select_dtypes(exclude="number").columns.tolist()

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

        insights = generate_insights(
            st.session_state.df
        )


        for insight in insights:

            st.success(insight)



# -----------------------------
# Footer
# -----------------------------

st.divider()

st.caption(
    "InsightIQ | Built using Python, Streamlit & Data Analytics"
)