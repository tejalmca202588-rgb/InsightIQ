import pandas as pd


def get_missing_values(df):
    """
    Returns the count of missing values in each column.
    """
    return df.isnull().sum()


def get_duplicate_count(df):
    """
    Returns the number of duplicate rows.
    """
    return df.duplicated().sum()


def remove_duplicates(df):
    """
    Removes duplicate rows.
    """
    return df.drop_duplicates()


def fill_missing_values(df):
    """
    Fill missing values:
    - Numeric columns -> Median
    - Text columns -> 'Unknown'
    """

    cleaned_df = df.copy()

    for column in cleaned_df.columns:

        if cleaned_df[column].dtype in ["int64", "float64"]:

            cleaned_df[column] = cleaned_df[column].fillna(
                cleaned_df[column].median()
            )

        else:

            cleaned_df[column] = cleaned_df[column].fillna("Unknown")

    return cleaned_df