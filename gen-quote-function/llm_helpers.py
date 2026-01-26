import logging
import openai
from openai import OpenAI

# Configure logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def load_openai_key():
    """
    Loads the OpenAI API key from AWS SSM Parameter Store.
    """
    try:
        import boto3
        ssm = boto3.client('ssm')
        response = ssm.get_parameter(
            Name='/rss-feed/global/openai_key',
            WithDecryption=True
        )
        return response['Parameter']['Value']
    except Exception as e:
        logger.error(f"Error loading OpenAI key: {e}")
        return None

def generate_quote():
    """
    Generates a quote using OpenAI's gpt-4o-mini model.
    """
    api_key = load_openai_key()
    if not api_key:
        logger.error("OpenAI API key not found.")
        return None

    client = OpenAI(api_key=api_key)

    try:
        prompt = """
Generate a famous quote.

CRITICAL REQUIREMENTS:
- Use the ORIGINAL wording exactly as written by the author.
- The quote MUST be in the author's native language.
- DO NOT translate quotes.
- DO NOT use quotes that are commonly known only through translations.
- If the original language cannot be verified with high confidence, choose a different author.
- DO NOT include quotes from controversial figures.
- HARD LIMIT: Under 250 characters total (quote + author).

PROCESS (must be followed):
1. Identify the author's native language.
2. Confirm the quote was originally written in that language.
3. Validate total character count.

FORMAT (exact):
[Quote] - [Author]
"""
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=100,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Error generating quote: {e}")
        return None
