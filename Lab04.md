# Lab session #4: Use of services programmatically through their API

[Scrapy](https://scrapy.org/) is a Python framework for large-scale web scraping. It provides all the tools needed to extract data from websites efficiently, process them as required, and [store them in the most suitable structure and format](https://doc.scrapy.org/en/latest/topics/feed-exports.html).

[AWS Rekognition](https://aws.amazon.com/rekognition/)  is an image recognition service that detects objects, scenes, activities, landmarks, faces, dominant colors, and image quality. AWS Rekognition also extracts text, recognizes celebrities, and identifies inappropriate image content.

In this lab session, you will learn how to extract data from web pages and then analyze the images and videos using AWS Rekognition to obtain some interesting insights.

#  Pre-lab homework

<a name="aws"/>

Go to the AWS Academy and log into the course [AWS Academy Learner Lab](https://awsacademy.instructure.com/courses/109367). 

Watch the videos
- Demo - How to Access Learner Lab
- Demo - General Troubleshooting Tips
- Demo - How to Launch Services through AWS Console

If you cannot see the Learner Lab as shown below you may need to check that your browser is allowing 3rd party cookies (at least to execute the Learner Lab).

  <img src="images/Lab04-LearnerLab.jpeg" alt="Lab04-LearnerLab.jpeg"  style="width: 50%; padding-left: 25%;">


 You can go back into stopping 3rd party cookies after working with the environment.

  <img src="images/Lab04-3rd-party-cookies.png" alt="Lab04-3rd-party-cookies.png"  style="width: 50%; padding-left: 25%;">

#  Tasks for Lab session #4

* [Task 4.1: Extract images from a website](#Tasks41)
* [Task 4.2: Obtain insights about an image using AWS Rekognition](#Tasks42) 
* [Task 4.3: Get insights into a website images using AWS Rekognition](#Tasks43) 

<a name="Tasks41"/>

## Task 4.1: Extract images from a website

Learn more about Scrapy by reading a detailed [Scrapy Tutorial](https://doc.scrapy.org/en/latest/intro/tutorial.html) and [Scrapy documentation](https://doc.scrapy.org/en/latest/).

### Scrapy installation

Scrapy can be installed using pip.

```bash
_$ pip install scrapy
```

### Scrapy shell

Once the Scrapy package is installed, you can use the Scrapy shell to do some testing before programming your web data extraction. In the following example, we download the home page of ["Universitat Politècnica de Catalunya"](https://www.upc.edu/). Please, inspect the structure of the HTML, and extract the images included in each page. As you can see we can use a CSS syntax to select the HTML elements of the page.

```python
fetch("https://www.upc.edu/")
print(response.text)
response.css("img").extract_first()
response.css("a").extract_first()
```

To find the "search path" you may want to use Google Chrome, find the URL, inspect the code, and use the search bar at the bottom of the code to match the path.

### Scrapy custom spyders

Once you have explored the page you can write a custom spyder to programmatically extract data from HTML pages.

```bash
_$ scrapy startproject imageScraper
```

The above command will create the following file structure in the current directory:


  <img src="images/Lab04-imageScraper.png" alt="Lab04-imageScraper.png"  style="height: 400px; padding-left: 25%;">


The most important components are the file `imageScraper/settings.py` containing the settings for the project and the directory `imageScraper/spiders/` that keeps all the custom spiders.

We can use the DEPTH_LIMIT configuration variable to restrict image retrieval to first-level pages (e.g., www.upc.edu/xxx/) and exclude second-level (e.g., www.upc.edu/xxx/yyy/) and third-level URLs (e.g., www.upc.edu/xxx/yyy/zzz/) and beyond. By setting DEPTH_LIMIT to 0, which is the default value, the crawler will access pages at all levels within the website.

```python
DEPTH_LIMIT = 1
```

Now you can create a new spider by typing:

```bash
_$ cd imageScraper
_$ scrapy genspider image www.upc.edu
```

The execution creates a file named `imageScraper/spiders/image.py` inside the project directory. The file contains the following basic code:
```python
import scrapy


class ImageSpider(scrapy.Spider):
    name = 'image'
    allowed_domains = ['www.upc.edu']
    start_urls = ['http://www.upc.edu/']

    def parse(self, response):
        pass
```

Few things to note here:

- **name**: Name of the spider, in this case, it is “image”. Naming spiders properly is essential when you have to maintain hundreds of spiders.
- **allowed_domains**: An optional list of strings containing domains that this spider is allowed to crawl. Requests for URLs not belonging to the domain names specified in this list won’t be followed.
- **parse(self, response)**: This function is called whenever the crawler successfully crawls a URL. Remember the response object from earlier?.

After every successful crawl the *parse(..)* method is called, and so that’s where you write your extraction logic. 

For our example, we decide that we want to extract the list of images from the homepage.

```python
import scrapy
from urllib.parse import urljoin

class ImagesSpider(scrapy.Spider):
    name = "images"
    allowed_domains = ["www.upc.edu"]
    start_urls = ["https://www.upc.edu"]

    def parse(self, response):
        # Extract image URLs
        for img in response.css("img"):
            image_src = img.attrib.get('src') or img.attrib.get('data-src')  # Fallback to 'data-src'
            if image_src is not None:
                full_image_url = urljoin(response.url, image_src)
                yield {
                    'img_url': full_image_url,
                    'appears_url': response.url,
                }
```

Once the homepage has been crawled we can continue crawling the rest of the URLs that appear in the page by selecting the tag **a** (anchor) with the attribute **href**.
```python
        # Extract and follow hyperlinks
        for link in response.css("a[href]"):
            link_href = link.attrib.get('href')
            if link_href and link_href.startswith('https://'):  # Validating full link
                yield response.follow(link_href, callback=self.parse)
```
We can feed the crawler with all the URLs found. The only URLs that will be crawled will be the ones matching the allowed_domains and the DEPTH_LIMIT defined.

```python
    allowed_domains = ["www.upc.edu"]
```
We need to get the list of unique images found. It is possible to define `unique_images` inside the `ImagesSpider` class.
```python
    unique_images = []
```

We'll add the images to the list only if it is not already present.

```python
                if full_image_url not in self.unique_images:
                    self.unique_images.append(full_image_url)
```

`closed` is a method that can be defined in class `ImagesSpider` and it is invoked once all the URLs have been crawled.

```python

    def closed(self, cause):
        self.unique_images.sort()
        print(self.unique_images)
```

The above code yields a JSON record containing something like the following example:

```json
   {
    "img_url": "https://www.upc.edu/++theme++homeupc/assets/images/Logo.svg",
    "appears_url": "https://www.upc.edu/ca"
  }
```

### Extract your results to a JSON file

To obtain the results of parsing the home page of the UPC we can type at the command line below. We use the *name* of the parser and tell it to output the result to a file that will contain a list of JSON records.

```bash
_$ scrapy crawl image -o image.json

```

To debug the code using PyCharm we can add a new file named `main.py`, in the same directory containing `scrapy.cnf`, that will contain the command line that we typed before. I strongly advise you to use this option to speed up the creation of your parsers.


  <img src="images/Lab04-pycharmConfig.png" alt="Lab04-pycharmConfig" style="width: 50%; padding-left: 25%">



```python
from scrapy import cmdline

cmdline.execute("scrapy crawl image -o image.json".split())
```


**Q41** Add all the files that you have created to your private .*https://github.com/CCBDA-UPC/2024-4-xx* repository. Add your thoughts about the above task.



<a name="Tasks42"/>

## Task 4.2: Obtain insights about an image using AWS Rekognition

Open the modules and open the "Learner Lab". Click the button "Start Lab", wait until the environment is up, and then click "AWS" at the top of the window and open the AWS Console.

<img src="./images/Lab04-LearnerLab.jpeg" alt="Learner lab" title="Learner lab"/>

Once the AWS Console is open find the service "Amazon Rekognition" and launch the demo.


Play with the demo using the provided image some of the images obtained in the previous section.

![Lab04-sampleImage.jpeg](images/Lab04-sampleImage.jpeg)

![Lab04-RekognitionDemo.png](images/Lab04-RekognitionDemo.png)

**Q421 Add your thoughts about the above task.** 

### Create a Python script that sends an image to AWS Rekognition and retrieves the analysis

Using the "AWS Academy Learner Lab" AWS console it is only possible to execute Python code in the browser terminal of the environment.

Currently, the terminal shown in the screenshot above includes Python 3.7 which is incompatible with the boto3 version. You can also obtain a terminal by clicking on the icon shown in blue in the screenshot below.

![Lab04-terminal.png](images/Lab04-terminal.png)


#### Create a Personal Access Token on GitHub

From your GitHub account, 

1. go to Settings 
2. Developer Settings 
3. Personal Access Token 
4. Generate New Token (Classic)
5. Fillup the form 
6. Click full control of private repositories
7. Click Generate token
8. Copy the generated Token, it will be something like ``ghp_sFhFsSHhTzMDreGRLjmks4Tzuzgthdvfsrta``

Keep the token in a safe place, such as a password manager, for future use.


#### Clone your repository

Use the following command to clone your repository inside the AWS command line environment. For the password use the Personal Access Token created before.

```bash
_$ git clone https://github.com/CCBDA-UPC/2025-4-XX.git Lab4
Cloning into 'Lab4'...
Username for 'https://github.com': YOUR@EMAIL.COM
Password for 'https://YOUR@EMAIL.COM@github.com': ghp_sFhFsSHhTzMDreGRLjmks4Tzuzgthdvfsrta
remote: Enumerating objects: 9, done.
remote: Counting objects: 100% (9/9), done.
remote: Compressing objects: 100% (7/7), done.
remote: Total 9 (delta 1), reused 3 (delta 0), pack-reused 0
Unpacking objects: 100% (9/9), done.
Checking connectivity... done.
```

#### Add a script to interact with AWS Comprehend

Use the code in [`Recognize_1.py`](Recognize_1.py) which uses the [boto3 library](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/quickstart.html) to invoke the [image recognition service](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rekognition.html) and outputs the result.

```python
import boto3
import json

with open('sample.jpeg', 'rb') as fd:
    image = fd.read()

recognize = boto3.client('rekognition')
labels_list = recognize.detect_labels(Image={'Bytes': image}, MaxLabels=10, MinConfidence=70)
print(json.dumps(labels_list, indent=4))
```

Commit the Python file to the session repo, add the image file [`sample.jpg`](../images/Lab04-sampleimage.jpg) and push them both it. At the AWS console pull the code and execute it.

```bash
_$ git pull
_$ python Recognize_1.py
{
    "Labels": [
        {
            "Name": "Crowd",
            "Confidence": 99.99995422363281,
            "Instances": [],
            "Parents": [
                {
                    "Name": "Person"
                }
            ],
            "Aliases": [],
            "Categories": [
                {
                    "Name": "Person Description"
                }
            ]
        },
        {
            "Name": "Person",
            "Confidence": 99.99995422363281,
            "Instances": [
                {
                    "BoundingBox": {
                        "Width": 0.12894393503665924,
                        "Height": 0.35750454664230347,
                        "Left": 0.4808120131492615,
                        "Top": 0.3740279972553253
                    },
                    "Confidence": 99.70088958740234
                },
...
```
**Q422 Add your thoughts about the above task.** 

<a name="Tasks43"/>

## Task 4.3: Get insights of website images using AWS Rekognition

Using the code above build a Python application that obtains some insights out of website images. You are free to use any AWS Rekognition functionality.

You may want to use the [requests](https://pypi.org/project/requests/) Python library to interact with the images.

**Q431 What is the goal of your application?**

Include the code modifications and eventual new files in the repo.

**Q432  Add your thoughts about the application developed and the results that you have obtained.**


Make sure that you have updated your local GitHub repository (using the `git` commands `add`, `commit`, and `push`) with all the files generated during this session. 

**Before the deadline**, all team members shall push their responses to their private *https://github.com/CCBDA-UPC/2024-4-xx* repository.