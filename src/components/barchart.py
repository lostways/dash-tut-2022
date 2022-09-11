from dash import Dash, dcc, html
import plotly.express as px
from dash.dependencies import Input, Output

from ..data.loader import DataSchema
from ..data.source import DataSource
from . import ids


def render(app: Dash, source: DataSource) -> html.Div:
    @app.callback(
        Output(ids.BARCHART, "children"),
        [
            Input(ids.YEAR_DROPDOWN, "value"),
            Input(ids.MONTH_DROPDOWN, "value"),
            Input(ids.CATEGORY_DROPDOWN, "value"),
        ],
    )
    def update_barchart(
        years: list[str], months: list[str], categories: list[str]
    ) -> html.Div:
        filtered_data = source.filter(years, months, categories)

        if not filtered_data.row_count:
            return html.Div("No data selected")

        fig = px.bar(
            filtered_data.create_pivot_table(),
            x=DataSchema.CATEGORY,
            y=DataSchema.AMOUNT,
            color=DataSchema.CATEGORY,
        )

        return html.Div(dcc.Graph(figure=fig), id=ids.BARCHART)

    return html.Div(id=ids.BARCHART)
