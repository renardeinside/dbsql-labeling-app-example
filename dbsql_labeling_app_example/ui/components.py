from typing import List

from dash import dcc, html

header = dcc.Markdown(
    "## Sample labeling app, built with [Dash](https://plotly.com/dash/) "
    "and [Databricks SQL](https://www.databricks.com/product/databricks-sql) 🔥",
    style={
        "font-size": "46px",
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
        "padding-top": "20px",
        "padding-bottom": "5px",
    },
)
current_index_view = html.Div(
    id="current-index-view",
    style={
        "text-align": "left",
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
                    "height": "50vh",
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


def dropdown(classes: List[str]) -> html.Div:
    return html.Div(
        dcc.Loading(
            id="dropdown-loader",
            children=[
                dcc.Dropdown(
                    classes,
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

class_guideline = html.Div(
    "Please select the class below and click confirm",
    style={"text-align": "center"},
)
