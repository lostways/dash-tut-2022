from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import pandas as pd
from ..data.loader import DataSchema
from . import ids


def render(app: Dash, data: pd.DataFrame) -> html.Div:
    all_months: list[str] = data[DataSchema.MONTH].tolist()
    unique_months = sorted(set(all_months))

    @app.callback(
        Output(ids.MONTH_DROPDOWN, "value"),
        [
            Input(ids.SELECT_ALL_MONTHS_BUTTON, "n_clicks"),
            Input(ids.YEAR_DROPDOWN, "value"),
        ],
    )
    def update_months(_: int, years: list[str]) -> list[str]:
        filtered_data = data.query("year in @years")
        return sorted(set(filtered_data[DataSchema.MONTH].tolist()))

    return html.Div(
        children=[
            html.H6("Month"),
            dcc.Dropdown(
                id=ids.MONTH_DROPDOWN,
                options=[{"label": month, "value": month} for month in unique_months],
                value=all_months,
                multi=True,
            ),
            html.Button(
                id=ids.SELECT_ALL_MONTHS_BUTTON,
                className="dropdown-button",
                children=["Select All"],
            ),
        ]
    )
