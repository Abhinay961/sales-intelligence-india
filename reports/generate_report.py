import pandas as pd
import matplotlib.pyplot as plt
import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet

from src.predict import predict

def generate_pdf():

    df = pd.read_csv("data/processed/data.csv")

    # -------------------------
    # METRICS
    # -------------------------
    total_revenue = int(df["revenue"].sum())
    total_profit = int(df["profit"].sum())
    total_orders = len(df)

    # -------------------------
    # CHARTS (SAVE AS IMAGES)
    # -------------------------
    os.makedirs("reports/assets", exist_ok=True)

    # Monthly trend
    monthly = df.groupby("month")["revenue"].sum()
    plt.figure()
    monthly.plot()
    plt.title("Monthly Revenue Trend")
    plt.savefig("reports/assets/monthly.png")
    plt.close()

    # Category chart
    cat = df["product_name"].value_counts().head(5)
    plt.figure()
    cat.plot(kind="bar")
    plt.title("Top Products")
    plt.savefig("reports/assets/products.png")
    plt.close()

    # -------------------------
    # PREDICTION SUMMARY
    # -------------------------
    sample_pred = predict(1000, 2, 10, 6)

    # -------------------------
    # CREATE PDF
    # -------------------------
    doc = SimpleDocTemplate("reports/business_report.pdf")
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph("Sales Intelligence Report", styles["Title"]))
    content.append(Spacer(1, 10))

    content.append(Paragraph(f"Total Revenue: ₹{total_revenue}", styles["Normal"]))
    content.append(Paragraph(f"Total Profit: ₹{total_profit}", styles["Normal"]))
    content.append(Paragraph(f"Total Orders: {total_orders}", styles["Normal"]))

    content.append(Spacer(1, 10))

    content.append(Paragraph("📊 Key Insights:", styles["Heading2"]))
    content.append(Paragraph("• High revenue driven by specific regions and products", styles["Normal"]))
    content.append(Paragraph("• Discount strategy impacts profit significantly", styles["Normal"]))
    content.append(Paragraph("• Seasonal trends observed in monthly data", styles["Normal"]))

    content.append(Spacer(1, 10))

    content.append(Paragraph("📈 Charts:", styles["Heading2"]))
    content.append(Image("reports/assets/monthly.png", width=400, height=200))
    content.append(Image("reports/assets/products.png", width=400, height=200))

    content.append(Spacer(1, 10))

    content.append(Paragraph("🔮 Prediction Insight:", styles["Heading2"]))
    content.append(Paragraph(f"Expected revenue for sample input: ₹{int(sample_pred)}", styles["Normal"]))
    content.append(Paragraph("Prediction indicates pricing and discount optimization opportunities.", styles["Normal"]))

    content.append(Spacer(1, 10))

    content.append(Paragraph("💡 Business Recommendations:", styles["Heading2"]))
    content.append(Paragraph("• Focus on high-performing states", styles["Normal"]))
    content.append(Paragraph("• Reduce excessive discounting", styles["Normal"]))
    content.append(Paragraph("• Promote region-specific products", styles["Normal"]))

    doc.build(content)

    return "reports/business_report.pdf"