import i18n
from dash import Dash, dcc, html
import plotly.express as px
from dash.dependencies import Input, Output

from ..data.source import DataSource
from . import ids


def render(app: Dash, source: DataSource) -> html.Div:
    @app.callback(
        Output(ids.LINECHART, "children"),
        [
            Input(ids.YEAR_DROPDOWN, "value"),
            Input(ids.MONTH_DROPDOWN, "value"),
            Input(ids.CATEGORY_DROPDOWN, "value"),
        ],
    )
    def update_linechart(
        years: list[str], months: list[str], categories: list[str]
    ) -> html.Div:
        filtered_data = source.filter(years, months, categories)

        if not filtered_data.row_count:
            return html.Div("No data selected")

        chart_data = filtered_data.create_month_pivot_table()
        line_chart = px.line(
            chart_data,
            labels={
                "value": i18n.t("general.amount"),
                "category": i18n.t("general.category"),
                "month": i18n.t("general.month"),
            },
            markers=True,
        )

        return html.Div(dcc.Graph(figure=line_chart), id=ids.LINECHART)

    return html.Div(id=ids.LINECHART)
