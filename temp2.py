from google import genai
import os

# The client automatically picks up GEMINI_API_KEY from your environment variables
client = genai.Client()

PROMPT = """
You are an Highly Skilled Agent capable of selecting the available tools based on user query.
Available tools are "get_transactions" and "update_transactions".
User: Get the summary of ganesh
"""
response = client.models.generate_content(
    model="gemini-3.5-flash",
    contents=PROMPT,
)

print(response.text)
