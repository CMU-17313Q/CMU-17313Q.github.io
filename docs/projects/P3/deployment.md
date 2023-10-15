# Serverless NodeBB Deployment on GCP

This document will provide instructions to create a serverless deployment of NodeBB on GCP.

## Setup Redis Database on upstash

We'll be using a database-as-a-service called upstash to host the Redis database associated with our NodeBB deployment.

1. Visit [upstash](upstash.com) and create an account.
2. Make sure Redis and selected, and click "Create Database"
3. Name your database, select an appropriate region and hit "Create"

You should see a page that contains the endpoint, port, password, and other details associated with the redis instance you just created.

## Update your Dockerfile

To have all the packages we need to build NodeBB, we need to change our Dockerfile. Make the following change and push your changes to your repository.

```
- RUN npm install --only=prod && \
+ RUN npm install && \
```

## Redeem your GCP Credits

First, you need to redeem your GCP credits using the following instructions.

1. Fill out the [this form](https://gcp.secure.force.com/GCPEDU?cid=XufGAKC79oWNCFv7SSDIXbCrKy3MTPzQgZwC9%2FJ1AuF%2Fv89lUW0CmubO%2FsGm2Izw/) link with your first/last name, and Andrew ID
2. Go to your school email and click the link in an email from "Google Cloud Notifications" to verify your email address
3. Go back to your email, click on the link ("click here to redeem") within a second email from "Google Cloud Notifications," and copy the provided code into the field within the new link

Once you submit, a $50 credit should be applied to your GCP billing account.

!!! Warning "Do not misuse!"
	We've been awarded enough credits such that each student in 17-313 can redeem one coupon. We'll be closely monitoring coupon redemption. Any and all misuse including sharing redemption instructions, redeeming multiple times, etc. will be punished.


## Deploy on GCP Cloud Run

Make sure you're logged into the Google account you used to redeem your GCP credits.

Once you're logged into the right credit-bearing Google account, use the following instructions to deploy on GCP Cloud Run.

1. Create a project called "NodeBB" using the [GCP Cloud Console](https://console.cloud.google.com/projectcreate?previousPage=%2Fwelcome%3Fproject%3Dextreme-startup&organizationId=703967796528) (you can set the location to "Students")
2. Visit the [Cloud Run console](https://console.cloud.google.com/run) and select the project you just created using the project selector drop down(top-left)
3. Click on "Create Service"
4. Select "Continuously deploy new revisions from a source repository" and click "Set up with Cloud Build"
5. Set the Source repository to be your team's NodeBB repository - you may need to click on "Manage connected repositories" and authenticate with GitHub if you don't see the repository.
6. Set the Build Type to the "Dockerfile" option
7. In the "Autoscaling" section, set the minimum number of instances to 1
8. In the "Authentication" section select "Allow unauthenticated invocations"
9. Click on the "Container, Networking, and Security" dropdown and set the "Container Port" to 4567
10.Click "Create"
11. Once the deployment is complete, click on the URL of the form `*.run.app` at the top of the page to view the deployment.

You should see a form that says "NodeBB Web Installer". Keep this URL handy because you'll need it later :)

## Create Config Script

At this point, we could use the web installer to generate the `config.json` file in our container and setup NodeBB. However, since this a serverless deployment, we're not guaranteed any persistence of data generated at runtime.

Therefore, we need to change our Dockerfile to generate the `config.json` file at build time of the container.

To do so, first create a template file called `config_template.json` that looks exactly like the following, and push your changes to your repository.

```
{
  "url": "",
  "secret": "c5502d62-84a5-41f1-87eb-ee33a76fb7bc",
  "database": "redis",
  "redis": {
    "host": "",
    "port": "",
    "password": "",
    "database": "0"
  },
  "port": "4567"
}
```

!!! info "Why can't we just push a pre-populated `config.json` file?"
    This would solve the persistence problem and deploy NodeBB correctly. However, as a result, we expose secrets like the upstash redis connection details on a public GitHub repository. Injecting these secrets as environment variables at runtime gives our deployment access to them, while ensuring that the secrets remain secret.

Configure the following environment variables by visiting the Cloud Run dashboard for your deployment, clicking on "Edit and deploy new revision" and then clicking on "Add Variable" in the "Environment Variables" section.

* `DEPLOYMENT_URL`: URL of the form `*.run.app` that your Cloud Run deployment is live at.
* `REDIS_HOST`: Endpoint value from your upstash redis database dashboard.
* `REDIS_PORT`: Port value from your upstash redis database dashboard.
* `REDIS_PASSWORD`: Password value from your upstash redis database dashboard.

Click on "Deploy" at the bottom of the page to save your changes.

We'll now add a bash script that will populate this template with environment variables defined at build time of our Docker container. Create a file called `create_config.sh` in your NodeBB repo, and populate the file with the following bash script.

```
#!/bin/bash

# Check that environment variables have been defined
if [[ -z "${REDIS_HOST+x}" ]]; then
  # var is not defined
  echo "Error: REDIS_HOST is not defined!"
  exit 1
