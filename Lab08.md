### AWS API Gateway

AWS API Gateway is a fully managed service provided by Amazon Web Services (AWS) that enables developers to create, publish, maintain, monitor, and secure APIs at any scale. API Gateway acts as an entry point for applications, enabling communication between client apps (mobile, web, etc.) and backend services (AWS Lambda, EC2, other HTTP services).

### Key Features of AWS API Gateway:
1. **Create and Manage APIs**: 
   - You can create RESTful APIs, WebSocket APIs, or HTTP APIs to connect to services like AWS Lambda, HTTP endpoints, or other AWS services.
   
2. **Support for Multiple Protocols**: 
   - API Gateway supports HTTP, WebSocket, and REST APIs, making it versatile for various use cases.
   
3. **Security**:
   - API Gateway allows you to authenticate and authorize API calls through services like AWS IAM (Identity and Access Management), Amazon Cognito, and Lambda authorizers.
   - It also supports encryption and custom domain names.

4. **Rate Limiting and Throttling**:
   - You can set rate limits and throttling policies to control traffic, protect backend resources, and prevent abuse.

5. **Scaling**:
   - API Gateway automatically scales to handle varying amounts of traffic, ensuring that your APIs perform well under different load conditions.

6. **Logging and Monitoring**:
   - It integrates with AWS CloudWatch for logging and monitoring API usage, errors, and performance metrics.
   
7. **Caching**:
   - API Gateway supports caching responses to reduce load on backend services, improving performance for repeated requests.

8. **Deployments and Versioning**:
   - You can manage different stages of an API (development, staging, production) and deploy changes in a controlled manner.

### Use Cases:
- **Serverless Applications**: Often used with AWS Lambda to create serverless APIs, where no infrastructure management is needed.
- **Microservices**: API Gateway can serve as the entry point to microservices, handling incoming requests and routing them to different backend services.
- **Mobile and Web Applications**: Provides a reliable way to manage API calls from mobile apps and websites.


### Benefits:
- **Low Management Overhead**: Fully managed service, so you don’t need to worry about server management or scaling.
- **Security**: Built-in support for securing APIs through authentication, authorization, and encryption.
- **Cost-Effective**: Pay only for the API calls you make, with no upfront costs or fixed fees.




## AWS Lambda

**AWS Lambda** is a fully managed **serverless computing service** provided by Amazon Web Services (AWS). It allows developers to run code in response to events without provisioning or managing servers. In simple terms, AWS Lambda lets you focus purely on your code, while AWS takes care of all the infrastructure needed to run and scale your application.

### Key Features of AWS Lambda:

1. **Serverless**:
   - You don’t have to worry about provisioning or managing servers. AWS Lambda automatically manages the compute resources for you, scaling them as needed based on incoming requests or events.
   - This eliminates the need to maintain infrastructure and reduces overhead.

2. **Event-Driven**:
   - AWS Lambda is designed to be triggered by various AWS services or external events, such as:
     - **S3** events (e.g., file uploads)
     - **API Gateway** requests (for building APIs)
     - **DynamoDB** streams (e.g., when data is added/modified)
     - **CloudWatch Events** (e.g., scheduled jobs)
     - **SNS** (Simple Notification Service) messages
     - **Cognito** triggers (for user sign-up/sign-in events)
     - And many other sources (including custom event sources).

3. **Scalability**:
   - AWS Lambda automatically scales the number of execution environments to match the incoming event load. If there are hundreds or thousands of events, Lambda can scale to handle them without any manual intervention.
   - It scales **horizontally** by running multiple instances of your function in parallel when needed.

4. **Pay-As-You-Go Pricing**:
   - With AWS Lambda, you only pay for the compute time you use, i.e., the time your code runs. You are billed based on the number of requests and the duration of your code execution (in milliseconds).
   - No charges for idle time – Lambda only charges when the function is triggered.


6. **Stateless**:
   - Each invocation of an AWS Lambda function is stateless, meaning it doesn’t retain any state between executions. If you need to maintain state, you can use AWS services like **DynamoDB** or **S3** to store persistent data.

