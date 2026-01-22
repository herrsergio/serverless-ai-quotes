import boto3
import json
import os
import argparse

def upload_creds(file_path, feed_id, region_name='us-east-1'):
    """
    Reads credentials from a file and uploads them to SSM Parameter Store.
    """
    
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found.")
        return

    # Read credentials
    try:
        with open(file_path, 'r') as f:
            creds = json.load(f)
            
        required_keys = ["consumer_key", "consumer_secret", "access_key", "access_secret"]
        if not all(k in creds for k in required_keys):
            print(f"Error: JSON must contain keys: {required_keys}")
            return
            
        secret_value = json.dumps(creds)
        
    except json.JSONDecodeError:
        print("Error: File must be valid JSON.")
        return
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    # Upload to SSM
    ssm = boto3.client('ssm', region_name=region_name)
    parameter_name = "/serverless-ai-quotes/twitter_creds"
    
    print(f"Uploading credentials to {parameter_name}...")
    
    try:
        ssm.put_parameter(
            Name=parameter_name,
            Value=secret_value,
            Type='SecureString',
            Overwrite=True
        )
        print("Successfully uploaded credentials.")
    except Exception as e:
        print(f"Error uploading to SSM: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Upload Twitter credentials to SSM.")
    parser.add_argument("--file", required=True, help="Path to the JSON file containing credentials.")
    parser.add_argument("--region", default="us-east-1", help="AWS Region (default: us-east-1).")
    
    args = parser.parse_args()
    
    upload_creds(args.file, None, args.region)
