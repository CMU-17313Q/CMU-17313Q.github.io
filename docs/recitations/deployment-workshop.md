# Cloud Deployment Workshop



## Overview

Throughout this workshop, students will:



* Understand the fundamental steps involved in deployment

* Learn about CI/CD and the basics of how to set it up in a Github repo

* Get hands on experience deploying with cloud providers - Render.

* Set up and get familiarized with the _Extreme Startup_ web app for use in Thursday's (October 5th) recitation.



## Definitions



Before we begin, we have to understand our goals with CI/CD. It is a software development approach that utilizes frequent, automated testing and deployment to ensure that changes to the codebase can be rapidly and safely incorporated into the production environment.



**Continuous Integration (CI)** refers to the practice of automatically building and testing the codebase whenever new changes are introduced. This involves integrating code changes from multiple developers into a shared repository and running automated tests to ensure that the changes do not break the existing functionality.



**Continuous Deployment/Delivery (CD)** refers to the practice of automatically deploying code changes to the production environment after they have been tested and approved. Continuous Deployment involves automatically deploying changes to the production environment as soon as they pass automated tests, while Continuous Delivery involves deploying changes to a staging environment for further testing and approval before being deployed to production.



Together, CI/CD enables software teams to rapidly and safely develop, test, and deploy changes to the codebase, improving the speed and quality of software delivery while reducing the risk of errors and downtime.



There's quite a lot to learn about CI/CD. If you're interested in learning more, [click here!](https://about.gitlab.com/topics/ci-cd/)



## Task 0: Setting up your repository



For this workshop, we'll be working with a basic web app built on Next.js that responds to HTTP requests. Your job on Thursday during the _Extreme Startup_ game will be to parse these requests and figure out what the correct response is. Today we'll focus on setting up the app so that everything is in place for the game.



The steps to do this are as follows:


1. Fork this repo: [https://github.com/CMU-17313Q/basic-web-app](https://github.com/CMU-17313Q/basic-web-app).

2. Follow the instructions in the readme to run and test the development server locally.

3. Once you have it running locally visit [http://localhost:3000](http://localhost:3000) and try different queries like "Who was Shakespeare?" and "What is your Andrew ID?"

4. Also visit [http://localhost:3000/api?q=shakespeare](http://localhost:3000/api?q=shakespeare) - this is the API endpoint that our game server will use at next week's lecture.


## Task 1: Continuous Deployment

To start off, you'll be deploying the app you just forked on one cloud platform - Render. The goal here is to make your app accessible over the internet. You'll also be setting up continuous deployment such that this deployment is updated with the latest version of the app, whenever you push code to the main branch of your repository.

1. Create an account on [Render](https://render.com)
2. Create a new Web Service
3. Choose "Build and deploy from a Git repository"
4. Click on Configure account under GitHub, to give Render access to your GitHub repositories - this is necessary to setup continuous deployment.
5. Connect your basic-web-app fork to the Web Service you just created
6. Name your web server `<andrewID>-313`
7. Set the Runtime to "Node", Build Command to `npm install; npm run build` and Start Command to `npm start`
8. Select "Singapore (Southeast Asia)" as the region
9. Make sure that the "Free" Instance Type is selected, and click "Create Web Service"
10. When the build completes, click on the link of the form `*.onrender.com` at the top of the page to view the deployment.


## Task 2: Implement "What is your Andrew ID?"

To test that the continuous deployments are working as expected, and familiarize yourself with the basic web app codebase, let's implement support for the query "What is your Andrew ID?"

1. Extend the `QueryProcessor` function to support this question in `utils/QueryProcessor.tsx` - this is where all the Query Processing logic exists
2. Verify that the implementation is correct by running the app locally and testing manually.
2. Write a test for the query you just implemented in `__tests__/utils/QueryProcess.test.ts`
3. Verify that the tests function correctly by running `npm run test`.
5. Commit and push your changes
6. Once pushed, verify that CD is functioning correctly by checking that a new deployment is triggered on Render dashboard.
7. Once the deployments are complete manually verify that both support the query you just implemented.

## Bonus Task: Continuous Integration


While the steps above are all that is required for the _Extreme Startup_ game, we'll spend the rest of the recitation setting up CI for our repo as well. For our purposes, we'll set up an action that runs ESLint and our Jest tests whenever we push to the repo.



The process will be similar to above.


1. Create a new `.github/workflows/test.yml`

2. Copy the following into the files and fill in the blanks appropriately!

```

name: __BLANK 1__

on:

push:

branches:

- main

jobs:

__BLANK 2__:

    runs-on: ubuntu-latest

    name: __BLANK 3__

    steps:

    - uses: actions/checkout@v3

    - uses: bahmutov/npm-install@v1

    - run: npm run __BLANK 4__ (Run ESLint)

    - run: __BLANK 5__ (Run Jest)

```



Hint: Look at the readme of the basic-web-app repo!

!!! note "Conditional CD"
    In an ideal world, you would condition the deployment action on this action, such that your app is only deployed if the linter and tests pass. Sadly, our world is not ideal :(, but if you want to learn more, click [here](https://docs.github.com/en/actions/using-jobs/using-conditions-to-control-job-execution) and [here](https://docs.github.com/en/actions/learn-github-actions/expressions)!

With this complete, you'll be able to quickly iterate and any changes you make and push to your fork will be automatically deployed on Render. Cool!


Remember to do Cloud Deployment Workshop Quiz on [Gradescope](https://www.gradescope.com/courses/554799/assignments/3447721)!