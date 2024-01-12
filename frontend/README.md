# Deploy the serverless frontend using AWS Amplify

1. In the file [apigClient.js](/frontend/amplify/apigClient.js) replace *invokeUrl* variable with your API Gateway url. Refer AWS CloudFormation Outputs for API Gateway Invoke URL. 

![apigClient.js](/frontend/images/1.png)

2. In AWS Amplify console, create a new Web app, deploy without a Git Provider and finally Drag and drop the [amplify](/frontend/amplify/) directory.

![drage and drop](/frontend/images/2.png)

Use the *domain* to query the backend!