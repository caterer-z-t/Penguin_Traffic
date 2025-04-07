# In[1]: Imports
from dash import dcc, html
import dash_bootstrap_components as dbc

# In[2]: Initalize parameters
FRAME_RATE = 1000  # Update every second

# In[3]: app layout
layout = html.Div(
    [
        html.H1("Highway Traffic Simulation"),
        html.Div(
            [
                html.Div("Speed of simulation:", style={"margin-bottom": "5px"}),
                dcc.Graph(id="highway-graph", config={"displayModeBar": False}),
            ]
        ),
        html.Div(
            [
                html.Div(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [
                                                        dbc.Row(
                                                            [
                                                                html.Div(
                                                                    "Simulation controls:",
                                                                    style={
                                                                        "margin-bottom": "5px"
                                                                    },
                                                                ),
                                                                
                                                            ],
                                                        ),
                                                        dbc.Row(
                                                            [
                                                                dbc.Col(
                                                                    [
                                                                        dbc.Button(
                                                                            "Start",
                                                                            id="start-button",
                                                                            n_clicks=0,
                                                                            className="me-2",
                                                                        ),
                                                                    ],
                                                                    style={
                                                                        "display": "flex",
                                                                        "justify-content": "center",
                                                                    },
                                                                ),
                                                                dbc.Col(
                                                                    [
                                                                        dbc.Button(
                                                                            "Stop",
                                                                            id="stop-button",
                                                                            n_clicks=0,
                                                                            className="me-2",
                                                                        ),
                                                                    ],
                                                                    style={
                                                                        "display": "flex",
                                                                        "justify-content": "center",
                                                                    },
                                                                ),
                                                                dbc.Col(
                                                                    [
                                                                        dbc.Button(
                                                                            "Reset",
                                                                            id="reset-button",
                                                                            n_clicks=0,
                                                                            className="me-2",
                                                                        ),
                                                                    ],
                                                                    style={
                                                                        "display": "flex",
                                                                        "justify-content": "center",
                                                                    },
                                                                ),
                                                            ]
                                                        ),
                                                    ],
                                                ),
                                                dbc.Col(
                                                    [
                                                        html.Div(
                                                            "Additional Model Parameters:",
                                                            style={
                                                                "margin-bottom": "5px"
                                                            },
                                                        ),
                                                        dbc.Button(
                                                            "Additional Model Parameters",
                                                            id="collapse-button",
                                                            className="me-2",
                                                        ),
                                                        html.Br(),
                                                        dbc.Collapse(
                                                            dbc.Card(
                                                                dbc.CardBody(
                                                                    [
                                                                        html.Div(
                                                                            "Highway Length:",
                                                                            style={
                                                                                "margin-bottom": "5px"
                                                                            },
                                                                        ),
                                                                        dcc.Input(
                                                                            id="highway-length",
                                                                            type="number",
                                                                            value=100,
                                                                            style={
                                                                                "width": "50%"
                                                                            },
                                                                        ),
                                                                        html.Div(
                                                                            "Intervals:",
                                                                            style={
                                                                                "margin-top": "10px",
                                                                                "margin-bottom": "5px",
                                                                            },
                                                                        ),
                                                                        dcc.Input(
                                                                            id="interval-input",
                                                                            type="number",
                                                                            value=1000,
                                                                            style={
                                                                                "width": "50%"
                                                                            },
                                                                        ),
                                                                    ]
                                                                )
                                                            ),
                                                            id="collapse",
                                                        ),
                                                    ],
                                                ),
                                            ],
                                        ),
                                    ],
                                    width=6,
                                ),
                                dbc.Col(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [
                                                        html.Div(
                                                            "Simulation Type:",
                                                            style={
                                                                "margin-bottom": "5px"
                                                            },
                                                        ),
                                                        dcc.Dropdown(
                                                            id="simulation-type",
                                                            options=[
                                                                {
                                                                    "label": "Simple",
                                                                    "value": "simple",
                                                                },
                                                                {
                                                                    "label": "Individualistic",
                                                                    "value": "individualistic",
                                                                },
                                                                {
                                                                    "label": "Penguin",
                                                                    "value": "penguin",
                                                                },
                                                            ],
                                                            value="simple",  # Ensure valid default
                                                            style={"width": "50%"},
                                                        ),
                                                    ]
                                                ),
                                            ]
                                        ),
                                    ],
                                    width=6,
                                ),
                            ]
                        )
                    ]
                ),
            ],
            style={
                "margin-top": "20px",
                "padding": "10px",
                "background-color": "#f8f9fa",
                "border-radius": "5px",
            },
        ),
        html.Div(
            [
                html.Div("Number of lanes:", style={"margin-bottom": "5px"}),
                dcc.Slider(
                    id="lane-slider",
                    min=1,
                    max=8,
                    step=1,
                    value=5,
                    marks={i: str(i) for i in range(1, 9)},  # Match range with min/max
                    tooltip={"placement": "bottom", "always_visible": True},
                ),
            ],
            style={
                "margin-top": "20px",
                "padding": "10px",
                "background-color": "#f8f9fa",
                "border-radius": "5px",
            },
        ),
        html.Div(
            [
                html.Div("Car spawn rate:", style={"margin-bottom": "5px"}),
                dcc.Slider(
                    id="speed-slider",
                    min=0,
                    max=100,
                    step=1,
                    value=50,
                    marks={0: "0", 25: "25", 50: "50", 75: "75", 100: "100"},
                    tooltip={"placement": "bottom", "always_visible": True},
                ),
            ],
            style={
                "margin-top": "20px",
                "padding": "10px",
                "background-color": "#f8f9fa",
                "border-radius": "5px",
            },
        ),
        html.Div(
            [
                # html.Div("Speed of simulation:", style={"margin-bottom": "5px"}),
                html.Br(),
                dcc.Graph(id="highway-graph-statistics", config={"displayModeBar": False}),
            ]
        ),
        dcc.Interval(
            id="interval-component", interval=FRAME_RATE, n_intervals=0, disabled=True
        ),
    ],
    style={"padding": "20px", "font-family": "Arial"},
)
