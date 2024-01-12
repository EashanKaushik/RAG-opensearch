from semantic_search.create_embedding import CreateEmbedding
from semantic_search.bulk_upload import BulkOSUpload
from semantic_search.helper import get_ssm_parameter
import boto3
import json

ssm = boto3.client("ssm")

COLLECTION_NAME = get_ssm_parameter(ssm, "/opensearch-search/name")
INDEX_NAME = get_ssm_parameter(ssm, "/opensearch-search/index_name")
REGION = get_ssm_parameter(ssm, "/opensearch-search/region")
BUCKET_NAME = get_ssm_parameter(ssm, "/opensearch-search/bucket")
ENDPOINT = get_ssm_parameter(ssm, "/opensearch-search/endpoint", with_decryption=True)
DYNAMODB_TABLE_NAME = get_ssm_parameter(ssm, "/opensearch-search/dynamodb")

OS_SERVERLESS = boto3.client("opensearchserverless", REGION)
S3 = boto3.resource("s3")
DYNAMODB = boto3.client("dynamodb", REGION)
BEDROCK = boto3.client("bedrock-runtime", REGION)
