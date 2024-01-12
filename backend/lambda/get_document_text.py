import json
import boto3
import urllib.parse

ssm = boto3.client("ssm")

def get_ssm_parameter(parameter_name, with_decryption=False):
    return ssm.get_parameter(Name=parameter_name, WithDecryption=with_decryption)["Parameter"]["Value"]
    
DYNAMODB_TABLE_NAME = get_ssm_parameter("/opensearch-search/dynamodb")
REGION = get_ssm_parameter("/opensearch-search/region")

dynamodb = boto3.client('dynamodb', REGION)

def lambda_handler(event, context):

    document_id = urllib.parse.unquote(event["queryStringParameters"]["document_id"])
    
    query = {'document_id': {'S': document_id}}

    response = dynamodb.get_item(TableName=DYNAMODB_TABLE_NAME, Key=query)
    
    if 'Item' in response:
        text = response['Item']['text']['S']
        s3_file_path = response['Item']['s3_file_path']['S']
        
        return {
            'statusCode': 200,
            'body': json.dumps({'text' :text, 's3_file_path': s3_file_path}),
            'headers': {
                "Access-Control-Allow-Methods": "GET,OPTIONS",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Credentials": 'true'

            }
            
        }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps('Document ID not found'),
            'headers': {
                "Access-Control-Allow-Methods": "GET,OPTIONS",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Credentials": 'true'
            }
        }

    
