import pandas as pd
import plotly.express as px

from src.analysis_planner import create_analysis_plan
from src.column_mapper import detect_columns


class AIAnalyst:

    def __init__(self, df):
        self.df = df

    def analyze(self, question):

        question = question.strip().lower()

        # Detect business-friendly column names
        detected = detect_columns(
            self.df,
            question
        )

        # =====================================================
        # Dataset Summary
        # =====================================================

        if "summary" in question:

            return {
                "type": "summary",
                "data": self.df.describe(include="all")
            }

        # =====================================================
        # Missing Values
        # =====================================================

        elif "missing" in question:

            missing = self.df.isnull().sum()

            return {
                "type": "table",
                "title": "Missing Values",
                "data": missing.reset_index().rename(
                    columns={
                        "index": "Column",
                        0: "Missing Values"
                    }
                )
            }

        # =====================================================
        # Duplicate Rows
        # =====================================================

        elif "duplicate" in question:

            duplicates = self.df.duplicated().sum()

            return {
                "type": "text",
                "message":
                f"Dataset contains {duplicates} duplicate rows."
            }

        # =====================================================
        # AI Insights
        # =====================================================

        elif (
            "insight" in question
            or "analysis" in question
            or "recommendation" in question
        ):

            from src.ai_insights import generate_insights

            insights = generate_insights(self.df)

            return {
                "type": "text",
                "message": "\n\n".join(insights)
            }

        # =====================================================
        # Numeric Columns
        # =====================================================

        elif "numeric" in question:

            cols = self.df.select_dtypes(
                include="number"
            ).columns.tolist()

            return {
                "type": "list",
                "title": "Numeric Columns",
                "items": cols
            }

        # =====================================================
        # Distribution Analysis
        # =====================================================

        elif "distribution" in question:

            amount_column = detected.get("amount")

            if amount_column:

                fig = px.histogram(
                    self.df,
                    x=amount_column,
                    title=f"{amount_column.title()} Distribution"
                )

                analysis = create_analysis_plan(question)

                return {
                    "type": "chart",
                    "chart": fig,
                    "message":
                    f"This histogram shows the distribution of {amount_column}.",
                    "plan": analysis["plan"],
                    "code": analysis["code"]
                }

            else:

                return {
                    "type": "text",
                    "message":
                    "I could not identify a numerical column for this distribution."
                }

        # =====================================================
        # Highest / Most / Top Category
        # =====================================================

        elif (
            (
                "highest" in question
                or "most" in question
                or "maximum" in question
                or "top" in question
            )
            and detected.get("amount")
            and detected.get("channel")
        ):

            amount_column = detected["amount"]
            channel_column = detected["channel"]

            data = (
                self.df
                .groupby(channel_column)[amount_column]
                .sum()
                .sort_values(ascending=False)
                .reset_index()
            )

            top_category = data.iloc[0][channel_column]
            top_amount = data.iloc[0][amount_column]

            fig = px.bar(
                data,
                x=channel_column,
                y=amount_column,
                title=(
                    f"Total {amount_column.title()} "
                    f"by {channel_column.title()}"
                )
            )

            analysis = create_analysis_plan(question)

            return {
                "type": "chart",
                "chart": fig,
                "message":
                f"🏆 {top_category} generates the highest "
                f"total {amount_column}: {top_amount:,.2f}.",
                "plan": analysis["plan"],
                "code": analysis["code"]
            }

        # =====================================================
        # Compare Amount by Category
        # =====================================================

        elif (
            "compare" in question
            and detected.get("amount")
            and detected.get("channel")
        ):

            amount_column = detected["amount"]
            channel_column = detected["channel"]

            data = (
                self.df
                .groupby(channel_column)[amount_column]
                .sum()
                .reset_index()
            )

            fig = px.bar(
                data,
                x=channel_column,
                y=amount_column,
                title=(
                    f"Total {amount_column.title()} "
                    f"by {channel_column.title()}"
                )
            )

            analysis = create_analysis_plan(question)

            return {
                "type": "chart",
                "chart": fig,
                "message":
                f"This chart compares {amount_column} across {channel_column}.",
                "plan": analysis["plan"],
                "code": analysis["code"]
            }

        # =====================================================
        # Relationship / Correlation Analysis
        # =====================================================

        elif (
            "relationship" in question
            or "correlation" in question
        ):

            fig = px.scatter(
                self.df,
                x="fee_amount",
                y="tax_amount",
                title="Relationship Between Fee and Tax Amount"
            )

            analysis = create_analysis_plan(question)

            return {
                "type": "chart",
                "chart": fig,
                "message":
                "This scatter plot shows the relationship between fee and tax amount.",
                "plan": analysis["plan"],
                "code": analysis["code"]
            }

        # =====================================================
        # Unknown Question
        # =====================================================

        else:

            return {
                "type": "text",
                "message":
                "Sorry, I don't understand that question yet."
            }