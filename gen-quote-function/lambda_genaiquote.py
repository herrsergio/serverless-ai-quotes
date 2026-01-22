import boto3
import os
import logging
from config_loader import ConfigLoader
from twitter import Twitter
from llm_helpers import generate_quote

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    """
    AWS Lambda handler function.
    Triggered by EventBridge Scheduler to generate and post a quote.
    """
    logger.info("Received event: %s", event)
    
    config_loader = ConfigLoader()
    secrets = config_loader.load_secrets()
    
    if not secrets:
        logger.error("No secrets found. Cannot post.")
        return {"statusCode": 500, "body": "Configuration error: Missing secrets."}

    twitter = Twitter(**secrets)
    tweet_text = generate_quote()
    
    if not tweet_text:
        logger.error("No quote generated. Cannot post.")
        return {"statusCode": 500, "body": "Generation error: No quote produced."}
        
    try:
        twitter.update_status(tweet_text)
        logger.info("Tweet posted successfully: %s", tweet_text)
        return {"statusCode": 200, "body": "Tweet posted successfully."}
    except Exception as e:
        logger.error("Error posting tweet: %s", e)
        return {"statusCode": 500, "body": "Error posting tweet."}
    