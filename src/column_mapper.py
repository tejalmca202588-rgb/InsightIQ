import re


def normalize_text(text):
    """
    Convert text into a simple normalized format.
    """

    text = text.lower().strip()

    text = re.sub(r"[_\-]+", " ", text)

    text = re.sub(r"\s+", " ", text)

    return text


def find_column(df, aliases):
    """
    Find the best matching dataset column using aliases.
    """

    columns = list(df.columns)

    normalized_columns = {
        normalize_text(col): col
        for col in columns
    }

    # Exact alias match
    for alias in aliases:

        alias = normalize_text(alias)

        if alias in normalized_columns:
            return normalized_columns[alias]

    # Partial match
    for alias in aliases:

        alias = normalize_text(alias)

        for normalized, original in normalized_columns.items():

            if alias in normalized or normalized in alias:
                return original

    return None


def detect_columns(df, question):
    """
    Detect important business columns from a natural-language question.
    """

    question = normalize_text(question)

    detected = {}

    # -------------------------
    # Amount / Revenue
    # -------------------------

    amount_aliases = [
        "amount",
        "revenue",
        "sales",
        "transaction amount",
        "transaction value",
        "value",
        "income",
        "total amount"
    ]

    amount_column = find_column(
        df,
        amount_aliases
    )

    if amount_column:
        detected["amount"] = amount_column


    # -------------------------
    # Channel / Payment Mode
    # -------------------------

    channel_aliases = [
        "channel",
        "payment mode",
        "payment method",
        "payment type",
        "mode",
        "method"
    ]

    channel_column = find_column(
        df,
        channel_aliases
    )

    if channel_column:
        detected["channel"] = channel_column


    # -------------------------
    # Fraud
    # -------------------------

    fraud_aliases = [
        "fraud",
        "fraud status",
        "is fraud",
        "fraudulent"
    ]

    fraud_column = find_column(
        df,
        fraud_aliases
    )

    if fraud_column:
        detected["fraud"] = fraud_column


    # -------------------------
    # Risk
    # -------------------------

    risk_aliases = [
        "risk",
        "risk score",
        "risk level",
        "risk rating"
    ]

    risk_column = find_column(
        df,
        risk_aliases
    )

    if risk_column:
        detected["risk"] = risk_column


    # -------------------------
    # Date
    # -------------------------

    date_aliases = [
        "date",
        "transaction date",
        "order date",
        "purchase date",
        "time",
        "timestamp"
    ]

    date_column = find_column(
        df,
        date_aliases
    )

    if date_column:
        detected["date"] = date_column


    # -------------------------
    # Customer
    # -------------------------

    customer_aliases = [
        "customer",
        "customer id",
        "client",
        "client id"
    ]

    customer_column = find_column(
        df,
        customer_aliases
    )

    if customer_column:
        detected["customer"] = customer_column


    # -------------------------
    # Category
    # -------------------------

    category_aliases = [
        "category",
        "merchant category",
        "product category",
        "type"
    ]

    category_column = find_column(
        df,
        category_aliases
    )

    if category_column:
        detected["category"] = category_column


    return detected