7. **Customizable Execution Role**:
   - You can configure **IAM (Identity and Access Management)** roles for Lambda functions, granting them permissions to interact with other AWS services securely.
   - This enables Lambda functions to read from/write to S3, DynamoDB, or any other AWS service you need to interact with.

8. **Short-lived Execution**:
   - AWS Lambda functions can run for a maximum of 15 minutes per invocation. If the function doesn't complete within this time frame, it will be terminated. This makes Lambda best suited for tasks that can be completed quickly, such as real-time data processing, image resizing, API responses, etc.

9. **Logging and Monitoring**:
   - AWS Lambda integrates with **Amazon CloudWatch** for logging and monitoring, so you can track metrics such as the number of invocations, execution time, error rates, and more.
   - Logs are automatically generated by Lambda, making it easy to debug and monitor function performance.

    
### Benefits of AWS Lambda:

- **No Server Management**: You don’t have to provision or manage servers.
- **Automatic Scaling**: Automatically scales depending on the number of requests/events, handling any workload.
- **Cost-Effective**: Pay only for the compute time used, with no cost for idle time.
- **Quick Deployment**: You can deploy your code in minutes, and AWS automatically handles the scaling and infrastructure.
- **Integrated with AWS Ecosystem**: Lambda integrates seamlessly with other AWS services like S3, DynamoDB, SNS, and more.


## WebSockets

**WebSockets** are a communication protocol that enables **full-duplex** (two-way) communication channels over a single, long-lived connection between a client (usually a web browser) and a server. Unlike the traditional HTTP request-response model, which is **stateless** and works in a **request-response** pattern, WebSockets provide a persistent, open connection that allows continuous, real-time data exchange between the client and server.

### Key Features of WebSockets:

1. **Full-Duplex Communication**:
   - WebSockets allow both the client and the server to send messages to each other independently, at any time, over a single connection. This allows for real-time interactions, making it ideal for applications like live chats, online gaming, financial apps, etc.

2. **Persistent Connection**:
   - Once established, a WebSocket connection remains open until either the client or the server decides to close it. This eliminates the need to repeatedly open and close connections, reducing the overhead compared to traditional HTTP requests.

3. **Low Latency**:
   - WebSockets provide a low-latency communication channel because there’s no need to establish a new connection for each message. Once the connection is established, messages can be sent and received instantly.

4. **Efficient Communication**:
   - WebSockets reduce the amount of data overhead, as there’s no need for the repeated HTTP headers that occur with each request in a standard HTTP communication. This makes WebSockets more efficient for applications requiring frequent communication.

5. **Bidirectional**:
   - Unlike HTTP, which only allows the client to request and the server to respond, WebSockets enable both the client and the server to send messages at any time. This allows for real-time updates (e.g., chat messages, notifications, live score updates).

### How WebSockets Work:

1. **Handshake**:
   - A WebSocket connection starts with an HTTP handshake. The client sends an HTTP request to the server with an **Upgrade** header, indicating that it wants to establish a WebSocket connection.
   
   - Example WebSocket request:
     ```
     GET /chat HTTP/1.1
     Host: example.com
     Upgrade: websocket
     Connection: Upgrade
     Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
     Sec-WebSocket-Version: 13
     ```

2. **Connection Upgrade**:
   - If the server supports WebSockets, it responds with a status code **101 Switching Protocols**, indicating that the protocol has been switched to WebSocket and the connection is now open.
   
   - Example WebSocket response:
     ```
     HTTP/1.1 101 Switching Protocols
     Upgrade: websocket
     Connection: Upgrade
     Sec-WebSocket-Accept: dGhlIHNhbXBsZSBub25jZQ==
     ```

3. **Data Exchange**:
   - After the handshake, the connection is upgraded to WebSocket, and both the client and the server can send messages back and forth in real time.
   - WebSocket messages can be sent in text or binary format, making it flexible for various types of data.

4. **Closing the Connection**:
   - Either the client or the server can close the WebSocket connection at any time by sending a **close frame**. Once the connection is closed, no more messages can be sent or received.

### Common Use Cases of WebSockets:

1. **Real-Time Messaging and Chat Applications**:
   - WebSockets are ideal for applications like live chat or messaging, where users need instant communication with each other.
   
