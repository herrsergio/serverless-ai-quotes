# Serverless AI Quotes

A serverless application that uses OpenAI to generate quotes and posts them to Twitter on a daily schedule. Built with AWS CDK and Python.

## Architecture

- **AWS Lambda**: Runs the core logic (generating quote, posting to Twitter).
- **Amazon EventBridge Scheduler**: Triggers the Lambda function daily.
- **AWS SSM Parameter Store**: Securely stores API keys and secrets.
- **OpenAI API**: Generates the quotes (using `gpt-4o-mini`).
- **Twitter API**: Posts the quotes.

## Prerequisites

- [AWS CLI](https://aws.amazon.com/cli/) installed and configured.
- [AWS CDK](https://docs.aws.amazon.com/cdk/v2/guide/getting_started.html) installed.
- [Docker](https://www.docker.com/) installed (running) for building the Lambda image.
- Python 3.12+

## Setup & Configuration

### 1. Store Secrets
This application relies on AWS Systems Manager (SSM) Parameter Store for secrets. You must create the following parameters in your AWS account (us-east-1 or your default region):

**OpenAI Key:**
- Name: `/rss-feed/global/openai_key`
- Type: `SecureString`
- Value: `sk-...` (your OpenAI API key)

**Twitter Credentials:**
You can use the provided helper script `upload_twitter_creds.py` to upload your credentials.
1. Create a file named `twitter_creds.json` (or copy `twitter_creds_template.json`):
  ```json
  {
    "consumer_key": "...",
    "consumer_secret": "...",
    "access_key": "...",
    "access_secret": "..."
  }
  ```
2. Run the script:
  ```bash
  python3 upload_twitter_creds.py --file twitter_creds.json --region us-east-1
  ```
  This will upload the credentials to `/serverless-ai-quotes/twitter_creds`.

### 2. Install Dependencies
```bash
# Install CDK dependencies
pip install -r cdk/requirements.txt

# (Optional) Install function dependencies locally for development
pip install -r gen-quote-function/requirements.txt
```

### 3. Deploy
From the root directory:

```bash
cd cdk
cdk deploy
```

This command will:
1. Build the Docker image for the Lambda function.
2. Deploy the CloudFormation stack to your AWS account.

## Development

- **Lambda Code**: Located in `gen-quote-function/`.
- **CDK Infrastructure**: Located in `cdk/`.

### Local Testing
You can run the python scripts locally if you have the credentials set up or mocked:
```bash
cd gen-quote-function
python lambda_genaiquote.py
```
*Note: You may need to mock the SSM client or ConfigLoader if running outside AWS.*
Generate quotations from notable people using GenAI and Serverless
