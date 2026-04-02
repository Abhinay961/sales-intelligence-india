import streamlit as st
from src.predict import predict

def app():

    st.title("🔮 Revenue Prediction")

    col1, col2 = st.columns(2)

    with col1:
        price = st.slider("Price", 100, 50000, 1000)
        quantity = st.slider("Quantity", 1, 10, 2)

    with col2:
        discount = st.slider("Discount", 0, 50, 10)
        month = st.slider("Month", 1, 12, 6)

    model = st.selectbox("Model", ["xgb", "lr"])

    if st.button("Predict", key="predict_btn"):
        result = predict(price, quantity, discount, month, model)
        st.success(f"💰 Revenue: ₹{int(result)}")