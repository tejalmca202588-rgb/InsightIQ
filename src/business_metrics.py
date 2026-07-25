import pandas as pd


def get_business_metrics(df):

    metrics = {
        "Total Records": len(df),
        "Total Columns": len(df.columns),
    }

    numeric_columns = df.select_dtypes(include="number").columns.tolist()

    if numeric_columns:
        first_numeric = numeric_columns[0]

        metrics["Numeric Column"] = first_numeric
        metrics["Total"] = round(df[first_numeric].sum(), 2)
        metrics["Average"] = round(df[first_numeric].mean(), 2)
        metrics["Maximum"] = round(df[first_numeric].max(), 2)
        metrics["Minimum"] = round(df[first_numeric].min(), 2)

    return metrics