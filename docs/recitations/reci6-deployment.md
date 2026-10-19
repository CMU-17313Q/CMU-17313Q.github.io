# Recitation 6: Deployment



## Overview

Throughout this recitation, students will:

* Understand the fundamental steps involved in deployment
* Get hands on experience deploying OpenCode

## Definitions

In this recitation, you will deploy an OpenCode instance on this repo on a
server, so that anyone on the CMU network can open a browser and start a session
using it. First, fork [this
repo](https://github.com/CMU-17313Q/OpenCode-F26-Reci-7) under your GitHub
account.

```text
Browser ──► Docker container ──► OpenCode web server
```

- OpenCode runs inside a [Docker](https://cmu-17313q.github.io/projects/P1/development-tools-guide/#docker) container


Replace anything in `<ANGLE_BRACKETS>` with your team’s values:

- `<ANDREW-ID>`: Your andrew ID
- `<REPO_URL>`: HTTP link to the repository
- `<REPO_DIR>`: Repo directory account
- `<VM-HOSTNAME>`: Hostname of the machine you will use in this recitation

In this recitation, you will be provided with the hostname of the VM where your application will be deployed. Each student can connect to this VM via ssh:

```bash
ssh <ANDREW-ID>@<VM-HOSTNAME>
```

Authenticate with your GitHub account and follow the prompts:

```bash
gh auth login
```

Clone your the repository into your home directory:

```bash
cd ~
git clone <REPO_URL>
cd <REPO_DIR>
```

## Step 1: Creating Your Own Dockerfile

You will create your own Docker image to run OpenCode. Write a Dockerfile that defines the environment needed to run your team's OpenCode application. Your Dockerfile should specify an appropriate base image, install the required system dependencies, set the working directory, prepare the application dependencies, and define how the OpenCode web server is started. You can refer to the official instruction set for writing a Dockerfile. Make sure your Dockerfile installs the necessary dependencies and starts the OpenCode webserver.

In production, we want the applications we serve to work without us having to maintain a constant connection with the machine that is serving them. Additionally, we need the applications to restart automatically if the machine reboots. To achieve these two objectives, we need to configure Docker Compose to run the application in the background and automatically restart the container when the machine starts up again.
Create a docker-compose.yml file in your project directory on the VM, alongside your Dockerfile and add the configuration below.


```xml
services:
  opencode-<ANDREW-ID>:
    build: .
    ports:
      - '<YOUR PORT>:4096'
    restart: unless-stopped
```

- This creates a service called `opencode`.
- `build: .` tells Docker Compose to build a Docker image using the `Dockerfile` in the current directory
- `<YOUR PORT>4096:4096` under `ports` instructs Docker to forward network traffic from port <YOUR_PORT> to port 4096 inside the container.
- `restart: unless-stopped`: instructs Docker to automatically restart the container if it stops unexpectedly or when Docker restarts, unless the container has been explicitly stopped by the user.

## Step 2: Start The OpenCode Service

From the root of your repository, use Docker Compose to start the services listed in `docker-compose.yml` (in our case, `opencode`):

```bash
docker compose up -d
```
- The `-d` flaq Runs the containers in the background (detached mode). This allows the service to be independent of the current ssh session


**You now have a working OpenCode web application that you can access through your browser at `http://crs-17313-demo.qatar.cmu.edu:<YOUR_PORT>`, and it will automatically come back online if the server restarts.!**
