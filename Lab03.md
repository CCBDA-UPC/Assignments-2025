# Lab session #3: Basic use of the cloud

This lab session focuses on some fundamental AWS services, covering IAM, VPC setup, EC2. The goal is to build practical cloud computing skills and encourage critical thinking.

AWS Comprehend, a natural language processing service, is used to  explore the service's capabilities within the sandbox environment provided and connect it with the previous lab session analyzing text in a more sophisticated manner.

<a name="Prelab"/>

#  Pre-lab homework

<a name="aws"/>

Go to the AWS Academy and log into the course [AWS Academy Learner Lab](https://awsacademy.instructure.com/courses/109367). 

Watch the videos
- Demo - How to Access Learner Lab
- Demo - General Troubleshooting Tips
- Demo - How to Launch Services through AWS Console

If you cannot see the 

you may need to check that your browser is allowing 3rd party cookies (at least to execute the Learner Lab). You can go back into stopping 3rd party cookies after working with the environment.

![Lab03-3rd-party-cookies.png](images/Lab03-3rd-party-cookies.png)

#  Tasks for Lab session #3

Go to the AWS Academy and log into the course [AWS Academy Cloud Foundations](https://awsacademy.instructure.com/courses/109366) and follow the laboratories detailed below.

Provide screeenshots of the major milestones and your explanation about what you have learned or observed. It does not have to be a repetition of the course but your own thoughts and conclusions. Write your feedback in the README.md file linking the images appropiatedly.

## Task 3.1: Introduction to AWS IAM

Follow the lab session: **Module 4 - AWS Cloud Security** *Lab 1 - Introduction to AWS IAM*

**Q31 Provide screeenshots of the major milestones and your explanation about what you have learned or observed.** 

## Task 3.2: Build your VPC and Launch a Web Server

Follow the lab session: **Module 5 - Networking and Content Delivery** *Lab 2 - Build your VPC and Launch a Web Server*

**Q32 Provide screeenshots of the major milestones and your explanation about what you have learned or observed.** 

## Task 3.3: Introduction to Amazon EC2

Follow the lab session: **Module 6 - Compute** *Lab 3 - Introduction to Amazon EC2*

**Q33 Provide screeenshots of the major milestones and your explanation about what you have learned or observed.** 

## Task 3.4: use AWS Comprehend 

Open the modules and open the "Learner Lab". Click the button "Start Lab", wait until the environment is up and then click "AWS" at the top of the window and open the AWS Console.

<p align="center"><img src="./images/Lab03-LearnerLab.jpeg" alt="Learner lab" title="Learner lab"/></p>

Once the AWS Console is open find the service "Amazon Comprehend"

<p align="center"><img src="./images/Lab03-AWSConsole.jpeg" alt="Learner lab" title="Learner lab"/></p>

Launch the demo
<p align="center"><img src="./images/Lab03-AWSComprehend.jpeg" alt="Learner lab" title="Learner lab"/></p>

Play with the demo using the provided text and parts of the "First contact with tensor flow" book.

<p align="center"><img src="./images/Lab03-AWSComprehendPlay.jpeg" alt="Learner lab" title="Learner lab"/></p>

**Q34 Provide screeenshots of the major milestones and your explanation about what you have learned or observed.** 

## Task 3.5: Create a python script that sends a text to AWS Comprehend and retrieves the analysis

Using the "AWS Academy Learner Lab" AWS console it is only posible to execute python code in the browser terminal of the environment.

### Create a Personal Access Token on GitHub

From your GitHub account, 

1. go to Settings 
2. Developer Settings 
3. Personal Access Token 
4. Generate New Token (Classic)
5. Fillup the form 
6. Click Full control of private repositories
7. Click Generate token
8. Copy the generated Token, it will be something like ``ghp_sFhFsSHhTzMDreGRLjmks4Tzuzgthdvfsrta``

Keep the token on a safe place, such as a password manager, for future use.


### Clone your repository

Use the following command to clone your repository inside the AWS command line environment. For the password use the Personal Access Token created before.

```bash
_$ git clone https://github.com/CCBDA-UPC/2025-3-XX.git Lab3
Cloning into 'Lab3'...
Username for 'https://github.com': YOUR@EMAIL.COM
Password for 'https://YOUR@EMAIL.COM@github.com': ghp_sFhFsSHhTzMDreGRLjmks4Tzuzgthdvfsrta
remote: Enumerating objects: 9, done.
remote: Counting objects: 100% (9/9), done.
remote: Compressing objects: 100% (7/7), done.
remote: Total 9 (delta 1), reused 3 (delta 0), pack-reused 0
Unpacking objects: 100% (9/9), done.
Checking connectivity... done.
```

### Add a script to interact with AWS Comprehend

Use the code in [`Comprehend_1.py`](Comprehend_1.py) which uses the boto3 library to invoke the comprehend service and outputs the result.

```python
comprehend = boto3.client('comprehend')
entity_list = comprehend.detect_entities(Text=TEXT, LanguageCode='en')
print(json.dumps(entity_list, indent=4))
for entity in entity_list['Entities']:
    print(f"{entity['Text']}: {entity['Type']}, {entity['Score']}")
```

Commit the Python file to the session repo, add the text file [`MachineLearning.txt`](MachineLearning.txt) and push them both it. At the AWS console pull the code and execute it.

```bash
_$ git pull
_$ python Comprehend_1.py
{
    "Entities": [
        {
            "Score": 0.9569487571716309,
            "Type": "DATE",
            "Text": "a decade ago",
            "BeginOffset": 435,
            "EndOffset": 447
        },
        ......
        {
            "Score": 0.521251380443573,
            "Type": "QUANTITY",
            "Text": "actors",
            "BeginOffset": 2437,
            "EndOffset": 2443
        }
    ],
    "ResponseMetadata": {
        "RequestId": "0a4374e6-5bf9-43f5-8f12-35bae9b1e1ec",
        "HTTPStatusCode": 200,
        "HTTPHeaders": {
            "x-amzn-requestid": "0a4374e6-5bf9-43f5-8f12-35bae9b1e1ec",
            "content-type": "application/x-amz-json-1.1",
            "content-length": "3120",
            "date": "Sun, 12 Mar 2025 12:10:14 GMT"
        },
        "RetryAttempts": 0
    }
}
a decade ago: DATE, 0.9569487571716309
one of the fields: QUANTITY, 0.69606614112854
2006: DATE, 0.9996651411056519
Silicon Valley: LOCATION, 0.9980552196502686
...
```
**Q351 Provide screeenshots of the major milestones and your explanation about what you have learned or observed.**

### Play with the AWS Comprehend API

Keep the [Boto3 Comprehend API](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/comprehend.html#client) nearby and replace the file `MachineLearning.txt` by `FirstContactWithTensorFlow.txt` bearing in mind the restrictions on document size that the API has.

**Q352 Explain the differences that you have found using the NTLK and the AWS Comprehend service while analyzing the book.**

**Q353 Think of how can you take advantage on AWS Comprehend to analyze the book.** Add a file named ``Comprehend_2.py`` to implement that idea.


# How to submit this assignment:

**Q361 How long have you been working on this session?**

**Q362 What have been the main difficulties you have faced and how have you solved them?** 

Add your answers to README.md.

Use the **private** repo named *https://github.com/CCBDA-UPC/2025-3-xx*. It needs to have the `README.md` file with your responses to the above questions.

Make sure that you have updated your local GitHub repository (using the `git`commands `add`, `commit` and `push`) with all the files generated during this session. 

**Before the deadline**, all team members shall push their responses to their private *https://github.com/CCBDA-UPC/2025-3-xx* repository.