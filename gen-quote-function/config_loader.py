import os
import boto3
import json

class ConfigLoader:
    """
    Helper class to load configuration and secrets from AWS services.
    """
    def __init__(self):
        self.ssm = boto3.client('ssm')

    def load_secrets(self):
        """
        Load secrets (Twitter keys) from SSM Parameter Store.
        Expected path: /serverless-ai-quotes/twitter_creds
        """
        parameter_name = "/serverless-ai-quotes/twitter_creds"
        try:
            response = self.ssm.get_parameter(
                Name=parameter_name,
                WithDecryption=True
            )
            secrets_json = response['Parameter']['Value']
            return json.loads(secrets_json)
        except self.ssm.exceptions.ParameterNotFound:
            print(f"Secrets not found at {parameter_name}")
            return None
