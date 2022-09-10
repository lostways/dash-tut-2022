from dash import Dash, dcc, html
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import pandas as pd

from ..data.loader import DataSchema
from . import ids


def render(app: Dash, data: pd.DataFrame) -> html.Div:
    @app.callback(
        Output(ids.PIECHART, "children"),
        [
            Input(ids.YEAR_DROPDOWN, "value"),
            Input(ids.MONTH_DROPDOWN, "value"),
            Input(ids.CATEGORY_DROPDOWN, "value"),
        ],
    )
    def update_piechart(
        years: list[str], months: list[str], categories: list[str]
    ) -> html.Div:
        filtered_data = data.query(
            "year in @years and month in @months and category in @categories"
        )

        if filtered_data.shape[0] == 0:
            return html.Div("No data selected")

        pie = go.Pie(
            labels=filtered_data[DataSchema.CATEGORY].tolist(),
            values=filtered_data[DataSchema.AMOUNT].tolist(),
            hole=0.5,
        )

        fig = go.Figure(data=[pie])
        fig.update_layout(margin={"t": 40, "b": 0, "l": 0, "r": 0})
        fig.update_traces(hovertemplate="%{label}<br>$%{value:.2f}<extra></extra>")
        return html.Div(dcc.Graph(figure=fig), id=ids.PIECHART)

    return html.Div(id=ids.PIECHART)