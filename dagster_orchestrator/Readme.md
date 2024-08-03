# Data Ingestion from API to S3 using Dagster
In this project, we use Dagster to orchestrate ingestion data from an API to an S3 directory. A Dagster pipeline is set 
up to run every minute, fetching data from the API and storing it in S3. This allows for near-real-time data ingestion,
ensuring that the most recent data is always available for analysis and processing.

# Dagster Deployment with Docker

This project deploys a Dagster instance using Docker and Docker Compose. The instance includes a **Dagster webserver**,
a **Dagster daemon**, and a **PostgreSQL database**.

## Prerequisites

- Docker
- Docker Compose

## Configuration

Before starting the services, you need to set the following environment variables in the `.env` file:

```ini
DAGSTER_POSTGRES_DB=your_postgres_db
DAGSTER_POSTGRES_USER=your_postgres_user
DAGSTER_POSTGRES_PASSWORD=your_postgres_password
DAGSTER_POSTGRES_HOST=dagster_postgresql
```

## Starting the Services
```bash
docker-compose up --build
```