# Deployment Instructions: Hosting Your Own Coding Agent

In this guide you will take your team's fork of OpenCode from your laptop to a server, so that anyone on the CMU network can open a browser and start a session with *your* coding agent.

The setup has three layers:

```
Browser  ──►  Nginx (VM, port 8080)  ──►  Docker container (VM port 4096)  ──►  OpenCode web server
```

- **OpenCode** runs inside a Docker container.
- The container publishes port 4096 **only on the VM's loopback interface**, so nobody can reach OpenCode directly.
- **Nginx** is the only public entry point. It listens on port 8080 and forwards requests to OpenCode.

!!! note "Placeholders"
    Replace anything in `<ANGLE_BRACKETS>` with your team's values:

    - `<VM_HOSTNAME>`: your team's VM hostname (e.g., `crs-17313-demo-gpu.qatar.cmu.edu`)
    - `<REPO_URL>`: the URL of your team's OpenCode fork
    - `<REPO_DIR>`: the folder name of your cloned repository (e.g., `OpenCode-f26-R04`)

---

## Step 0: Creating Your Own Docker Image

As part of this project, you will create your own Docker image to run OpenCode on your assigned Virtual Machine (VM). Write a Dockerfile that defines the environment needed to run your team's OpenCode application. Your Dockerfile should specify an appropriate base image, install the required system dependencies, set the working directory, prepare the application dependencies, and define how the OpenCode web server is started. You can refer to the [official instruction set for writing a Dockerfile](https://docs.docker.com/get-started/docker-concepts/building-images/writing-a-dockerfile/) for guidance.

## Step 1: Connect to the VM and Clone Your Repository

1. SSH into your VM.

2. Make sure the GitHub CLI (`gh`) is installed so that you can authenticate with GitHub:

    ```bash
    gh --version
    ```

    If it is not installed, install it:

    ```bash
    sudo apt update
    sudo apt install gh
    ```

3. Authenticate with your GitHub account and follow the prompts:

    ```bash
    gh auth login
    ```

4. Clone your team's repository into your home directory:

    ```bash
    cd ~
    git clone <REPO_URL>
    cd <REPO_DIR>
    ```

## Step 2: Build the Docker Image

From the root of your repository, build the image:

```bash
sudo docker build -t opencode:dev -f <PATH-TO-YOUR-DOCKERFILE> .
```

!!! tip
    The image name `opencode:dev` is arbitrary. Pick any name, but use the same one in the next step.

## Step 3: Create and Start the Container

```bash
sudo docker run -it \
  --name opencode \
  -p 127.0.0.1:4096:4096 \
  -v "$HOME/<REPO_DIR>:/workspaces/<REPO_DIR>" \
  -w /workspaces/<REPO_DIR> \
  opencode:dev bash
```

What these options do:

| Option | Meaning |
|--------|---------|
| `--name opencode` | Gives the container a name you can refer to later |
| `-p 127.0.0.1:4096:4096` | Publishes container port 4096 on the VM's **loopback only**, so it is not reachable from other machines |
| `-v ...` | Mounts your cloned repository into the container, so edits persist on the VM |
| `-w ...` | Sets the working directory inside the container |

You are now **inside the container**. All commands in Steps 4–6 run inside the container unless stated otherwise.

!!! note "Coming back later"
    `docker run` creates the container once. If you exit and want to return, don't run it again (the name will already be taken). Instead:

    ```bash
    sudo docker start opencode
    sudo docker exec -it opencode bash
    ```

## Step 4: Prepare the Project Inside the Container

1. Add the container's root user to Git's trusted directories (the mounted folder is owned by a different user):

    ```bash
    git config --global --add safe.directory /workspaces/<REPO_DIR>
    ```

2. Install dependencies:

    ```bash
    bun install
    ```

3. If the install fails because Python or build tools are missing, install them inside the container and run `bun install` again:

    ```bash
    apt-get install -y python3 make g++
    bun install
    ```

## Step 5: Configure a Password and Start OpenCode

- Start the OpenCode web server:

    ```bash
    bun run packages/opencode/src/index.ts web --hostname 0.0.0.0 --port 4096
    ```

!!! note "Why `0.0.0.0`?"
    Inside the container, `--hostname 0.0.0.0` makes OpenCode listen on all of the container's network interfaces. This is required so that Docker can forward traffic from the published port into the container. It does **not** expose the server to the network: the `-p 127.0.0.1:4096:4096` option from Step 3 is what restricts access to the VM itself.

