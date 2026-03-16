import os
import json
import boto3
from dotenv import load_dotenv
from botocore.exceptions import ClientError

load_dotenv()


def _bedrock_client():
    region = os.getenv("AWS_REGION", "us-east-1")
    return boto3.client("bedrock-runtime", region_name=region)


def _invoke_nova_lite(
    prompt: str,
    *,
    max_new_tokens: int = 200,
    model_id: str = "amazon.nova-lite-v1:0",
) -> str:
    client = _bedrock_client()

    payload = {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "text": prompt
                    }
                ]
            }
        ],
        "inferenceConfig": {
            "max_new_tokens": max_new_tokens,
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
    except ClientError as exc:
        error = exc.response.get("Error", {})
        message = error.get("Message", str(exc))
        code = error.get("Code", "ClientError")
        raise RuntimeError(f"Bedrock invoke_model failed ({code}): {message}") from exc

    result = json.loads(response["body"].read())
    content = result.get("output", {}).get("message", {}).get("content", [])

    for item in content:
        if "text" in item:
            return item["text"]

    return "No text response returned from Nova Lite."


def call_nova_lite(user_text: str) -> str:
    model_id = os.getenv("MODEL_ID", "amazon.nova-lite-v1:0")
    prompt = (
        "You are a helpful assistant for seniors navigating U.S. government services. "
        "Answer clearly and simply.\n\n"
        f"User question: {user_text}"
    )
    return _invoke_nova_lite(prompt, max_new_tokens=80, model_id=model_id)
