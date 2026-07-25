import pandas as pd


def apply_filters(df):

    filtered_df = df.copy()

    categorical_columns = filtered_df.select_dtypes(
        exclude="number"
    ).columns.tolist()

    for column in categorical_columns:

        options = sorted(filtered_df[column].dropna().unique())

        selected = []

        import streamlit as st

        selected = st.sidebar.multiselect(
            f"Filter {column}",
            options
        )

        if selected:
            filtered_df = filtered_df[
                filtered_df[column].isin(selected)
            ]

    return filtered_df