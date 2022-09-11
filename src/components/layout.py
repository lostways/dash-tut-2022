from dash import Dash, html
from . import year_dropdown, month_dropdown, category_dropdown, barchart, piechart
from ..data.source import DataSource


def create_layout(app: Dash, source: DataSource) -> html.Div:
    return html.Div(
        className="app-div",
        children=[
            html.H1(app.title),
            html.Hr(),
            html.Div(
                className="dropdown-container",
                children=[
                    year_dropdown.render(app, source),
                    month_dropdown.render(app, source),
                    category_dropdown.render(app, source),
                ],
            ),
            html.Div(
                className="bar-container", children=[barchart.render(app, source)]
            ),
            html.Div(
                className="pie-container", children=[piechart.render(app, source)]
            ),
        ],
    )
