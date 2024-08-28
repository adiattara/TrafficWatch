# Structured Streaming Application

## Project Description

This application is a real-time traffic monitoring system that processes data fetched from a S3 bucket, transforms the 
data, and stores it in a PostgreSQL data warehouse . The system is built using Scala and Spark Structured Streaming.

### Prerequisites

- **Docker and Docker Compose** need to be installed on your machine.
- **Sbt** should be installed on your machine to compile and run the project.

## Technologies Used
- Scala
- Spark Structured Streaming
- Sbt
- PostgreSQL
- Docker

## Steps to Run the Project

1. **Clone the repository**:

    ```bash
       git clone https://github.com/adiattara/TrafficWatch.git
       cd TrafficWatch
    ```

2. **Start the PostgreSQL Database**:

   Navigate to the `database-service` directory and start the database:

    ```bash
    cd database-service
    docker-compose up -d
    ```


3. **Create checkpoint path**:

   Navigate to the `structured-streaming` directory and then :

    ```bash
    cd structured-streaming
    mkdir -p src/main/data/checkpoint
    ```

4. **Compile the project**:

    Navigate to the `structured-streaming` directory and compile the project using sbt:

    ```bash
    cd structured-streaming
    sbt compile
    ```

4. **Run the Structured Streaming application**:

   This will read the data from S3, transform it, and store it in the database.

    ```bash
    sbt "runMain RoadTraffic"
    ```

