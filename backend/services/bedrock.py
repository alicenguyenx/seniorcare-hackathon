import os
import json
import boto3


def call_nova_lite(user_text: str) -> str:
    region = os.getenv("AWS_REGION", "us-east-1")

    client = boto3.client(
        "bedrock-runtime",
        region_name=region
    )

    model_id = "amazon.nova-lite-v1:0"

    payload = {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "text": f"You are a helpful assistant for seniors navigating U.S. government services. Answer clearly and simply.\n\nUser question: {user_text}"
                    }
                ]
            }
        ],
        "inferenceConfig": {
            "max_new_tokens": 20,
            "temperature": 0.1
        }
    }

    response = client.invoke_model(
        modelId=model_id,
        body=json.dumps(payload),
        contentType="application/json",
        accept="application/json"
    )

    result = json.loads(response["body"].read())

    output_message = result["output"]["message"]["content"]
    for item in output_message:
        if "text" in item:
            return item["text"]

    return "No text response returned from Nova Lite."
