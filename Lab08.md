# Lab Session 8: Serverless applications

**Serverless applications** are applications that run without the need for server management by the developer. In a serverless model, cloud providers handle the infrastructure, scaling, and management of servers. Developers only focus on writing and deploying code, which is executed in response to events, such as HTTP requests, database changes, or file uploads.

#### Key features of serverless applications:
- **No Server Management**: Developers don’t need to provision or maintain servers.
- **Event-driven**: Functions are executed in response to specific events.
- **Scalability**: The cloud provider automatically scales resources based on demand.
- **Cost-efficient**: You pay only for the execution time of the functions, not for idle server resources.

### AWS Lambda

**AWS Lambda** is a fully managed **serverless computing service** provided by AWS. It allows developers to run code in response to events without provisioning or managing servers.

#### Key Features of AWS Lambda:

- **Serverless**: eliminating the need to maintain infrastructure and reducing overhead.

- **Event-Driven**: designed to be triggered by various AWS services or external events, such as:
     - **S3** events (e.g., file uploads)
     - **API Gateway** requests (for building APIs)
     - **DynamoDB** streams (e.g., when data is added/modified)
     - **CloudWatch Events** (e.g., scheduled jobs)
     - **SNS** (Simple Notification Service) messages
     - **Cognito** triggers (for user sign-up/sign-in events)
     - And many other sources (including custom event sources).

- **Scalability**: automatically scales the number of execution environments to match the incoming event load. If there are hundreds or thousands of events, Lambda can scale to handle them without any manual intervention. It scales **horizontally** by running multiple instances of your function in parallel when needed.

- **Pay-As-You-Go Pricing**: pay for the compute time used by the code than runs. The billing is based on the number of requests and the duration of the code execution (in milliseconds).

- **Stateless**: each invocation of an AWS Lambda function is stateless, meaning it doesn’t retain any state between executions. If you need to maintain state, you can use AWS services like **DynamoDB** or **S3** to store persistent data.

- **Customizable Execution Role**: using **IAM (Identity and Access Management)** for granting them permissions to interact with other AWS services securely.

- **Short-lived Execution**: functions can run for a maximum of 15 minutes per invocation. Best suited for tasks that can be completed quickly, such as real-time data processing, image resizing, API responses, etc.

- **Logging and Monitoring**: integrated with **Amazon CloudWatch**.

### AWS API Gateway

AWS API Gateway is a fully managed service provided by Amazon Web Services (AWS) that enables developers to create, publish, maintain, monitor, and secure APIs at any scale. API Gateway acts as an entry point for applications, enabling communication between client apps (mobile, web, etc.) and backend services (AWS Lambda, EC2, other HTTP services).

#### Key Features of AWS API Gateway:

- **Create and Manage APIs**: RESTful APIs, WebSocket APIs, or HTTP APIs to connect to services like AWS Lambda, HTTP endpoints, or other AWS services.
   
- **Support for Multiple Protocols**: HTTP, WebSocket, and REST APIs.
   
- **Security**: allows you to authenticate and authorize API calls through services like AWS IAM (Identity and Access Management), Amazon Cognito, and Lambda authorizers.

- **Rate Limiting and Throttling**: seting of rate limits and throttling policies to control traffic, protect backend resources, and prevent abuse.

- **Scaling**: automatically scales to handle varying amounts of traffic, ensuring that your APIs perform well under different load conditions.

- **Logging and Monitoring**: integrates with AWS CloudWatch for logging and monitoring API usage, errors, and performance metrics.
   
- **Caching** responses to reduce load on backend services, improving performance for repeated requests.

- **Deployments and Versioning**: management of different stages of an API (development, staging, production) and deploy changes in a controlled manner.

#### Use Cases of AWS API Gateway:
- **Serverless Applications**: Often used with AWS Lambda to create serverless APIs, where no infrastructure management is needed.
- **Microservices**: API Gateway can serve as the entry point to microservices, handling incoming requests and routing them to different backend services.
- **Mobile and Web Applications**: Provides a reliable way to manage API calls from mobile apps and websites.

