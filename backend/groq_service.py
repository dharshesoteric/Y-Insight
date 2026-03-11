import os
from groq import Groq

# Initialize client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_channel_insights(comparison_data):
    """
    Generate AI insights using Groq LLM.
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
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are an expert YouTube analytics assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=400,
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"AI insight generation failed: {str(e)}"
