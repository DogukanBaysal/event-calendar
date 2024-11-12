# Event Calendar Application

This is a Dockerized Event Calendar application built with Django. It allows users to manage events with features like adding, viewing, and searching for events, along with displaying event statuses (running, completed, and upcoming).

## Prerequisites

Before running the app, ensure you have the following tools installed:

- **Docker**: [Installation instructions](https://docs.docker.com/get-docker/)
- **Docker Compose**: [Installation instructions](https://docs.docker.com/compose/install/)

## Getting Started

Follow the steps below to get the application up and running using Docker.

### 1. Clone the repository

Start by cloning the repository to your local machine:

```bash
git clone https://github.com/DogukanBaysal/event-calendar.git
```
```
cd event-calendar
```

### 2. Build and start the Docker containers

Run the following command to build the Docker images and start the containers:

```bash
docker-compose up --build
```

This command will:
- Build the Docker images defined in the **Dockerfile**.
- Start the application container and related services as specified in the **docker-compose.yml** file.

### 3. Access the application

Once the containers are up and running, you can access the application in your web browser at:
```
https://localhost:8000
```

### 4. Stopping the application

To stop the application and the Docker containers, run:
```
docker-compose down
```
This command stops and removes the containers but retains the images.
