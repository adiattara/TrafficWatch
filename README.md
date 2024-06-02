# Traffic watch Application

## Description :

This is a structure streaming application that process the data fetched from an API,
Transform the data and store it in a database.
Our goal is to provide a real-time traffic monitoring system that can be used by the traffic department to monitor the traffic in the city.

## Project Structure

1. **Streaming Application**:
    - Reads traffic data from Renne API  and stores it in a specific directory.
    - **url** : https://data.rennesmetropole.fr/api/v1/console/datasets/1.0/search/
    - **directory path** : `TrafficWatch/src/main/data/json_raw_data`

2. **Structured Streaming**:
    - Streams files from the **json_raw_data** directory, processes , and writes them to a PostgreSQL database in 
      real-time.

3. **Database Service**:
    - A PostgreSQL database to store the processed  data into **traffic_table**.

4. **DASH Application**:
    - Retrieves the data from the PostgreSQL database and creates visualizations using the DASH framework.

## Technologies Used

- **Structure Streaming**: For real-time data processing.
- **Docker**: For containerizing the applications.
- **PostgreSQL**: As the database to store traffic data.
- **dash**: a python framework for building web app for data visulisation.

## Setup Instructions

### Prerequisites

- Docker, Docker Compose installed on your machine and IntelliJ also.

### Steps to Run the Project

1. **Clone the repository**:

    ```bash 
      git https://github.com/adiattara/TrafficWatch.git
       cd TrafficWatch
    ```

2. **Start the PostgreSQL Database**:

   Navigate to the `database-service` directory and start the database:

    ```bash
    cd database-service
    docker-compose up -d
    ```

3. **Run the Streaming Application**:

   Navigate to the `TrafficWatch/src/main/scala` directory then run `RoadTraffic.scala`

4. **Run the Structured Streaming**:

   Navigate to the `TrafficWatch/src/main/scala` directory and run `RoadTraffic.scala`


5. **Build and Start the DASH Application**:

   Navigate to the `dash-app` directory and start it using Docker Compose:

    ```bash
    cd dash-app
    docker-compose up --build
    ```

6. **Access the DASH Application**:

   Open your web browser and navigate to `http://localhost:8050` to view the traffic data visualizations.


