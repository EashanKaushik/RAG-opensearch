import json
import boto3
import os

s3 = boto3.client("s3")
ssm = boto3.client("ssm")

def get_ssm_parameter(parameter_name, with_decryption=False):
    return ssm.get_parameter(Name=parameter_name, WithDecryption=with_decryption)[
        "Parameter"
    ]["Value"]
    
BUCKET = get_ssm_parameter("/opensearch-search/bucket")

def lambda_handler(event, context):

    document = event["queryStringParameters"]["document"]
    
    filename = f"{abs(hash(document))}.txt"
    s3.put_object(Bucket=BUCKET, Key=filename, Body=document.encode('utf-8'))

    return {
        'statusCode': 200,
        'body': json.dumps(os.path.join(BUCKET, filename)),
        'headers': {
            "Access-Control-Allow-Methods": "PUT,OPTIONS",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
            "Access-Control-Allow-Credentials": 'true'

        }
    }
