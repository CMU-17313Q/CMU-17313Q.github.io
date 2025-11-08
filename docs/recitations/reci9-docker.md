# Recitation 9: Microservices and Docker

## Prerequisites

You should have downloaded Docker. If you haven't follow the installation instructions [here](https://docs.docker.com/get-docker/)

## Setup Instructions (10 min):

Fork [this repo](https://github.com/CMU-17313Q/f25-docker-recitation) and clone it.

Open the folder in VSCode.  Then you should "reopen in continer" similar to NodeBB, but this container is setup for python.

Also start the docker engine.

## Overview

During this recitation, students will create a simple FastAPI app, containerize it and deploy it.

## Context

The course staff is building an internal API to support dashboards and check-ins for project teams in 17-313.
An existing microservice already exposes team names by team ID.

Try it out:
`GET https://appbox.qatar.cmu.edu/313-teams/team_name/<team_id>`

Example:
```json
{ "team_name": "nodegpt" }
```

Now, the staff needs a more complete endpoint that returns both the team name and the team mentor (from Recitation 3: Team Contracts).
Your task is to build a new service that provides an endpoint `GET /team_info/<team_id>` that calls the existing microservice and enriches the response with the mentor’s name.

The endpoint has to return a JSON object in the following form:

```json
{
  "team_id": 1,
  "team_name": "nodegpt",
  "mentor": "Seckhen"
}
```
You can find the mentor assignment information in the **Recitation 3: Team Contracts** document, where each project team is paired with a course assistant (CA) mentor.


## Activity

1. Open the project in **VS Code** using the provided **devcontainer**.
   Follow the instructions in the `README.md` file to set up your environment.
2. Implement the `team_info` endpoint according to the specifications.
   Edit `app/main.py` to do so.
3. Test it by running the app locally, from a terminal in the devcontainer:
   ```bash
   pip install -r requirements.txt
   uvicorn app.main:app --host 0.0.0.0 --port 8080
   ```
   and by verifying the endpoint visting [http://localhost:8080/team_info/1]([http://localhost:8080/team_info/1).  You should receive a JSON response with the team name, and CA name. Your job is to implement the information for all the teams.
4. Now that the implementation is complete, let's dockerize the service. Complete the `Dockerfile`. You can use the slides and this [link](https://docs.docker.com/engine/reference/builder/) as resources.
5. Create the docker image using the command below, and check that the image has been created.
   ```
   docker build -t YOUR_IMAGE_NAME  .
   ```
6. Try running your image (it should work similarly to when you run the app locally).
   ```
   docker run --rm -p 8080:8080 YOUR_IMAGE_NAME
   ```
7. OPTIONAL: Implement `docker-compose.yml`. You can use the slides for reference.
8. OPTIONAL: Launch a container using the docker image using the command below.
   ```
   docker compose up -d --build
   ```
9. Check that your service is running correctly by visiting [http://localhost:8080/team_info/1](http://localhost:8080/team_info/1). You should receive a JSON response with the team name, and CA name. Your job is to implement the information for all the teams.


## Submission:

Make sure to [Submit on Gradescope](https://www.gradescope.com/courses/1096661/assignments/7128651) after this recitation. Everyone should submit individually.
