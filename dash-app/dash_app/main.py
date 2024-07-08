import dash
import folium
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import sqlalchemy
import json
def postgres_engine():
    return sqlalchemy.create_engine('postgresql://spark_user:password@postgres_database:5432/spark_db')
def load_data():
        conection = postgres_engine().connect()
        data = pd.read_sql("SELECT * FROM my_traffic_table", con=conection)
        conection.close()
        data['datetime'] = pd.to_datetime(data['datetime'], utc=True)
        data.dropna(subset=['nbVehiculePerRoad', 'meanVitessePerRoad', 'vitesseMaximumPerRoad', 'meanTravelTime'],
                    inplace=True)
        data.sort_values('datetime', inplace=True)
        data['speedDeviation'] = data['vitesseMaximumPerRoad'] - data['meanVitessePerRoad']
        return data

def load_data_map():

    queries = """select * from my_traffic_map where datetime in (select max(datetime) from my_traffic_map)"""

    connection = postgres_engine().connect()

    df = pd.read_sql(queries, connection)

    connection.close()

    road = [dict(name=row['name'], status=row['status'], coordinates=json.loads(row['coordinates'])) for _, row in
            df.iterrows()]

    return road

def get_color(status):
    colors = {
        'freeFlow': 'green',
        'heavy': 'red',
        'medium': 'orange',
        'slow': 'yellow'
    }
    return colors.get(status, 'blue')

def create_map(roads):
    # Centrer la carte sur Rennes avec le zoom souhaité
    m = folium.Map(location=[47.915407, -1.656561], zoom_start=11.49, max_bounds=True)
    folium.TileLayer('openstreetmap', overlay=True, control=False, opacity=0.5).add_to(m)
    # Ajouter une attribution pour l'auteur
    folium.map.LayerControl().add_to(m)
    folium.map.Marker(
        location=[47.915407, -1.656561],
        popup='Centre de Rennes',
        icon=folium.Icon(icon='info-sign')
    ).add_to(m)
    folium.map.CustomPane("labels").add_to(m)
    folium.Marker(
        location=[48.1173, -1.6778],
        icon=folium.Icon(color='green')
    ).add_to(m)

    # Ajouter un script pour centrer la barre de défilement par défaut

    for road in roads:
        color = get_color(road['status'])
        coordinates = road['coordinates'][0]
        folium.PolyLine(locations=[[lat, lon] for lon, lat in coordinates], color=color, weight=5).add_to(m)
    return m._repr_html_()  # Returns the HTML representation of the map

#
if __name__ == '__main__':
    # Initialize the Dash app
    app = dash.Dash(__name__)

    # Define the layout of the app
    app.layout = html.Div([

        html.Div([
            html.Iframe(id='map', srcDoc=create_map(load_data_map()), width='100%', height='350'),
            # Hauteur de la carte ajustée à 300px
        ], style={'width': '100%', 'height': '20%'}),
        html.H1('Traffic Data Visualization by Metric'),
        dcc.Dropdown(
            id='road-dropdown',
            options=[],
            value=None
        ),
        # Ajuster la hauteur de la division de la carte
        html.Div([
            dcc.Graph(id='avg-speed-graph', style={'height': '500px', 'width': '48%'}),
            dcc.Graph(id='travel-time-graph', style={'height': '500px', 'width': '48%'}),
        ], style={
            'display': 'flex',
            'flex-direction': 'row',
            'justify-content': 'space-between',
            'align-items': 'center',
            'height': '70%'  # Ajuster la hauteur de la division des graphiques
        }),
        dcc.Interval(
            id='interval-component',
            interval=1 * 60 * 1000,  # Rafraîchir toutes les 1 minute
            n_intervals=0
        )
    ])

    # Function to load data from the databas
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
        [
         Output('avg-speed-graph', 'figure'),
         Output('travel-time-graph', 'figure'),
        [Input('road-dropdown', 'value'),
         Input('interval-component', 'n_intervals')]]
    )
    def update_graphs(selected_road, n_intervals):
        filtered_data = data[data['denomination'] == selected_road]
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



        return  avg_speed_fig, travel_time_fig

    @app.callback(
        Output('map', 'srcDoc'),
        Input('interval-component', 'n_intervals')
    )
    def update_map(n_intervals):
        return create_map(load_data_map())

    app.run_server(host='0.0.0.0', port=8050, debug=True)






