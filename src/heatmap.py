import plotly.express as px


def create_correlation_heatmap(df):

    numeric_df = df.select_dtypes(include="number")

    if numeric_df.shape[1] < 2:
        return None

    corr = numeric_df.corr()

    fig = px.imshow(
        corr,
        text_auto=".2f",
        color_continuous_scale="RdBu_r",
        title="Correlation Heatmap"
    )

    fig.update_layout(
        height=650
    )

    return fig