import semantic_search

if __name__ == "__main__":
    
    # Step 1: Create CreateEmbedding instance
    create_embedding = semantic_search.CreateEmbedding()
    
    # Step 2: Create and load embedding from bedrock and save it into DynamoDB
    create_embedding.bulk_request_from_dataset_s3()
    
    # Step 2: Load embedding from DynamoDB
    # create_embedding.bulk_request_from_dynamodb()
    
    # Step 3: Creates bulk_request.json in local directory from loaded embeddings
    #         This works only if you have loaded embeddings from S3 or DynamoDB from Step 2
    create_embedding.save_bulk_request_json()

    # Step 4: Create  BulkOSUpload instance
    bulk_upload = semantic_search.BulkOSUpload()

    # Step5: Upload Data to OpenSearch from bulk_request.json
    #        This works only if you have bulk_request.json from Step 3 in local directory
    bulk_upload.upload_data()
