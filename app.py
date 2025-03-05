import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
import os
import sys

# Set the working directory to the directory of this file
current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)
sys.path.append(current_dir)

from Project import HighwayTrafficSimulation

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Create traffic simulation instance
traffic_sim = HighwayTrafficSimulation()

# Define the layout of the app
app.layout = html.Div(
    children=[
        html.H1(children="Enhanced Highway Traffic System"),
        dcc.Graph(
            id="highway-graph",
            config={"displayModeBar": False},  # Hide the toolbar
        ),
        html.Div(
            children=[
                # Number of cars input
                html.Label("Number of Cars:"),
                dcc.Input(
                    id="num-cars-input",
                    type="number",
                    min=1,
                    max=60,
                    value=6,
                    style={"marginRight": "10px"},
                ),
                # Start and Stop buttons
                dbc.Button("Start", id="start-button", n_clicks=0, className="me-2"),
                dbc.Button("Stop", id="stop-button", n_clicks=0),
            ]
        ),
        dcc.Interval(id="interval-component", interval=1000, n_intervals=0),
    ]
)


@app.callback(
    Output("highway-graph", "figure"),
    Input("interval-component", "n_intervals"),
    Input("num-cars-input", "value"),
    State("start-button", "n_clicks"),
    State("stop-button", "n_clicks"),
)
def update_traffic_system(n, num_cars, start_clicks, stop_clicks):
    # Regenerate cars if the number changes
    if (
        not hasattr(update_traffic_system, "last_num_cars")
        or update_traffic_system.last_num_cars != num_cars
    ):
        traffic_sim.generate_cars(num_cars)
        update_traffic_system.last_num_cars = num_cars

    # Determine if the simulation is active based on button presses
    simulation_active = start_clicks > stop_clicks

    # If the simulation is not active, don't update the car positions
    if not simulation_active:
        return {}

    # Update car positions
    car_positions = traffic_sim.update_car_positions(n)

    # Create a grid layout for the road (black squares for the road, green for sides)
    road_data = []

    # Create the black roadway grid (road in black)
    for y in range(traffic_sim.road_width):
        for x in range(traffic_sim.highway_length):
            road_data.append(
                go.Scatter(
                    x=[x],
                    y=[y],
                    mode="markers",
                    marker=dict(size=20, color="black", symbol="square"),
                    showlegend=False,
                )
            )

    # Create the green side squares (side of the road)
    side_data = []
    for y in [
        -traffic_sim.side_width,
        traffic_sim.road_width,
    ]:  # Green side on both sides
        for x in range(traffic_sim.highway_length):
            side_data.append(
                go.Scatter(
                    x=[x],
                    y=[y],
                    mode="markers",
                    marker=dict(size=20, color="green", symbol="square"),
                    showlegend=False,
                )
            )

    # Add cars as colored squares
    car_data = []
    for car in car_positions:
        car_data.append(
            go.Scatter(
                x=[car.position],
                y=[car.lane - 1],  # shift the car to match lane position
                mode="markers",
                marker=dict(size=20, color=car.color, symbol="square"),
                name=f"Car (Lane {car.lane}, Speed {car.speed:.1f})",
                showlegend=True,
            )
        )

    # Set up the layout of the figure
    figure = {
        "data": road_data + side_data + car_data,
        "layout": go.Layout(
            title="Highway Traffic Simulation",
            xaxis=dict(
                range=[0, traffic_sim.highway_length], title="Highway Position (m)"
            ),
            yaxis=dict(
                range=[-1, traffic_sim.road_width],
                tickvals=[i for i in range(traffic_sim.road_width)],
                ticktext=[f"Lane {i+1}" for i in range(traffic_sim.road_width)],
                title="Lanes",
            ),
            showlegend=True,
            plot_bgcolor="white",
            xaxis_showgrid=False,
            yaxis_showgrid=False,
            height=500,
        ),
    }
    return figure


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True, port=8050, host="0.0.0.0")
