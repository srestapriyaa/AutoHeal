\# AutoHeal



AutoHeal is a Python-based application health monitoring and automatic recovery project running inside Docker.



\## Features



\- HTTP health-check endpoint at `/health`

\- Python monitoring process that checks application health

\- Automatic application restart when the managed application process exits

\- Docker health checks to report container health

\- Timestamped monitoring and recovery logs



\## Tech Stack



\- Python

\- Docker

\- Git and GitHub



\## Run Locally



Build the Docker image:



```bash

docker build -t autoheal .

```



Run the container:



```bash

docker run -d --name autoheal-app -p 8000:8000 autoheal

```



Check application health at:



`http://localhost:8000/health`



Check container status:



```bash

docker ps

```



View monitoring logs:



```bash

docker logs autoheal-app

```



\## Recovery Behavior



The monitor detects when its managed application process exits and attempts to start the application again. Docker independently checks the `/health` endpoint and reports the container's health status.



\*\*Note:\*\* Docker health checks report health; they do not automatically restart a container simply because it becomes unhealthy.



\## Future Improvements



\- Improve recovery for health-endpoint failures when the process is still running

\- Add automated testing and a Jenkins CI/CD pipeline

\- Build a web dashboard for health status and recovery events
Webhook automation testttttt

