import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

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
from src.heatmap import create_correlation_heatmap
from src.reports import generate_report
from src.pdf_report import generate_pdf
from src.chatbot import ask_dataset
from src.data_quality import get_data_quality

# =============================================================
# Cached wrappers
# =============================================================
# These wrap pure, side-effect-free functions (no widgets created
# inside them) so Streamlit skips recomputation on every rerun as
# long as the input dataframe hasn't changed. apply_filters() is
# NOT cached here because it creates its own widgets and must run
# on every rerun to stay in sync with user input.

@st.cache_data(show_spinner=False)
def cached_dataset_summary(df):
    return dataset_summary(df)

@st.cache_data(show_spinner=False)
def cached_numerical_summary(df):
    return numerical_summary(df)

@st.cache_data(show_spinner=False)
def cached_missing_values(df):
    return missing_values(df)

@st.cache_data(show_spinner=False)
def cached_data_types(df):
    return data_types(df)

@st.cache_data(show_spinner=False)
def cached_business_metrics(df):
    return get_business_metrics(df)

@st.cache_data(show_spinner=False)
def cached_correlation_heatmap(df):
    return create_correlation_heatmap(df)

@st.cache_data(show_spinner=False)
def cached_generate_report(df):
    return generate_report(df)

@st.cache_data(show_spinner=False)
def cached_generate_insights(df):
    return generate_insights(df)


