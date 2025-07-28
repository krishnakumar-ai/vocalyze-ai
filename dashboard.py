import streamlit as st
import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
load_dotenv()

st.set_page_config(page_title="Vocalyze Dashboard", layout="wide")
st.title("📊 Vocalyze Chat Analytics Dashboard")

DATABASE_URL = os.getenv("DATABASE_URL")

try:
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM chat_logs ORDER BY timestamp DESC")
    records = cursor.fetchall()

    df = pd.DataFrame(records)

    cursor.close()
    conn.close()

    # 🔍 Filter UI
    with st.sidebar:
        st.header("🔍 Filter Options")
        sentiment_filter = st.multiselect("Sentiment", df["sentiment"].unique(), default=df["sentiment"].unique())
        intent_filter = st.multiselect("Intent", df["intent"].unique(), default=df["intent"].unique())
        keyword = st.text_input("Search keyword")

    filtered_df = df[
        df["sentiment"].isin(sentiment_filter) &
        df["intent"].isin(intent_filter)
    ]

    if keyword:
        filtered_df = filtered_df[filtered_df["user_message"].str.contains(keyword, case=False, na=False)]

    st.subheader("📜 Latest Conversations")
    st.dataframe(filtered_df, use_container_width=True)

    st.subheader("📈 Chat Insights")
    col1, col2 = st.columns(2)

    with col1:
        st.write("### Sentiment Distribution")
        st.bar_chart(filtered_df["sentiment"].value_counts())

    with col2:
        st.write("### Intent Distribution")
        st.bar_chart(filtered_df["intent"].value_counts())

    st.download_button("📥 Download CSV", filtered_df.to_csv(index=False), file_name="filtered_chat_logs.csv")

except Exception as e:
    st.warning(f"⚠️ Error loading dashboard: {e}")