2. **Online Gaming**:
   - In multiplayer games, WebSockets enable fast, real-time communication between players, which is crucial for game states, actions, and updates.
   
3. **Stock Market or Financial Applications**:
   - Financial apps that require real-time updates (e.g., stock prices, cryptocurrency rates) benefit from WebSockets because of the low latency and continuous data flow.
   
4. **Live Sports Updates**:
   - WebSockets allow sports applications to push live scores, statistics, and news to users without requiring them to refresh the page.

5. **Collaborative Applications**:
   - Applications like collaborative document editing (e.g., Google Docs) require real-time updates to synchronize changes made by different users.

6. **IoT (Internet of Things)**:
   - WebSockets are also useful for real-time communication between IoT devices (e.g., smart home devices, sensors) and control systems, where the devices need to send continuous streams of data.

7. **Push Notifications**:
   - WebSockets can be used for implementing push notifications in web applications, allowing users to receive instant alerts about various events (e.g., new messages, system updates).

### Example WebSocket Usage:

Here’s a basic example of how WebSocket communication works in a **web browser** using JavaScript (client-side) and **Node.js** (server-side).

#### **Client-Side (JavaScript - Browser)**:

```javascript
// Create a new WebSocket connection to the server
const socket = new WebSocket('ws://localhost:8080');

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

#### **Server-Side **:


To create a WebSocket server in Python, you can use the `websockets` library, which provides an easy way to handle WebSocket connections. 
First, you'll need to install the `websockets` library. You can do that by running:

```bash
pip install websockets
```

##### Server-Side WebSocket Example in Python:

Here is a simple WebSocket server in Python using the `websockets` library:

```python
import asyncio
import websockets

# This function will handle a WebSocket connection from the client
async def echo(websocket, path):
    # Print when a new client connects
    print(f"Client connected: {path}")
    
    # Send a welcome message to the client
    await websocket.send("Hello, Client!")

    try:
        # Wait for messages from the client
        async for message in websocket:
            print(f"Received from client: {message}")
            # Echo the received message back to the client
            await websocket.send(f"Echo: {message}")
    except websockets.exceptions.ConnectionClosed as e:
        print(f"Connection closed: {e}")
    finally:
        print("Connection closed by client.")

# Start the WebSocket server
async def main():
    # Start the WebSocket server on localhost:8765
    async with websockets.serve(echo, "localhost", 8765):
        print("Server started on ws://localhost:8765")
        # Run the server indefinitely
        await asyncio.Future()  # This will keep the server running

# Run the main coroutine
if __name__ == "__main__":
    asyncio.run(main())
```

##### Explanation of the Code:

1. **`echo` Function**:
   - This function handles the WebSocket connection for each client. It first sends a welcome message to the client and then listens for messages from the client. Any message received from the client is echoed back with the prefix "Echo: ".
   
2. **`main` Function**:
   - This function starts the WebSocket server by calling `websockets.serve(echo, "localhost", 8765)`, which listens for incoming WebSocket connections on `ws://localhost:8765`.
   - The `asyncio.Future()` keeps the server running indefinitely by waiting for events (like new incoming connections).

3. **Running the Server**:
   - The server will print `"Server started on ws://localhost:8765"` when it is up and running, and it will listen for incoming WebSocket connections.
   - If a client sends a message, the server will log the message and send it back (echo).

##### 3. Client-Side Example in JavaScript (Web Browser):

You can test this WebSocket server using the following JavaScript client code in the browser:

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

1. **Run the Python WebSocket Server**:
   - Save the Python WebSocket server code to a file (e.g., `websocket_server.py`).
   - Run the server:
     ```bash
     python websocket_server.py
     ```

2. **Run the JavaScript Client**:
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

   Save the JavaScript code in a file called `client.js`, then open the HTML file in your web browser.

##### 4. WebSocket Client (Python Example):

You can also write a Python WebSocket client to test the server using the `websockets` library:

```python
import asyncio
import websockets

async def hello():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        # Send a message to the server
        await websocket.send("Hello, Server!")
        
        # Receive the response from the server
        response = await websocket.recv()
        print(f"Response from server: {response}")

# Run the client
asyncio.run(hello())
```















