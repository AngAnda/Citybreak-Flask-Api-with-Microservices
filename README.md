# Project Overview

This repository features a Flask REST API for CRUD operations on weather and event data by date and city. Organized into microservices with a reusable template, it employs Docker for containerization, Elastic Stack for logging and monitoring, and Consul for service discovery and configuration. Each microservice is containerized for isolated, scalable deployment.

## Technologies Used
- **Flask**: Web framework for Python used to develop the REST API.
- **Docker**: Platform for containerization, ensuring portability across different environments.
- **Elastic Stack**: Suite for logging and monitoring, including Elasticsearch, Logstash, and Kibana.
- **Consul**: Tool for service discovery and configuration management.
- **MySQL**: Database used for storing event data.
- **Redis**: Database used for storing weather data.

## Getting Started

### Prerequisites
- Docker and Docker Compose installed on your machine.

### Installation
1. **Clone the repository**:
    ```sh
    git clone https://github.com/username/repo-name.git
    cd repo-name
    ```

2. **Build and run the Docker containers**:
    ```sh
    docker-compose up --build
    ```

## API Usage

### Endpoints

#### Access Citybreak Information
To get information about a citybreak for a specific city and date:
```sh
GET /citybreak?city=<CITY>&date=<DATE>
```

#### Post Weather Data
To post weather data for a specific city and date:
```sh
curl -X POST http://localhost:8081/weather -d "city=<CITY>&temperature=<TEMP>&humidity=<HUMIDITY>&wind=<WIND>&date=<DATE>"
```

#### Post Event Data
To post event data for a specific city and date:
```sh
curl -X POST http://localhost:5000/service_events -d "city=<CITY>&name=<EVENT_NAME>&date=<DATE>&description=<DESCRIPTION>"
```

### Monitoring and Logging
#### Accessing Kibana
To monitor logs and view data visualizations, access Kibana at:
```sh
http://localhost:5601
```

### Service Discovery and Configuration
#### Consul Usage
Consul is used for service discovery and configuration. Ensure that Consul is properly configured and running. Access the Consul UI at:
```sh
http://localhost:8500
```
