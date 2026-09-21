---
title: Recitation 4 - Software Archaeology
---

# Recitation 4: Software Archaeology

## Overview

In today's recitation, we will practice implementing a new feature in the OpenCode codebase.

You will begin by exploring OpenCode as a user. You will then use what you observed to investigate the codebase and trace the implementation of a specific behavior. Finally, you will modify the code and submit your changes as a pull request.

## Task 0: Clone the repo

- Fork [this repository](https://github.com/CMU-17313Q/OpenCode-f26-R04) and clone it.
- The repository has a pre-existing `.devcontainer` directory that includes a `Dockerfile` and a `devcontainer.json`.
- Start Docker Desktop on your computer. Then run `docker version` and make sure both Client and Server information are displayed.
- Press `CTRL + Shift + P`, then select `Dev Containers: Reopen in Container`. This should install all dependencies needed to run OpenCode.


## Task 1: Reproduce the existing behaviour

Before we change anything, let's first understand how OpenCode currently behaves.

Start OpenCode and spend a few minutes exploring the application. Your goal is select a simple behavior you want to modify.

- To start OpenCode, run:
    ```bash
    bun dev
    ```

Verify that the application starts successfully and that you can interact with it.

**Important:** You may be able to launch OpenCode successfully but receive a provider error when attempting to send a prompt. For this recitation, you do not need to configure an AI provider.

## Task 2: Diving into the code and implement the new behavior

Now that you have explored OpenCode as a user, let's investigate how its existing behavior is implemented. Your goal is to identify the code responsible for the behavior you selected. Think of this as software archaeology: start with something you can observe, then work backwards through the codebase to discover how it is implemented.

**Explore the OpenCode codebase**

- Look through the directory structure.
- Identify the parts of the codebase that seem relevant to the behavior you explored in Task 1.

**Search for relevant code**

- What keywords could you search for?
- Can you find a string, command, variable, function, or component related to the behavior you observed?
- Use repository search to find where it appears.

**Trace the behavior**

- Once you find a relevant piece of code, follow the functions, components, or modules it interacts with.
- Try to understand the path from the user's action to the resulting behavior.

**Navigate the codebase**

- Use your IDE to jump to definitions and declarations.
- In VS Code, you can press F12 to go to a definition and Alt+Left to return to where you were.
- Use these tools to follow the code rather than manually searching through every file.


**Make a small change**

- Remember to create a new branch
- The change you implement should be easy to show
- Choose something simple! (you'll do complicated things later)

## Task 3: Making a Pull Request

If you’ve finished all that,

- Add and commit your changes
- Push the code to the repository.
- Submit your pull request with a brief description of your change.

Remember to do [Recitation 4 quiz](https://www.gradescope.com/courses/1360202/assignments/8685282) on Gradescope! Please only open it after you have completed all the steps above.