### Advantages of WebSockets:

- **Real-Time Communication**: WebSockets enable instant communication between the client and server, making them ideal for real-time applications.
- **Reduced Latency**: Since the connection is persistent, there’s no need to repeatedly open and close connections, which results in lower latency.
- **Efficiency**: WebSockets use less bandwidth and are more efficient than HTTP for frequent message exchanges, as they avoid the overhead of HTTP headers with every request.
- **Lower Overhead**: There’s less overhead compared to HTTP polling or long-polling because WebSockets maintain a single connection, and data can be sent immediately when available.

### Limitations of WebSockets:

- **Browser and Network Compatibility**: WebSockets require support from the client (browser or app) and the server. Some firewalls or proxies might block WebSocket traffic.
- **Single Connection**: WebSockets typically use a single connection for each client, which can become limiting if you need to scale to millions of users.
- **No Built-In Message Queuing**: WebSockets don’t provide built-in message persistence, so you need to implement your own system for queuing or persisting messages.







# Tasks



## AWS API Gateway

### **Step 1: Create a Lambda Function**

First, let's create a simple Lambda function in Python that will process incoming HTTP requests.

```python
import json

def lambda_handler(event, context):
    """
    Lambda function to handle API Gateway events.
    """
    # Example of how to handle GET request
    http_method = event.get('httpMethod')
    
    if http_method == 'GET':
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Hello from Lambda!',
                'input': event,
            })
        }
    
    # Handle other HTTP methods here (POST, PUT, DELETE, etc.)
    return {
        'statusCode': 405,
        'body': json.dumps({'message': 'Method Not Allowed'})
    }
```

### **Step 2: Create an API in API Gateway**

1. **Navigate to API Gateway Console**: 
   - Go to the **API Gateway Console** in AWS.
   - Select **Create API** and choose **REST API**.
   - Name your API (e.g., `MyTestAPI`), and choose the protocol type as REST.
   
2. **Create a Resource and Method**:
   - In the **API Gateway Console**, create a new resource. This will be the path that your API responds to, for example `/test`.
   - Create a **GET** method for this resource, which will invoke the Lambda function when called.

3. **Link API Gateway with Lambda**:
   - When creating the **GET** method, select **Lambda Function** as the integration type.
   - Choose the region where you created the Lambda function and enter the name of the Lambda function you created earlier (`lambda_handler`).
   - Ensure that **Use Lambda Proxy integration** is checked. This allows API Gateway to forward the request as a JSON payload.

4. **Deploy the API**:
   - Deploy your API to a stage (e.g., `dev`).
   - After deployment, you will receive an **Invoke URL** for your API (e.g., `https://xyz123.execute-api.us-west-2.amazonaws.com/dev`).

### **Step 3: Test the API**

Once the API is deployed, you can test it using the following Python code that sends an HTTP request to your newly created API endpoint.

```python
import requests

# Replace with your actual API Gateway Invoke URL
api_url = "https://xyz123.execute-api.us-west-2.amazonaws.com/dev/test"

# Send a GET request to the API
response = requests.get(api_url)

# Print the response from the API
if response.status_code == 200:
    print("Success!")
    print("Response Body:", response.json())
else:
    print(f"Error: {response.status_code}")
    print("Response Body:", response.text)
```

### **Step 4: Deploy and Monitor**

Once your API is deployed and working, you can monitor its usage in the AWS API Gateway and Lambda dashboards:
- **API Gateway**: You can track metrics like the number of requests, latency, and any errors.
- **Lambda**: Use AWS CloudWatch Logs to view detailed logs for each invocation of your Lambda function.

### **Explanation of the Components**:
1. **Lambda Function**: This is where you process the incoming API requests. In the example, we simply return a JSON message with a "Hello from Lambda!" message.
2. **API Gateway**: Acts as the entry point to your API, routing incoming HTTP requests to the appropriate Lambda function.
3. **Requests Library in Python**: The `requests` library is used to send HTTP requests from your local machine or another system to the API Gateway endpoint.

