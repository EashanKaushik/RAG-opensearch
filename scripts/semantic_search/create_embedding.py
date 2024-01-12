import json
import os
import shutil
import semantic_search

class CreateEmbedding:
    
    def __init__(self, prefix=""):
        self.prefix = prefix
        self.bucket = semantic_search.S3.Bucket(semantic_search.BUCKET_NAME)
        self.documents = list()
        self.bulk_request = list()


    def get_embedding(self, document):
        data_body = json.dumps({
            "inputText": document
        })
        modelId = "amazon.titan-embed-text-v1"
        accept = "*/*"
        contentType = "application/json"
        
        response = semantic_search.BEDROCK.invoke_model(body=data_body, modelId=modelId, accept=accept, contentType=contentType)
        
        data_embedding = json.loads(response.get('body').read())["embedding"]
        
        return data_embedding
    

    def save_text_embedding(self, document_id, text, vector_field, s3_file_path):
        
        item = {
            "document_id" : {"S":str(document_id)},
            "text":{"S":text},
            "vector_field": {"L": [{"N": str(vector)} for vector in vector_field]},
            "s3_file_path": {"S": s3_file_path}
        }
        
        semantic_search.DYNAMODB.put_item(TableName=semantic_search.DYNAMODB_TABLE_NAME, Item=item)

    def bulk_request_from_dataset_s3(self):
        _idx = 1
        for objects in self.bucket.objects.filter(Prefix=self.prefix):
            obj = semantic_search.S3.Object(semantic_search.BUCKET_NAME, objects.key)
            text = obj.get()["Body"].read().decode('utf-8')
        
            if len(text) != 0:
                try:
                    vector_field = self.get_embedding(text)
                    document_id = str(abs(hash(text)))
                    if self.check_item_exist(document_id):
                        print(f'Items exists: {os.path.join(semantic_search.BUCKET_NAME, objects.key)}')
                        continue
        
                    self.save_text_embedding(document_id, text, vector_field, os.path.join(semantic_search.BUCKET_NAME, objects.key))
                    self.create_bulk_request(document_id, vector_field)

                    print(f"Completed {_idx}")
                    
                    _idx += 1

                except Exception as ex:
                    print(f"Exception Occured: {ex}")
    
    def bulk_request_from_dynamodb(self):
        self.bulk_request = list()
        
        paginator = semantic_search.DYNAMODB.get_paginator('scan')
        count = 0
        # Loop through all items in the table
        for page in paginator.paginate(TableName=semantic_search.DYNAMODB_TABLE_NAME):
            for item in page['Items']:
                # Process the item
                self.create_bulk_request(item['document_id']['S'], [float(vector['N']) for vector in item['vector_field']['L']])
                
                count += 1
        
        print(f"Total Documents: {count}")

    def create_bulk_request(self, document_id, vector_field):
        
        # self.bulk_request.append({"index": {"_id": document_id, "_index": semantic_search.INDEX_NAME}})
        self.bulk_request.append({"document_id":document_id, "vector_field": vector_field})
        
    
    def save_bulk_request_json(self):
        if len(self.bulk_request) == 0:
            print("Create bulk request first from S3 or DynamoDB")
            return
        bulk_request_json = '\n'.join(map(json.dumps, self.bulk_request))

        with open('bulk_request.json', 'w') as file:
            file.write(bulk_request_json)
        
        print("Bulk request saved to 'bulk_request.json'")
    
    def check_item_exist(self, document_id):
        key_to_check = {'document_id': {'S': document_id}}
        
        response = semantic_search.DYNAMODB.get_item(TableName=semantic_search.DYNAMODB_TABLE_NAME, Key=key_to_check)
        
        if 'Item' in response:
            return True
        else:
            return False

        
            