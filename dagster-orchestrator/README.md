# Data Ingestion from API to S3 using Dagster

In this project, we use Dagster to orchestrate ingestion data from an API to an S3 directory. A Dagster pipeline is set
up to run every minute, fetching data from the API and storing it in S3. This allows for near-real-time data ingestion,
ensuring that the most recent data is always available for analysis and processing.

## Project Structure

The project mainly consists of two Python files: `__init__.py` and `ingestion.py`.

#### `__init__.py` file :

This file is used to define the Dagster job and schedule. The job `near_real_time_data_ingestion` is defined here, which is scheduled to run every minute.

#### `ingestion.py` File

This file contains the main logic for data ingestion. It defines an operation `fetch_and_write_data_to_s3_bucket` that fetches data from the API and writes it to an S3 bucket.

# Dagster Deployment with Docker

We deploy also a Dagster instance using Docker and Docker Compose. The instance includes a **Dagster 
webserver**, a **Dagster daemon**, and a **PostgreSQL database**.

## Prerequisites

- Docker
- Docker Compose

## Configuration

Before starting the services, we need to set the following environment variables in the `.env` file:

```ini

POSTGRES_DB=your_postgres_db
POSTGRES_USER=your_postgres_user
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_HOST=your_postgres_host

## AWS credentials
AWS_ACCESS_KEY_ID="your_access_key_id"
AWS_SECRET_ACCESS_KEY="your_secret_key_id"

##  AWS S3 bucket
AWS_S3_BUCKET="your_bucket_name"
INPUT_S3_PATH="your_input_path_file"
```

## Starting the Services

```bash
docker-compose up -build
```
