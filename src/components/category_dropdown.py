from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import pandas as pd
from ..data.loader import DataSchema
from . import ids


def render(app: Dash, data: pd.DataFrame) -> html.Div:
    all_categories: list[str] = data[DataSchema.CATEGORY].tolist()
    unique_categories = sorted(set(all_categories))

    @app.callback(
        Output(ids.CATEGORY_DROPDOWN, "value"),
        [
            Input(ids.SELECT_ALL_CATEGORIES_BUTTON, "n_clicks"),
            Input(ids.YEAR_DROPDOWN, "value"),
            Input(ids.MONTH_DROPDOWN, "value"),
        ],
    )
    def update_categories(_: int, years: list[str], months: list[str]) -> list[str]:
        filtered_data = data.query("year in @years and month in @months")
        return sorted(set(filtered_data[DataSchema.CATEGORY].tolist()))

    return html.Div(
        children=[
            html.H6("CATEGROY"),
            dcc.Dropdown(
                id=ids.CATEGORY_DROPDOWN,
                options=[
                    {"label": category, "value": category}
                    for category in unique_categories
                ],
                value=all_categories,
                multi=True,
            ),
            html.Button(
                id=ids.SELECT_ALL_CATEGORIES_BUTTON,
                className="dropdown-button",
                children=["Select All"],
            ),
        ]
    )
