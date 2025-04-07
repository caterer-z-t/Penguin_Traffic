# In[1]: Imports
import plotly.graph_objects as go
import os
import sys

# Set the working directory to the directory of this file
current_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_dir)
sys.path.append(current_dir)

from app.utils.highway_traffic_and_car_sim import HIGHWAY_LENGTH

# In[2]: Define functions
def create_figure(lane_slider_value, traffic_sim):
    # Road background (gray area)
    road_background = go.Scatter(
        x=[0, HIGHWAY_LENGTH, HIGHWAY_LENGTH, 0, 0],
        y=[-0.5, -0.5, lane_slider_value - 0.5, lane_slider_value - 0.5, -0.5],
        fill="toself",
        fillcolor="lightgray",
        line=dict(width=0),
        mode="lines",
        hoverinfo="none",
    )

    # Lane markers (dashed white lines)
    lane_lines = [
        go.Scatter(
            x=[i for i in range(0, HIGHWAY_LENGTH, 5)],
            y=[lane + 0.5] * (HIGHWAY_LENGTH // 5),
            mode="markers",
            marker=dict(size=2, color="white", symbol="line-ew"),
            hoverinfo="none",
        )
        for lane in range(lane_slider_value - 1)
    ]

    # Car representations
    car_data = []
    for car in traffic_sim.cars:
        car_data.append(
            go.Scatter(
                x=[car.position],
                y=[car.lane - 1],  # Centering cars in lanes
                mode="markers",
                marker=dict(size=15, color=car.color, symbol="circle", opacity=0.9),
                hovertext=f"Lane: {car.lane}, Speed: {car.speed:.1f}, Type: {car.driver_type}",
                hoverinfo="text",
            )
        )

    # Create the figure
    fig = {
        "data": [road_background] + lane_lines + car_data,
        "layout": go.Layout(
            title="Highway Traffic Simulation",
            xaxis=dict(
                range=[0, HIGHWAY_LENGTH], title="Highway Position", showgrid=False
            ),
            yaxis=dict(
                range=[-1, lane_slider_value],
                title="Lanes",
                tickvals=[i for i in range(lane_slider_value)],
                ticktext=[f"Lane {i+1}" for i in range(lane_slider_value)],
                showgrid=False,
                tickangle=-45,  # Rotate y-axis text 45 degrees
            ),
            showlegend=False,
            plot_bgcolor="white",
            margin=dict(l=50, r=50, b=50, t=50),
            height=500,
        ),
    }

    return fig


def create_placeholder_figure(filepath):
    fig = go.Figure()

    # Add an image using the local path (served via Dash assets)
    fig.add_layout_image(
        dict(
            source=filepath,  # Reference to local image
            x=0.5,
            y=0.5,  # Center the image
            xref="paper",
            yref="paper",
            sizex=1.5,
            sizey=1.5,
            xanchor="center",
            yanchor="middle",
            layer="below",
        )
    )

    # Remove axes and grid
    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)
    fig.update_layout(
        # title="Waiting for Simulation to Start...",
        showlegend=False,
        plot_bgcolor="white",
        margin=dict(l=0, r=0, t=40, b=0)
    )

    return fig


def create_figure_statisticts(traffic_sim):
    """Creates a figure displaying the traffic simulation statistics over time."""

    stats = traffic_sim.statistics  # Extract statistics dictionary

    if not stats["time_elapsed"]:  # Ensure there's data to plot
        return go.Figure()  # Return an empty figure if no data exists

    fig = go.Figure()

    # Plot number of cars over time
    # fig.add_trace(
    #     go.Scatter(
    #         x=stats["time_elapsed"],
    #         y=stats["avg_cars_per_lane"],
    #         mode="lines",
    #         name="Number of Cars",
    #     )
    # )

    # Plot average speed over time
    fig.add_trace(
        go.Scatter(
            x=stats["time_elapsed"],
            y=stats["avg_speed"],
            mode="lines",
            name="Average Speed",
        )
    )

    # Plot density over time
    fig.add_trace(
        go.Scatter(
            x=stats["time_elapsed"],
            y=stats["avg_density"],
            mode="lines",
            name="Traffic Density",
        )
    )



    # Set figure layout
    fig.update_layout(
        title="Traffic Simulation Statistics",
        xaxis_title="Time Steps",
        yaxis_title="Value",
        legend_title="Metrics",
        template="plotly_dark",
    )

    return fig

def collapse_button(n, is_open):
    if n:
        return not is_open
    return is_open
