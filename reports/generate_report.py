from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
import matplotlib.pyplot as plt
import os

def generate_pdf(df):

    os.makedirs("reports/assets", exist_ok=True)

    file_path = "reports/business_report.pdf"

    doc = SimpleDocTemplate(file_path)
    styles = getSampleStyleSheet()

    elements = []

    # ===============================
    # TITLE
    # ===============================
    elements.append(Paragraph("📊 Sales Intelligence Report", styles["Title"]))
    elements.append(Spacer(1, 0.3 * inch))

    # ===============================
    # METRICS
    # ===============================
    total_rev = int(df["revenue"].sum())
    total_profit = int(df["profit"].sum())
    orders = len(df)

    elements.append(Paragraph("🔹 Key Metrics", styles["Heading2"]))
    elements.append(Spacer(1, 0.2 * inch))

    elements.append(Paragraph(f"Total Revenue: ₹{total_rev:,}", styles["Normal"]))
    elements.append(Paragraph(f"Total Profit: ₹{total_profit:,}", styles["Normal"]))
    elements.append(Paragraph(f"Total Orders: {orders}", styles["Normal"]))

    elements.append(Spacer(1, 0.3 * inch))

    # ===============================
    # INSIGHTS
    # ===============================
    elements.append(Paragraph("🔹 Business Insights", styles["Heading2"]))
    elements.append(Spacer(1, 0.2 * inch))

    top_category = df.groupby("product_category")["revenue"].sum().idxmax()
    top_state = df.groupby("state")["revenue"].sum().idxmax()

    elements.append(Paragraph(f"Top Category: {top_category}", styles["Normal"]))
    elements.append(Paragraph(f"Top State: {top_state}", styles["Normal"]))

    if total_profit > total_rev * 0.25:
        elements.append(Paragraph("Strong profitability observed.", styles["Normal"]))
    else:
        elements.append(Paragraph("Profit margins can be improved.", styles["Normal"]))

    elements.append(Spacer(1, 0.4 * inch))

    # ===============================
    # CHART 1: MONTHLY SALES
    # ===============================
    monthly = df.groupby("month")["revenue"].sum()

    plt.figure()
    monthly.plot()
    plt.title("Monthly Revenue Trend")

    chart1_path = "reports/assets/monthly.png"
    plt.savefig(chart1_path)
    plt.close()

    elements.append(Paragraph("🔹 Monthly Sales Trend", styles["Heading2"]))
    elements.append(Spacer(1, 0.2 * inch))
    elements.append(Image(chart1_path, width=5*inch, height=3*inch))

    elements.append(Spacer(1, 0.4 * inch))

    # ===============================
    # CHART 2: CATEGORY REVENUE
    # ===============================
    category_rev = df.groupby("product_category")["revenue"].sum()

    plt.figure()
    category_rev.plot(kind="bar")
    plt.title("Revenue by Category")

    chart2_path = "reports/assets/category.png"
    plt.savefig(chart2_path)
    plt.close()

    elements.append(Paragraph("🔹 Category Performance", styles["Heading2"]))
    elements.append(Spacer(1, 0.2 * inch))
    elements.append(Image(chart2_path, width=5*inch, height=3*inch))

    elements.append(Spacer(1, 0.4 * inch))

    # ===============================
    # FINAL BUILD
    # ===============================
    doc.build(elements)

    return file_path