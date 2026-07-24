import plotly.express as px


def create_bar_chart(df, x_col, y_col):
    """
    Creates an interactive bar chart.
    """
    fig = px.bar(
        df,
        x=x_col,
        y=y_col,
        title=f"{y_col} by {x_col}",
    )
    return fig


def create_line_chart(df, x_col, y_col):
    """
    Creates an interactive line chart.
    """
    fig = px.line(
        df,
        x=x_col,
        y=y_col,
        title=f"{y_col} over {x_col}",
    )
    return fig


def create_scatter_chart(df, x_col, y_col):
    """
    Creates an interactive scatter plot.
    """
    fig = px.scatter(
        df,
        x=x_col,
        y=y_col,
        title=f"{x_col} vs {y_col}",
    )
    return fig


def create_histogram(df, column):
    """
    Creates a histogram.
    """
    fig = px.histogram(
        df,
        x=column,
        title=f"Distribution of {column}",
    )
    return fig


def create_box_plot(df, column):
    """
    Creates a box plot.
    """
    fig = px.box(
        df,
        y=column,
        title=f"Box Plot of {column}",
    )
    return fig


def create_pie_chart(df, column):
    """
    Creates a pie chart.
    """
    counts = df[column].value_counts().reset_index()
    counts.columns = [column, "Count"]

    fig = px.pie(
        counts,
        names=column,
        values="Count",
        title=f"{column} Distribution",
    )
    return fig