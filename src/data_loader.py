import pandas as pd


def load_data(uploaded_file):
    """
    Load CSV or Excel file into a Pandas DataFrame.
    """

    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)

        elif uploaded_file.name.endswith((".xlsx", ".xls")):
            df = pd.read_excel(uploaded_file)

        else:
            return None

        return df

    except Exception as e:
        print("Error loading file:", e)
        return None