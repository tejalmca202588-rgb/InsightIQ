import pandas as pd


def generate_insights(df):
    """
    Generate simple business insights from the dataset.
    """

    insights = []

    # Dataset size
    insights.append(
        f"📊 Dataset contains {df.shape[0]} rows and {df.shape[1]} columns."
    )

    # Missing values
    missing = df.isnull().sum().sum()

    if missing == 0:
        insights.append("✅ No missing values found.")
    else:
        insights.append(f"⚠ Dataset contains {missing} missing values.")

    # Duplicate rows
    duplicates = df.duplicated().sum()

    if duplicates == 0:
        insights.append("✅ No duplicate rows found.")
    else:
        insights.append(f"⚠ Dataset contains {duplicates} duplicate rows.")

    # Numeric columns
    numeric_cols = df.select_dtypes(include="number").columns

    if len(numeric_cols) > 0:

        highest_mean = df[numeric_cols].mean().idxmax()

        insights.append(
            f"📈 '{highest_mean}' has the highest average value."
        )

        lowest_mean = df[numeric_cols].mean().idxmin()

        insights.append(
            f"📉 '{lowest_mean}' has the lowest average value."
        )

    insights.append(
        "💡 Recommendation: Review columns with unusually high values and investigate trends using the dashboard."
    )

    return insights