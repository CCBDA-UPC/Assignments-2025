<style>
img{
    border:1px solid red;
    width: 50%;
}
</style>

# Lab session 5: Deploy a custom web app using additional cloud services

### Django: web framework

[Django](https://www.djangoproject.com/start/) is a high-level Python web framework designed for rapid development and
clean, pragmatic design. Built by experienced developers, it handles many complexities of web development, allowing you
to focus on building your application without reinventing the wheel. Plus, it’s free and open source.

### AWS ECS: Elastic Container Service

Amazon Elastic Container Service (ECS) is a fully managed container orchestration service that simplifies deploying,
managing, and scaling containerized applications. It seamlessly integrates with AWS, offering a secure and flexible
solution for running workloads in the cloud or on-premises with Amazon ECS Anywhere.

Containerizing a Django app with Docker enhances productivity and consistency. Here’s why:

- **Stable and Consistent Environment**: Docker eliminates the “*it works on my machine*” problem by ensuring a
  consistent environment with all dependencies pre-installed. This allows you to reproduce the app seamlessly across
  different systems and servers, making local development, testing, and deployment more reliable.

- **Reproducibility and Portability**: A Dockerized app packages all its dependencies, environment variables, and
  configurations, guaranteeing it runs the same way across various environments. This simplifies deployment and reduces
  compatibility issues.

- **Improved Team Collaboration**: With Docker, every developer works in an identical environment, preventing conflicts
  caused by different system setups. Shared Docker images streamline onboarding and reduce setup time.

- **Faster Deployment**: Docker accelerates project setup by automating environment configuration, so developers can
  start coding right away. It ensures uniformity across development, staging, and production, making it easier to
  integrate and deploy changes.

## Deploying an example Web App Using Docker

We are going to assume that you are working on a new subject on Cloud Computing that isn't ready for students to enroll
yet, but in the meantime, you plan to deploy a small placeholder app that collects contact information from the website
visitors who sign up to hear more. The signup app will help you reach potential students who might take part in a
private beta test of the laboratory sessions.

### The Signup App

The app will allow your future students to submit contact information and express interest in a preview of the new
subject on Cloud Computing that you're developing.

To make the app look good, we use [Bootstrap](https://getbootstrap.com/), a mobile-first front-end framework that
started as a Twitter project.

### AWS DynamoDB

**Amazon DynamoDB**, a NoSQL database service, is going to be used to store the contact information that users submit.

DynamoDB is a schema-less database, so you need to specify only a primary key attribute. Let us use the email field as a
key for each register.

### AWS Simple Notification Service (SNS)

We want to know when customers submit a form, therefore we are going to use **AWS Simple Notification Service** (AWS
SNS), a message pushing service that can deliver notifications over various protocols. For our web app, we are going to
push notifications to an email address.

### AWS CloudFront CDN

A content delivery network or content distribution network (CDN) is a geographically distributed network of proxy
servers that disseminate a service spatially, as close to end-users as possible, to provide high availability, low
latency, and high performance.

![Lab05-CDN.png](images/Lab05-CDN.png)

The information that flows every day on the Internet can be classified as "static" and "dynamic" content. The "dynamic"
part is the one that changes depending on the user's input. It is distributed by, for instance, PaaS servers with load
balancers. The "static" part does not change based on the user's input, and it can be moved as close to the end user as
possible to improve the "user experience".

Nowadays, CDNs serve a substantial portion of the "static" content of the Internet: text, graphics, scripts,
downloadable media files (documents, software products, videos, etc.), live streaming media, on-demand streaming media,
social networks and so much more.

Content owners pay CDN operators to deliver the content that they produce to their end users. In turn, a CDN pays ISPs (
Internet Service Providers), carriers, and network operators for hosting its servers in their data centers.

**AWS CloudFront CDN** is a global CDN service that securely delivers static content with low latency and high transfer
speeds. CloudFront CDN works seamlessly with other AWS services including **AWS Shield** for DDoS mitigation, **AWS S3
**, **Elastic Load Balancing** or **AWS EC2** as origins for your applications, and **AWS Lambda** to run custom code
close to final viewers.

## Prerequisites

Make sure that you :

- Have [Django](https://www.djangoproject.com/start/) installed on your system.
- Install [Docker Desktop](https://www.docker.com/products/docker-desktop/)
  and [Docker Compose](https://docs.docker.com/compose/) on your machine.

If you need help with the installation, you can find detailed instructions on the Docker and Django websites.

## Session taks

* [Task 5.1: Download the code for the Web App](#Task51)
* [Task 5.2: Create a DynamoDB Table](#Task52)
* [Task 5.3: Test the web app locally](#Task53)
* [Task 5.4: Configure Docker CLI and deploy the target web app](#Task54)
* [Task 5.5: Use AWS Simple Notification Service in your web app](#Tasks55)
* [Task 5.6: Create a new option to retrieve the list of leads](#Tasks56)
* [Task 5.7: Improve the web app transfer of information](#Tasks57)
* [Task 5.8: Deliver static content using a Content Delivery Network](#Tasks58)

<a name="Task51"/>

## Task 5.1: Download the code for the Web App

You are going to make a few changes to the base Python code. Therefore, download the repository on your local disk drive
as a *[zip file](ccbda-signup.zip)*. Unzip the file inside your responses repository for the current Lab session, and
change the name of the folder to *ccbda-signup*.

![Lab05-webapp-zip.png](images/Lab05-webapp-zip.png)


<a name="Task52"/>

## Task 5.2: Create a DynamoDB Table

The signup app uses a DynamoDB table to store the contact information that users submit.

#### To create a DynamoDB table

Go to the course "AWS Academy Learner Lab", open the modules and open the "Learner Lab". Click the button "Start Lab",
wait until the environment is up and then click "AWS" at the top of the window and open the AWS Console.

1. At the console search for "DynamoDB".

3. Go to Tables and **Create table**.

4. For Table name, type **ccbda-signup-table**.

5. For the `Partition key`, type `email`. Choose **Create**.

<a name="Task53"/>

## Task 5.3: Test the web app locally

Once you are inside the directory create a `.env` file with the configuration of the project:

```bash
DEBUG=True
STARTUP_SIGNUP_TABLE=ccbda-signup-table
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=<YOUR-ACCESS-KEY-ID>
AWS_SECRET_ACCESS_KEY=<YOUR-SECRET-ACCESS-KEY>
AWS_SESSION_TOKEN=<YOUR-AWS-SESSION-TOKEN>
```

All service access to the *AWS Learner Lab account* is limited to the **us-east-1** and **us-west-2** regions unless
mentioned otherwise in the service details that appear in the Learner Lab service description. If you load a service
console page in another AWS Region you will see access error messages.

To obtain the values missing above, at your CLI type the following command that will provide the necessary values

````bash
ddd_v1_w_3cWf_628331@runweb75472:~$ cat $HOME/.aws/credentials
[default]
aws_access_key_id = <YOUR-ACCESS-KEY-ID>
aws_secret_access_key = <YOUR-SECRET-ACCESS-KEY>
aws_session_token = <YOUR-AWS-SESSION-TOKEN>
````

**DO NOT PUSH AWS CREDENTIALS TO YOUR PRIVATE REPOSITORY !!!**

Next, create a **new Python 3.10 virtual environment** specially for this web app and install the packages required to
run it.

Check the contents of the file **requirements.txt** that the web application declares as the set of Python packages, and
its version, that it requires to be executed successfully.

The package `boto3` is a library that hides de AWS REST API to the programmer and manages the communication between the
web app and all the AWS services. Check [**Boto 3 Documentation
**](https://boto3.readthedocs.io/en/latest/reference/services/index.html) for more details.

Please, note the different prompt  `(.env) _$`  vs. `_$` when you are inside or outside of the Python virtual
environment.

```
_$ virtualenv -p python3 ../.venv
_$ source ../.venv/bin/activate
(.env)_$ pip install -r requirements.txt
```

You will now need to run a local testing server.

```
(.venv)_$ python manage.py runserver
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
January 08, 2025 - 19:36:44
Django version 5.1.7, using settings 'ccbda.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
(.venv)_$ deactivate
```

Check that you have configured the access to DynamoDB correctly by interacting with the web app through your
browser [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

Go to the DynamoDB table browser tab and verify that the **ccbda-signup-table** table contains the new records that the
web app should have created. If all the above works correctly, you are almost ready to transfer the web app to Docker.

We are creating a new Python virtual environment locally only to keep the packages that the web app uses. Having a small
Python environment implies a faster web app startup and avoids, as much as possible, any hidden dependencies and
ambiguities.

That Python virtual environment is re-created remotely by Docker through the use of the file *requirements.txt* and
other configuration that you are going to set up later.


<p align="center"><img src="./images/Lab04-pycharm-config.png" alt="AWS service" title="AWS service" width="550"/></p>

<a name="Task54"/>

## Task 5.4: Configure Docker and deploy the target web app

### Test the Web App

To open a new browser with your application, type:

```
_$ eb open
```

You can check your Docker that will console will show changes, as seen below.

<p align="center"><img src="./images/Lab04-11.png " alt="Sample web app" title="Sample web app"/></p>

Interact with the web app and check that the new records inserted are stored in DynamoDB.

### Troubleshoot Deployment Issues

If you followed all the steps, opened the URL, and obtained no app, there is a deployment problem. To troubleshoot a
deployment issue, you may need to use the logs that are provided by Docker.

You can check the logs of the Docker environment using `eb logs --all`. Once they have been retrieved you'll
be able to find them at the `.Docker` folder.

You can check that the values are correct using `eb printenv`.

```
_$ eb printenv
Environment Variables:
     AWS_ACCESS_KEY_ID = *****
     AWS_REGION =  us-east-1
     AWS_SECRET_ACCESS_KEY = ********<YOURS>*********
     AWS_SESSION_TOKEN = ********<YOURS>*********
     DEBUG = True
     STARTUP_SIGNUP_TABLE = ccbda-signup-table
```

Of course, you would try to catch such an error in development. However, if an error does get through to production, or
you want to update your app, Docker makes it fast and easy to redeploy. Just modify your code, and issue "
deploy" again.

```
_$ eb deploy
Creating application version archive "app-3a7a-230322_155801427873".
Uploading eb-django-express-signup/app-3a7a-230322_155801427873.zip to S3. This may take a while.
Upload Complete.
2025-03-22 14:58:05    INFO    Environment update is starting.      
2025-03-22 14:58:10    INFO    Deploying new version to instance(s).
2025-03-22 14:58:14    INFO    Instance deployment successfully generated a 'Procfile'.
2025-03-22 14:58:18    INFO    Instance deployment completed successfully.
2025-03-22 14:58:24    INFO    New application version was deployed to running EC2 instances.
2025-03-22 14:58:24    INFO    Environment update completed successfully.

```

Since Docker infrastructure maintenante is part of AWS responsibilities, that includes updating the operating
system, web server, application server, etc. Such updates may interfere with your application, therefore you can decide
when it is the best moment to use the following command that updates the environment to the most recent platform
version.

```bash
_$ eb upgrade
```

You can check the health of your Docker environment.

```bash
_$ eb health
  eb-django-express-signup-dev2                  Ok                  2025-03-22 16:02:05
WebServer                              Python 3.8 running on 64bit Amazon Linux 2/3.5.0
  total      ok    warning  degraded  severe    info   pending  unknown 
    1        1        0        0        0        0        0        0    
```

Now, go to your EC2 console and check the EC2 instance that AWS uses for the Docker environment. Terminate
the
instance. Check the health. Wait a couple of minutes and check again.

**Q51a: What has happened? Why do you think that has happened?** Add your responses to `README.md`.

<p align="center"><img src="./images/Lab04-13.png " alt="EC instances" title="EC instances"/></p>

Now, to save expenses, you can terminate your environment, this time from the EB console.

**Q51b: What has happened? Why do you think that has happened?** Check both EC2 and EB consoles. Add your responses
to `README.md`.

**Q51c: Can you terminate the application using the command line? What is the command? if it exists.**

**Q51d: What parameters have you added to the `eb create` command to create your environment? Explain why you have
selected each parameter.**


<a name="Tasks55" />

## Task 5.5: Use AWS Simple Notification Service in your web app

### Create a AWS SNS Topic

Our signup web app wants to notify you each time a user signs up. When the data from the signup form is written to the
DynamoDB table, the app will send you an AWS SNS notification.

First, you need to create an AWS SNS topic, which is a stream for notifications, and then you need to create a
subscription that tells AWS SNS where and how to send the notifications.

**To set up AWS SNS notifications**

At the "AWS" console search for "Simple Notification Service"

- Choose **Create topic**.
- For Topic name, type *gsg-signup-notifications*. Choose **Standard** type and **Create topic**.
- Choose  **Create subscription**.
- For **Protocol**, choose *Email*. For **Endpoint**, enter *your email address*. Choose **Create Subscription**.

To confirm the subscription, AWS SNS sends you an email named *AWS Notification — Subscription Confirmation*. Open the
link in the email to confirm your subscription.

Do not forget that before testing the new functionality you need to have the AWS SNS subscription approved.

<p align="center"><img src="./images/Lab05-2.png " alt="Confirmed" title="Confirmed"/></p>

Add the *unique identifier* for the AWS SNS topic to the configuration environment of your local deployment.

```bash
_$ export NEW_SIGNUP_TOPIC="arn:aws:sns:us-east-1:YOUR-ACCOUNT-ID:gsg-signup-notifications"
```

Before you forget, you can also add a new variable to the environment of the Docker deployment.

### Modify the web app to send messages

Open the files *form/models.py* and *form/views.py* read and understand what the code does.

Add the code below to *form/models.py* as a new operation of the model *Leads()*.

```python
def send_notification(self, email):
    sns = boto3.client('sns', region_name=AWS_REGION,
                       aws_access_key_id=AWS_ACCESS_KEY_ID,
                       aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                       aws_session_token=AWS_SESSION_TOKEN)
    try:
        sns.publish(
            TopicArn=NEW_SIGNUP_TOPIC,
            Message='New signup: %s' % email,
            Subject='New signup',
        )
        logger.error('SNS message sent.')

    except Exception as e:
        logger.error(
            'Error sending AWS SNS message: ' + (e.fmt if hasattr(e, 'fmt') else '') + ','.join(e.args))
```

You have probably noticed that there is a Python variable that needs to be instantiated. Scroll up that file and add
*NEW_SIGNUP_TOPIC* next to the other two environment variables, as shown below:

```python
STARTUP_SIGNUP_TABLE = os.environ['STARTUP_SIGNUP_TABLE']
AWS_REGION = os.environ['AWS_REGION']
NEW_SIGNUP_TOPIC = os.environ['NEW_SIGNUP_TOPIC']
```

Go to *form/views.py* and modify the signup view: if the lead has been correctly inserted in our DynamoDB table we can
send the notification.

```python
def signup(request):
    leads = Leads()
    status = leads.insert_lead(request.POST['name'], request.POST['email'], request.POST['previewAccess'])
    if status == 200:
        leads.send_notification(request.POST['email'])
    return HttpResponse('', status=status)
```

Close the file and execute the Django web app locally. You can post a new record. This time you see no error and you
receive a notification in your e-mail.

```bash
New item added to database.
SNS message sent.
"POST /signup HTTP/1.1" 200 0
```

Now that the web app is working in your computer, commit the changes. Deploy the new version to your Docker
environment and test that it works correctly. For that, you need to update the Elastinc Beanstalk Environment

```bash
_$ eb setenv "NEW_SIGNUP_TOPIC=arn:aws:sns:us-east-1:YOUR-ACCOUNT-ID:gsg-signup-notifications"
_$ eb printenv
Environment Variables:
     AWS_ACCESS_KEY_ID = *****
     AWS_REGION =  us-east-1
     AWS_SECRET_ACCESS_KEY = ********<YOURS>*********
     AWS_SESSION_TOKEN = ********<YOURS>*********
     DEBUG = True
     STARTUP_SIGNUP_TABLE = ccbda-signup-table
     NEW_SIGNUP_TOPIC = arn:aws:sns:us-east-1:YOUR-ACCOUNT-ID:gsg-signup-notifications
```

**Q52: Has everything gone alright?** Add your answers to the `README.md` file in the responses repository.

<a name="Tasks56" />

## Task 5.6: Create a new option to retrieve the list of leads

Edit the file *form/urls.py* to add the new URL and associate it to the new view *search*.

```python
urlpatterns = [
    # ex: /
    path('', views.home, name='home'),
    # ex: /signup
    path('signup', views.signup, name='signup'),
    # ex: /search
    path('search', views.search, name='search'),
]
```

To create the controller for the new view edit *form/views.py* and include the following code:

```python
from collections import Counter


def search(request):
    domain = request.GET.get('domain')
    preview = request.GET.get('preview')
    leads = Leads()
    items = leads.get_leads(domain, preview)
    if domain or preview:
        return render(request, 'search.html', {'items': items})
    else:
        domain_count = Counter()
        domain_count.update([item['email'].split('@')[1] for item in items])
        return render(request, 'search.html', {'domains': sorted(domain_count.items())})
```

The search view gets two parameters:

- preview: (*values are Yes/No*) lists the leads that are interested, or not, in a preview.
- domain: (*value is the part right after the @ of an e-mail address*) will list only the leads from that domain.

Reading the code, we understand that the search view retrieves the value of the parameters, gets the complete list of
leads and then:

- if any parameter is set, the program just lists all the records matching the search.
- if both parameters are empty the program extracts the domain from each e-mail address and counts how many addresses
  belong to each domain.

To access the records stored at the NoSQL table *ccbda-signup-table* you need to add a method *get_leads* to the model
*Leads()* file *form/models.py*.
The [Scan](https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_Scan.html) operation allows us to filter
values from the table.

```python
def get_leads(self, domain, preview):
    try:
        dynamodb = boto3.resource('dynamodb',
                                  region_name=AWS_REGION,
                                  aws_access_key_id=AWS_ACCESS_KEY_ID,
                                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                                  aws_session_token=AWS_SESSION_TOKEN)
        table = dynamodb.Table('ccbda-signup-table')
    except Exception as e:
        logger.error(
            'Error connecting to database table: ' + (e.fmt if hasattr(e, 'fmt') else '') + ','.join(e.args))
        return None
    expression_attribute_values = {}
    FilterExpression = []
    if preview:
        expression_attribute_values[':p'] = preview
        FilterExpression.append('preview = :p')
    if domain:
        expression_attribute_values[':d'] = '@' + domain
        FilterExpression.append('contains(email, :d)')
    if expression_attribute_values and FilterExpression:
        response = table.scan(
            FilterExpression=' and '.join(FilterExpression),
            ExpressionAttributeValues=expression_attribute_values,
        )
    else:
        response = table.scan(
            ReturnConsumedCapacity='TOTAL',
        )
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return response['Items']
    logger.error('Unknown error retrieving items from database.')
    return None
```

A final step is to move the file *extra-file/search.html* to *form/templates/search.html*. That file receives the data
from the view controller and creates the HTML to show the results.

Save the changes and, before committing them, check that everything works fine by typing *http://127.0.0.1:8000/search*
in your browser.

<p align="center"><img src="./images/Lab05-6.fw.png " alt="Search" title="Search"/></p>

To add the new option to the menu bar, simply edit the file *form/templates/generic.html*, go to line 28 and add the
second navbar as shown below. Save the file and, with no further delay, check that you have it added in the version that
runs in your computer.

```html

<div class="collapse navbar-collapse" id="navbarResponsive">
	<ul class="navbar-nav">
		<li class="nav-item active">
			<a class="nav-link active" href="{% url 'form:home' %}">Home</a>
		</li>
		<li class="nav-item">
			<a class="nav-link" href="#">About</a>
		</li>
		<li class="nav-item">
			<a class="nav-link" href="#">Blog</a>
		</li>
		<li class="nav-item">
			<a class="nav-link" href="#">Press</a>
		</li>
	</ul>
	<ul class="nav navbar-nav ml-auto">
		<li class="nav-item">
			<a class="nav-link" href="{% url 'form:search' %}">Admin search</a>
		</li>
	</ul>
</div>
```

<p align="center"><img src="./images/Lab05-7.png " alt="Search" title="Search"/></p>

If the web app works correctly in your computer commit the changes and deploy the new version in the cloud. Change
whatever is necessary to make it work.

**Q53: Has everything gone alright? What have you changed?** Add your answers to the `README.md` file in the responses
repository.

<a name="Tasks57" />

## Task 5.7: Improve the web app transfer of information (optional)

You can work on this section locally in order to save expenses; you can terminate your environment from the EB console.

If you analyze the new function added, probably a wise thing to do will be to optimize the data transfer from the
DynamoDB table: imagine that instead of a few records in your NoSQL table you have millions of records. Transferring
millions of records to your web app just to count how many e-mail addresses match a domain doesn't seem to be a great
idea.

DynamoDB is a NoSQL database and does not allow aggregation SQL queries. You are encouraged to improve the above code to
obtain a more efficient way of counting the e-mail addresses for each domain. Try to optimize the transfer of
information as well as the web app processing. Maybe you need to change the way that the records are stored.

Test the changes locally, commit them to your GitHub repository.

**Q54: Describe the strategy used to fulfill the requirements of this section. What have you changed in the code and the
configuration of the different resources used by the web app? What are the tradeoffs of your solution?** Add your
responses to `README.md`.

<a name="Tasks58" />

## Task 5.8: Deliver static content using a Content Delivery Network

### The static content in our web app

If you check line 11 of the file *templates/generic.html* you will see that, instead of loading in our server
Bootstrap 4 CSS, we are already using a CDN to retrieve the CSS and send it to the final users. Bootstrap uses
*maxcdn.bootstrapcdn.com* as their CDN distribution point.

```html

<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet" crossorigin="anonymous">
```

We can now add our CSS code to customize the look and feel of our web app even more. In that same file, add the
following line just before closing the **head** HTML tag:

```html

<link href="{% static 'custom.css' %}" rel="stylesheet"></head>
```

If you check the contents of the file *static/custom.css* you will see that it includes some images, also available in
the same folder. If you save the modifications to *form/templates/generic.html* and review your web
app, http://127.0.0.1:8000, you will see that it appears slightly different.

### Upload your static content to AWS S3 and grant object permissions

All the distributed static content overloads our server with requests. Moving it to a CDN will reduce our server's load
and, at the same time, the users will experience a much lower latency while using our web app. We only have static files
in this app, but a typical web app distributes hundreds of pieces of static content.

To configure our CDN, we are going to follow the steps
at ["Getting Started with CloudFront CDN"](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/GettingStarted.html).
Check that document if you need extra details.

Review the QuickStart
hands-on [Getting Started in the Cloud with AWS](../../../Cloud-Computing-QuickStart/blob/master/Quick-Start-AWS.md) and
create a new bucket in 'us-east-1' region to deposit the web app static content. Let us name this bucket *
*eb-django-express-signup-YOUR-ID** (YOUR-ID can be your AWS account number or any other distinctive string because you
will not be allowed to create two buckets with the same name, regardless the owner).

AWS has recently set some restrictions when creating an S3 bucket with public access. Make sure that you uncheck all the
following options before uploading files. You can later check them back.

 <p align="center"><img src="./images/Lab06-S3-public-access.png" alt="S3 public access" title="S3 public access"/></p>

 <p align="center"><img src="./images/Lab05-8.png " alt="S3 bucket" title="S3 bucket"/></p>

This time add the files manually and grant them public read permission.

  <p align="center"><img src="./images/Lab05-9.png " alt="S3 bucket" title="S3 bucket"/></p>

You can also use AWS CLI to sync the contents of your static folder with that
bucket. [Synchronize with your S3 bucket](https://docs.aws.amazon.com/cli/latest/reference/s3/sync.html) using the
following command:

```bash
_$ aws s3 sync --acl public-read ./static s3://eb-django-express-signup-YOUR-ID
upload: ./static/custom.css to s3://eb-django-express-signup-YOUR-ID/custom.css
upload: ./static/CCBDA-Square.png to s3://eb-django-express-signup-YOUR-ID/CCBDA-Square.png
upload: ./static/startup-bg.png to s3://eb-django-express-signup-YOUR-ID/startup-bg.png
```

If you explore in your S3 console you will see that there is a URL available to retrieve the files. Verify that you can
access the contents of that URL, making the file public if it was not already.

```
https://s3-us-east-1.amazonaws.com/eb-django-express-signup-YOUR-ID/CCBDA-Square.png
```

<p align="center"><img src="./images/Lab05-12.png " alt="S3 address" title="S3 address"/></p>

### Create a CloudFront CDN Web Distribution

Following the steps
at ["Getting Started with CloudFront CDN"](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/GettingStarted.html)
we end up having to wait until the files are distributed. It takes five minutes or more, be patient. Once the first
distribution is set up, whenever you resync your static contents it will take much less.

 <p align="center"><img src="./images/Lab05-10.png " alt="CloudFront CDN distribution" title="CloudFront CDN distribution"/></p>

### Change the code and test your links

The HTML code of our web app has only one direct access to a static file; the images referenced (using a relative route)
through the CSS stylesheet. We just need to change *form/templates/generic.html* and our web app is now retrieving all
static content from our CDN distribution.

Consider that we are now borrowing a CloudFront URL (RANDOM-ID-FROM-CLOUDFRONT.cloudfront.net) but usually, in the
setup, we will use a URL from our domain, something like *static.mydomain.com* to map the CDN distribution.

```html

<link href="//RANDOM-ID-FROM-CLOUDFRONT.cloudfront.net/custom.css" rel="stylesheet">
```

**Q55: Take a couple of screenshots of you S3 and CloudFront consoles to demonstrate that everything worked all right.**
Commit the changes on your web app, deploy them on Docker and check that it also works fine from there: **use
Google Chrome and check the origin of the files that you are loading (attach a screen shot similar to the one below)**:

 <p align="center"><img src="./images/Lab05-11.png " alt="Files loaded" title="Files loaded"/></p>

**Q56: How long have you been working on this session (including the optional part)? What have been the main
difficulties that you have faced and how have you solved them?** Add your answers to `README.md`.

Add all these files to your repository and comment what you think is relevant in your session's *README.md*.

### Django support for CDN

Having to go through the code of a web app to locate all the static files is a not only tedious task but also prone to
errors. Since Django Framework distinguishes the static content from the dynamic content, it supports the smooth
integration of a CDN to distribute it. Try configuring this feature if you are curious and have time.

First of all, you need to add the following package to your environment:

```bash
(eb-virt)_$ pip install django-storages
```

Then modify `eb-django-express-signup\eb-django-express-signup\settings.py` by adding 'storages' as an installed
application and tell Django to use the new storage schema as well as the name of your bucket and the name of the
CloudFront domain.

```python
INSTALLED_APPS = [
    ...
    'storages',
    ...
]

...

CLOUD_FRONT = os.environ['CLOUD_FRONT'] == 'True'

if CLOUD_FRONT:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_STORAGE_BUCKET_NAME = 'eb-django-express-signup-YOUR-ID'
    AWS_S3_CUSTOM_DOMAIN = 'RANDOM-ID-FROM-CLOUDFRONT.cloudfront.net'

```

Having done that you should be able to keep all static files declared the way Django expects to and, at the same time,
access them using a CDN.

```html

<link href="{% static 'custom.css' %}" rel="stylesheet"></head>
```

This should be the last step on the deployment of the web app and you can activate it only if the variable DEBUG is set
to False.

Django can also assume the synchronization of the static files to the CDN by means of the maintenace
command `python manage.py collectstatic`.

# How to submit this assignment:

Use the **private** repo named *https://github.com/CCBDA-UPC/2025-5-xx*. It needs to have, at least, two
files `README.md` with your responses to the above questions and `authors.json` with both members email addresses:

```json5
{
  "authors": [
    "FIRSTNAME1.LASTNAME1@estudiantat.upc.edu",
    "FIRSTNAME2.LASTNAME2@estudiantat.upc.edu"
  ]
}
```

1. Create some screen captures of your:

- DyanmoDB table with the data of the new leads.
- Make sure you have written your responses to the above questions in `README.md`.

2. Add any comment that you consider necessary at the end of the 'README.md' file

Make sure that you have updated your local GitHub repository (using the `git`commands `add`, `commit` and `push`) with
all the files generated during this session.

Commit the `README.md` file to your **responses repository** and commit all changes to the **web app repository**. Do
not mix the repository containing the course answers with the repository that holds the changes to your web app.

Make sure that you have updated your local GitHub repository (using the `git`commands `add`, `commit` and `push`) with
all the files generated during this session.

**Before the deadline**, all team members shall push their responses to their private
*https://github.com/CCBDA-UPC/2025-5-xx* repository.