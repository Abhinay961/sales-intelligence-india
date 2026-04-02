import streamlit as st

def app(df):

    st.title("🇮🇳 Sales Intelligence Dashboard")

    col1,col2,col3 = st.columns(3)
    col1.metric("Revenue", int(df.revenue.sum()))
    col2.metric("Orders", len(df))
    if "profit" in df.columns:
        col3.metric("Profit", int(df["profit"].sum()))
    else:
        col3.metric("Profit", "Not Available")

    st.subheader("📈 Monthly Trend")
    state = st.selectbox("Select State", df.state.unique())
    temp = df[df.state==state]
    st.line_chart(temp.groupby("month")["revenue"].sum())

    st.info("Peak months indicate seasonal demand")

    st.subheader("🥧 Product Distribution")
    st.pyplot(temp["product_name"].value_counts().plot.pie(autopct="%1.1f%%").figure)