### WebSockets

**WebSockets** are a communication protocol that enables **full-duplex** (two-way) communication channels over a single, long-lived connection between a client (usually a web browser) and a server. Unlike the traditional HTTP request-response model, which is **stateless** and works in a **request-response** pattern, WebSockets provide a persistent, open connection that allows continuous, real-time data exchange between the client and server.

#### Advantages of WebSockets:

- **Real-Time Communication**: WebSockets enable instant communication between the client and server, making them ideal for real-time applications.
- **Reduced Latency**: Since the connection is persistent, there’s no need to repeatedly open and close connections, which results in lower latency.
- **Efficiency**: WebSockets use less bandwidth and are more efficient than HTTP for frequent message exchanges, as they avoid the overhead of HTTP headers with every request.
- **Lower Overhead**: There’s less overhead compared to HTTP polling or long-polling because WebSockets maintain a single connection, and data can be sent immediately when available.

#### Limitations of WebSockets:

- **Browser and Network Compatibility**: WebSockets require support from the client (browser or app) and the server. Some firewalls or proxies might block WebSocket traffic.
- **Single Connection**: WebSockets typically use a single connection for each client, which can become limiting if you need to scale to millions of users.
- **No Built-In Message Queuing**: WebSockets don’t provide built-in message persistence, so you need to implement your own system for queuing or persisting messages.

#### How WebSockets Work:

- **Handshake**: a WebSocket connection starts with an HTTP handshake. The client sends an HTTP request to the server with an **Upgrade** header, indicating that it wants to establish a WebSocket connection.
   
   - Example WebSocket request:
     ```
     GET /chat HTTP/1.1
     Host: example.com
     Upgrade: websocket
     Connection: Upgrade
     Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
     Sec-WebSocket-Version: 13
     ```

- **Connection Upgrade**: If the server supports WebSockets, it responds with a status code **101 Switching Protocols**, indicating that the protocol has been switched to WebSocket and the connection is now open.
   
   - Example WebSocket response:
     ```
     HTTP/1.1 101 Switching Protocols
     Upgrade: websocket
     Connection: Upgrade
     Sec-WebSocket-Accept: dGhlIHNhbXBsZSBub25jZQ==
     ```

- **Data Exchange**: After the handshake, the connection is upgraded to WebSocket, and both the client and the server can send messages back and forth in real time. WebSocket messages can be sent in text or binary format, making it flexible for various types of data.

- **Closing the Connection**: Either the client or the server can close the WebSocket connection at any time by sending a **close frame**. Once the connection is closed, no more messages can be sent or received.

#### Common Use Cases of WebSockets:

- Real-Time Messaging and Chat Applications.
- Online Gaming.
- Stock Market or Financial Applications for instant value update (e.g., stock prices, cryptocurrency rates).
- Live Sports Updates.
- Collaborative Applications with real-time updates (e.g., Google Docs)
- IoT (Internet of Things) communication between IoT devices (e.g., smart home devices, sensors) and control systems
- Push Notifications in web applications

# Pre-lab homework

In this lab session we'll be creating a REST API. Therefore, you first, create a DynamoDB table named `ccbda-lambda-first` with `thingID` as the partition key.

### **Understanding `kwargs` in Python:**

In Python, **`kwargs`** (short for **keyword arguments**) allows you to pass a variable number of named arguments to a function, which are then collected into a dictionary.

##### **Example:**
```python
def greet_user(**kwargs):
    print(kwargs)

greet_user(name="Alice", age=30)

params = {'name': 'Alice', 'age': 30}
greet_user(**params)
```
In both cases the output is
```python
{'name': 'Alice', 'age': 30}
```

# Tasks

## Task 8.1: Simple serverless web application

### CRUD REST API : Implementing the 4 Basic Operations in Software Development

