# Cloud Deployment Activity



## Overview

Throughout this workshop, students will:



* Understand the fundamental steps involved in deployment

* Learn about CD and the basics of how to set it up in a Github repo

* Get hands on experience deploying with Vercel

* Set up the web app for use in the _Extreme Startup_ game


## Definitions



Before we begin, we have to understand our goals with CI/CD. It is a software development approach that utilizes frequent, automated testing and deployment to ensure that changes to the codebase can be rapidly and safely incorporated into the production environment.



**Continuous Integration (CI)** refers to the practice of automatically building and testing the codebase whenever new changes are introduced. This involves integrating code changes from multiple developers into a shared repository and running automated tests to ensure that the changes do not break the existing functionality.



**Continuous Deployment/Delivery (CD)** refers to the practice of automatically deploying code changes to the production environment after they have been tested and approved. Continuous Deployment involves automatically deploying changes to the production environment as soon as they pass automated tests, while Continuous Delivery involves deploying changes to a staging environment for further testing and approval before being deployed to production.



Together, CI/CD enables software teams to rapidly and safely develop, test, and deploy changes to the codebase, improving the speed and quality of software delivery while reducing the risk of errors and downtime.



There's quite a lot to learn about CI/CD. If you're interested in learning more, [click here!](https://about.gitlab.com/topics/ci-cd/)



## Task 0: Setting up your repository



For this workshop, we'll be working with a basic web app built on Next.js that responds to HTTP requests. Your job during the _Extreme Startup_ game will be to parse these requests and figure out what the correct response is. Today we'll focus on setting up the app so that everything is in place for the game.



The steps to do this are as follows:


1. Fork this repo: [https://github.com/CMU-17313Q/basic-web-app-f25](https://github.com/CMU-17313Q/basic-web-app-f25).

2. Follow the instructions in the readme to run and test the development server locally.

3. Once you have it running locally visit [http://localhost:3000](http://localhost:3000) and try different queries like "Who was Shakespeare?" and "What is your Andrew ID?"

4. Also visit [http://localhost:3000/api?q=shakespeare](http://localhost:3000/api?q=shakespeare) - this is the API endpoint that our game server will use at next week's lecture.


## Task 1: Continuous Deployment

To start off, you'll be deploying the app you just forked on one cloud platform - Vercel. The goal here is to make your app accessible over the internet. You'll also be setting up continuous deployment such that this deployment is updated with the latest version of the app, whenever you push code to the main branch of your repository.

1. Create an account on [Vercel](https://vercel.com)
2. Create a new Project
3. Import your Git Repository. You probably need to Adjust GitHub App Permissions and  give Vercel access to your GitHub repository - this is necessary to setup continuous deployment.
5. Connect your basic-web-app-f25 fork to the project you just created
6. Name your project `<andrewID>-313`
7. Set the Framework Preset to "NextJS"
8. Leave the other settings with their default values
10. Deploy. When the build completes, click on the page preview, which should take you to your deployed app at `*.vercel.com`


## Task 2: Implement "What is your Andrew ID?"

To test that the continuous deployments are working as expected, and familiarize yourself with the basic web app codebase, let's implement support for the query "What is your Andrew ID?"

1. (Optional) Use VSCode to open the project. We have included a devcontainer to simplify development.
2. Modify the `QueryProcessor` function to support this question in `utils/QueryProcessor.tsx` - this is where all the Query Processing logic exists
3. Verify that the implementation is correct by running the app locally and testing manually.
4. Write a test for the query you just implemented in `__tests__/utils/QueryProcess.test.ts`
5. Verify that the tests function correctly by running `npm run test`.
6. Commit and push your changes
7. Once pushed, verify that CD is functioning correctly by checking that a new deployment is triggered on Vercel dashboard.
8. Once the deployments are complete manually verify that both support the query you just implemented.
9. Submit a link to your deployed app to

Once this is complete, you will be ready for the game next week. Good job and good luck!
