# Create AWS Cloud9 environment, clone repository, and Create OpenSearch collection

## Cloud9 Environment Setup

1. [Create](https://docs.aws.amazon.com/cloud9/latest/user-guide/create-environment-main.html) an AWS Cloud9 environment, of instance type t3.small (2 GiB RAM + 2 vCPU), and open the environment in Cloud9.

2. Create a Lambda Layer. Run the following commands in Cloud9 terminal. 

```
mkdir opensearchpy
cd opensearchpy
mkdir -p aws-layer/python/lib/python3.11/site-packages
pip install opensearch-py --target aws-layer/python/lib/python3.11/site-packages  
pip install boto3 --target aws-layer/python/lib/python3.11/site-packages
pip install requests-aws4auth --target aws-layer/python/lib/python3.11/site-packages
cd aws-layer
zip -r9 lambda-layer.zip .
aws lambda publish-layer-version --layer-name OpenSearchPy --description "Semantic Search Lambda Layer" --zip-file fileb://lambda-layer.zip --compatible-runtimes python3.11
```

3. Clone the git repository in Cloud9 *environemnt* directory.

```
git clone TODO: PUT git clone
```

4. Configure the AWS CLI in Cloud9 Environment. Run the following command and provide Access Key and Secret Access Key for the user. 

```
aws configure
```
For more details [refer](https://docs.aws.amazon.com/cli/latest/reference/configure/).

***Note: If the AWS Cloud9 Environment prompts to refresh Access Keys, select cancel***


![cancel force upate](/scripts/images/8.png)

![disable update](/scripts/images/9.png)

5. Install requirements

```
pip install -r scripts/requirements.txt
```

## Create Amazon OpenSearch Collection

![create collection step 1](/scripts/images/1.png)

![create collection step 2](/scripts/images/2.png)

Click **Next** > **Submit** to create the collection.

***Note: Wait for the collection to be creted before moving forward and then note down the OpenSearch Collection endpoint.***

![collection endpoint](/scripts/images/6.png)

## Create an Index

![create index step 1](/scripts/images/7.png)

![create index step 2](/scripts/images/3.png)

![create index step 3](/scripts/images/4.png)

![create index step 3](/scripts/images/5.png)

Select *create index*.