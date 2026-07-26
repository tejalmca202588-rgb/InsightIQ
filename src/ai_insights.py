import pandas as pd


def generate_insights(df):
    """
    Generate AI-powered business insights from the dataset.
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
        lowest_mean = df[numeric_cols].mean().idxmin()

        insights.append(f"📈 '{highest_mean}' has the highest average value.")
        insights.append(f"📉 '{lowest_mean}' has the lowest average value.")

    # Recommendation
    insights.append(
        "💡 Recommendation: Review columns with unusually high values and investigate trends using the dashboard."
    )

    # -----------------------------
    # Categorical columns
    # -----------------------------
    categorical_cols = df.select_dtypes(include="object").columns

    for col in categorical_cols:
        if df[col].nunique() > 0:
            top_value = df[col].mode()[0]
            insights.append(
                f"🏆 Most common value in '{col}' is '{top_value}'."
            )

    # -----------------------------
    # Numeric summary
    # -----------------------------
    for col in numeric_cols:
        insights.append(
            f"📊 {col}: Mean={df[col].mean():.2f}, Max={df[col].max():.2f}, Min={df[col].min():.2f}"
        )

    # -----------------------------
    # Outlier Detection
    # -----------------------------
    for col in numeric_cols:

        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        outliers = df[(df[col] < lower) | (df[col] > upper)]

        if len(outliers) > 0:
            insights.append(
                f"⚠ {len(outliers)} outliers detected in '{col}'."
            )

    # -----------------------------
    # Correlation Analysis
    # -----------------------------
    if len(numeric_cols) >= 2:

        corr = df[numeric_cols].corr()

        max_corr = 0
        pair = None

        for i in range(len(corr.columns)):
            for j in range(i + 1, len(corr.columns)):

                value = abs(corr.iloc[i, j])

                if value > max_corr:
                    max_corr = value
                    pair = (
                        corr.columns[i],
                        corr.columns[j]
                    )

        if pair:
            insights.append(
                f"🔗 Strongest correlation is between '{pair[0]}' and '{pair[1]}' ({max_corr:.2f})."
            )

    # -----------------------------
    # AI Recommendations
    # -----------------------------
    insights.append("")
    insights.append("📌 AI Recommendations")

    if missing > 0:
        insights.append(
            "• Clean missing values before performing predictive analysis."
        )

    if duplicates > 0:
        insights.append(
            "• Remove duplicate records to improve data quality."
        )

    if len(numeric_cols) > 0:
        insights.append(
            "• Investigate columns with unusually high averages."
        )

    insights.append(
        "• Use the Dashboard module to explore trends interactively."
    )

    return insights