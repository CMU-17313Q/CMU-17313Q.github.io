# Recitation 6: Deployment



## Overview

Throughout this recitation, students will:



* Understand the fundamental steps involved in deployment
                                                                * Get hands on experience deploying OpenCode

## Definitions

                                                                In this recitation, you will deploy an OpenCode instance on this repo on a server, so that anyone on the CMU network can open a browser and start a session using it. First, fork 
[this repo](https://github.com/CMU-17313Q/OpenCode-F26-Reci-7) under your GitHub account.

```text
Browser ──► Nginx ──► Docker container ──► OpenCode web server
```

- OpenCode runs inside a [Docker](https://cmu-17313q.github.io/projects/P1/development-tools-guide/#docker) container
- [Nginx](https://nginx.org/) is the only public entry point. It listens on a specific port and forwards web requests to OpenCode.


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
      - '127.0.0.1:4096:4096'
    restart: unless-stopped
```

- This creates a service called `opencode`.
- `build: .` tells Docker Compose to build a Docker image using the `Dockerfile` in the current directory
- `127.0.0.1:4096:4096` under `ports` instructs Docker to forward network traffic from port 4096 on the VM's local interface (127.0.0.1) to port 4096 inside the container.
- `restart: unless-stopped`: instructs Docker to automatically restart the container if it stops unexpectedly or when Docker restarts, unless the container has been explicitly stopped by the user.

## Step 2: Start The OpenCode Service

From the root of your repository, use Docker Compose to start the services listed in `docker-compose.yml` (in our case, `opencode`):

```bash
docker compose up --build -d
```

- The `-build` flag tells Docker Compose to build / rebuild the Docker image before strating the container
- The `-d` flaq Runs the containers in the background (detached mode). This allows the service to be independent of the current ssh session

## Step 3: Set Up Nginx

So far, we have OpenCode running inside a Docker container. OpenCode listens for HTTP requests on port 4096 inside the container. Docker forwards requests from the VM's local address, 127.0.0.1:4096, to port 4096 inside the container.

However, OpenCode is not yet accessible to users on other computers. This is intentional: our Docker configuration binds port 4096 to 127.0.0.1, making it accessible only from the VM itself.

To allow users on other computers within CMU Qatar to access OpenCode, we will configure Nginx as a reverse proxy. Nginx will listen for incoming HTTP requests and forward them to OpenCode through the container in which OpenCode’s web server is running.

With this configuration, users can access OpenCode through the VM's public hostname and port, while OpenCode itself remains bound to the VM's local interface.

The request flow will be:

- **A user opens `http://<VM-HOSTNAME>:<PORT>` in their browser:** If the default HTTP port (80) is used, `<PORT>` can be omitted, and the user can access `http://<VM-HOSTNAME>`. Similarly, if HTTPS is configured on the default port (443), the user can access `https://<VM-HOSTNAME>` without specifying the port.

- **The request reaches Nginx:** The browser sends an HTTP request to the virtual machine (VM), where Nginx is listening for incoming connections on the specified port.

- **Nginx forwards the request to OpenCode:**  Nginx forwards the incoming request to the host machine's local port, which is mapped to the port exposed by the Docker container running OpenCode.

- **Nginx forwards the request to OpenCode:**  Nginx forwards the incoming request to the host machine's local port, which is mapped to the port exposed by the Docker container running OpenCode.

- **OpenCode processes the request and returns a response:** OpenCode processes the HTTP request and sends an HTTP response back to the browser through Nginx, which forwards the response to the user.


We will create a Nginx configuration that listens on port 80, forward browser requests to http://127.0.0.1:4096 , and pass through the headers needed for normal HTTP and WebSocket connections.

Open a configuration file:

```bash
sudo vim /etc/nginx/sites-available/opencode
```

Enter the following configuration for handling HTTP requests.

```xml
server {
    listen 80;
    listen [::]:80;
    server_name <VM-HOSTNAME>;

    location / {
        proxy_pass http://127.0.0.1:4096;

        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Here's what the important parts mean:

- `listen 80;` — Nginx receives requests on port 80.

- `listen [::]:80`; allows Nginx to listen for HTTP connections over IPv6 alongside IPv4

- `server_name ...;` — matches your VM's hostname.

`proxy_pass http://127.0.0.1:4096;` — forwards requests to OpenCode.

The remaining directives preserve request information and support WebSocket connections.

Create a symbolic link from sites-enabled to the new file in sites-available. This tells Nginx to load the OpenCode configuration when it reloads.

```bash
sudo ln -s /etc/nginx/sites-available/opencode /etc/nginx/sites-enabled/opencode
```

Reload Nginx to activate the OpenCode configuration:

```bash
sudo systemctl reload nginx
```

From a remote machine, open the web interface on the following URL:

```bash
http://<VM-HOSTNAME>:<PORT>/
```

## Step 5: Restarting Service at Reboot

Your container is currently running. To make sure it automatically comes back after a VM reboot, we need two things:

- Docker must start automatically when the VM boots.

```bash
sudo systemctl enable docker
```

`systemctl` is the command-line tool used to manage services through systemd, Ubuntu's service manager.

- The OpenCode container must have a restart policy telling Docker to restart it.

This is already achieved by the `restart: unless-stopped` line in the `docker-compose.yml` file

**You now have a working OpenCode web application that you can securely access through your browser, and it will automatically come back online if the server restarts.!**

