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
speeds. CloudFront CDN works seamlessly with other AWS services including **AWS Shield** for DDoS mitigation,
**AWS S3**, **Elastic Load Balancing** or **AWS EC2** as origins for your applications, and **AWS Lambda** to run
custom code close to final viewers.

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

* [Task 5.5: Create a new option to retrieve the list of leads](#Tasks55)
* [Task 5.6: Improve the web app transfer of information](#Tasks56)
* [Task 5.7: Deliver static content using a Content Delivery Network](#Tasks57)


The Python virtual environment will be re-created remotely by Docker through the use of the file *requirements.txt* and
other configuration that you are going to set up later.


<a name="Task54"/>


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

CLOUD_FRONT = bool(os.environ.get("CLOUD_FRONT", default=False))

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