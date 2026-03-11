import os
import google.generativeai as genai

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.0-flash")


def generate_channel_insights(comparison_data):
    """
    Generate AI insights for compared channels.
    """

    if not comparison_data:
        return "Not enough data for AI insights."

    prompt = f"""
You are a YouTube analytics expert.

Analyze the following channel comparison data.

Provide:

1. Which channel is performing best and why
2. Which channel has the most loyal audience
3. Any signs of controversy
4. A short viewer recommendation

DATA:
{comparison_data}
"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI insight generation failed: {str(e)}"
