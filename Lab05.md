# Lab session 5: Deploy a custom web app using additional cloud services

We are going to assume that you are working on a new subject on Cloud Computing that isn't ready for students to enroll
yet, but in the meantime, you plan to deploy a small placeholder app that collects contact information from the website
visitors who sign up to hear more. The signup app will help you reach potential students who might take part in a
private beta test of the laboratory sessions.

### The Signup App

The app will allow your future students to submit contact information and express interest in a preview of the new
subject on Cloud Computing that you're developing.

To make the app look good, we use [Bootstrap](https://getbootstrap.com/), a mobile-first front-end framework that started as a Twitter project.

#### Django: web framework

[Django](https://www.djangoproject.com/start/) is a high-level Python web framework designed for rapid development and
clean, pragmatic design. Built by experienced developers, it handles many complexities of web development, allowing you
to focus on building your application without reinventing the wheel. Plus, it’s free and open source.

### AWS DynamoDB

**Amazon DynamoDB**, a NoSQL database service, is going to be used to store the contact information that users submit.

DynamoDB is a schema-less database, so you need to specify only a primary key attribute. Let us use the email field as a
key for each register.

### AWS Simple Notification Service (SNS)

We want to know when customers submit a form, therefore we are going to use **AWS Simple Notification Service** (AWS
SNS), a message pushing service that can deliver notifications over various protocols. For our web app, we are going to
push notifications to an email address.

# Pre-lab homework

Make sure that you install [Docker Desktop](https://www.docker.com/products/docker-desktop/)
  and [Docker Compose](https://docs.docker.com/compose/) on your machine.

If you need help with the installation, you can find detailed instructions on the Docker and Django websites.

# Tasks for Lab session #5

* [Task 5.1: Create a DynamoDB Table](#Task51)
* [Task 5.2: Download the code for the Web App](#Task52)
* [Task 5.3: Test the web app locally](#Task53)
* [Task 5.4: Use AWS Simple Notification Service in your web app](#Tasks54)
* [Task 5.5: Configure Docker and deploy the target web app](#Tasks55)

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

Unzip the file inside your responses repository for the current Lab session, and change the name of the folder to 
**django-webapp**.

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

The .gitignore file contains rules to avoid pushing to the repository files such as `.env` containing sensitive
information. **Make sure to have such functionality present in your future projects**.

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

Please, note the different prompt  `(.env)_$`  vs. `_$` when you are inside or outside the Python virtual
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

**Q53: Create some screen captures of your DyanmoDB table with the data of the new leads. Add your thoughts on the above
tasks**

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

You have probably noticed that there is a Python variable *NEW_SIGNUP_TOPIC*  that needs to be instantiated in the files
`settings.py` and `.env`.

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

**Q54: Has everything gone alright? Share your thoughts on the task developed above.** 

<a name="Tasks55" />

## Task 5.5: Configure Docker and deploy the target web app

In this task, you will migrate the web application to run in a Docker container. The Docker container is portable and
could run on any OS that has the Docker engine installed.

### Create a Dockerfile

A Dockerfile is a script that tells Docker how to build your Docker image. Put it in the root directory of your Django
project. Here’s a basic Dockerfile setup for Django:

```dockerfile
# Use the official Python runtime image
FROM python:3.10.16  
 
# Create the app directory
RUN mkdir /app
 
# Set the working directory inside the container
WORKDIR /app
 
# Set environment variables 
# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
#Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED=1 
 
# Upgrade pip
RUN pip install --upgrade pip 
 
# Copy the Django project  and install dependencies
COPY requirements.txt  /app/
 
# run this command to install all dependencies 
RUN pip install --no-cache-dir -r requirements.txt
 
# Copy the Django project to the container
COPY . /app/
 
# Expose the Django port
EXPOSE 8000
 
# Run Django’s development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

Each line in the Dockerfile serves a specific purpose:

- **FROM**: Selects the image with the Python version you need.

- **WORKDIR**: Sets the working directory of the application within the container.

- **ENV**: Sets the environment variables needed to build the application

- **RUN** and **COPY** commands: Install dependencies and copy project files.

- **EXPOSE** and **CMD**: Expose the Django server port and define the startup command.

Go to your Docker Desktop and open the terminal, move to the directory where the web application is stored and build the
docker image.

```bash
_$ cd django-webapp               
_$ docker build -t django-docker .
[+] Building 46.9s (13/13) FINISHED                                                                 docker:desktop-linux
 => [internal] load build definition from Dockerfile                                                                0.0s
 => => transferring dockerfile: 837B                                                                                0.0s
 => [internal] load metadata for docker.io/library/python:3.10.16                                                   1.7s
 => [auth] library/python:pull token for registry-1.docker.io                                                       0.0s
 => [internal] load .dockerignore                                                                                   0.0s
 => => transferring context: 2B                                                                                     0.0s
 => [1/7] FROM docker.io/library/python:3.10.16@sha256:e70cd7b54564482c0dee8cd6d8e314450aac59ea0ff669ffa715207ea0  19.7s
 => => resolve docker.io/library/python:3.10.16@sha256:e70cd7b54564482c0dee8cd6d8e314450aac59ea0ff669ffa715207ea0e  0.1s
 => => sha256:2268f82e627e15f49be0d4a2ea64b579609dd1e83f7109001c1ba2b503d25c0a 21.38MB / 21.38MB                    0.9s
 => => sha256:7fda9d093afe6ee82a63b57b784201a3ff4cdc44bc37993859b2235396f03a39 250B / 250B                          0.4s
 => => sha256:a6c2fd51c72cc349607cc3d9f533a6b1b06da6bdd9ad1fb45853184de242cf15 6.16MB / 6.16MB                      1.0s
 => => sha256:1d281e50d3e435595c266df06531a7e8c2ebb0c185622c8ab2eed8d760e6576b 64.39MB / 64.39MB                    2.9s
 => => sha256:447713e77b4fc3658cfba0c1e816b70ff6d9bf06563dc8cfcb0459406aed33b4 211.34MB / 211.34MB                  6.2s
 => => sha256:155ad54a8b2812a0ec559ff82c0c6f0f0dddb337a226b11879f09e15f67b69fc 48.48MB / 48.48MB                    3.2s
 => => sha256:8031108f3cda87bb32f090262d0109c8a0db99168050967becefad502e9a681b 24.06MB / 24.06MB                    1.7s
 => => extracting sha256:155ad54a8b2812a0ec559ff82c0c6f0f0dddb337a226b11879f09e15f67b69fc                           2.8s
 => => extracting sha256:8031108f3cda87bb32f090262d0109c8a0db99168050967becefad502e9a681b                           0.7s
 => => extracting sha256:1d281e50d3e435595c266df06531a7e8c2ebb0c185622c8ab2eed8d760e6576b                           2.5s
 => => extracting sha256:447713e77b4fc3658cfba0c1e816b70ff6d9bf06563dc8cfcb0459406aed33b4                           7.3s
 => => extracting sha256:a6c2fd51c72cc349607cc3d9f533a6b1b06da6bdd9ad1fb45853184de242cf15                           0.7s
 => => extracting sha256:2268f82e627e15f49be0d4a2ea64b579609dd1e83f7109001c1ba2b503d25c0a                           1.1s
 => => extracting sha256:7fda9d093afe6ee82a63b57b784201a3ff4cdc44bc37993859b2235396f03a39                           0.0s
 => [internal] load build context                                                                                   4.4s
 => => transferring context: 71.02MB                                                                                4.3s
 => [2/7] RUN mkdir /app                                                                                            0.9s
 => [3/7] WORKDIR /app                                                                                              0.0s
 => [4/7] RUN pip install --upgrade pip                                                                             4.4s
 => [5/7] COPY requirements.txt  /app/                                                                              0.0s
 => [6/7] RUN pip install --no-cache-dir -r requirements.txt                                                        8.4s
 => [7/7] COPY . /app/                                                                                              1.8s
 => exporting to image                                                                                              9.7s
 => => exporting layers                                                                                             4.1s
 => => exporting manifest sha256:d87943d350d33c0c740353df3bcea16d2deac8c7b44b5707c2da351931f97f67                   0.0s
 => => exporting config sha256:d640e1522ea15b0f8031ecbd330582bed81a840d193bdd29e3895e98807dd490                     0.0s
 => => exporting attestation manifest sha256:02829dc4a862290e2162b98e564e2469800e39fe76a06e713515d1f7e701c0f7       0.0s
 => => exporting manifest list sha256:ce7ad84af491aee38a9ddd1aa48c3091ef95db73bddaed0edd097b891cdd13d1              0.0s
 => => naming to docker.io/library/django-docker:latest                                                             0.0s
 => => unpacking to docker.io/library/django-docker:latest                                                          5.5s

View build details: docker-desktop://dashboard/build/desktop-linux/desktop-linux/5ij0nji3h7am2wijladmaaxf1

What's next:
    View a summary of image vulnerabilities and recommendations → docker scout quickview 
_$ 
```

To see your image, you can run:

```bash 
_$ docker image list
REPOSITORY                 TAG       IMAGE ID       CREATED         SIZE
django-docker              latest    ce7ad84af491   4 minutes ago   1.71GB
docker/welcome-to-docker   latest    eedaff45e3c7   16 months ago   29.5MB
```

Although this is a great start in containerizing the application, you’ll need to make a number of improvements to get it
ready for production.

- The CMD manage.py is only meant for development purposes and should be changed for a WSGI server.
- Reduce the size of the image by using a smaller image.
- Optimize the image by using a multistage build process.

Let’s get started with these improvements.

### Update requirements.txt

Make sure to add `gunicorn` and `psycopg2-binary` to your `requirements.txt`. The updated file should include something
like this:

```text
gunicorn==23.0.0
packaging==24.2
psycopg2-binary==2.9.10
```

### Make improvements to the Dockerfile

The Dockerfile below has changes that solve the three items on the list. The changes to the file are as follows:

- Updated the FROM python:3.10 image to FROM python:3.10.16-slim. This change reduces the size of the image
  considerably, as the image now only contains what is needed to run the application.
- Added a multi-stage build process to the Dockerfile. When you build applications, there are usually many files left on
  the file system that are only needed during build time and are not needed once the application is built and running.
  By adding a build stage, you use one image to build the application and then move the built files to the second image,
  leaving only the built code. Read more about [multi-stage builds](https://docs.docker.com/build/building/multi-stage/)
  in the documentation.
- Add the Gunicorn WSGI server to the server to enable a production-ready deployment of the application.

```dockerfile
# Stage 1: Base build stage
FROM python:3.10.16-slim AS builder
 
# Create the app directory
RUN mkdir /app
 
# Set the working directory
WORKDIR /app
 
# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 
 
# Upgrade pip and install dependencies
RUN pip install --upgrade pip 
 
# Copy the requirements file first (better caching)
COPY requirements.txt /app/
 
# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
 
# Stage 2: Production stage
FROM python:3.13-slim
 
RUN useradd -m -r appuser && \
   mkdir /app && \
   chown -R appuser /app
 
# Copy the Python dependencies from the builder stage
COPY --from=builder /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/
 
# Set the working directory
WORKDIR /app
 
# Copy application code
COPY --chown=appuser:appuser . .
 
# Set environment variables to optimize Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 
 
# Switch to non-root user
USER appuser
 
# Expose the application port
EXPOSE 8000 
 
# Start the application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "my_docker_django_app.wsgi:application"]
```

Build the Docker container image again.

```bash
_$ docker build -t django-docker .
[+] Building 17.1s (17/17) FINISHED                                                                 docker:desktop-linux
 => [internal] load build definition from Dockerfile                                                                0.0s
 => => transferring dockerfile: 1.31kB                                                                              0.0s
 => [internal] load metadata for docker.io/library/python:3.10.16-slim                                              1.2s
 => [auth] library/python:pull token for registry-1.docker.io                                                       0.0s
 => [internal] load .dockerignore                                                                                   0.0s
 => => transferring context: 2B                                                                                     0.0s
 => [internal] load build context                                                                                   2.3s
 => => transferring context: 1.80MB                                                                                 2.2s
 => [builder 1/6] FROM docker.io/library/python:3.10.16-slim@sha256:f680fc3f447366d9be2ae53dc7a6447fe9b33311af2092  0.0s
 => => resolve docker.io/library/python:3.10.16-slim@sha256:f680fc3f447366d9be2ae53dc7a6447fe9b33311af209225783932  0.0s
 => CACHED [stage-1 2/6] RUN useradd -m -r appuser &&    mkdir /app &&    chown -R appuser /app                     0.0s
 => CACHED [builder 2/6] RUN mkdir /app                                                                             0.0s
 => CACHED [builder 3/6] WORKDIR /app                                                                               0.0s
 => CACHED [builder 4/6] RUN pip install --upgrade pip                                                              0.0s
 => CACHED [builder 5/6] COPY requirements.txt /app/                                                                0.0s
 => CACHED [builder 6/6] RUN pip install --no-cache-dir -r requirements.txt                                         0.0s
 => CACHED [stage-1 3/6] COPY --from=builder /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/si  0.0s
 => CACHED [stage-1 4/6] COPY --from=builder /usr/local/bin/ /usr/local/bin/                                        0.0s
 => CACHED [stage-1 5/6] WORKDIR /app                                                                               0.0s
 => [stage-1 6/6] COPY --chown=appuser:appuser . .                                                                  3.3s
 => exporting to image                                                                                             10.1s
 => => exporting layers                                                                                             4.1s
 => => exporting manifest sha256:bc9eadc64772ed10808c5a6e47fd759eabd0a3c028a7b9ba46f1c5adabb923c2                   0.0s
 => => exporting config sha256:b7bff0e3440c318539527ef475f58d151cfb45f961153bdb55c301bbc58b500e                     0.0s
 => => exporting attestation manifest sha256:69d0d27273e87affa3839514b30030693ec7f5e469ebb81e1cc305b5e8ed7eed       0.0s
 => => exporting manifest list sha256:e9bb759c1f1a64332b7dcc96f8273f9296e97162ac06191dcb6e86c6690cd7c0              0.0s
 => => naming to docker.io/library/django-docker:latest                                                             0.0s
 => => unpacking to docker.io/library/django-docker:latest                                                          5.9s

View build details: docker-desktop://dashboard/build/desktop-linux/desktop-linux/0abs142dld08kfq2hn6favhh7

What's next:
    View a summary of image vulnerabilities and recommendations → docker scout quickview 
```

After making these changes, we can run a docker image list again:

```text
_$ docker image list   
REPOSITORY                 TAG       IMAGE ID       CREATED          SIZE
django-docker              latest    e9bb759c1f1a   About a minute ago   472MB
docker/welcome-to-docker   latest    eedaff45e3c7   16 months ago        29.5MB
```

You can see a significant improvement in the size of the container.

The size was reduced from 1.71GB to 472MB, which leads to faster a deployment process when images are downloaded and
cheaper storage costs when storing images.

You could use docker init as a command to generate the Dockerfile and compose.yml file for your application to get you
started.

### Configure the Docker Compose file

A `compose.yml` file allows you to manage multi-container applications. Here, we’ll define both a Django container and a
PostgreSQL database container. The compose file makes use of the `.env` file.

```yaml
services:
  django-web:
    build: .
    container_name: django-docker
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      DJANGO_SECRET_KEY: ${DJANGO_SECRET_KEY}
      DEBUG: ${DEBUG}
      DJANGO_LOGLEVEL: ${DJANGO_LOGLEVEL}
      DJANGO_ALLOWED_HOSTS: ${DJANGO_ALLOWED_HOSTS}
    env_file:
      - .env
```

### Build and run your new Django project

To build and start your containers, run:

```bash
docker compose up --build
Compose now can delegate build to bake for better performances
Just set COMPOSE_BAKE=true
[+] Building 11.7s (17/17) FINISHED                                                                  docker:desktop-linux
 => [web internal] load build definition from Dockerfile                                                             0.0s
 => => transferring dockerfile: 1.31kB                                                                               0.0s
 => [web internal] load metadata for docker.io/library/python:3.10.16-slim                                           0.7s
 => [web internal] load .dockerignore                                                                                0.0s
 => => transferring context: 2B                                                                                      0.0s
 => [web internal] load build context                                                                                2.4s
 => => transferring context: 1.78MB                                                                                  2.4s
 => [web builder 1/6] FROM docker.io/library/python:3.10.16-slim@sha256:f680fc3f447366d9be2ae53dc7a6447fe9b33311af2  0.1s
 => => resolve docker.io/library/python:3.10.16-slim@sha256:f680fc3f447366d9be2ae53dc7a6447fe9b33311af2092257839327  0.0s
 => CACHED [web stage-1 2/6] RUN useradd -m -r appuser &&    mkdir /app &&    chown -R appuser /app                  0.0s
 => CACHED [web builder 2/6] RUN mkdir /app                                                                          0.0s
 => CACHED [web builder 3/6] WORKDIR /app                                                                            0.0s
 => CACHED [web builder 4/6] RUN pip install --upgrade pip                                                           0.0s
 => CACHED [web builder 5/6] COPY requirements.txt /app/                                                             0.0s
 => CACHED [web builder 6/6] RUN pip install --no-cache-dir -r requirements.txt                                      0.0s
 => CACHED [web stage-1 3/6] COPY --from=builder /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10  0.0s
 => CACHED [web stage-1 4/6] COPY --from=builder /usr/local/bin/ /usr/local/bin/                                     0.0s
 => CACHED [web stage-1 5/6] WORKDIR /app                                                                            0.0s
 => [web stage-1 6/6] COPY --chown=appuser:appuser . .                                                               1.6s
 => [web] exporting to image                                                                                         6.8s
 => => exporting layers                                                                                              4.2s
 => => exporting manifest sha256:15d7d9cbdd1c90804fc4beea182006d6212497d936182a5c19e3b52ca24932e6                    0.0s
 => => exporting config sha256:e3cc9933aa06751ff84a74acef780fb333bf8f10b9104b9b91bdf49e20e79e9f                      0.0s
 => => exporting attestation manifest sha256:f7148ebbf59e9d417787189935b5b1db8f2de609a2bfbde559a13fed2125fc09        0.0s
 => => exporting manifest list sha256:2678252713306015408b4236326c85c11e059cb3b10904650a299143789a90df               0.0s
 => => naming to docker.io/library/django-webapp-web:latest                                                          0.0s
 => => unpacking to docker.io/library/django-webapp-web:latest                                                       2.5s
 => [web] resolving provenance for metadata file                                                                     0.0s
[+] Running 3/3
 ✔ web                            Built                                                                              0.0s 
 ✔ Network django-webapp_default  Created                                                                            0.1s 
 ✔ Container django-docker        Created                                                                            0.4s 
Attaching to django-docker
django-docker  | [2025-03-09 17:31:35 +0000] [1] [INFO] Starting gunicorn 23.0.0
django-docker  | [2025-03-09 17:31:35 +0000] [1] [INFO] Listening at: http://0.0.0.0:8000 (1)
django-docker  | [2025-03-09 17:31:35 +0000] [1] [INFO] Using worker: sync
django-docker  | [2025-03-09 17:31:35 +0000] [7] [INFO] Booting worker with pid: 7
django-docker  | [2025-03-09 17:31:35 +0000] [8] [INFO] Booting worker with pid: 8
django-docker  | [2025-03-09 17:31:35 +0000] [9] [INFO] Booting worker with pid: 9

v View in Docker Desktop   o View Config   w Enable Watch
```

This command will download any necessary Docker images, build the project, and start the containers. Once complete, your
Django application should be accessible at http://localhost:8000.

### Test and access your application

Once the webapp is running, you can test it by navigating to http://localhost:8000. You should see Django’s welcome
page, indicating that your app is up and running. To verify the database connection, try running a migration:

```
_$ docker compose run django-web python manage.py migrate
```

**Q55: Share your thoughts on the task developed above.**

# How to submit this assignment:

Make sure that you have updated your local GitHub repository (using the `git` commands `add`, `commit`, and `push`) with
all the files generated during this session.

**Before the deadline**, all team members shall push their responses to their private
*https://github.com/CCBDA-UPC/2024-5-xx* repository.