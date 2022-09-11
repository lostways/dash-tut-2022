from typing import Protocol
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import i18n

from . import ids


class CategoryDataSource(Protocol):
    @property
    def unique_categories(self) -> list[str]:
        ...


def render(app: Dash, source: CategoryDataSource) -> html.Div:
    @app.callback(
        Output(ids.CATEGORY_DROPDOWN, "value"),
        [
            Input(ids.SELECT_ALL_CATEGORIES_BUTTON, "n_clicks"),
            Input(ids.YEAR_DROPDOWN, "value"),
            Input(ids.MONTH_DROPDOWN, "value"),
        ],
    )
    def update_categories(_: int, years: list[str], months: list[str]) -> list[str]:
        filtered_data = source.filter(years=years, months=months)
        return filtered_data.unique_categories

    return html.Div(
        children=[
            html.H6(i18n.t("general.category")),
            dcc.Dropdown(
                id=ids.CATEGORY_DROPDOWN,
                options=[
                    {"label": category, "value": category}
                    for category in source.unique_categories
                ],
                value=source.unique_categories,
                multi=True,
            ),
            html.Button(
                id=ids.SELECT_ALL_CATEGORIES_BUTTON,
                className="dropdown-button",
                children=[i18n.t("general.select_all")],
            ),
        ]
    )
