import pandas as pd


def get_data_quality(df):
    """
    Calculate dataset quality score and statistics.
    """

    total_cells = df.shape[0] * df.shape[1]

    missing = df.isnull().sum().sum()

    duplicates = df.duplicated().sum()

    completeness = (
        ((total_cells - missing) / total_cells) * 100
        if total_cells > 0 else 0
    )

    duplicate_score = (
        ((len(df) - duplicates) / len(df)) * 100
        if len(df) > 0 else 0
    )

    health_score = round((completeness + duplicate_score) / 2, 2)

    return {
        "Health Score": health_score,
        "Completeness": round(completeness, 2),
        "Missing Values": int(missing),
        "Duplicate Rows": int(duplicates)
    }