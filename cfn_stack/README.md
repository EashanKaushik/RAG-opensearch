# Create the CloudFormation Stack

### Deploy the [init_stack.yaml](/cfn_stack/init_stack.yaml) in AWS CloudFormation

Provide the following parameter values: 

1. SemanticSearchCollectionName: Name of the OpenSearch collection created in step 2.

2. SemanticSearchIndexName: Name of the OpenSearch index created in step 2.

3. SemanticSearchCollectionEndpoint: Endpoint of the OpenSearch collection created in step 2. Make sure you remove https://. 

4. SemanticSearchLambdaLayerNameVersion: Layername and version of Lambda layer created in step 2. This is format in which value needs to be provided "LayeName:Version". 
  
5. SemanticSearchCollectionId: CollectionID of the OpenSearch collection created in Step 2. CollectionID can be found using the arn of the collection.

```
arn:aws:aoss:{REGION}:{ACCOUNT_ID}:collection/{CollectionID}
```

### AWS CloudFormation Outputs

![CloudFormation Outputs](/cfn_stack/images/1.png)

### Upload Data into S3

Upload entire [sample_dataset](/sample_dataset/) into Amazon S3 created the CloudFormation stack, refer AWS CloudFormation Outputs for S3 Bucket name.

***Note: Wait for the data to be uploaded to Amazon S3 before continuing to next step.***

### Update the first stack and replace current template (init_stack.yaml) with [add_trigger.yaml](/cfn_stack/add_trigger.yaml) using change sets. 

Follow instructions [here](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-cfn-updating-stacks-changesets.html). 

### Update Data Access Policy of your Amazon OpenSearch collection.

1. Select the Collection created.

![Update Data Access Policy Step 1](/cfn_stack/images/2.png)

2. Scroll down to Data Access and select the Associated policy.

![Update Data Access Policy Step 2](/cfn_stack/images/3.png)

3. Click on Edit, scroll down to Rule 1 and Add principals.

![Update Data Access Policy Step 3](/cfn_stack/images/4.png)

4. Select Roles.

![Update Data Access Policy Step 4](/cfn_stack/images/5.png)

5. Add two roles, *SemanticSearchQuerySearchIndexRole* and *SemanticSearchCreateEmbeddingRole*. Refer AWS CloudFormation Outputs for SemanticSearchCreateEmbeddingRole ARN and SemanticSearchQuerySearchIndexRole ARN.

![Update Data Access Policy Step 5](/cfn_stack/images/6.png)

Save changes.

### Upload the data using AWS Cloud9 Environment

Run the following command in Cloud9 terminal.

```
python scripts/main.py
```