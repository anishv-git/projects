from __future__ import annotations
import streamlit as st
import altair as alt
from .io import duckdb_connection
from .model import predict_title

st.set_page_config(page_title="HN Pulse", layout="wide")
st.title("HN Pulse: Hacker News Trends and Predictions")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Daily Story Stats")
    with duckdb_connection() as con:
        daily = con.execute("SELECT * FROM daily_stats ORDER BY day DESC LIMIT 60").df()
    if not daily.empty:
        chart = (
            alt.Chart(daily)
            .mark_line(point=True)
            .encode(x="day:T", y="avg_score:Q")
            .properties(height=300)
        )
        st.altair_chart(chart, use_container_width=True)
    else:
        st.info("No analytics yet. Run ingest and build.")

with col2:
    st.subheader("Top Titles")
    with duckdb_connection() as con:
        top = con.execute(
            "SELECT title, score FROM stories WHERE score IS NOT NULL ORDER BY score DESC LIMIT 30"
        ).df()
    if not top.empty:
        st.table(top)
    else:
        st.info("No stories yet. Run ingest.")

st.subheader("What-if: Predict Title Popularity")
user_title = st.text_input("Propose a title", "Show HN: I built a tiny data warehouse with DuckDB")
if st.button("Predict popularity"):
    try:
        prob = predict_title(user_title)
        st.success(f"Estimated probability of top-quartile score: {prob:.2%}")
    except Exception as e:
        st.error(str(e))
