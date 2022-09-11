from typing import Protocol
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import i18n

from . import ids


class MonthDataSource(Protocol):
    @property
    def unique_months(self) -> list[str]:
        ...


def render(app: Dash, source: MonthDataSource) -> html.Div:
    @app.callback(
        Output(ids.MONTH_DROPDOWN, "value"),
        [
            Input(ids.SELECT_ALL_MONTHS_BUTTON, "n_clicks"),
            Input(ids.YEAR_DROPDOWN, "value"),
        ],
    )
    def update_months(_: int, years: list[str]) -> list[str]:
        filtered_data = source.filter(years=years)
        return filtered_data.unique_months

    return html.Div(
        children=[
            html.H6(i18n.t("general.month")),
            dcc.Dropdown(
                id=ids.MONTH_DROPDOWN,
                options=[
                    {"label": month, "value": month} for month in source.unique_months
                ],
                value=source.unique_months,
                multi=True,
            ),
            html.Button(
                id=ids.SELECT_ALL_MONTHS_BUTTON,
                className="dropdown-button",
                children=[i18n.t("general.select_all")],
            ),
        ]
    )
