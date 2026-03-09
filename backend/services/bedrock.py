import boto3
import json
import os
from dotenv import load_dotenv

load_dotenv()

client = boto3.client(
    "bedrock-runtime",
    region_name=os.getenv("AWS_REGION", "us-east-1")
)

def call_nova_lite(prompt: str) -> str:
    response = client.converse(
        modelId="us.amazon.nova-lite-v1:0",
        messages=[{
            "role": "user",
            "content": [{"text": prompt}]
        }],
        inferenceConfig={"maxTokens": 512, "temperature": 0.5}
    )
    return response["output"]["message"]["content"][0]["text"]
