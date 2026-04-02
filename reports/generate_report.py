from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
import matplotlib.pyplot as plt
import os

def generate_pdf(df, state, category):

    os.makedirs("reports/assets", exist_ok=True)

    file_path = "reports/business_report.pdf"

    # -------------------------------
    # FILTER DATA
    # -------------------------------
    df = df[
        (df["state"] == state) &
        (df["product_category"] == category)
    ]

    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(file_path)

    elements = []

    # ===============================
    # TITLE
    # ===============================
    elements.append(Paragraph("📊 Sales Intelligence Report", styles["Title"]))
    elements.append(Spacer(1, 0.2 * inch))

    elements.append(Paragraph(f"State: {state}", styles["Normal"]))
    elements.append(Paragraph(f"Category: {category}", styles["Normal"]))
    elements.append(Spacer(1, 0.3 * inch))

    # ===============================
    # EXECUTIVE SUMMARY
    # ===============================
    total_rev = int(df["revenue"].sum())
    total_profit = int(df["profit"].sum())
    orders = len(df)

    elements.append(Paragraph("🔹 Executive Summary", styles["Heading2"]))
    elements.append(Spacer(1, 0.2 * inch))

    summary_text = f"""
    This report analyzes sales performance for the selected segment.
    Total revenue is ₹{total_rev:,} across {orders} orders, generating
    an estimated profit of ₹{total_profit:,}. The report combines
    historical analysis with predictive modeling to recommend
    optimal pricing strategies.
    """

    elements.append(Paragraph(summary_text, styles["Normal"]))
    elements.append(Spacer(1, 0.3 * inch))

    # ===============================
    # KEY METRICS
    # ===============================
    elements.append(Paragraph("🔹 Key Metrics", styles["Heading2"]))
    elements.append(Spacer(1, 0.2 * inch))

    elements.append(Paragraph(f"Revenue: ₹{total_rev:,}", styles["Normal"]))
    elements.append(Paragraph(f"Profit: ₹{total_profit:,}", styles["Normal"]))
    elements.append(Paragraph(f"Orders: {orders}", styles["Normal"]))

    elements.append(Spacer(1, 0.3 * inch))

    # ===============================
    # MONTHLY TREND
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

    elements.append(Spacer(1, 0.3 * inch))

    # ===============================
    # PRODUCT DISTRIBUTION
    # ===============================
    plt.figure()
    df["product_name"].value_counts().plot.pie(autopct="%1.1f%%")

    chart2_path = "reports/assets/products.png"
    plt.savefig(chart2_path)
    plt.close()

    elements.append(Paragraph("🔹 Product Distribution", styles["Heading2"]))
    elements.append(Spacer(1, 0.2 * inch))
    elements.append(Image(chart2_path, width=4*inch, height=4*inch))

    elements.append(Spacer(1, 0.3 * inch))

    # ===============================
    # 🔥 DECISION ENGINE + DEMAND CURVE
    # ===============================
    price = 1000
    discount = 10
    month = 6

    def demand(price, discount, month):

        base = 120
        price_factor = max(0.3, 1 - price / 100000)
        discount_factor = 1 + discount / 50
        seasonal = 1 + (month - 6) * 0.05

        return int(base * price_factor * discount_factor * seasonal)

    d = demand(price, discount, month)
    revenue = price * d * (1 - discount / 100)
    profit = (price * 0.3) * d

    elements.append(Paragraph("🔹 Predictive Insights", styles["Heading2"]))
    elements.append(Spacer(1, 0.2 * inch))

    elements.append(Paragraph(f"Expected Sales: {d}", styles["Normal"]))
    elements.append(Paragraph(f"Predicted Revenue: ₹{int(revenue):,}", styles["Normal"]))
    elements.append(Paragraph(f"Predicted Profit: ₹{int(profit):,}", styles["Normal"]))

    elements.append(Spacer(1, 0.3 * inch))

    # ===============================
    # DEMAND CURVE
    # ===============================
    prices = list(range(500, 80000, 2000))
    demands = [demand(p, discount, month) for p in prices]

    plt.figure()
    plt.plot(prices, demands)
    plt.title("Demand Curve (Price vs Demand)")
    plt.xlabel("Price")
    plt.ylabel("Demand")

    chart3_path = "reports/assets/demand_curve.png"
    plt.savefig(chart3_path)
    plt.close()

    elements.append(Paragraph("🔹 Demand Curve Analysis", styles["Heading2"]))
    elements.append(Spacer(1, 0.2 * inch))
    elements.append(Image(chart3_path, width=5*inch, height=3*inch))

    elements.append(Spacer(1, 0.3 * inch))

    # ===============================
    # STRATEGIC RECOMMENDATION
    # ===============================
    best_price = price
    best_profit = profit

    for p in range(500, 80000, 1000):
        d_temp = demand(p, discount, month)
        pr = (p * 0.3) * d_temp

        if pr > best_profit:
            best_profit = pr
            best_price = p

    elements.append(Paragraph("🔹 Strategic Recommendation", styles["Heading2"]))
    elements.append(Spacer(1, 0.2 * inch))

    recommendation_text = f"""
    The optimal price point is ₹{best_price}, which maximizes profit to ₹{int(best_profit):,}.
    This occurs due to a balance between demand and margin. Lower prices increase demand
    but reduce profitability per unit, while higher prices reduce demand significantly.
    
    The demand curve highlights price sensitivity, indicating that strategic pricing
    adjustments can significantly influence total revenue and profitability.
    """

    elements.append(Paragraph(recommendation_text, styles["Normal"]))

    elements.append(Spacer(1, 0.4 * inch))

    # ===============================
    # BUILD PDF
    # ===============================
    doc.build(elements)

    return file_path