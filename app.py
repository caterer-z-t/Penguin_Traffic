# In[1]: Imports
import dash
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
import os
import sys

# Set the working directory to the directory of this file
current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)
sys.path.append(current_dir)

# Import the HighwayTrafficSimulation class from our local file
from app.utils.highway_traffic_and_car_sim import (
    HighwayTrafficSimulation,
    HIGHWAY_LENGTH,
)
from app.main import layout
from app.utils.utils import (
    create_figure,
    create_placeholder_figure,
    create_figure_statisticts,
    collapse_button,
)

# In[2]: Initialize the Dash app
# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SANDSTONE])

# Define the layout of the app
app.layout = layout


# In[3]: Define the callbacks
@app.callback(
    Output("interval-component", "disabled"),
    Input("start-button", "n_clicks"),
    Input("stop-button", "n_clicks"),
    prevent_initial_call=True,
)
def control_simulation(start_clicks, stop_clicks):
    ctx = dash.callback_context
    if not ctx.triggered:
        return True  # Disabled by default

    button_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if button_id == "start-button":
        return False  # Enable interval when Start is clicked
    else:
        return True  # Disable interval when Stop is clicked


@app.callback(
    Output("collapse", "is_open"),
    Input("collapse-button", "n_clicks"),
    State("collapse", "is_open"),
    prevent_initial_call=True,
)
def toggle_collapse(n, is_open):
    collapse_button(n, is_open)


# Initialize the traffic simulation
traffic_sim = HighwayTrafficSimulation()


@app.callback(
    Output("highway-graph", "figure"),
    Output("highway-graph-statistics", "figure"),
    Input("interval-component", "n_intervals"),
    Input("simulation-type", "value"),
    State("start-button", "n_clicks"),
    State("speed-slider", "value"),
    State("lane-slider", "value"),
)
def update_traffic(
    n, simulation_type, start_button, speed_slider_value, lane_slider_value
):

    if start_button == 0:
        return (
            create_placeholder_figure("/assets/mana5280-DAQOskiNFtg-unsplash.jpg"),
            create_placeholder_figure(
                "/assets/rod-long-ZFA5c0loQE8-unsplash.jpg"
            ),
        )

    # Make sure function executes only when necessary
    if simulation_type == "simple":
        traffic_sim.update_simple(speed_slider_value, lane_slider_value)

    elif simulation_type == "individualistic":
        traffic_sim.update_individualistic(speed_slider_value, lane_slider_value)

    elif simulation_type == "penguin":
        traffic_sim.update_penguin(speed_slider_value, lane_slider_value)

    # Handle other simulation types or return a default figure
    return (
        create_figure(lane_slider_value, traffic_sim), 
        create_figure_statisticts(traffic_sim)
    )


# In[4]: Run the app
if __name__ == "__main__":
    app.run_server(debug=True, port=8050)
