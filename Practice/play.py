import boto3
import os

#set parameters
model_id = "us.anthropic.claude-sonnet-4-5-20251001-v1:0"

#initiate AWS Bedrock client
bedrock_runtime = boto3.client('bedrock-runtime', region_name=os.getenv("AWS_REGION", "us-east-1"))

#query to send to claude
query = input("Enter your query: ")

#make the APi call using converse API
try:
    print("System call")
    response = bedrock_runtime.converse(
        modelId=model_id,
        messages=[
            {
                "role": "user",
                "content": [{"text": query}]
            }
        ],
        inferenceConfig={"maxTokens":1024}
    )
    #Extract and print the response
    output = response['output']['content'][0]['text']
    print(f"QUery: {query}")
    print(f"\nResponse: {output}")
except Exception as e:
    print(f"Error calling Bedrock: {e}")    