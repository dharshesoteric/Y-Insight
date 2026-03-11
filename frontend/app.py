import streamlit as st
import requests

st.set_page_config(
    page_title="YouTube Channel Intelligence",
    page_icon="📊",
    layout="wide"
)

st.title("YouTube Channel Sentiment Analyzer")
st.write("Enter a YouTube channel name and get its intelligence score")

channel_name = st.text_input("Channel Name")

if st.button("Analyze"):

    if not channel_name.strip():
        st.warning("Please enter a channel name")
    else:
        with st.spinner("Analyzing channel..."):

            try:
                response = requests.post(
                    "http://127.0.0.1:8000/analyze-channel",
                    json={"channel_name": channel_name}
                )

                if response.status_code == 200:
                    data = response.json()
                    metrics = data["metrics"]

                    st.success("Analysis completed!")

                    st.subheader("Overall Channel Intelligence")

                    col1, col2, col3 = st.columns(3)

                    col1.metric(
                        "Sentiment Index",
                        f"{metrics['sentiment_index']}/100"
                    )

                    col2.metric(
                        "Engagement Score",
                        metrics["engagement_score"]
                    )

                    col3.metric(
                        "Controversy",
                        metrics["controversy_score"]
                    )

                    st.divider()

                    st.subheader("Detailed Metrics")

                    st.json(metrics)

                else:
                    st.error("Backend error. Is FastAPI running?")

            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to FastAPI. Make sure the backend is running.")

st.divider()
st.header("🔍Compare Channels (AI Powered)")

channels_input = st.text_input(
    "Enter up to 3 channels (comma separated)",
    placeholder="MrBeast, MKBHD, Fireship"
)

if st.button("Compare Channels"):
    if not channels_input.strip():
        st.warning("Enter at least one channel")
    else:
        names = [c.strip() for c in channels_input.split(",") if c.strip()]

        with st.spinner("Running AI comparison..."):
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/compare-channels",
                    json={"channel_names": names}
                )

                if response.status_code == 200:
                    data = response.json()

                    st.success("Comparison complete!")

                    st.subheader("📊 Channel Rankings")

                    for i, ch in enumerate(data["comparison"], 1):
                        st.write(
                            f"**{i}. {ch['channel_name']}** — "
                            f"Sentiment: {ch['metrics']['sentiment_index']}"
                        )

                    st.subheader("AI Insights")
                    st.write(data["ai_insights"])

                else:
                    st.error("Backend error during comparison.")

            except requests.exceptions.ConnectionError:
                st.error("Cannot connect to FastAPI.")
