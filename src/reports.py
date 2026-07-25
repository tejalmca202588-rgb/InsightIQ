from datetime import datetime
import pandas as pd


def generate_report(df):

    report = {}

    report["Generated On"] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    report["Total Rows"] = df.shape[0]

    report["Total Columns"] = df.shape[1]

    report["Missing Values"] = int(df.isnull().sum().sum())

    report["Duplicate Rows"] = int(df.duplicated().sum())

    report["Numeric Columns"] = len(
        df.select_dtypes(include="number").columns
    )

    report["Categorical Columns"] = len(
        df.select_dtypes(exclude="number").columns
    )

    report_df = pd.DataFrame(
        report.items(),
        columns=["Metric", "Value"]
    )

    return report_df