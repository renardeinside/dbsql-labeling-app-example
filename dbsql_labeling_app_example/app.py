import os
from random import choice

from dash import Dash, Input, Output, State, ctx, dcc, html

from dbsql_labeling_app_example.crud import DataOperator
from dbsql_labeling_app_example.mode import debug_mode

external_stylesheets = [
    # bootstrap
    {
        "href": "https://cdn.jsdelivr.net/npm/bootstrap@3.4.1/dist/css/bootstrap.min.css",
        "rel": "stylesheet",
        "integrity": "sha384-HSMxcRTRxnN+Bdg0JdbxYKrThecOKuH5zCYotlSAcp1+c8xmyTe9GYg1l9a69psu",
        "crossorigin": "anonymous",
    },
    {"rel": "preconnect", "href": "https://fonts.googleapis.com"},
    {
        "rel": "preconnect",
        "href": "https://fonts.gstatic.com",
        "crossorigin": "anonymous",
    },
    {
        "href": "https://fonts.googleapis.com/css2?family=Inter&family=Noto+Sans&display=swap",
        "rel": "stylesheet",
    },
]

app = Dash(
    __name__, title="Data Labeling App", external_stylesheets=external_stylesheets
)
operator = DataOperator()
CLASSES = operator.get_all_classes()
ALL_IDS = operator.get_all_ids()

header = dcc.Markdown(
    """
    # This is a sample text labeling app, built with [Dash](https://plotly.com/dash/) and [Databricks SQL](https://www.databricks.com/product/databricks-sql) 🔥
    """,
    style={
        "font-size": "46px",
        "padding-left": "2vw",
        # "background-color": "#1b3139",
        "min-height": "64px",
        "max-height": "96px",
        "padding-top": "16px",
        "padding-bottom": "16px",
    },
)

guideline = dcc.Markdown(
    "Please click below to navigate between texts and correct their class labels if required.",
    style={
        "font-size": "20px",
        "padding-left": "2vw",
        "padding-top": "20px",
        "padding-bottom": "5px",
    },
)

current_index_view = html.Div(
    id="current-index-view",
    style={
        "text-align": "left",
        "padding-left": "2vw",
    },
)

text_container = html.Div(
    dcc.Loading(
        id="text-block-loading",
        children=[
            dcc.Markdown(
                id="text-container",
                style={
                    "font-size": "1.2em",
                    "font-family": "'Noto Sans', sans-serif",
                    "height": "60vh",
                    "overflow-y": "auto",
                },
            ),
        ],
    ),
    style={
        "flex-basis": "90%",
        "padding-right": "1em",
    },
)

navigation_buttons = [
    html.Button(
        "⬅️ Previous",
        id="prev_btn",
        n_clicks=0,
        className="btn btn-default btn-lg",
    ),
    html.Button(
        "🔀 Random",
        id="random_btn",
        n_clicks=0,
        className="btn btn-default btn-lg",
    ),
    html.Button(
        "Next ➡️",
        id="next_btn",
        n_clicks=0,
        className="btn btn-default btn-lg",
    ),
]

dropdown = html.Div(
    dcc.Loading(
        id="dropdown-loader",
        children=[
            dcc.Dropdown(
                CLASSES,
                id="class-selector",
                placeholder="Select the class",
                multi=False,
                clearable=False,
                style={
                    "color": "black",
                },
            ),
        ],
    ),
    style={
        "padding-top": "10px",
        "padding-bottom": "10px",
    },
)

confirm_button = dcc.Loading(
    id="submit-loading",
    children=[
        html.Button(
            "Confirm",
            id="confirm_btn",
            n_clicks=0,
            className="btn btn-success btn-block btn-md",
        ),
        html.Div(id="output-mock", style={"display": "none"}),
    ],
)

app.layout = html.Div(
    [
        header,
        html.Div(
            [
                guideline,
                current_index_view,
                html.Div(
                    [
                        text_container,
                        html.Div(
                            [
                                html.Div(
                                    "Please select the class below and click confirm",
                                    style={"text-align": "center"},
                                ),
                                dropdown,
                                confirm_button,
                            ],
                            style={"flex-basis": "10%", "padding-left": "1em"},
                        ),
                    ],
                    style={
                        "display": "flex",
                        "flex-direction": "row",
                        "padding": "5em",
                    },
                ),
                html.Div(
                    navigation_buttons,
                    style={
                        "justify-content": "space-evenly",
                        "display": "flex",
                        "padding-left": "30vw",
                        "padding-right": "30vw",
                    },
                ),
                dcc.Store(id="current-index", data=choice(ALL_IDS)),
            ],
            style={"padding": "20px", "height": "100%"},
        ),
    ]
)


@app.callback(
    Output("output-mock", "children"),
    Input("confirm_btn", "n_clicks"),
    State("class-selector", "value"),
    State("current-index", "data"),
)
def save_selected_class(_, value, current_index):
    if value:
        operator.update_element_by_id(current_index, value)
    return value


@app.callback(
    Output("current-index-view", "children"),
    Input("current-index", "data"),
)
def update_index_view(current_index):
    return f"Sample #{current_index} (out of {len(ALL_IDS)-1})"


@app.callback(
    Output("current-index", "data"),
    Output("text-container", "children"),
    Output("class-selector", "value"),
    Output("prev_btn", "disabled"),
    Output("next_btn", "disabled"),
    inputs=[
        Input("current-index", "data"),
        Input("prev_btn", "n_clicks"),
        Input("next_btn", "n_clicks"),
        Input("random_btn", "n_clicks"),
    ],
)
def navigate_to_element(current_index, _, __, ___):
    if "prev_btn" == ctx.triggered_id:
        current_index -= 1
    elif "random_btn" == ctx.triggered_id:
        current_index = choice(ALL_IDS)
    elif "next_btn" == ctx.triggered_id:
        current_index += 1

    label_data = operator.get_element_by_id(current_index)
    disable_previous = current_index <= 0
    disable_next = current_index >= len(ALL_IDS) - 1
    return (
        current_index,
        label_data.text,
        label_data.label,
        disable_previous,
        disable_next,
    )


if __name__ == "__main__":
    app.run(debug=debug_mode, host="0.0.0.0")
