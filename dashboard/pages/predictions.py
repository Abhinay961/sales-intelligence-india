import streamlit as st
import sys, os

# -------------------------------
# FIX PATH
# -------------------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.insert(0, BASE_DIR)

from src.predict import predict

def app():

    st.title("🔮 Sales Revenue Prediction")

    col1, col2 = st.columns(2)

    with col1:
        price = st.slider("Product Price", 100, 50000, 1000)
        quantity = st.slider("Quantity Sold", 1, 10, 2)

    with col2:
        discount = st.slider("Discount (%)", 0, 50, 10)
        month = st.slider("Month", 1, 12, 6)

    model = st.selectbox("Model", ["xgb", "lr"])

    if st.button("Predict Revenue", key="predict_btn_main"):
        try:
            result = predict(price, quantity, discount, month, model)
            st.success(f"💰 Predicted Revenue: ₹{int(result)}")

            st.info(
                "📊 Insight: Adjust pricing and discounts to maximize revenue."
            )

        except Exception as e:
            st.error(f"❌ Prediction failed: {e}")