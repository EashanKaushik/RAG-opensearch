import json
from opensearchpy import OpenSearch, RequestsHttpConnection, exceptions
from opensearchpy.helpers import bulk
from requests_aws4auth import AWS4Auth
import boto3
import urllib.parse

ssm = boto3.client("ssm")

def get_ssm_parameter(parameter_name, with_decryption=False):
    return ssm.get_parameter(Name=parameter_name, WithDecryption=with_decryption)[
        "Parameter"
    ]["Value"]
    
ENDPOINT = get_ssm_parameter("/opensearch-search/endpoint")
REGION = get_ssm_parameter("/opensearch-search/region")
INDEX_NAME = get_ssm_parameter("/opensearch-search/index_name")

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

def lambda_handler(event, context):

    document = urllib.parse.unquote(event["queryStringParameters"]["text"])
    
    print(document)
    
    embedding = get_embedding(document)
    
    knn_query = {
                    "size": 3,
                    "query": {
                        "knn": {
                            "vector_field": {
                                "vector": embedding,  # The vector you want to search for
                                "k": 3  # Number of nearest neighbors to retrieve
                            }
                        }
                    }
                }
    response = ops_client.search(index=INDEX_NAME, body=knn_query)
    
    result = list()
    
    for hit in response['hits']['hits']:
        result.append({'score': hit['_score'], 'document_id': hit['_source']['document_id']})
    
    return ({
        'statusCode': 200,
        'body': json.dumps(result),
         'headers': {
            "Access-Control-Allow-Methods": "GET,OPTIONS",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
            "Access-Control-Allow-Credentials": 'true'

        }
    })

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