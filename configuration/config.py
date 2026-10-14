from dotenv import load_dotenv
import os
import boto3

load_dotenv()

service_name = "bedrock-runtime"


def build_llm(service_name):
    client = boto3.client(
        service_name=service_name,
        region_name=os.getenv("AWS_REGION_NAME", "us-east-1"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    # Strip the 'bedrock/' prefix if present for native Boto3 execution
    raw_model = os.getenv("BEDROCK_MODEL", "us.meta.llama3-1-8b-instruct-v1:0")
    model_id = raw_model.replace("bedrock/", "")

    return client, model_id
