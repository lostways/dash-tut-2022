from dash import Dash, dcc, html
import plotly.graph_objects as go
from dash.dependencies import Input, Output

from ..data.source import DataSource
from . import ids


def render(app: Dash, source: DataSource) -> html.Div:
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
        filtered_data = source.filter(years, months, categories)

        if not filtered_data.row_count:
            return html.Div("No data selected")

        pie = go.Pie(
            labels=filtered_data.all_categories,
            values=filtered_data.all_amounts,
            hole=0.5,
        )

        fig = go.Figure(data=[pie])
        fig.update_layout(margin={"t": 40, "b": 0, "l": 0, "r": 0})
        fig.update_traces(hovertemplate="%{label}<br>$%{value:.2f}<extra></extra>")
        return html.Div(dcc.Graph(figure=fig), id=ids.PIECHART)

    return html.Div(id=ids.PIECHART)