### **Additional Features**:
- You can handle more HTTP methods like `POST`, `PUT`, or `DELETE` by adding additional logic in your Lambda function.
- Use **API Gateway Authorizers** (like IAM roles, Lambda authorizers, or Cognito) to secure your API.
- You can also enable **CORS** (Cross-Origin Resource Sharing) in API Gateway if you need to access the API from a frontend application hosted on a different domain.

This is a basic example to get you started. You can expand it by adding more resources, using environment variables, setting up custom domains, and more depending on your needs.



## AWS CLI for API Gateway

To create an **AWS API Gateway** using the **AWS CLI**, you can follow these steps. We will create a simple REST API that invokes a Lambda function, but the approach is general enough for creating any type of API Gateway.

### Prerequisites:
1. **AWS CLI Installed**: Ensure that the AWS CLI is installed and configured with proper credentials (use `aws configure`).
2. **Lambda Function**: For this example, we will assume that you already have a Lambda function created.
3. **IAM Role**: Ensure you have an appropriate IAM role with the correct permissions for API Gateway to invoke the Lambda function.

---

### Steps to Create an API Gateway Using AWS CLI

#### 1. **Create the API Gateway**

You can create a REST API using the `aws apigateway` command.

```bash
aws apigateway create-rest-api --name "MyApi" --description "This is my sample API"
```

This will create a REST API with the name `MyApi`. You will get a response with the API's **ID** (e.g., `"id": "abcd1234"`), which you will need for the next steps.

#### 2. **Get the Root Resource ID**

After creating the API, you need to find the root resource ID. This is usually the top-level resource in your API, often referred to as `/`.

```bash
aws apigateway get-resources --rest-api-id <api-id>
```

Replace `<api-id>` with the ID returned from the previous command (e.g., `abcd1234`). This command will return a list of resources, and you'll need the root resource ID (it will look like `"/"`).

Example output:
```json
{
    "items": [
        {
            "id": "root",
            "parentId": "string",
            "pathPart": "",
            "path": "/"
        }
    ]
}
```

Here, the root resource has the `id` of `"root"`.

#### 3. **Create a New Resource (Path)**

You can create a new resource (path) in the API. For example, let's create a `/hello` path:

```bash
aws apigateway create-resource --rest-api-id <api-id> --parent-id <root-id> --path-part "hello"
```

Replace `<api-id>` with the ID of your API, and `<root-id>` with the ID of the root resource (often `root`).

#### 4. **Create a Method for the Resource**

Now, we will create a `GET` method on the `/hello` resource. This method will invoke a Lambda function when called.

```bash
aws apigateway put-method --rest-api-id <api-id> --resource-id <resource-id> --http-method GET --authorization-type NONE
```

Here, `<resource-id>` is the ID of the newly created `/hello` resource (you can get it by running `aws apigateway get-resources`), and the method type is `GET`.

#### 5. **Integrate the Method with Lambda Function**

Next, you'll integrate this `GET` method with a Lambda function. Assume the Lambda function ARN is `arn:aws:lambda:us-west-2:123456789012:function:MyLambdaFunction`.

```bash
aws apigateway put-integration --rest-api-id <api-id> --resource-id <resource-id> --http-method GET --integration-http-method POST --type AWS_PROXY --uri arn:aws:apigateway:us-west-2:lambda:path/2015-03-31/functions/arn:aws:lambda:us-west-2:123456789012:function:MyLambdaFunction/invocations
```

In this command:
- Replace `<api-id>` with your API ID.
- Replace `<resource-id>` with the ID of the `/hello` resource.
- The Lambda function ARN should be replaced with your actual Lambda ARN.

The integration type is `AWS_PROXY`, which means the entire request will be passed to the Lambda function, allowing you to handle it however you like.

#### 6. **Grant API Gateway Permission to Invoke Lambda**

Before API Gateway can invoke your Lambda function, you need to grant it permission. You can do that using the following command:

```bash
aws lambda add-permission --function-name MyLambdaFunction --principal apigateway.amazonaws.com --statement-id <unique-id> --action "lambda:InvokeFunction"
```

- Replace `MyLambdaFunction` with your Lambda function name.
- Replace `<unique-id>` with a unique string for this permission (e.g., `12345`).

