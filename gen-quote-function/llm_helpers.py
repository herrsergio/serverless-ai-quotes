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
Generate a famous quote. The number of characters, including the quote and the author, must fit in a tweet.
Quotes must be written in the author's language.
CRITICAL INSTRUCTIONS:
- DO NOT INCLUDE QUOTES FROM CONTROVERSIAL FIGURES
- HARD LIMIT: Under 250 characters total.
- Write the sentence in the author's native language
FORMAT: [Quote] - [Author]
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
