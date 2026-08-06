def create_analysis_plan(question):

    question = question.lower()

    plan = []
    code = ""

    # Distribution

    if "distribution" in question:

        plan = [
            "Identify numerical column from the request",
            "Analyze value distribution",
            "Generate histogram visualization"
        ]

        code = """
# Distribution Analysis

fig = px.histogram(
    df,
    x="amount",
    title="Amount Distribution"
)
"""


    # Comparison

    elif "compare" in question and "channel" in question:

        plan = [
            "Identify category column: channel",
            "Aggregate amount values",
            "Create comparison chart"
        ]

        code = """
# Category Comparison

summary = (
    df.groupby("channel")["amount"]
    .sum()
    .reset_index()
)

fig = px.bar(
    summary,
    x="channel",
    y="amount"
)
"""


    # Relationship

    elif (
        "relationship" in question
        or "correlation" in question
    ):

        plan = [
            "Select numerical variables",
            "Calculate relationship",
            "Generate scatter visualization"
        ]

        code = """
# Relationship Analysis

fig = px.scatter(
    df,
    x="fee_amount",
    y="tax_amount"
)
"""


    else:

        plan = [
            "Understand user question",
            "Analyze dataset columns",
            "Generate suitable output"
        ]

        code = "# No code generated"


    return {
        "plan": plan,
        "code": code
    }