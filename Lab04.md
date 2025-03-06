# Lab session #4: Use of services programmatically through their API

[Scrapy](https://scrapy.org/) is a Python framework for large-scale web scraping. It provides all the tools needed to extract data from websites efficiently, process them as required, and [store them in the most suitable structure and format](https://doc.scrapy.org/en/latest/topics/feed-exports.html).

[AWS Rekognition](https://aws.amazon.com/rekognition/)  is an image recognition service that detects objects, scenes, activities, landmarks, faces, dominant colors, and image quality. AWS Rekognition also extracts text, recognizes celebrities, and identifies inappropriate image content.

In this lab session, you will learn how to extract data from webpages and then analyze the images and videos using AWS Rekognition to obtain some interesting insights.

* [Task 4.1: Extract images from a website](#Tasks41)
* [Task 4.2: Obtain insights about an image using AWS Rekognition](#Tasks42) 
* [Task 4.3: Study the obtained data using the AWS Rekognition](#Tasks43) 

<a name="Tasks41"/>

## Task 4.1: Extract images from a website

Learn more about Scrapy by reading a detailed [Scrapy Tutorial](https://doc.scrapy.org/en/latest/intro/tutorial.html) and [Scrapy documentation](https://doc.scrapy.org/en/latest/).

### Scrapy installation

Scrapy can be installed using pip.

```bash
_$ pip install scrapy
```

### Scrapy shell

Once the Scrapy package is installed, you can use the Scrapy shell to do some testing before programming your web data extraction. In the following example, we download the home page of ["Universitat Politècnica de Catalunya"](https://www.upc.edu/), take a look at the structure of the HTML and extract the images included in each page. As you can see we can use a CSS syntax to select the HTML elements of the page.

```python
fetch("https://www.upc.edu/")
print(response.text)
response.css("img").extract_first()
response.css("a").extract_first()
```

To find the "search path" you may want to use Google Chrome, find the URL, inspect the code and use the search bar at the botom of the code to match the path.

### Scrapy custom spyders

Once you have explored the page you can write a custom spyder to programmatically extract data from HTML pages.

```bash
_$ scrapy startproject imageScraper
```

The above command will create the following file structure in the current directory:

<p style="text-align: center;">
  <img src="images/Lab04-imageScraper.png" alt="Lab04-imageScraper.png" style="width: 50%;">
</p>

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
We'd like to get the list of unique images found. It is possible to define `unique_images` inside the `ImagesSpider` class.
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

<p style="text-align: center;">
  <img src="images/Lab04-pycharmConfig.png" alt="Lab04-pycharmConfig" style="width: 50%;">
</p>


```python
from scrapy import cmdline

cmdline.execute("scrapy crawl image -o image.json".split())
```


**Q41** Add all the files that you have created to your private .*https://github.com/CCBDA-UPC/2024-4-xx* repository. Add your thoughts about the task.



<a name="Tasks42"/>

## Task 4.2: Obtain insights about an image using AWS Rekognition



Make sure that you have updated your local GitHub repository (using the `git`commands `add`, `commit` and `push`) with all the files generated during this session. 

**Before the deadline**, all team members shall push their responses to their private *https://github.com/CCBDA-UPC/2024-4-xx* repository.