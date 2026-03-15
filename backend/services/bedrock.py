import os
import json
import boto3
from dotenv import load_dotenv
from botocore.exceptions import NoCredentialsError, ClientError

load_dotenv()


def call_nova_lite(user_text: str) -> str:
    region = os.getenv("AWS_REGION", "us-east-1")
    model_id = os.getenv("MODEL_ID", "amazon.nova-lite-v1:0")

    client = boto3.client(
        "bedrock-runtime",
        region_name=region
    )

    payload = {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "text": (
                            "You are a helpful assistant for seniors navigating "
                            "U.S. government services. Answer clearly and simply.\n\n"
                            f"User question: {user_text}"
                        )
                    }
                ]
            }
        ],
        "inferenceConfig": {
            "max_new_tokens": 200,
            "temperature": 0.1
        }
    }

    try:
        response = client.invoke_model(
            modelId=model_id,
            body=json.dumps(payload),
            contentType="application/json",
            accept="application/json"
        )

        result = json.loads(response["body"].read())

        content = (
            result.get("output", {})
            .get("message", {})
            .get("content", [])
        )

        for item in content:
            if "text" in item:
                return item["text"]

        return "No text response returned from Nova Lite."

    except NoCredentialsError:
        raise Exception("AWS credentials not found.")
    except ClientError as e:
        raise Exception(f"AWS Bedrock error: {str(e)}")