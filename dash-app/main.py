import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import sqlalchemy

def postgres_engine():
    return sqlalchemy.create_engine('postgresql://spark_user:password@postgres_database:5432/spark_db')


# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1('Traffic Data Visualization by Metric'),
    dcc.Dropdown(
        id='road-dropdown',
        options=[],
        value=None
    ),
    html.Div([
        dcc.Graph(id='vehicles-graph'),
        dcc.Graph(id='avg-speed-graph'),
        dcc.Graph(id='travel-time-graph'),
        dcc.Graph(id='speed-deviation-graph')
    ], style={
        'display': 'grid',
        'grid-template-columns': '1fr 1fr',
        'grid-gap': '20px'
    }),
    dcc.Interval(
        id='interval-component',
        interval=1 *60*1000,  # Refresh every 1 minute
        n_intervals=0
    )
])


# Function to load data from the database
def load_data():
    conection = postgres_engine().connect()
    data = pd.read_sql("SELECT * FROM traffic_table", con=conection)
    conection.close()
    data['datetime'] = pd.to_datetime(data['datetime'], utc=True)
    data.dropna(subset=['nbVehiculePerRoad', 'meanVitessePerRoad', 'vitesseMaximumPerRoad', 'meanTravelTime'],
                inplace=True)
    data.sort_values('datetime', inplace=True)
    data['speedDeviation'] = data['vitesseMaximumPerRoad'] - data['meanVitessePerRoad']
    return data


# Initial load of data
data = load_data()


# Update dropdown options on initial load and every interval
@app.callback(
    Output('road-dropdown', 'options'),
    Output('road-dropdown', 'value'),
    Input('interval-component', 'n_intervals')
)
def update_dropdown(n_intervals):
    global data
    data = load_data()
    options = [{'label': i, 'value': i} for i in data['denomination'].unique()]
    value = data['denomination'].unique()[0] if options else None
    return options, value


# Define callback to update graphs based on selected road and interval
@app.callback(
    [Output('vehicles-graph', 'figure'),
     Output('avg-speed-graph', 'figure'),
     Output('travel-time-graph', 'figure'),
     Output('speed-deviation-graph', 'figure')],
    [Input('road-dropdown', 'value'),
     Input('interval-component', 'n_intervals')]
)
def update_graphs(selected_road, n_intervals):
    filtered_data = data[data['denomination'] == selected_road]

    # Number of Vehicles
    vehicles_trace = go.Scatter(
        x=filtered_data['datetime'],
        y=filtered_data['nbVehiculePerRoad'],
        mode='lines+markers',
        name='Number of Vehicles',
        line=dict(color='blue')
    )
    vehicles_fig = {
        'data': [vehicles_trace],
        'layout': go.Layout(title='Number of Vehicles for ' + selected_road, xaxis={'title': 'Time'},
                            yaxis={'title': 'Number of Vehicles'})
    }

    # Average Speed
    avg_speed_trace = go.Scatter(
        x=filtered_data['datetime'],
        y=filtered_data['meanVitessePerRoad'],
        mode='lines+markers',
        name='Average Speed',
        line=dict(color='green')
    )
    avg_speed_fig = {
        'data': [avg_speed_trace],
        'layout': go.Layout(title='Average Speed for ' + selected_road, xaxis={'title': 'Time'},
                            yaxis={'title': 'Speed (km/h)'})
    }

    # Travel Time
    travel_time_trace = go.Scatter(
        x=filtered_data['datetime'],
        y=filtered_data['meanTravelTime'],
        mode='lines+markers',
        name='Average Travel Time',
        line=dict(color='red')
    )
    travel_time_fig = {
        'data': [travel_time_trace],
        'layout': go.Layout(title='Average Travel Time for ' + selected_road, xaxis={'title': 'Time'},
                            yaxis={'title': 'Travel Time (seconds)'})
    }

    # Speed Deviation
    speed_deviation_trace = go.Scatter(
        x=filtered_data['datetime'],
        y=filtered_data['speedDeviation'],
        mode='lines+markers',
        name='Speed Deviation',
        line=dict(color='purple')
    )
    speed_deviation_fig = {
        'data': [speed_deviation_trace],
        'layout': go.Layout(title='Speed Deviation for ' + selected_road, xaxis={'title': 'Time'},
                            yaxis={'title': 'Speed Deviation (km/h)'})
    }

    return vehicles_fig, avg_speed_fig, travel_time_fig, speed_deviation_fig


# Run the app
if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=8050, debug=True)


