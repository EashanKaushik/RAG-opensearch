import json
from opensearchpy import OpenSearch, RequestsHttpConnection, exceptions
from opensearchpy.helpers import bulk
from requests_aws4auth import AWS4Auth
import boto3
import random
import os

ssm = boto3.client("ssm")

def get_ssm_parameter(parameter_name, with_decryption=False):
    return ssm.get_parameter(Name=parameter_name, WithDecryption=with_decryption)[
        "Parameter"
    ]["Value"]
    
ENDPOINT = get_ssm_parameter("/opensearch-search/endpoint")
REGION = get_ssm_parameter("/opensearch-search/region")
INDEX_NAME = get_ssm_parameter("/opensearch-search/index_name")
DYNAMODB_TABLE_NAME = get_ssm_parameter("/opensearch-search/dynamodb")

credentials = boto3.Session().get_credentials()

awsauth = AWS4Auth(
    credentials.access_key,
    credentials.secret_key,
    REGION,
    "aoss",
    session_token=credentials.token,
)


ops_client = OpenSearch(
    hosts=[{"host": ENDPOINT, "port": 443}],
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection,
    timeout=300,
)
bedrock = boto3.client('bedrock-runtime')
s3 = boto3.client('s3')
dynamodb = boto3.client('dynamodb', REGION)

def lambda_handler(event, context):

    for e in event["Records"]:
        bucket_name = e["s3"]["bucket"]["name"]
        file_key = e["s3"]["object"]["key"]
        
        response = s3.get_object(Bucket=bucket_name, Key=file_key)
    
        # Read the content of the file
        document = response['Body'].read().decode('utf-8')
        
        document_id = str(abs(hash(document)))
        
        if check_item_exist(document_id):
            print("Document Exist")
            continue
        
        embedding = get_embedding(document)
        
        
        save_text_embedding(document_id, document, embedding, os.path.join(bucket_name, file_key))

    return {
        'statusCode': 200,
        'body': "complete"
    }

def save_text_embedding(document_id, text, vector_field, s3_file_path):
    item = {
        "document_id": {"S": str(document_id)},
        "text": {"S": text},
        "vector_field": {"L": [{"N": str(vector)} for vector in vector_field]},
        "s3_file_path": {"S": s3_file_path},
    }

    dynamodb.put_item(
        TableName=DYNAMODB_TABLE_NAME, Item=item
    )
    
    index_opensearch(document_id, text, vector_field)

def get_embedding(document):
        data_body = json.dumps({"inputText": document})
        modelId = "amazon.titan-embed-text-v1"
        accept = "*/*"
        contentType = "application/json"

        response = bedrock.invoke_model(
            body=data_body, modelId=modelId, accept=accept, contentType=contentType
        )

        data_embedding = json.loads(response.get("body").read())["embedding"]

        return data_embedding
    
def index_opensearch(document_id, text, vector_field):
    document = {
      'vector_field': vector_field,
      'document_id': document_id,
    }
    
    response = ops_client.index(
        index = INDEX_NAME,
        body = document,
        )
    print(response)

def check_item_exist(document_id):
    key_to_check = {'document_id': {'S': document_id}}
    
    response = dynamodb.get_item(TableName=DYNAMODB_TABLE_NAME, Key=key_to_check)
    
    if 'Item' in response:
        return True
    else:
        return False
