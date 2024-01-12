from opensearchpy import OpenSearch, RequestsHttpConnection, exceptions
from opensearchpy.helpers import bulk
from requests_aws4auth import AWS4Auth
import semantic_search
from opensearchpy.helpers import bulk
import json


class BulkOSUpload:
    def __init__(self):
        self.create_connection()

    def create_connection(self):
        credentials = semantic_search.boto3.Session().get_credentials()

        awsauth = AWS4Auth(
            credentials.access_key,
            credentials.secret_key,
            semantic_search.REGION,
            "aoss",
            session_token=credentials.token,
        )

        self.ops_client = OpenSearch(
            hosts=[{"host": semantic_search.ENDPOINT, "port": 443}],
            http_auth=awsauth,
            use_ssl=True,
            verify_certs=True,
            connection_class=RequestsHttpConnection,
            timeout=300,
        )

    def upload_data(self, file_path="bulk_request.json"):
        data = list()
        with open(file_path, "r") as file:
            for line in file:
                # Convert each line to a dictionary
                line = json.loads(line)
                data.append(line)
        print(f'Total Data: {len(data)}')
        print(f'Success, Error: {bulk(self.ops_client, data, index=semantic_search.INDEX_NAME)}')
