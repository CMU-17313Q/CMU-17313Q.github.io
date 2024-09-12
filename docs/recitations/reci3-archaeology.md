---
title: Recitation 3 - Software Archaeology
---

# Recitation 3: Software Archaeology

## Overview

In today’s recitation, we will practice implementing a new feature for the NodeBB codebase.

**Let's implement a new feature!**

Check out [this issue](https://github.com/CMU-17313Q/NodeBB-F24-R3/issues/1) of the feature request. NodeBB should suggest a new username if existing username is taken.

## Task 0: Clone the repo

- Fork [this repository](https://github.com/CMU-17313Q/NodeBB-F24-R3) and clone it. Follow the directions for further installation on the readme.


## Task 1: Reproduce the existing behaviour

- After you've successfully ran the program, go through it to reproduce the current behaviour.

## Task 2: Diving into the code and implement the new behavior

Let’s learn more about this feature! Your high-level goal is to identify the code producing the current feature. We’d like you to dive into the codebase and “excavate” the code.

Try some or all of the following tasks, and think about whether you’re doing them statically or dynamically. It’s okay if you don’t get to all of these tasks.


- Explore the NodeBB directory
- Understand how current features are implemented.
- Can you identify whether to modify the front-end or back-end
  code of the program?
  - Frontend code is located in public directory
  - Backend code is located in `src` directory
- Can you identify the keywords that you would like to search in the repository?
  - Error message that is currently showing.
- Use your IDE to jump to a definition implicated in the code you’re debugging (If you are using VSCode, click on F12 to go to a function definition or variable declaration, then alt+left to go back when you are done).


## Task 3: Making a Pull Request

If you’ve finished all that,

- Add and commit your changes
- Push the code to your forked repository.
- Create a pull request that links the issue.
- Submit your pull request.

## Task 4 (Optional): Suggest a unique username

Can you suggest a unique username by querying the backend server again? For example, if `test123` is taken, you should check if `test1231` is taken, then `test1232`, etc. You should display a username that has not yet been registered by anyone.
