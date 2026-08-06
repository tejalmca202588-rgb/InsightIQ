import pandas as pd
import plotly.express as px

from src.analysis_planner import create_analysis_plan


class AIAnalyst:

    def __init__(self, df):
        self.df = df


    def analyze(self, question):

        question = question.lower()


        # =========================
        # Dataset Summary
        # =========================

        if "summary" in question:

            return {
                "type": "summary",
                "data": self.df.describe(include="all")
            }


        # =========================
        # Missing Values
        # =========================

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


        # =========================
        # Duplicate Rows
        # =========================

        elif "duplicate" in question:

            duplicates = self.df.duplicated().sum()

            return {
                "type": "text",
                "message":
                f"Dataset contains {duplicates} duplicate rows."
            }



        # =========================
        # AI Insights
        # =========================

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



        # =========================
        # Numeric Columns
        # =========================

        elif "numeric" in question:

            cols = self.df.select_dtypes(
                include="number"
            ).columns.tolist()


            return {
                "type": "list",
                "title": "Numeric Columns",
                "items": cols
            }



        # =========================
        # Distribution Chart
        # =========================

        elif (
            "distribution" in question
            and "amount" in question
        ):

            fig = px.histogram(
                self.df,
                x="amount",
                title="Transaction Amount Distribution"
            )


            analysis = create_analysis_plan(question)


            return {
                "type": "chart",
                "chart": fig,
                "message":
                "This histogram shows the distribution of transaction amounts.",
                "plan": analysis["plan"],
                "code": analysis["code"]
            }



        # =========================
        # Compare Amount by Channel
        # =========================

        elif (
            "compare" in question
            and "channel" in question
        ):

            data = (
                self.df
                .groupby("channel")["amount"]
                .sum()
                .reset_index()
            )


            fig = px.bar(
                data,
                x="channel",
                y="amount",
                title="Total Transaction Amount by Channel"
            )


            analysis = create_analysis_plan(question)


            return {
                "type": "chart",
                "chart": fig,
                "message":
                "This chart compares transaction amounts across channels.",
                "plan": analysis["plan"],
                "code": analysis["code"]
            }



        # =========================
        # Relationship Analysis
        # =========================

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



        # =========================
        # Unknown Question
        # =========================

        else:

            return {
                "type": "text",
                "message":
                "Sorry, I don't understand that question yet."
            }