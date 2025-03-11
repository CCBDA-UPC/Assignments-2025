# Lab session 5: Deploy a custom web app using additional cloud services

### Django: web framework

[Django](https://www.djangoproject.com/start/) is a high-level Python web framework designed for rapid development and
clean, pragmatic design. Built by experienced developers, it handles many complexities of web development, allowing you
to focus on building your application without reinventing the wheel. Plus, it’s free and open source.

## Deploying an example Web App

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


## Prerequisites

Make sure that you :

- Have [Django](https://www.djangoproject.com/start/) installed on your system.
- Install [Docker Desktop](https://www.docker.com/products/docker-desktop/)
  and [Docker Compose](https://docs.docker.com/compose/) on your machine.

If you need help with the installation, you can find detailed instructions on the Docker and Django websites.

## Session taks

* [Task 5.1: Create a DynamoDB Table](#Task51)
* [Task 5.2: Download the code for the Web App](#Task52)
* [Task 5.3: Test the web app locally](#Task53)
* [Task 5.4: Use AWS Simple Notification Service in your web app](#Tasks54)


<a name="Task51"/>

## Task 5.1: Create a DynamoDB Table

The signup app uses a DynamoDB table to store the contact information that users submit.

#### To create a DynamoDB table

Go to the course "AWS Academy Learner Lab", open the modules and open the "Learner Lab". Click the button "Start Lab",
wait until the environment is up and then click "AWS" at the top of the window and open the AWS Console.

1. At the console search for "DynamoDB".

3. Go to Tables and **Create table**.

4. For Table name, type **ccbda-signup-table**.

5. For the `Partition key`, type `email`. Choose **Create**.

<a name="Task52"/>
## Task 5.2: Download the code for the Web App

You are going to make a few changes to the base Python code. Therefore, download
the [repository](https://github.com/CCBDA-UPC/django-webapp) on your local disk drive
as a **zip file**.

<img alt="Lab05-webapp-zip.png" src="images/Lab05-webapp-zip.png" width="50%"/>

Unzip the file inside your responses repository for the current Lab session, and change the name of the folder to **django-webapp**.

<a name="Task53"/>
## Task 5.3: Test the web app locally

Create a `.env` file with the configuration of the project:

```bash
DEBUG=True
STARTUP_SIGNUP_TABLE=ccbda-signup-table
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=<YOUR-ACCESS-KEY-ID>
AWS_SECRET_ACCESS_KEY=<YOUR-SECRET-ACCESS-KEY>
AWS_SESSION_TOKEN=<YOUR-AWS-SESSION-TOKEN>
```

The .gitignore file contains rules to avoid pushing to the repository files such as `.env` containing sensitive information. **Make sure to have such functionality present in your future projects**.

Next, create a **new Python 3.10 virtual environment** specially for this web app and install the packages required to
run it.

We are creating a new Python virtual environment locally only to keep the packages that the web app uses. Having a small
Python environment implies a faster web app startup avoiding, as much as possible, any hidden dependencies and
ambiguities.

Check the contents of the file **requirements.txt** that the web application declares as the set of Python packages, and
its version, that it requires to be executed successfully.

The package `boto3` is a library that hides de AWS REST API to the programmer and manages the communication between the
web app and all the AWS services. 
Check [**Boto 3 Documentation**](https://boto3.readthedocs.io/en/latest/reference/services/index.html) for more details.

Please, note the different prompt  `(.env) _$`  vs. `_$` when you are inside or outside the Python virtual
environment.

```
_$ virtualenv -p python3 ../.venv
_$ source ../.venv/bin/activate
(.venv)_$ pip install -r requirements.txt
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

You can also create a PyCharm configuration tu run or debug the code.

<img src="./images/Lab04-pycharm-config.png" alt="AWS service" title="AWS service" width="80%"/>


Once the web app is running, check that you have configured the access to DynamoDB correctly by interacting with the web
app through your browser [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

Go to the DynamoDB table browser tab and verify that the **ccbda-signup-table** table contains the new records that the
web app should have created. If all the above works correctly, you are almost ready to transfer the web app to Docker.


<a name="Tasks54" />

## Task 5.4: Use AWS Simple Notification Service in your web app

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

To confirm the subscription, AWS SNS sends an email named *AWS Notification — Subscription Confirmation*. Open the
link in the email to confirm your subscription.

Do not forget that before testing the new functionality you need to have the AWS SNS subscription approved.

<img src="./images/Lab05-2.png " alt="Confirmed" title="Confirmed"/>

Add the *unique identifier* for the AWS SNS topic to the configuration environment of your local deployment.

```bash
_$ export NEW_SIGNUP_TOPIC="arn:aws:sns:us-east-1:YOUR-ACCOUNT-ID:gsg-signup-notifications"
```

Before you forget, you can also add a new variable to the configuration file.

### Modify the web app to send messages

Open the files *form/models.py* and *form/views.py* read and understand what the code does.

Add the code below to *form/models.py* as a new operation of the model *Leads()*.

```python
def send_notification(self, email):
    sns = boto3.client('sns', region_name=settings.AWS_REGION,
                       aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                       aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                       aws_session_token=settings.AWS_SESSION_TOKEN)
    try:
        sns.publish(
            TopicArn=settings.NEW_SIGNUP_TOPIC,
            Message='New signup: %s' % email,
            Subject='New signup',
        )
        logger.error('SNS message sent.')

    except Exception as e:
        logger.error(
            'Error sending AWS SNS message: ' + (e.fmt if hasattr(e, 'fmt') else '') + ','.join(e.args))
```

You have probably noticed that there is a Python variable *NEW_SIGNUP_TOPIC*  that needs to be instantiated in the files `settings.py` and `.env`.

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

Close the file and execute the Django web app locally. You can post a new record. This time you see no error, and you
receive a notification in your e-mail.

```bash
New item added to database.
SNS message sent.
"POST /signup HTTP/1.1" 200 0
```

**Q52: Has everything gone alright?** Add your answers to the `README.md` file in the responses repository.


# How to submit this assignment:

1. Create some screen captures of your:

- DyanmoDB table with the data of the new leads.
- Make sure you have written your responses to the above questions in `README.md`.

2. Add any comment that you consider necessary at the end of the 'README.md' file

Make sure that you have updated your local GitHub repository (using the `git` commands `add`, `commit`, and `push`) with
all the files generated during this session.

**Before the deadline**, all team members shall push their responses to their private
*https://github.com/CCBDA-UPC/2024-5-xx* repository.