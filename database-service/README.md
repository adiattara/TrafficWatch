## Local Data Warehouse Setup

#### Prerequisites

- **Docker**: Ensure Docker is installed on your machine. You can download it from [here](https://www.docker.com/get-started).

#### Steps to Start the Data Warehouse on Local

1. **Clone the Repository**:

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
   

