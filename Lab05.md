# Lab session 5: Deploy a custom web app using additional cloud services

### Django: web framework

[Django](https://www.djangoproject.com/start/) is a high-level Python web framework designed for rapid development and
clean, pragmatic design. Built by experienced developers, it handles many complexities of web development, allowing you
to focus on building your application without reinventing the wheel. Plus, it’s free and open source.

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

<img alt="Lab05-CDN.png" src="images/Lab05-CDN.png" width="50%"/>

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
as a **zip file**.

<img alt="Lab05-webapp-zip.png" src="images/Lab05-webapp-zip.png" width="50%"/>

Unzip the file inside your responses repository for the current Lab session, and change the name of the folder to *
*django-webapp*.

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

## boto3

Once you are inside the directory create a `.env` file with the configuration of the project:

```bash
DEBUG=True
STARTUP_SIGNUP_TABLE=ccbda-signup-table
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=<YOUR-ACCESS-KEY-ID>
AWS_SECRET_ACCESS_KEY=<YOUR-SECRET-ACCESS-KEY>
AWS_SESSION_TOKEN=<YOUR-AWS-SESSION-TOKEN>
```

**DO NOT PUSH AWS CREDENTIALS TO YOUR PRIVATE REPOSITORY !!!**

Next, create a **new Python 3.10 virtual environment** specially for this web app and install the packages required to
run it.

We are creating a new Python virtual environment locally only to keep the packages that the web app uses. Having a small
Python environment implies a faster web app startup avoiding, as much as possible, any hidden dependencies and
ambiguities.

Check the contents of the file **requirements.txt** that the web application declares as the set of Python packages, and
its version, that it requires to be executed successfully.

The package `boto3` is a library that hides de AWS REST API to the programmer and manages the communication between the
web app and all the AWS services. Check [**Boto 3 Documentation
**](https://boto3.readthedocs.io/en/latest/reference/services/index.html) for more details.

Please, note the different prompt  `(.env) _$`  vs. `_$` when you are inside or outside the Python virtual
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

You can also create a PyCharm configuration tu run or debug the code.

<img src="./images/Lab04-pycharm-config.png" alt="AWS service" title="AWS service" width="80%"/>

Once the web app is running, check that you have configured the access to DynamoDB correctly by interacting with the web
app through your browser [http://127.0.0.1:8000/](http://127.0.0.1:8000/).

Go to the DynamoDB table browser tab and verify that the **ccbda-signup-table** table contains the new records that the
web app should have created. If all the above works correctly, you are almost ready to transfer the web app to Docker.

The Python virtual environment will be re-created remotely by Docker through the use of the file *requirements.txt* and
other configuration that you are going to set up later.

<a name="Task54"/>

## Task 5.4: Configure Docker and deploy the target web app

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

### Adding the Docker images to Amazon ECR

In this task you will add the Docker images that you created to an Amazon Elastic Container Registry (Amazon ECR)
repository.

Authorize your Docker client to connect to the Amazon ECR service.

#### Discover your AWS account ID.

In the AWS Management Console, in the upper-right corner, choose your user name. Your user name begins with voclab/user.

<img alt="Lab05-aws-account.png" src="images/Lab05-aws-account.png" width="50%"/>

Copy the My Account value from the menu. This is your AWS account ID.

Next, return to the VS Code IDE Bash terminal.

To authorize your VS Code IDE Docker client, run the following command. Replace `<account-id>` with the actual account
ID that you just found:

```bash
_$ aws ecr get-login-password --region us-east-1 --profile learning-lab | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
Login Succeeded
```

A message indicates that the login succeeded.

To create the repository, run the following command:

```bash
_$ aws ecr create-repository --region us-east-1 --profile learning-lab --repository-name django-webapp-web
{
    "repository": {
        "repositoryArn": "arn:aws:ecr:us-east-1:383312122003:repository/django-webapp-web",
        "registryId": "383312122003",
        "repositoryName": "django-webapp-web",
        "repositoryUri": "383312122003.dkr.ecr.us-east-1.amazonaws.com/django-webapp-web",
        "createdAt": "2025-03-11T19:34:44.374000+01:00",
        "imageTagMutability": "MUTABLE",
        "imageScanningConfiguration": {
            "scanOnPush": false
        }
    }
}
```

The response data is in JSON format and includes a repositoryArn value. This is the URI that you would use to reference
your image for future deployments.

The response also includes a registryId, which you will use in a moment.

### Tag the Docker image.

In this step, you will tag the image with your unique registryId value to make it easier to manage and keep track of
this image.

Run the following command. Replace <registry-id> with your actual registry ID number.

```
_$ docker tag django-webapp-web:latest <registry-id>.dkr.ecr.us-east-1.amazonaws.com/django-webapp-web:latest
```

The command does not provide a response.

To verify that the tag was applied, run the following command:

```bash
_$ docker images
REPOSITORY                                                       TAG       IMAGE ID       CREATED         SIZE
383312122003.dkr.ecr.us-east-1.amazonaws.com/django-webapp-web   latest    267825271330   50 minutes ago      472MB
django-webapp-web                                                latest    267825271330   50 minutes ago      472MB
django-docker                                                    latest    76fe7cceb54c   50 minutes ago      472MB
docker/welcome-to-docker                                         latest    eedaff45e3c7   16 months ago      29.5MB
```

This time, notice that the latest tag was applied and the image name includes the remote repository name where you
intend to store it.

### Push the Docker image to the Amazon ECR repository.

To push your image to Amazon ECR, run the following command. Replace <registry-id> with your actual registry ID number:

```bash
_$ docker push <registry-id>.dkr.ecr.us-east-1.amazonaws.com/django-webapp-web:latest
The push refers to repository [383312122003.dkr.ecr.us-east-1.amazonaws.com/django-webapp-web]
4b785e93aa71: Pushed 
be1449717b1e: Pushed 
ff1399ac0930: Pushed 
7cf63256a31a: Pushed 
dac1d3453b30: Pushed 
e1599d0f5c4d: Pushed 
8b6fcbaf930d: Pushed 
000e068808cd: Pushed 
latest: digest: sha256:2678252713306015408b4236326c85c11e059cb3b10904650a299143789a90df size: 856
```

To confirm that the django-webapp-web image is now stored in Amazon ECR, run the following aws ecr list-images command:

```bash
_$ aws ecr list-images --region us-east-1 --profile learning-lab --repository-name django-webapp-web
{
    "imageIds": [
        {
            "imageDigest": "sha256:f7148ebbf59e9d417787189935b5b1db8f2de609a2bfbde559a13fed2125fc09"
        },
        {
            "imageDigest": "sha256:15d7d9cbdd1c90804fc4beea182006d6212497d936182a5c19e3b52ca24932e6"
        },
        {
            "imageDigest": "sha256:2678252713306015408b4236326c85c11e059cb3b10904650a299143789a90df",
            "imageTag": "latest"
        }
    ]
}
```

You can also find more details about the repositories that you have created.

```bash
_$ aws ecr --region us-east-1 --profile learning-lab describe-repositories
{
    "repositories": [
        {
            "repositoryArn": "arn:aws:ecr:us-east-1:383312122003:repository/django-webapp-web",
            "registryId": "383312122003",
            "repositoryName": "django-webapp-web",
            "repositoryUri": "383312122003.dkr.ecr.us-east-1.amazonaws.com/django-webapp-web",
            "createdAt": "2025-03-09T19:34:44.374000+01:00",
            "imageTagMutability": "MUTABLE",
            "imageScanningConfiguration": {
                "scanOnPush": false
            }
        }
    ]
}
```

And information about the images of the repository.

```bash
_$ aws ecr --region us-east-1 --profile learning-lab describe-images --repository-name django-webapp-web 
{
    "imageDetails": [
        {
            "registryId": "383312122003",
            "repositoryName": "django-webapp-web",
            "imageDigest": "sha256:f7148ebbf59e9d417787189935b5b1db8f2de609a2bfbde559a13fed2125fc09",
            "imageSizeInBytes": 1347,
            "imagePushedAt": "2025-03-09T19:36:55.306000+01:00"
        },
        {
            "registryId": "383312122003",
            "repositoryName": "django-webapp-web",
            "imageDigest": "sha256:15d7d9cbdd1c90804fc4beea182006d6212497d936182a5c19e3b52ca24932e6",
            "imageSizeInBytes": 107561397,
            "imagePushedAt": "2025-03-09T19:36:55.302000+01:00"
        },
        {
            "registryId": "383312122003",
            "repositoryName": "django-webapp-web",
            "imageDigest": "sha256:2678252713306015408b4236326c85c11e059cb3b10904650a299143789a90df",
            "imageTags": [
                "latest"
            ],
            "imageSizeInBytes": 107561397,
            "imagePushedAt": "2025-03-09T19:36:55.949000+01:00"
        }
    ]
}
```

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

<img src="./images/Lab05-2.png " alt="Confirmed" title="Confirmed"/>

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

<img src="./images/Lab05-6.fw.png " alt="Search" title="Search"/>

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

<img src="./images/Lab05-7.png " alt="Search" title="Search"/>

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

 <img src="./images/Lab06-S3-public-access.png" alt="S3 public access" title="S3 public access"/>

 <img src="./images/Lab05-8.png " alt="S3 bucket" title="S3 bucket"/>

This time add the files manually and grant them public read permission.

  <img src="./images/Lab05-9.png " alt="S3 bucket" title="S3 bucket"/>

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

<img src="./images/Lab05-12.png " alt="S3 address" title="S3 address"/>

### Create a CloudFront CDN Web Distribution

Following the steps
at ["Getting Started with CloudFront CDN"](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/GettingStarted.html)
we end up having to wait until the files are distributed. It takes five minutes or more, be patient. Once the first
distribution is set up, whenever you resync your static contents it will take much less.

 <img src="./images/Lab05-10.png " alt="CloudFront CDN distribution" title="CloudFront CDN distribution"/>

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

 <img src="./images/Lab05-11.png " alt="Files loaded" title="Files loaded"/>

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

1. Create some screen captures of your:

- DyanmoDB table with the data of the new leads.
- Make sure you have written your responses to the above questions in `README.md`.

2. Add any comment that you consider necessary at the end of the 'README.md' file

Make sure that you have updated your local GitHub repository (using the `git` commands `add`, `commit`, and `push`) with
all the files generated during this session.

**Before the deadline**, all team members shall push their responses to their private
*https://github.com/CCBDA-UPC/2024-5-xx* repository.