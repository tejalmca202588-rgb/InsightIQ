import pandas as pd


def ask_dataset(df, question):

    question = question.lower()

    # Total rows
    if "row" in question or "record" in question:
        return f"The dataset contains {df.shape[0]} records."

    # Total columns
    elif "column" in question:
        return f"The dataset contains {df.shape[1]} columns."

    # Missing values
    elif "missing" in question:
        return f"There are {df.isnull().sum().sum()} missing values."

    # Column names
    elif "column names" in question or "columns" in question:
        return ", ".join(df.columns)

    # Numeric column statistics
    for col in df.select_dtypes(include="number").columns:

        if col.lower() in question:

            if "average" in question or "mean" in question:
                return f"Average {col}: {df[col].mean():,.2f}"

            elif "maximum" in question or "max" in question:
                return f"Maximum {col}: {df[col].max():,.2f}"

            elif "minimum" in question or "min" in question:
                return f"Minimum {col}: {df[col].min():,.2f}"

            elif "sum" in question or "total" in question:
                return f"Total {col}: {df[col].sum():,.2f}"

    return (
        "Sorry, I couldn't understand that question.\n\n"
        "Try asking:\n"
        "- How many rows?\n"
        "- How many columns?\n"
        "- Missing values\n"
        "- Average Sales\n"
        "- Maximum Profit"
    )