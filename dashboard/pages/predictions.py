import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from src.predict import predict

def app():

    st.title("🔮 Sales Prediction")

    price = st.slider("Price",100,50000,1000)
    qty = st.slider("Quantity",1,10,2)
    discount = st.slider("Discount",0,50,10)
    month = st.slider("Month",1,12,6)

    model = st.selectbox("Model",["xgb","lr"])

    if st.button("Predict"):
        try:
            res = predict(price, qty, discount, month, model)
            st.success(f"Predicted Revenue: ₹{int(res)}")
        except Exception as e:
            st.error(f"Error: {e}")