!!! tip "Keep it running after you disconnect"
    To keep OpenCode running after you disconnect from SSH, start it in the background inside the running Docker container:

    ```bash
    nohup bun run packages/opencode/src/index.ts web \
      --hostname 0.0.0.0 \
      --port 4096 \
      > /tmp/opencode.log 2>&1 < /dev/null &

    echo $! > /tmp/opencode.pid
    ```
    - **What this command does:**

        - `nohup` helps OpenCode continue running after you disconnect from SSH
        -  `> /tmp/opencode.log` saves normal output to a log file 
        - `2>&1` sends error messages to the same file
        - `< /dev/null` disconnects the process from terminal input
        - `&` runs it in the background 
        - `echo $! > /tmp/opencode.pid` saves the background process ID so you can stop it later.

    - **Check the logs:** `cat /tmp/opencode.log`
    - **Stop the server:** `kill "$(cat /tmp/opencode.pid)"`

    The server will continue running after you disconnect from SSH, provided the Docker container remains running. It will not automatically restart if the container stops or the VM reboots.

If the server is running in the foreground, open a **second SSH session** to the VM for the next steps. These run on the **VM**, not inside the container.

- To verify that the serve is running, send an HTTP request to it using `curl` by first opening a new SSH session and typing the command below into the terminal. If you see a `200` status (e.g, `HTTP/1.1 200 OK`), then the server is running.
    ```bash
    curl -I --max-time 5 http://127.0.0.1:8080/
    ```

## Step 6: Put Nginx in Front of OpenCode

We use Nginx as a reverse proxy to make your agent accessible remotely. Your site will be available at:

```
http://<VM_HOSTNAME>:8080
```

from anywhere within the CMU network.

1. Check what Nginx is already serving, so you don't conflict with an existing configuration:

    ```bash
    sudo nginx -T 2>/dev/null | grep -nE 'server_name|listen|proxy_pass|location'
    ```

2. Check that port 8080 is free (no output means it is available):

    ```bash
    sudo ss -ltnp | grep ':8080'
    ```

3. Create a new Nginx configuration file:

    ```bash
    sudo vim /etc/nginx/sites-available/opencode
    ```

4. Enter the following configuration:

    ```nginx
    server {
        listen 8080;
        server_name <VM_HOSTNAME>;

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

    What the important parts mean:

    - `listen 8080;` — Nginx receives requests on port 8080.
    - `server_name ...;` — matches your VM's hostname.
    - `proxy_pass http://127.0.0.1:4096;` — forwards requests to OpenCode.
    - The `Upgrade` and `Connection` headers support WebSocket connections, and the remaining `proxy_set_header` lines preserve information about the original request.
    - `proxy_buffering off;` and `proxy_read_timeout` keep the agent's streamed output from being delayed or cut off.

5. Enable the configuration by creating a symbolic link from `sites-enabled` to the new file. This tells Nginx to load it:

    ```bash
    sudo ln -s /etc/nginx/sites-available/opencode /etc/nginx/sites-enabled/opencode
    ```

6. **Test the configuration for syntax errors** before applying it:

    ```bash
    sudo nginx -t
    ```

    You should see `syntax is ok` and `test is successful`. If not, fix the reported line before continuing.

7. Reload Nginx to activate the configuration:

    ```bash
    sudo systemctl reload nginx
    ```

## Step 7: Verify the Deployment

1. From the VM, confirm that Nginx forwards requests to OpenCode:

    ```bash
    curl -I --max-time 5 http://127.0.0.1:8080/
    ```

3. From a **different machine** on the CMU network, open the web interface in a browser:

    ```
    http://<VM_HOSTNAME>:8080/
    ```

## Troubleshooting

| Symptom | Things to check |
|---------|-----------------|
| `502 Bad Gateway` | OpenCode isn't running. Re-check Step 5, and confirm the container is up with `sudo docker ps`. |
| `nginx -t` fails | Read the line number in the error. A missing `;` is the most common cause. |
| Port 8080 already in use | Another service is listening. Re-run the `ss` check in Step 6, or ask a CA for a free port. |
| Works on the VM but not from your laptop | Confirm you are on the CMU network and using the correct hostname and port. |
| Page loads but the agent never responds | Check that the `Upgrade`/`Connection` headers and `proxy_buffering off;` are in your Nginx config. |
| `bun install` fails | Install the build tools from Step 4 and retry. |

## Security Checklist

Before you share your URL with anyone:

- [ ] A password is set, and an unauthenticated request returns `401`
- [ ] Port 4096 is published only on `127.0.0.1` (check the `-p` option from Step 3)
- [ ] Model-provider API keys are stored as environment variables, **not** committed to your repository
- [ ] API keys have a spending limit, and you know how to rotate them
- [ ] Your Nginx configuration and Docker files are committed to your repository, **without any secrets in them**

!!! warning "HTTP is not encrypted"
    This setup serves traffic over plain HTTP, so your password and session contents travel unencrypted. That is acceptable for coursework inside the CMU network, but you should never use this setup as-is for anything sensitive. A real deployment would add HTTPS.
