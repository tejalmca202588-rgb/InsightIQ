from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf(report_df, filename):

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    elements = []

    elements.append(
        Paragraph(
            "<b>InsightIQ Business Report</b>",
            styles["Title"]
        )
    )

    elements.append(Spacer(1, 20))

    data = [["Metric", "Value"]]

    for _, row in report_df.iterrows():
        data.append(
            [
                row["Metric"],
                str(row["Value"])
            ]
        )

    table = Table(data)

    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

                ("GRID", (0, 0), (-1, -1), 1, colors.black),

                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),

                ("ALIGN", (0, 0), (-1, -1), "CENTER"),

                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
            ]
        )
    )

    elements.append(table)

    doc.build(elements)