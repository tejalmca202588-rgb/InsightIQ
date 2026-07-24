import pandas as pd


def dataset_summary(df):
    """
    Returns basic dataset information.
    """

    summary = {
        "Rows": df.shape[0],
        "Columns": df.shape[1],
        "Missing Values": int(df.isnull().sum().sum()),
        "Duplicate Rows": int(df.duplicated().sum()),
        "Memory Usage (KB)": round(df.memory_usage(deep=True).sum() / 1024, 2)
    }

    return summary


def numerical_summary(df):
    """
    Returns summary statistics for numeric columns.
    """

    return df.describe()


def missing_values(df):
    """
    Returns missing values per column.
    """

    return df.isnull().sum()


def data_types(df):
    """
    Returns data types of all columns.
    """

    return df.dtypes.astype(str)