This command ensures that API Gateway can invoke your Lambda function.

#### 7. **Deploy the API**

After creating the method and integration, you need to deploy the API to make it accessible. First, create a deployment stage:

```bash
aws apigateway create-deployment --rest-api-id <api-id> --stage-name prod
```

This will deploy the API to the `prod` stage. You can choose any name for the stage (e.g., `dev`, `test`, etc.).

#### 8. **Test the API**

After deploying the API, you can test it by sending an HTTP request to the `GET` method you created. The endpoint URL will look like this:

```
https://<api-id>.execute-api.<region>.amazonaws.com/prod/hello
```

Replace `<api-id>` with your actual API ID, and `<region>` with your AWS region (e.g., `us-west-2`).

For example, if you have a `GET` method on `/hello` that integrates with your Lambda, you can use `curl` or any HTTP client to test it:

```bash
curl https://abcd1234.execute-api.us-west-2.amazonaws.com/prod/hello
```

You should receive a response from your Lambda function (e.g., `"Hello from Lambda!"`).

---

### Summary of AWS CLI Commands:

1. **Create API Gateway**:
   ```bash
   aws apigateway create-rest-api --name "MyApi" --description "This is my sample API"
   ```

2. **Get Root Resource ID**:
   ```bash
   aws apigateway get-resources --rest-api-id <api-id>
   ```

3. **Create Resource**:
   ```bash
   aws apigateway create-resource --rest-api-id <api-id> --parent-id <root-id> --path-part "hello"
   ```

4. **Create Method for Resource**:
   ```bash
   aws apigateway put-method --rest-api-id <api-id> --resource-id <resource-id> --http-method GET --authorization-type NONE
   ```

5. **Integrate Method with Lambda**:
   ```bash
   aws apigateway put-integration --rest-api-id <api-id> --resource-id <resource-id> --http-method GET --integration-http-method POST --type AWS_PROXY --uri arn:aws:apigateway:<region>:lambda:path/2015-03-31/functions/arn:aws:lambda:<region>:<account-id>:function:MyLambdaFunction/invocations
   ```

6. **Grant API Gateway Permission to Invoke Lambda**:
   ```bash
   aws lambda add-permission --function-name MyLambdaFunction --principal apigateway.amazonaws.com --statement-id <unique-id> --action "lambda:InvokeFunction"
   ```

7. **Deploy API**:
   ```bash
   aws apigateway create-deployment --rest-api-id <api-id> --stage-name prod
   ```

8. **Test the API**:
   ```bash
   curl https://<api-id>.execute-api.<region>.amazonaws.com/prod/hello
   ```

This should help you set up a basic API Gateway using AWS CLI and integrate it with a Lambda function.













## AWS CLI for Lambda

Deploying a Lambda function using the AWS CLI involves a few steps. Here's a comprehensive guide to deploying your Lambda function from the command line.

### Prerequisites:

