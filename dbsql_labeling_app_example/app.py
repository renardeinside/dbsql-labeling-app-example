from random import choice

from dash import Dash, Input, Output, State, ctx, dcc, html

from dbsql_labeling_app_example.crud import DataOperator
from dbsql_labeling_app_example.mode import debug_mode
from dbsql_labeling_app_example.ui import external_stylesheets
from dbsql_labeling_app_example.ui.components import (class_guideline,
                                                      confirm_button,
                                                      current_index_view,
                                                      dropdown, guideline,
                                                      header,
                                                      navigation_buttons,
                                                      text_container)

app = Dash(
    __name__, title="Data Labeling App", external_stylesheets=external_stylesheets
)
operator = DataOperator()
CLASSES = operator.get_all_classes()
ALL_IDS = operator.get_all_ids()

app.layout = html.Div(
    [
        html.Div(
            [
                header,
                guideline,
                current_index_view,
                html.Div(
                    [
                        text_container,
                        html.Div(
                            [
                                class_guideline,
                                dropdown(CLASSES),
                                confirm_button,
                            ],
                            style={"flex-basis": "10%", "padding-left": "1em"},
                        ),
                    ],
                    style={
                        "display": "flex",
                        "flex-direction": "row",
                        "padding": "2em",
                        "margin-bottom": "2em",
                    },
                ),
                html.Div(
                    navigation_buttons,
                    style={
                        "justify-content": "space-evenly",
                        "display": "flex",
                    },
                ),
                dcc.Store(id="current-index", data=choice(ALL_IDS)),
            ],
            style={
                "padding-top": "1em",
                "padding-left": "2em",
                "padding-right": "2em",
                "padding-bottom": "5em",
            },
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
