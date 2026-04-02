from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os

def generate_pdf(df):

    os.makedirs("reports", exist_ok=True)
    file_path = "reports/business_report.pdf"

    doc = SimpleDocTemplate(file_path)
    styles = getSampleStyleSheet()
    elements = []

    # -------------------------------
    # 🔥 SAFE COLUMN HANDLING
    # -------------------------------

    # Ensure revenue
    if "revenue" not in df.columns:
        df["revenue"] = df["price"] * df["quantity"] * (1 - df["discount"]/100)

    # Ensure profit
    if "profit" not in df.columns:
        df["cost"] = df["price"] * 0.7
        df["profit"] = (df["price"] - df["cost"]) * df["quantity"]

    # -------------------------------
    # METRICS
    # -------------------------------
    total_revenue = int(df["revenue"].sum())
    total_profit = int(df["profit"].sum())

    # -------------------------------
    # CONTENT
    # -------------------------------
    elements.append(Paragraph("Sales Business Report", styles["Title"]))
    elements.append(Spacer(1, 20))

    elements.append(Paragraph(f"Total Revenue: ₹{total_revenue}", styles["Normal"]))
    elements.append(Paragraph(f"Total Profit: ₹{total_profit}", styles["Normal"]))

    doc.build(elements)

    return file_path