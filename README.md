# Semantic Search Engine for Retrieval-Augmented Generation (RAG)
</br>

## Description
</br>

A **Semantic Search Engine** is an advanced information retrieval system that goes beyond traditional keyword-based searches to understand the meaning of the user's query and the content of web pages. Unlike conventional search engines that rely on keyword matching, semantic search engines use **natural language processing (NLP)**, **artificial intelligence (AI)**, and **machine learning (ML)** techniques to comprehend the context and intent behind user queries.

The Semantic Search Engine initially transforms all documents within the corpus into **embeddings**, storing them in a **vector database**. Subsequently, when a user submits a query, the query is converted into an embedding, and the **k most similar embeddings** are retrieved from the vector database using a **similarity index**, such as Euclidean distance or cosine similarity.

## Audience

This is an introductory-level repository meant for individuals who want to gain experience in developing a semantic search engine to supplement Large Language models (LLM's) performance with Retrieval-Augmented Generation (RAG) framework. The application developed in this workshop is intended for educational purposes and can serve as an inspiration for production-level applications.

## Architecture
</br>
![Architecture Diagram](/images/Architecture.png)

## Semantic Search Engine and Retrieval-Augmented Generation (RAG)

**Retrieval-Augmented Generation (RAG)** is an AI framework for retrieving facts from an external knowledge base to ground **Large Language Models (LLMs)** on the most accurate, up-to-date information and to give users insight into LLMs' generative process.

In a RAG model, **a retriever component**, semantic search engine, first retrieves relevant passages or documents from a large corpus, and then a **generator component**, large language model, utilizes this retrieved information to generate a detailed response or answer. This two-step process allows RAG models to leverage the benefits of both retrieval and generation approaches.

This repository introduces an architecture for the retrieval component of the RAG model using **Amazon OpenSearch** as a vector database and **Amazon Bedrock Titan Embeddings G1 - Text** base model to create embeddings.

***Note: Check Amazon OpenSearch serverless availability in your [region](https://aws.amazon.com/about-aws/whats-new/2023/01/amazon-opensearch-serverless-available/).***

***Note: In this repository we are using [AWS Systems Manager Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html). However, when dealing with sensitive secrets such as Database credentials, the best practice is to use [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/).***

## Pre-requisites

1. Basic experience working with Amazon Web Services (AWS) environment.
2. An AWS Account, to deploy the infrastructure. You can find more instructions [here](https://aws.amazon.com/free/).
3. Basic knowledge with [Amazon S3](https://aws.amazon.com/s3/), [Amazon Bedrock](https://aws.amazon.com/bedrock/), [AWS Amplify](https://aws.amazon.com/amplify/), [Amazon API Gateway](https://aws.amazon.com/api-gateway/), [AWS Lambda](https://aws.amazon.com/pm/lambda/), [Amazon OpenSearch](https://aws.amazon.com/opensearch-service/), [AWS Cloud9](https://aws.amazon.com/pm/cloud9/), [Amazon DynamoDB](https://aws.amazon.com/pm/dynamodb), [AWS CloudFormation](https://aws.amazon.com/cloudformation/), and [AWS Systems Manager Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html).
4. IAM User with Aministrator privileges and [Access keys and Secret Access keys](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey_CLIAPI). 

***Note: It is best practice to grant least-privilege to all IAM users, however, for simplicity for deployment we are using Admin user. For a production ready environment please follow [Techniques for writing least privilege IAM policies](https://aws.amazon.com/blogs/security/techniques-for-writing-least-privilege-iam-policies/) for further instructions.***

## Intructions
</br>

1. Request model access for Titan Embedding G1 - Text, follow instructions [here](https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html). 

2. Create AWS Cloud9 environment, clone repository, and Create OpenSearch collection. Follow instructions [here](/scripts/README.md).

3. Create the CloudFormation Stack, follow instructions [here](/cfn_stack/README.md).

***Note: If your data is sensitive in nature or you want increased security consider [Protecting your Rest API](https://docs.aws.amazon.com/apigateway/latest/developerguide/rest-api-protect.html). For a production ready application [control and manage access to the REST API in API Gateway](https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-control-access-to-api.html).***

4. Deploy the serverless frontend using AWS Amplify, follow instructions [here](/frontend/README.md).

## Demo

![Demo](/images/demo.png)

Try running "Graphic Design", "Sports", "India", and "United States" as the query.

## Clean-Up
</br>
In order to avoid incurring any cost and as a general best practice, please follow the steps to clean up the resources.

1. Delete the AWS Cloud9 environment. 
2. [Empty](https://docs.aws.amazon.com/AmazonS3/latest/userguide/empty-bucket.html) the Amazon S3 Bucket.
3. Delete the AWS CloudFormation stack.
4. Delete the Amazon OpenSearch Collection and Index.
5. Delete the AWS Lambda Layer. 
6. Delete the web app from AWS Amplify.

## Security
</br>

See the [CONTRIBUTING](CONTRIBUTING.md) file for more information.

## License
</br>

See the [LICENSE](LICENSE) file for our project's licensing.