# =============================================================
# Page Configuration (must be the very first Streamlit call)
# =============================================================
st.set_page_config(
    page_title="InsightIQ",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================
# Global CSS — professional theme
# =============================================================
st.markdown("""
<style>

.main {
    background-color: #f8f9fc;
}

/* ---------- KPI Cards ---------- */
.kpi-card {
    background: white;
    padding: 22px 18px;
    border-radius: 16px;
    box-shadow: 0px 4px 14px rgba(0,0,0,0.06);
    text-align: center;
    border: 1px solid #eef0f6;
    transition: transform 0.15s ease, box-shadow 0.15s ease;
}

.kpi-card:hover {
    transform: translateY(-3px);
    box-shadow: 0px 8px 20px rgba(0,0,0,0.10);
}

.kpi-icon {
    font-size: 26px;
    margin-bottom: 6px;
}

.kpi-title {
    color: #6b7280;
    font-size: 14px;
    font-weight: 600;
    letter-spacing: 0.3px;
    text-transform: uppercase;
    margin-bottom: 6px;
}

.kpi-value {
    font-size: 30px;
    color: #1f2937;
    font-weight: 700;
}

/* ---------- Section headers ---------- */
.section-header {
    font-size: 22px;
    font-weight: 700;
    color: #1f2937;
    margin: 10px 0 14px 0;
    padding-left: 10px;
    border-left: 5px solid #4F46E5;
}

/* ---------- Hero banner ---------- */
.hero-banner {
    background: linear-gradient(90deg, #4F46E5, #06B6D4);
    padding: 28px 30px;
    border-radius: 16px;
    color: white;
    margin-bottom: 22px;
}

.hero-banner h1 {
    margin: 0;
    font-size: 30px;
}

.hero-banner p {
    font-size: 16px;
    margin-top: 8px;
    opacity: 0.95;
}

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] {
    background-color: #111827;
}

section[data-testid="stSidebar"] * {
    color: #f3f4f6 !important;
}

/* Chart containers */
div[data-testid="stPlotlyChart"] {
    background: white;
    border-radius: 14px;
    padding: 10px;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.05);
}

</style>
""", unsafe_allow_html=True)

# =============================================================
# Session State
# =============================================================
if "df" not in st.session_state:
    st.session_state.df = None


# =============================================================
# KPI Cards Component
# =============================================================
def kpi_card(col, icon, title, value):
    with col:
        st.markdown(
            f"""
            <div class="kpi-card">
                <div class="kpi-icon">{icon}</div>
                <div class="kpi-title">{title}</div>
                <div class="kpi-value">{value}</div>
            </div>
            """,
            unsafe_allow_html=True
        )


def show_kpi_cards(df):
    total_rows = df.shape[0]
    total_columns = df.shape[1]
    missing_vals = df.isnull().sum().sum()

    numeric_columns = df.select_dtypes(include="number")
    avg_value = numeric_columns.mean().mean() if not numeric_columns.empty else 0

    col1, col2, col3, col4 = st.columns(4)

    kpi_card(col1, "📄", "Total Records", f"{total_rows:,}")
    kpi_card(col2, "📊", "Total Columns", f"{total_columns:,}")
    kpi_card(col3, "⚠️", "Missing Values", f"{missing_vals:,}")
    kpi_card(col4, "📈", "Average Value", f"{avg_value:.2f}")


def section_header(text):
    st.markdown(f'<div class="section-header">{text}</div>', unsafe_allow_html=True)


# =============================================================
# Sidebar Navigation
# =============================================================
st.sidebar.title("📊 InsightIQ")

st.sidebar.markdown(
    """
    ---
    **AI-Powered Business Intelligence Platform**

    Transform your data into insights.
    ---
    """
)

option = st.sidebar.radio(
    "Choose Module",
    [
        "🏠 Home",
        "📂 Data Upload",
        "🧹 Data Cleaning",
        "📊 EDA",
        "📈 Dashboard",
        "🤖 AI Insights",
        "💬 AI Chat",
        "📄 Reports",
    ]
)

# Remove emoji prefix only when emoji exists
if " " in option:
    option = option.split(" ", 1)[1]

# Debug (remove later)
st.write(option)

if st.session_state.df is not None:
    st.sidebar.markdown("---")
    st.sidebar.success(
        f"Loaded dataset: {st.session_state.df.shape[0]:,} rows × "
        f"{st.session_state.df.shape[1]:,} columns"
    )


# =============================================================
# Home
# =============================================================
if option == "Home":

    st.markdown(
        """
        <div class="hero-banner">
            <h1>📊 InsightIQ</h1>
            <p>AI-Powered Business Analytics Platform — Analyze • Visualize • Discover</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write(
        """
        ### AI-Powered Business Intelligence Platform

        InsightIQ transforms raw business data into meaningful insights
        using data cleaning, exploratory analysis, interactive visualization,
        and intelligent recommendations.
        """
    )

    section_header("✨ Current Features")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.success(
            """
            **📂 Data Upload**

            ✔ CSV Support
            ✔ Excel Support
            ✔ Dataset Preview
            """
        )

    with col2:
        st.success(
            """
            **🧹 Data Cleaning**

            ✔ Missing Values
            ✔ Duplicate Detection
            ✔ Clean Dataset Download
            """
        )

    with col3:
        st.success(
            """
            **📊 Analytics**

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


# =============================================================
# Data Upload
# =============================================================
elif option == "Data Upload":

    section_header("📂 Upload Dataset")

    uploaded_file = st.file_uploader(
        "Choose CSV or Excel File",
        type=["csv", "xlsx", "xls"]
    )

    if uploaded_file is not None:

        MAX_SIZE_MB = 200
        size_mb = uploaded_file.size / (1024 * 1024)

        if size_mb > MAX_SIZE_MB:
            st.error(
                f"File is {size_mb:.1f} MB, which exceeds the {MAX_SIZE_MB} MB "
                "limit. Try a smaller file or pre-filter it before uploading."
            )

        else:
            try:
                with st.spinner("Reading file..."):
                    df = load_data(uploaded_file)
            except Exception as e:
                df = None
                st.error(f"Could not read this file: {e}")

            if df is not None and not df.empty:
                st.session_state.df = df
                # Clear any cached/stale state from a previous dataset
                st.session_state.dashboard_loaded = False

                st.success("Dataset uploaded successfully ✅")

                st.subheader("Preview")
                st.dataframe(df.head(), use_container_width=True)

                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Rows", df.shape[0])
                with col2:
                    st.metric("Columns", df.shape[1])

            elif df is not None and df.empty:
                st.error("This file was read successfully but contains no rows.")

            else:
                st.error("Unable to read file. Please check the format and try again.")


# =============================================================
# Data Cleaning
# =============================================================
elif option == "Data Cleaning":

    section_header("🧹 Data Cleaning")

    if st.session_state.df is None:
        st.warning("Please upload a dataset first.")

    else:
        df = st.session_state.df

        try:
            st.subheader("Missing Values")
            st.dataframe(get_missing_values(df), use_container_width=True)

            duplicate_count = get_duplicate_count(df)
            st.metric("Duplicate Rows", duplicate_count)
        except Exception as e:
            st.error(f"Could not compute missing values / duplicates: {e}")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Remove Duplicates", use_container_width=True):
                try:
                    st.session_state.df = remove_duplicates(df)
                    st.success("Duplicates removed")
                except Exception as e:
                    st.error(f"Could not remove duplicates: {e}")

        with col2:
            if st.button("Fill Missing Values", use_container_width=True):
                try:
                    st.session_state.df = fill_missing_values(df)
                    st.success("Missing values filled")
                except Exception as e:
                    st.error(f"Could not fill missing values: {e}")

        st.subheader("Cleaned Dataset")
        st.dataframe(st.session_state.df.head(), use_container_width=True)


# =============================================================
# EDA
# =============================================================
elif option == "EDA":

    section_header("📊 Exploratory Data Analysis")

    if st.session_state.df is None:
        st.warning("Please upload a dataset first.")

    else:
        df = st.session_state.df

        st.subheader("📋 Dataset Summary")
        st.dataframe(cached_dataset_summary(df), use_container_width=True)

        st.subheader("📈 Statistics")
        st.dataframe(cached_numerical_summary(df), use_container_width=True)

        st.subheader("🚨 Missing Values")
        st.dataframe(cached_missing_values(df), use_container_width=True)

        st.subheader("🏷 Data Types")
        st.dataframe(cached_data_types(df), use_container_width=True)


# =============================================================
# Dashboard
# =============================================================
elif option == "Dashboard":

    st.markdown(
        """
        <div class="hero-banner">
            <h1>📊 InsightIQ Dashboard</h1>
            <p>Analyze • Visualize • Discover Business Insights with AI</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.session_state.df is None:
        st.warning("Please upload a dataset first.")

    else:
        raw_df = st.session_state.df

        st.caption(
            f"Loaded dataset: {raw_df.shape[0]:,} rows × {raw_df.shape[1]:,} columns"
        )

        # ---------------- Load gate ----------------
        # Nothing heavy runs until the user explicitly asks for it. This
        # stops the tab from freezing on arrival if apply_filters(), a
        # default chart, or the heatmap turns out to be expensive on a
        # large dataset / high-cardinality column.
        if "dashboard_loaded" not in st.session_state:
            st.session_state.dashboard_loaded = False

        if not st.session_state.dashboard_loaded:
            st.info(
                "Click below to build the dashboard. On very large datasets, "
                "the first render (filters, charts, correlation heatmap) can "
                "take a few seconds."
            )
            if st.button("🚀 Load Dashboard", type="primary"):
                st.session_state.dashboard_loaded = True
                st.rerun()
            st.stop()

        with st.spinner("Applying filters..."):
            df = apply_filters(raw_df)

        # ---------------- KPI Cards ----------------
        section_header("📌 Business Overview")
        show_kpi_cards(df)

        st.divider()

                # ---------------- Data Health ----------------

        section_header("🩺 Dataset Health")

        quality = get_data_quality(df)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "🏆 Health Score",
                f"{quality['Health Score']}%"
            )

        with col2:
            st.metric(
                "✅ Completeness",
                f"{quality['Completeness']}%"
            )

        with col3:
            st.metric(
                "⚠ Missing Values",
                quality["Missing Values"]
            )

        with col4:
            st.metric(
                "📄 Duplicate Rows",
                quality["Duplicate Rows"]
            )

        if quality["Health Score"] >= 90:
            st.success("🟢 Excellent Dataset Quality")

        elif quality["Health Score"] >= 70:
            st.warning("🟡 Good Dataset Quality")

        else:
            st.error("🔴 Poor Dataset Quality")

        st.divider()

        # ---------------- Business Metrics ----------------
        section_header("📈 Business Metrics")

        metrics = cached_business_metrics(df)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("📦 Total Records", metrics["Total Records"])
            st.metric("📊 Total Columns", metrics["Total Columns"])

        with col2:
            if "Numeric Column" in metrics:
                st.metric(f"💰 Total ({metrics['Numeric Column']})", metrics["Total"])
                st.metric(f"📈 Average ({metrics['Numeric Column']})", metrics["Average"])

        with col3:
            if "Numeric Column" in metrics:
                st.metric(f"🔺 Maximum ({metrics['Numeric Column']})", metrics["Maximum"])
                st.metric(f"🔻 Minimum ({metrics['Numeric Column']})", metrics["Minimum"])

        st.divider()

        # ---------------- Charts ----------------
        section_header("📊 Interactive Visualizations")

        # Cap which columns are even offered as chart axes. A column with
        # thousands of unique values (an ID, a name, free text) will make
        # Plotly try to draw thousands of bars/slices and freeze the tab —
        # so those columns are excluded from the dropdowns entirely.
        MAX_UNIQUE_FOR_BAR_X = 50
        MAX_UNIQUE_FOR_PIE = 30
        MAX_NUMERIC_FOR_HEATMAP = 30

        numeric_columns = df.select_dtypes(include="number").columns.tolist()
        categorical_columns = df.select_dtypes(exclude="number").columns.tolist()

        nunique_counts = df.nunique()

        safe_bar_x_columns = [
            c for c in df.columns if nunique_counts.get(c, 0) <= MAX_UNIQUE_FOR_BAR_X
        ]
        safe_pie_columns = [
            c for c in categorical_columns
            if nunique_counts.get(c, 0) <= MAX_UNIQUE_FOR_PIE
        ]

        left, right = st.columns(2)

        # ---- Bar Chart ----
        with left:
            st.subheader("📊 Bar Chart")
            if len(numeric_columns) > 0 and len(safe_bar_x_columns) > 0:
                x = st.selectbox("Bar X-axis", safe_bar_x_columns, key="bar_x")
                y = st.selectbox("Bar Y-axis", numeric_columns, key="bar_y")
                fig = create_bar_chart(df, x, y)
                st.plotly_chart(fig, use_container_width=True)
            elif len(numeric_columns) == 0:
                st.info("No numeric columns available for a bar chart.")
            else:
                st.info(
                    "Every column has too many unique values to plot as a "
                    "bar chart (an ID or free-text column, for example)."
                )

        # ---- Pie Chart ----
        with right:
            st.subheader("🥧 Pie Chart")
            if len(safe_pie_columns) > 0:
                category = st.selectbox("Category", safe_pie_columns, key="pie")
                fig = create_pie_chart(df, category)
                st.plotly_chart(fig, use_container_width=True)
            elif len(categorical_columns) == 0:
                st.info("No categorical columns available for a pie chart.")
            else:
                st.info(
                    f"No categorical column has {MAX_UNIQUE_FOR_PIE} or fewer "
                    "unique values, so a readable pie chart isn't possible."
                )

        left2, right2 = st.columns(2)

        # ---- Line Chart ----
        with left2:
            st.subheader("📈 Line Chart")
            if len(numeric_columns) > 0:
                x = st.selectbox("Line X-axis", safe_bar_x_columns or df.columns, key="line_x")
                y = st.selectbox("Line Y-axis", numeric_columns, key="line_y")
                fig = create_line_chart(df, x, y)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No numeric columns available for a line chart.")

        # ---- Histogram ----
        with right2:
            st.subheader("📦 Histogram")
            if len(numeric_columns) > 0:
                column = st.selectbox("Histogram Column", numeric_columns, key="hist")
                fig = create_histogram(df, column)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No numeric columns available for a histogram.")

        st.divider()

        # ---------------- Correlation Heatmap ----------------
        section_header("🔥 Correlation Heatmap")

        if len(numeric_columns) > MAX_NUMERIC_FOR_HEATMAP:
            st.warning(
                f"This dataset has {len(numeric_columns)} numeric columns. "
                f"Showing a heatmap for the first {MAX_NUMERIC_FOR_HEATMAP} "
                "to avoid freezing the browser."
            )
            heatmap_fig = cached_correlation_heatmap(
                df[numeric_columns[:MAX_NUMERIC_FOR_HEATMAP]]
            )
        else:
            heatmap_fig = cached_correlation_heatmap(df)

        if heatmap_fig is not None:
            st.plotly_chart(heatmap_fig, use_container_width=True)
        else:
            st.info(
                "At least two numeric columns are required to generate a correlation heatmap."
            )

        st.divider()
        if st.button("🔄 Reset Dashboard"):
            st.session_state.dashboard_loaded = False
            st.rerun()


# =============================================================
# AI chat
# =============================================================
# =============================================================
# =============================================================
# AI Chat
# =============================================================

elif option == "AI Chat":

    section_header("💬 AI Chat Assistant")


    if st.session_state.df is None:

        st.warning("Please upload a dataset first.")


    else:

        df = st.session_state.df


        st.write(
            "Ask questions about your dataset like a business analyst."
        )


        # Initialize chat history

        if "chat_history" not in st.session_state:

            st.session_state.chat_history = []



        # Suggested Questions

        st.markdown("### 💡 Try asking:")


        col1, col2, col3 = st.columns(3)


        with col1:

            if st.button(
                "📊 Dataset Summary",
                key="summary_btn"
            ):

                user_question = "summary"



        with col2:

            if st.button(
                "❓ Missing Values",
                key="missing_btn"
            ):

                user_question = "missing values"



        with col3:

            if st.button(
                "🔢 Numeric Columns",
                key="numeric_btn"
            ):

                user_question = "numeric columns"



        # User Input

        user_input = st.text_input(

            "Ask your question",

            placeholder="Example: Give me insights about this dataset",

            key="chat_input"

        )



        ask = st.button(
            "🚀 Ask InsightIQ",
            key="ask_button"
        )



        if ask:


            question = user_input.lower()



            if question.strip() == "":

                st.warning(
                    "Please enter a question."
                )



            else:


                # Rows

                if "row" in question:


                    answer = (

                        f"📌 Your dataset contains "

                        f"{df.shape[0]:,} rows."

                    )



                # Columns

                elif "column" in question:


                    answer = (

                        f"📌 Your dataset contains "

                        f"{df.shape[1]} columns."

                    )



                # Missing values

                elif "missing" in question:


                    answer = (

                        f"📌 Missing values found: "

                        f"{df.isnull().sum().sum()}"

                    )



                # Duplicate

                elif "duplicate" in question:


                    answer = (

                        f"📌 Duplicate rows found: "

                        f"{df.duplicated().sum()}"

                    )



                # Numeric columns

                elif "numeric" in question:


                    answer = (

                        "🔢 Numeric columns:\n\n"

                        +

                        ", ".join(

                            df.select_dtypes(

                                include="number"

                            ).columns

                        )

                    )



                # Categorical columns

                elif "categorical" in question:


                    answer = (

                        "📂 Categorical columns:\n\n"

                        +

                        ", ".join(

                            df.select_dtypes(

                                exclude="number"

                            ).columns

                        )

                    )



                # Summary

                elif "summary" in question:


                    answer = (

                        "📊 Dataset Summary\n\n"

                        f"Rows: {df.shape[0]:,}\n"

                        f"Columns: {df.shape[1]}\n"

                        f"Missing Values: {df.isnull().sum().sum()}\n"

                        f"Duplicate Rows: {df.duplicated().sum()}"

                    )



                # AI Insights Integration ⭐

                elif (

                    "insight" in question

                    or "recommendation" in question

                    or "analysis" in question

                ):


                    insights = generate_insights(df)


                    answer = (

                        "🤖 AI Generated Insights:\n\n"

                        +

                        "\n\n".join(insights)

                    )



                else:


                    answer = (

                        "🤖 I can help you with:\n\n"

                        "• Dataset summary\n"

                        "• Rows and columns\n"

                        "• Missing values\n"

                        "• Duplicate records\n"

                        "• Numeric columns\n"

                        "• Categorical columns\n"

                        "• Business insights\n"

                        "• Recommendations"

                    )



                # Store conversation

                st.session_state.chat_history.append(

                    {

                        "role": "user",

                        "message": user_input

                    }

                )



                st.session_state.chat_history.append(

                    {

                        "role": "assistant",

                        "message": answer

                    }

                )



        st.divider()



        # Display Chat History

        for chat in st.session_state.chat_history:


            if chat["role"] == "user":


                with st.chat_message("user"):

                    st.write(

                        chat["message"]

                    )


            else:


                with st.chat_message("assistant"):

                    st.write(

                        chat["message"]

                    )
                
# Reports
# =============================================================
elif option == "Reports":

    section_header("📄 Dataset Report")

    if st.session_state.df is None:
        st.warning("Please upload a dataset first.")

    else:
        df = st.session_state.df

        try:
            report_df = cached_generate_report(df)
        except Exception as e:
            report_df = None
            st.error(f"Could not generate the report: {e}")

        if report_df is not None:
            st.subheader("Generated Report")
            st.dataframe(report_df, use_container_width=True)

            # ---- CSV Report ----
            csv = report_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="⬇ Download CSV Report",
                data=csv,
                file_name="InsightIQ_Report.csv",
                mime="text/csv"
            )

            # ---- PDF Report ----
            import tempfile, os

            pdf_path = None
            try:
                with st.spinner("Generating PDF..."):
                    with tempfile.NamedTemporaryFile(
                        suffix=".pdf", delete=False
                    ) as tmp:
                        pdf_path = tmp.name
                    generate_pdf(report_df, pdf_path)

                    with open(pdf_path, "rb") as pdf_file:
                        pdf_bytes = pdf_file.read()

                st.download_button(
                    label="📄 Download PDF Report",
                    data=pdf_bytes,
                    file_name="InsightIQ_Report.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Could not generate the PDF report: {e}")
            finally:
                if pdf_path and os.path.exists(pdf_path):
                    os.remove(pdf_path)


# =============================================================
# AI Insights
# =============================================================
elif option == "AI Insights":

    section_header("🤖 AI Business Insights")

    if st.session_state.df is None:
        st.warning("Please upload a dataset first.")

    else:
        try:
            with st.spinner("Generating insights..."):
                insights = cached_generate_insights(st.session_state.df)
        except Exception as e:
            insights = None
            st.error(f"Could not generate insights: {e}")

        if insights is not None:
            if len(insights) == 0:
                st.info("No insights were generated for this dataset.")

            for insight in insights:
                if "Recommendation" in insight or "AI" in insight:
                    st.info(insight)
                elif "⚠" in insight:
                    st.warning(insight)
                elif "📈" in insight or "📊" in insight:
                    st.success(insight)
                else:
                    st.write(insight)


# =============================================================
# Footer
# =============================================================
st.divider()
st.caption("InsightIQ | Built using Python, Streamlit & Data Analytics")