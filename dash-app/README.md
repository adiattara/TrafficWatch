# Dash Traffic Data Visualization App

This application is a Dash web application for visualizing traffic data. It fetches data from a PostgreSQL a data 
warehouse and displays it on a map and in graphs.

## Features

- Interactive map showing the current traffic status of different roads.
- Dropdown menu to select a specific road.
- Graphs showing the average speed and travel time for the selected road.
- Data is refreshed every minute.

## Technologies Used

- Python
- Dash
- Plotly
- Poetry
- Docker

## Setup and Installation

### Prerequisites

- Docker
- Docker Compose
- Data Warehouse with traffic data
- Poetry

### Steps

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/adiattara/TrafficWatch.git
   cd TrafficWatch
   ```
2. **Start the Dash app service**:

   Navigate to the `dash-app` directory and start the dash-app service:

   ```bash
   cd dash-app
   cd dash-app
   docker-compose up -d
   ```
3. **Open a browser** :

   Go to `http://localhost:8050` uou should see the Dash app running and displaying the traffic data visualization.