1. **AWS CLI Installed**: Ensure the AWS Command Line Interface (CLI) is installed on your machine. You can install it by following the instructions [here](https://aws.amazon.com/cli/).

2. **AWS Account and Credentials**: Ensure you have an AWS account, and your AWS credentials are configured (Access Key ID and Secret Access Key) using the `aws configure` command.
   ```bash
   aws configure
   ```
   - Enter your **AWS Access Key** and **Secret Access Key**.
   - Enter the **Region** where your Lambda function will be deployed (e.g., `us-west-2`).
   - Enter the **default output format** (e.g., `json`).

3. **IAM Role for Lambda**: Ensure you have an IAM role for your Lambda function that grants necessary permissions. Lambda requires a role with policies like `AWSLambdaBasicExecutionRole` to write logs to CloudWatch.

### Steps to Deploy a Lambda Function Using AWS CLI:

#### 1. **Write Your Lambda Function Code**

Create a file with your Lambda function code. For example, let's use a simple Python Lambda function (`lambda_function.py`).

```python
def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'body': 'Hello from Lambda!'
    }
```

#### 2. **Create a ZIP Archive of Your Code**

You need to package your Lambda function into a ZIP file before deploying. If your Lambda code is in a single file (like `lambda_function.py`), you can run the following command to create the ZIP:

```bash
zip function.zip lambda_function.py
```

If you have additional dependencies, you need to install them first into a directory and include them in the ZIP file. Here’s how to package everything together:

```bash
mkdir my_lambda_package
cd my_lambda_package
# Copy your lambda function code into this directory
cp ../lambda_function.py .

# If you have any dependencies, install them into the directory
# Example (if you have external libraries):
# pip install requests -t .

# Zip everything
zip -r ../function.zip .
cd ..
```

#### 3. **Create an IAM Role for Lambda (If Not Already Created)**

If you don't have an IAM role with the necessary permissions for Lambda, you can create one using the following steps:

```bash
aws iam create-role --role-name lambda-execution-role \
  --assume-role-policy-document file://trust-policy.json
```

`trust-policy.json` is a JSON file defining the trust relationship between AWS Lambda and IAM, and it should look like this:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

You can also attach a basic Lambda execution policy (if not done yet) to the role for logging permissions:

```bash
aws iam attach-role-policy --role-name lambda-execution-role \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
```

#### 4. **Deploy the Lambda Function Using the AWS CLI**

Now, you're ready to deploy the function. Use the following command to create the Lambda function:

```bash
aws lambda create-function --function-name my-lambda-function \
  --zip-file fileb://function.zip \
  --handler lambda_function.lambda_handler \
  --runtime python3.8 \
  --role arn:aws:iam::your-account-id:role/lambda-execution-role
```

- `--function-name`: The name you want to give to your Lambda function (e.g., `my-lambda-function`).
- `--zip-file`: The path to the ZIP file containing your Lambda function code (e.g., `fileb://function.zip`).
- `--handler`: The function that AWS Lambda will call when your function is invoked. It’s the file name (without the `.py` extension) and the function name (e.g., `lambda_function.lambda_handler`).
- `--runtime`: The runtime environment for the Lambda function. Use the appropriate runtime (e.g., `python3.8`, `nodejs14.x`, etc.).
- `--role`: The ARN (Amazon Resource Name) of the IAM role your Lambda function will assume.

Make sure to replace `your-account-id` with your actual AWS account ID.

#### 5. **Verify the Lambda Deployment**

To verify that the function has been created successfully, you can use the following command:

```bash
aws lambda get-function --function-name my-lambda-function
```

This will return metadata about the function you just created, including its ARN and other configuration details.

#### 6. **Invoke Your Lambda Function**

To invoke the Lambda function from the CLI and test it, use the following command:

```bash
aws lambda invoke --function-name my-lambda-function output.txt
```

- `--function-name`: The name of your Lambda function (e.g., `my-lambda-function`).
- `output.txt`: The file where the output from the Lambda function will be written.

If everything works fine, you'll see the result in `output.txt`.

#### 7. **Update an Existing Lambda Function (Optional)**

If you want to update an existing Lambda function, you can use the `update-function-code` command:

```bash
aws lambda update-function-code --function-name my-lambda-function \
  --zip-file fileb://function.zip
```

This will update the Lambda function code with the new contents of `function.zip`.

#### 8. **Delete the Lambda Function (Optional)**

If you want to delete the Lambda function after testing, you can do so with the following command:

```bash
aws lambda delete-function --function-name my-lambda-function
```

This removes the Lambda function from AWS.

---

### Summary of Commands

1. **Zip the Lambda code**:
   ```bash
   zip function.zip lambda_function.py
   ```

2. **Create the Lambda function**:
   ```bash
   aws lambda create-function --function-name my-lambda-function \
     --zip-file fileb://function.zip \
     --handler lambda_function.lambda_handler \
     --runtime python3.8 \
     --role arn:aws:iam::your-account-id:role/lambda-execution-role
   ```

3. **Invoke the Lambda function**:
   ```bash
   aws lambda invoke --function-name my-lambda-function output.txt
   ```

4. **Update the Lambda function** (if needed):
   ```bash
   aws lambda update-function-code --function-name my-lambda-function \
     --zip-file fileb://function.zip
   ```

5. **Delete the Lambda function** (if needed):
   ```bash
   aws lambda delete-function --function-name my-lambda-function
   ```