**CRUD** stands for **Create, Read, Update, Delete**, which are the four fundamental operations used in databases and APIs to manage data.

| **Operation** | **Description** | **Example in SQL** | **Example in REST API** |
|--------------|---------------|-------------------|------------------|
| **Create**   | Adds new data | `INSERT INTO users (name, email) VALUES ('John', 'john@example.com');` | `POST /users` |
| **Read**     | Retrieves data | `SELECT * FROM users WHERE id = 1;` | `GET /users/1` |
| **Update**   | Modifies existing data | `UPDATE users SET name = 'Jane' WHERE id = 1;` | `PUT /users/1` |
| **Delete**   | Removes data | `DELETE FROM users WHERE id = 1;` | `DELETE /users/1` |

Such operations can be applied in different contexts.

- **REST APIs**: CRUD maps to HTTP methods (`POST`, `GET`, `PUT`, `DELETE`).
- **Databases**: CRUD operations are used to manipulate records (SQL, MongoDB, Firebase).
- **User Interfaces**: A CRUD-based UI allows users to **add, view, edit, and delete** items.

### Deploying the CRUD Lambda function

Download the [serverless-app repository](https://github.com/CCBDA-UPC/serverless-app) as a ZIP file and add it to your project repository. 

Inside the `crud` folder, you'll find an AWS Lambda function written in Python. This function establishes a connection to DynamoDB and waits to be invoked by the AWS API Gateway. Depending on the HTTP method (GET, POST, etc.) received, it will perform different operations on the database.

We’ll use `kwargs` to dynamically pass the values of parameters directly to the `boto3` operations in our Lambda function.
Check the [Boto3 DynamoDB documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html)
for more information on the [`scan`](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/scan.html), [`put_item`](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/put_item.html), [`delete_item`](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/delete_item.html), and [`update_item`](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb/client/update_item.html) functions.

```python
import boto3
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.client('dynamodb', region_name='us-east-1')

def lambda_handler(event, context):
    operation = event['requestContext']['http']['method']
    logger.info(f'operation {operation}')
    try:
        if operation == 'GET':
            return respond(dynamodb.scan(**event['queryStringParameters']))
        elif operation == 'POST':
            return respond(dynamodb.put_item(**json.loads(event['body'])))
        elif operation == 'DELETE':
            return respond(dynamodb.delete_item(**json.loads(event['body'])))
        elif operation == 'PUT':
            return respond(dynamodb.update_item(**json.loads(event['body'])))
        elif operation == 'OPTIONS':
            return respond('')
        else:
            return respond(None, f'Unsupported method "{operation}"')
    except Exception as e:
        respond(None, f'{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}')

def respond(res, err=None):
    response = {
        'statusCode': '200' if err is None else '400',
        'body': json.dumps(res) if err is None else err,
        'headers': {
            'Content-Type': 'application/json',
            "Access-Control-Allow-Headers": "Content-Type",
            'Access-Control-Allow-Origin': '*',
            "Access-Control-Allow-Methods": "GET, POST, DELETE, PUT, OPTIONS",
        },
    }
    logger.info(f'response {json.dumps(response, indent=2)}')
    return response
```

The file `requirements.txt` in the `crud` folder defines the Python environment for the above function to be executed.

We are going to use the **AWS CLI** to deploy the **Lambda function** and build the **API Gateway**. Open a terminal and set the variables to the corresponding value. Create a zip file with the Python code and its requirements. The command `aws lambda create-function` sends the zip file to AWS. In response, it obtains a JSON record with some values that we'll be needing to use for future steps, i.e. `LAMBDA_ARN` needs to be updated to the value of the response field `FunctionArn`.

```bash
_$ ACCOUNT_ID=<YOUR-ACCOUNT-ID>
_$ REGION=us-east-1
_$ cd crud
_$ zip lambda_crud.zip lambda_crud.py requirements.txt
updating: lambda_crud.py (deflated 64%)
updating: requirements.txt (deflated 19%)
_$ aws lambda create-function --function-name LambdaCRUD \
  --zip-file fileb://lambda_crud.zip \
  --handler lambda_crud.lambda_handler \
  --runtime python3.13 \
  --role arn:aws:iam::${ACCOUNT_ID}:role/LabRole
{
    "FunctionName": "LambdaCRUD",
    "FunctionArn": "arn:aws:lambda:us-east-1:<YOUR-ACCOUNT-ID>:function:LambdaCRUD",
    "Runtime": "python3.13",
    "Role": "arn:aws:iam::992382765078:role/LabRole",
    "Handler": "lambda_crud.lambda_handler",
    "CodeSize": 1147,
    "Description": "",
    "Timeout": 3,
    "MemorySize": 128,
    "LastModified": "2025-03-12T15:24:35.266+0000",
    "CodeSha256": "CX13dQVlx3hpf3YOcDh07USeHFRcGLfjX6hTKiF/bX8=",
    "Version": "$LATEST",
    "TracingConfig": {
        "Mode": "PassThrough"
    },
    "RevisionId": "ae25f8b8-1d06-4bc9-826e-3d56c0df3d0e",
    "State": "Pending",
    "StateReason": "The function is being created.",
    "StateReasonCode": "Creating"
}
_$ LAMBDA_ARN="arn:aws:lambda:us-east-1:<YOUR-ACCOUNT-ID>:function:LambdaCRUD"
```

In Unix, using the command `jq` ([more info](https://jqlang.org/)) and the backquotes ``` we can execute the command and automatically extract the JSON field value to set the LAMBDA_ARN variable.

```bash
_$ LAMBDA_ARN=`aws lambda create-function --function-name LambdaCRUD \
  --zip-file fileb://lambda_crud.zip \
  --handler lambda_crud.lambda_handler \
  --runtime python3.13 \
  --role arn:aws:iam::${ACCOUNT_ID}:role/LabRole \
  | jq '.FunctionArn' `
_$ echo $LAMBDA_ARN
"arn:aws:lambda:us-east-1:<YOUR-ACCOUNT-ID>:function:LambdaCRUD"
```

Once the Lambda function is deployed you can go to the AWS Lambda console and see the outcome of the above commands.

<img alt="Lab08-LambdaConsole.png" src="images/Lab08-LambdaConsole.png" width="100%"/>


#### Summary of Commands

- **Zip the Lambda code**:
   ```bash
   zip function.zip lambda_function.py
   ```

- **Create the Lambda function**:
   ```bash
   aws lambda create-function --function-name my-lambda-function \
     --zip-file fileb://function.zip \
     --handler lambda_function.lambda_handler \
     --runtime python3.13 \
     --role arn:aws:iam::your-account-id:role/lambda-execution-role
   ```

- **Invoke the Lambda function**:
   ```bash
   aws lambda invoke --function-name my-lambda-function output.txt
   ```

- **Update the Lambda function** (if needed):
   ```bash
   aws lambda update-function-code --function-name my-lambda-function \
     --zip-file fileb://function.zip
   ```

- **Delete the Lambda function** (if needed):
   ```bash
   aws lambda delete-function --function-name my-lambda-function
   ```

### API Gateway creation

To allow the Lambda function to be accessed by any API Gateway it is necessary to create a "statement" with a unique value for the parameter `statement-id`. The Unix command `uuidgen` creates a random value to be used by the command `aws lambda add-permission` which creates that premission. Please note the ``` backslashes used in the first command.

```bash
_$ STATEMENT_ID=`uuidgen`
_$ echo $STATEMENT_ID
CDCFB599-79CC-4877-B480-6B97B4125D4D
_$ aws lambda add-permission \
  --function-name LambdaCRUD \
  --principal apigateway.amazonaws.com \
  --statement-id "${STATEMENT_ID}" \
  --action lambda:InvokeFunction
{
    "Statement": "{\"Sid\":\"CDCFB599-79CC-4877-B480-6B97B4125D4D\",\"Effect\":\"Allow\",\"Principal\":{\"Service\":\"apigateway.amazonaws.com\"},\"Action\":\"lambda:InvokeFunction\",\"Resource\":\"arn:aws:lambda:us-east-1:992382765078:function:LambdaCRUD\"}"
}
```

To create the API Gateway named "CrudHttpAPI" of HTTP type we use `aws apigatewayv2 create-api` that produces, amongst others, the "ApiId" field used to set the value of the variable `API_ID`.
You can use `jq` instead of doing it manually.

```bash
_$ aws apigatewayv2 create-api \
  --name "CrudHttpAPI" \
  --protocol-type HTTP
{
    "ApiEndpoint": "https://9h1wag0ywe.execute-api.us-east-1.amazonaws.com",
    "ApiId": "9h1wag0ywe",
    "ApiKeySelectionExpression": "$request.header.x-api-key",
    "CreatedDate": "2025-03-12T15:25:33+00:00",
    "Name": "CrudHttpAPI",
    "ProtocolType": "HTTP",
    "RouteSelectionExpression": "$request.method $request.path"
}
_$ API_ID=9h1wag0ywe
```

The following step uses `aws apigatewayv2 create-integration` to bind the created API Gateway with the Lambda function deployed before. Make sure that you save the value of the `INTEGRATION_ID` variable using the "IntegrationId" response field.

```bash
_$ aws apigatewayv2 create-integration \
    --api-id ${API_ID} \
    --integration-type AWS_PROXY \
    --integration-uri ${LAMBDA_ARN} \
    --integration-method ANY \
    --payload-format-version 2.0
{
    "ConnectionType": "INTERNET",
    "IntegrationId": "wp0uj9i",
    "IntegrationMethod": "ANY",
    "IntegrationType": "AWS_PROXY",
    "IntegrationUri": "arn:aws:lambda:us-east-1:992382765078:function:LambdaCRUD",
    "PayloadFormatVersion": "2.0",
    "TimeoutInMillis": 30000
}
_$ INTEGRATION_ID=wp0uj9i
```

Now, `aws apigatewayv2 create-route` creates different routes in the API Gateway, one for each HTTP **method** and **path**. In this example all methods use the same Lambda function, but usually different Lambda functions serve each HTTP method and path.

```bash
_$ aws apigatewayv2 create-route \
  --api-id ${API_ID} \
  --route-key "GET /" \
  --target "integrations/${INTEGRATION_ID}"
{
    "ApiKeyRequired": false,
    "AuthorizationType": "NONE",
    "RouteId": "6jrmmkf",
    "RouteKey": "GET /",
    "Target": "integrations/wp0uj9i"
}
_$ aws apigatewayv2 create-route \
  --api-id ${API_ID} \
  --route-key "POST /" \
  --target "integrations/${INTEGRATION_ID}"
{
    "ApiKeyRequired": false,
    "AuthorizationType": "NONE",
    "RouteId": "zay7v4g",
    "RouteKey": "POST /",
    "Target": "integrations/wp0uj9i"
}
_$ aws apigatewayv2 create-route \
  --api-id ${API_ID} \
  --route-key "OPTIONS /" \
  --target "integrations/${INTEGRATION_ID}"
{
    "ApiKeyRequired": false,
    "AuthorizationType": "NONE",
    "RouteId": "b2qe62a",
    "RouteKey": "OPTIONS /",
    "Target": "integrations/wp0uj9i"
}
_$ aws apigatewayv2 create-route \
  --api-id ${API_ID} \
  --route-key "PUT /" \
  --target "integrations/${INTEGRATION_ID}"
{
    "ApiKeyRequired": false,
    "AuthorizationType": "NONE",
    "RouteId": "hjwebad",
    "RouteKey": "PUT /",
    "Target": "integrations/wp0uj9i"
}
_$ aws apigatewayv2 create-route \
  --api-id ${API_ID} \
  --route-key "DELETE /" \
  --target "integrations/${INTEGRATION_ID}"
{
    "ApiKeyRequired": false,
    "AuthorizationType": "NONE",
    "RouteId": "9kyl2hi",
    "RouteKey": "DELETE /",
    "Target": "integrations/wp0uj9i"
}
```

As mentioned above, each API Gateway can have different stages: *production*, *development*, *testing*, etc. We are only going to create one stage named "prod" that will need to be manually deployed. Changing `--not-auto-deploy` to `--auto-deploy` will make it redeploy as soon as there is a change in the configuration or the Lambda function.

```bash
_$ STAGE="prod"
_$ aws apigatewayv2 create-stage \
  --api-id ${API_ID} \
  --stage-name ${STAGE}
  --no-auto-deploy
{
    "CreatedDate": "2025-03-12T15:30:24+00:00",
    "DefaultRouteSettings": {
        "DetailedMetricsEnabled": false
    },
    "LastUpdatedDate": "2025-03-12T15:30:25+00:00",
    "RouteSettings": {},
    "StageName": "prod",
    "StageVariables": {},
    "Tags": {}
}
```

Finally, `aws apigatewayv2 create-deployment` allows the API Gateway to be deployed and ready to be used. The "**CrudHttpAPI**" API Gateway URL is composed using the value of different variables set up above: `https://${API_ID}.execute-api.${REGION}.amazonaws.com/${STAGE}/`

```bash
_$ aws apigatewayv2 create-deployment --api-id ${API_ID} --stage-name prod
{
    "AutoDeployed": false,
    "CreatedDate": "2025-03-12T15:40:58+00:00",
    "DeploymentId": "01jigd",
    "DeploymentStatus": "DEPLOYED"
}
_$ URL="https://${API_ID}.execute-api.${REGION}.amazonaws.com/${STAGE}/"
_$ echo $URL
https://9h1wag0ywe.execute-api.us-east-1.amazonaws.com/prod/
```

Go to the AWS API Gateway console and see the outcome of the above commands.

<img alt="Lab08-APIGateway.png" src="images/Lab08-APIGateway.png" width="100%"/>

### Test the REST API

[**Postman**](https://www.postman.com) is a popular API development and testing tool that allows developers to send HTTP requests to web servers and view responses. It provides an easy-to-use interface for testing RESTful APIs, making it simple to construct and send requests, view responses, and automate tests. Postman supports features like request chaining, environment variables, collections, and collaboration, making it a powerful tool for API development and debugging.

Use this [URL](https://www.postman.com/ccbda-upc-edu/serverless/request/ck4fxrd/testing?action=share&creator=43659146&ctx=documentation&active-environment=43659146-8433b233-679d-4f13-a332-b972334ca409) to access the Postman web interface where there are some REST API calls to test the above deployed CRUD API Gateway. You can also download the Postman desktop app and import the testing collection of operations into your laptop. 

The testing collection is using two variables defined in the Postman environment named "CRUD". Make sure that the Postman environment named "CRUD" is selected before testing the HTTP operations.

<img alt="Lab08-Postman-collections.png" src="images/Lab08-Postman-collections.png" width="100%"/>

The variable in the Postman environment named "CRUD".

<img alt="Lab08-Postman-environments.png" src="images/Lab08-Postman-environments.png" width="100%"/>

### Use the REST API

Once the API is tested, you can see it working inside a web page. The files in the `webpage1` folder of the zip file that you downloaded, are a mininmal web page using the REST API built above. But before opening in your browser the file "index.html", you need to change the value of the variable `apiUrl` to the current value of the "**CrudHttpAPI**" API Gateway.

The JavaScript code uses jQuery to create a "GET" request as soon as the web page loads and a "POST" request when the visitor submits the form.

```javascript
(function ($) {
    apiUrl = "https://9h1wag0ywe.execute-api.us-east-1.amazonaws.com/prod/"
    TableName = 'ccbda-lambda-first';

    $.ajax({
        type: 'GET',
        url: apiUrl,
        data: {'TableName': TableName},
        crossDomain: true,
        success: function (result) {
            $.each(result.Items, function (i, item) {
                $('#items').append('<li>' + item.thingID.S + '</li>');
            });
        },
        error: function (xhr, status, error) {
            $('#error').toggle().append('<div>' + error + '</div>');
        }
    });

    // Form submit
    $("#form").submit(function (event) {
        event.preventDefault();
        thingID = $('#thingID').val();
        payload = {
            'TableName': TableName,
            'Item': {
                'thingID': {
                    'S': thingID
                }
            }
        }
        $.ajax({
            type: 'POST',
            url: apiUrl,
            crossDomain: true,
            contentType: 'application/json',
            data: JSON.stringify(payload),
            cache: false,
            success: function (result) {
                $('#thingID').val('');
                $('#items').append('<li>' + thingID + '</li>');
            },
            error: function (xhr, status, error) {
                $('#error').toggle().append('<div>' + status + ',' + error + '</div>');
            }
        });
    });
})(jQuery);
```

Open the "index.html" file using your browser and start to create items in the list.

<img alt="Lab08-webpage.png" src="images/Lab08-webpage.png" width="80%"/>


### Observability

You may have noticed that the Lambda function includes some logging calls. Open the AWS CloudWatch console and check the outcome.

<img alt="Lab08-CloudWatch.png" src="images/Lab08-CloudWatch.png" width="100%"/>


**Q811: Assess the current version of the web application against each of the twelve factor application.**

**Q812: Play with the application and with AWS CloudWatch logs that you have obtained. Share your insights.**


# Task 8.2: Simple serverless using WebSockets


To create the new API Gateway we will follow similar steps. Now `--protocol-type` is set to `WEBSOCKET` for WebSocket APIs. The parameter `--route-selection-expression` defines the routing logic based on the WebSocket messages. In this example, it routes based on the `action` field in the incoming WebSocket messages (`$request.body.action`).

```bash
_$ aws apigatewayv2 create-api \
  --name "MyWebSocketAPI" \
  --protocol-type WEBSOCKET \
  --route-selection-expression "$request.body.action"
{
    "ApiEndpoint": "wss://ww0pxtgs8g.execute-api.us-east-1.amazonaws.com",
    "ApiId": "ww0pxtgs8g",
    "ApiKeySelectionExpression": "$request.header.x-api-key",
    "CreatedDate": "2025-04-04T09:53:49+00:00",
    "Name": "MyWebSocketAPI",
    "ProtocolType": "WEBSOCKET",
    "RouteSelectionExpression": ".body.action"
}
_$ API_ID=ww0pxtgs8g
```

```bash
_$ aws apigatewayv2 create-integration \
    --api-id ${API_ID} \
    --integration-type AWS_PROXY \
    --integration-uri ${LAMBDA_ARN} \
    --integration-method ANY \
    --payload-format-version 2.0

_$ INTEGRATION_ID=
```

In a WebSocket API, you define **routes** that map to different actions or message types. For example, you may define routes for `connect`, `disconnect`, and custom message types like `sendMessage`.

- **Connect Route**: Triggered when a client connects to the WebSocket.
- **Disconnect Route**: Triggered when a client disconnects.
- **Custom Routes**: Any custom action you want to handle in your WebSocket API.

Let’s create the `connect` and `disconnect` routes. `--route-key` sets the route identifier. For the `connect` route, use `$connect`, and for the `disconnect` route, use `$disconnect`.

```bash
_$ aws apigatewayv2 create-route \
  --api-id ${API_ID} \
  --route-key "$connect" \
  --target "integrations/${INTEGRATION_ID}"

_$ aws apigatewayv2 create-route \
  --api-id ${API_ID} \
  --route-key "$disconnect" \
  --target "integrations/${INTEGRATION_ID}"
```


### Summary of AWS CLI Commands for WebSocket API:

- **Create the WebSocket API**:
   ```bash
   aws apigatewayv2 create-api \
     --name "MyWebSocketAPI" \
     --protocol-type WEBSOCKET \
     --route-selection-expression "$request.body.action"
   ```

- **Create Routes (e.g., connect, disconnect)**:
   ```bash
   aws apigatewayv2 create-route \
     --api-id m96mpy7qz4 \
     --route-key "$connect" \
     --target "integrations/<integration-id>"
   ```

   ```bash
   aws apigatewayv2 create-route \
     --api-id m96mpy7qz4 \
     --route-key "$disconnect" \
     --target "integrations/<integration-id>"
   ```

- **Create Lambda Integration**:
   ```bash
   aws apigatewayv2 create-integration \
     --api-id m96mpy7qz4 \
     --integration-type AWS_PROXY \
     --integration-uri arn:aws:lambda:us-west-2:123456789012:function:MyLambdaFunction \
     --payload-format-version 2.0
   ```

- **Grant API Gateway Permission to Invoke Lambda**:
   ```bash
   aws lambda add-permission --function-name MyLambdaFunction \
     --principal apigateway.amazonaws.com \
     --statement-id <unique-id> \
     --action "lambda:InvokeFunction"
   ```

- **Deploy the WebSocket API**:
   ```bash
   aws apigatewayv2 create-stage \
     --api-id m96mpy7qz4 \
     --stage-name prod \
     --auto-deploy
   ```

- **Test the WebSocket API**:
   - Use `wscat` or any WebSocket client to connect to:
     ```bash
     wscat -c wss://m96mpy7qz4.execute-api.us-west-2.amazonaws.com/prod
     ```










##### Client-Side Example in JavaScript (Web Browser):

You can test this WebSocket server using the following JavaScript client code in the browser.
Save the JavaScript code in a file called `client.js`, then open the HTML file in your web browser.

```javascript
// Create a new WebSocket connection to the server
const socket = new WebSocket('ws://localhost:8765');

// When the WebSocket connection is established
socket.onopen = function(event) {
    console.log("Connected to the server!");
    socket.send('Hello, Server!');
};

// When a message is received from the server
socket.onmessage = function(event) {
    console.log("Message from server:", event.data);
};

// When the WebSocket connection is closed
socket.onclose = function(event) {
    console.log("Disconnected from the server.");
};

// Handling errors
socket.onerror = function(error) {
    console.log("WebSocket error:", error);
};
```

##### How to Test:

- **Run the Python WebSocket Server**:
   - Save the Python WebSocket server code to a file (e.g., `websocket_server.py`).
   - Run the server:
     ```bash
     python websocket_server.py
     ```

- **Run the JavaScript Client**:
   - You can open the JavaScript code in the browser by saving it in an HTML file or running it in the browser console.
   
   Example HTML file:
   ```html
   <!DOCTYPE html>
   <html lang="en">
   <head>
       <meta charset="UTF-8">
       <meta name="viewport" content="width=device-width, initial-scale=1.0">
       <title>WebSocket Client</title>
   </head>
   <body>
       <h1>WebSocket Client</h1>
       <script src="client.js"></script>
   </body>
   </html>
   ```



























Q823: Assess the current version of the web application against each of the twelve factor application.

Q824: How long have you been working on this session? What have been the main difficulties that you have faced and how have you solved them? Add your answers to README.md.

## How to submit this assignment:

Make sure that you have updated your local GitHub repository (using the git commands add, commit, and push) with all the files generated during this session.

Before the deadline, all team members shall push their responses to their private https://github.com/CCBDA-UPC/2024-8-xx repository.

Add all the web application files to your repository and comment what you think is relevant in your session's *README.md*.