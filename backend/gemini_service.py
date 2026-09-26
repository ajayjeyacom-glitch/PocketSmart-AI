import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is not set in the .env file")

client = genai.Client(api_key=API_KEY)


def generate_recommendation(financial_data):
    """
    Generate a budgeting recommendation using Gemini.

    financial_data should contain the user's financial information,
    for example:
    {
        "income": 50000,
        "expenses": 30000,
        "savings": 10000
    }
    """

    prompt = f"""
You are a personal budgeting assistant for PocketSmart-AI.

Analyze the following financial information:

{financial_data}

Give a practical and easy-to-understand budgeting recommendation.

Include:
1. A short summary of the user's financial situation.
2. Main spending concerns, if any.
3. Specific suggestions to improve budgeting.
4. A simple savings recommendation.

Do not invent financial information that was not provided.
Keep the response concise and useful.
"""

    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=prompt
    )

    return response.text