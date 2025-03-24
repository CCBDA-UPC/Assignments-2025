
### Install github CLI

[Install](https://github.com/cli/cli#installation)

```bash
_$ brew install gh
```

```bash

gh secret set AWS_ACCESS_KEY_ID --repo CCBDA-UPC/django-webapp --body "$ENV_VALUE"
gh secret set AWS_ACCOUNT_ID --repo origin/repo --body "$ENV_VALUE"
gh secret set AWS_SECRET_ACCESS_KEY --repo origin/repo --body "$ENV_VALUE"
gh secret set AWS_SESSION_TOKEN --repo origin/repo --body "$ENV_VALUE"


```


### Github actions

GitHub Actions is a powerful CI/CD platform that enables developers to build, test, and deploy pipelines efficiently.
These pipelines are essential for maintaining consistency in deployments, identifying errors quickly, improving
efficiency, and streamlining the development process.

**Continuous Integration (CI)** and **Continuous Delivery (CD)** are critical practices for delivering high-quality
software. They ensure a great user experience by preventing bugs from being pushed to production. GitHub Actions allows
you to create custom workflows that are triggered based on specific events, such as pull requests, code commits, or
pushes to a repository.

In this laboratory session, you will learn how to create CI/CD pipelines using GitHub Actions. This process continues
with the previous session using the created Docker image, pushing it to AWS Elastic Container Registry (AWS ECR) ,
and deploying the application to AWS Elastic Container Service (AWS ECS).

### CI/CD build using GitHub Actions

A workflow is an automated process that runs one or more defined jobs. A workflow file contains various sections within
which each action in the pipeline is defined. These are:

- **name**: This is the workflow's name as will appear on your repository's ‘Actions’ section.
- **on**: This section specifies the workflow trigger. Here, you can have successful merges to the repository and pushes
  to the main or other branches among other actions.
- **jobs**: Here, all the jobs that are run in the workflow will be defined.

```yaml
name: Deploy to AWS ECS

on:
  push:
    branches: [ "main" ]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
```

To create the workflow, add to your responses repo the file `.github/workflows/aws.yml`

The proposed workflow will build and push a new container image to AWS ECR,
and then will deploy a new task definition to AWS ECS, when there is a push to the "main" branch.

To use this workflow, you will need to complete the following set-up steps:

1. Create an ECR repository to store your images.
   For example: `aws ecr create-repository --repository-name my-ecr-repo`.
   Replace the value of the `ECR_REPOSITORY` environment variable in the workflow below with your repository's name.
   Replace the value of the `AWS_REGION` environment variable in the workflow below with your repository's region.

2. Create an ECS task definition, an ECS cluster, and an ECS service.
   For example, follow the Getting Started guide on the ECS console:
   https://us-east-1.console.aws.amazon.com/ecs/home?region=us-east-1#/firstRun
   Replace the value of the `ECS_SERVICE` environment variable in the workflow below with the name you set for the
   AWS ECS service.
   Replace the value of the `ECS_CLUSTER` environment variable in the workflow below with the name you set for the
   cluster.

3. Store your ECS task definition as a JSON file in your repository.
   The format should follow the output of `aws ecs register-task-definition --generate-cli-skeleton`.
   Replace the value of the `ECS_TASK_DEFINITION` environment variable in the workflow below with the path to the JSON
   file.
   Replace the value of the `CONTAINER_NAME` environment variable in the workflow below with the name of the container
   in the `containerDefinitions` section of the task definition.

4. Store an IAM user access key in GitHub Actions secrets named `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`.
   See the documentation for each action used below for the recommended IAM policies for this IAM user,
   and best practices on handling the access key credentials.

Starter workflow outline

trigger and branches

permissions

jobs and runner

steps

name and uses