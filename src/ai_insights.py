import pandas as pd
import numpy as np


def generate_insights(df):
    """
    Generate clean business insights from dataset.
    """

    insights = []

    rows, columns = df.shape

    # Dataset Overview
    insights.append(
        f"📊 Dataset contains **{rows:,} rows** and **{columns} columns**."
    )


    # Missing Values
    missing = df.isnull().sum().sum()

    if missing == 0:
        insights.append(
            "✅ No missing values found."
        )
    else:
        insights.append(
            f"⚠ {missing:,} missing values detected. "
            "Consider cleaning before analysis."
        )


    # Duplicate Rows
    duplicates = df.duplicated().sum()

    if duplicates == 0:
        insights.append(
            "✅ No duplicate records found."
        )
    else:
        insights.append(
            f"⚠ {duplicates:,} duplicate records detected."
        )


    # Numeric Analysis
    numeric_cols = df.select_dtypes(
        include=np.number
    ).columns


    if len(numeric_cols) > 0:

        means = df[numeric_cols].mean()

        highest = means.idxmax()
        lowest = means.idxmin()


        insights.append(
            f"📈 **{highest}** has the highest average value "
            f"({means[highest]:,.2f})."
        )


        insights.append(
            f"📉 **{lowest}** has the lowest average value "
            f"({means[lowest]:,.2f})."
        )


    # Outlier Detection

    outlier_found = False

    for col in numeric_cols:

        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)

        IQR = Q3 - Q1

        outliers = df[
            (df[col] < Q1 - 1.5 * IQR)
            |
            (df[col] > Q3 + 1.5 * IQR)
        ]


        if len(outliers) > 0:

            insights.append(
                f"⚠ **{len(outliers):,} unusual values detected in {col}.**"
            )

            outlier_found = True

            break


    if not outlier_found:

        insights.append(
            "✅ No significant outliers detected."
        )


    # Correlation

    if len(numeric_cols) > 1:

        corr = df[numeric_cols].corr()

        corr_pairs = (
            corr
            .where(
                np.triu(
                    np.ones(corr.shape),
                    k=1
                ).astype(bool)
            )
            .stack()
        )


        if not corr_pairs.empty:

            pair = corr_pairs.idxmax()

            value = corr_pairs.max()


            insights.append(
                f"🔗 Strong relationship found between "
                f"**{pair[0]}** and **{pair[1]}** "
                f"(correlation: {value:.2f})."
            )


    # Recommendations

    insights.append(
        """
💡 **AI Recommendations**

• Clean missing values before advanced analysis.

• Remove duplicate records to improve accuracy.

• Investigate unusual values and outliers.

• Explore trends using interactive dashboards.
"""
    )


    return insights