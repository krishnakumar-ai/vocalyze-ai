import streamlit as st
import pandas as pd

st.set_page_config(page_title="Vocalyze Dashboard", layout="wide")
st.title("📊 Vocalyze Chat Analytics Dashboard")

try:
    # 📥 Load data
    df = pd.read_csv("chat_logs.csv", names=["Timestamp", "Message", "Sentiment", "Intent", "Bot Reply"])
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])

    # 🔍 Search/filter section
    with st.sidebar:
        st.header("🔍 Filter Options")
        sentiment_filter = st.multiselect("Sentiment", df["Sentiment"].unique(), default=df["Sentiment"].unique())
        intent_filter = st.multiselect("Intent", df["Intent"].unique(), default=df["Intent"].unique())
        keyword = st.text_input("Search keyword in message")

    # 🧠 Apply filters
    filtered_df = df[
        df["Sentiment"].isin(sentiment_filter) &
        df["Intent"].isin(intent_filter)
    ]

    if keyword:
        filtered_df = filtered_df[filtered_df["Message"].str.contains(keyword, case=False, na=False)]

    # 📋 Latest chat data
    st.subheader("📜 Latest Conversations")
    st.dataframe(filtered_df.sort_values("Timestamp", ascending=False), use_container_width=True)

    # 📊 Charts
    st.subheader("📈 Chat Insights")
    col1, col2 = st.columns(2)

    with col1:
        st.write("### Sentiment Distribution")
        st.bar_chart(filtered_df["Sentiment"].value_counts())

    with col2:
        st.write("### Intent Distribution")
        st.bar_chart(filtered_df["Intent"].value_counts())

    # 📤 Export option
    st.download_button("📥 Download Filtered CSV", filtered_df.to_csv(index=False), file_name="filtered_chat_logs.csv")

except FileNotFoundError:
    st.warning("⚠️ No chat logs found. Send some messages through the bot to populate the dashboard.")