from dash import Dash, dcc, html
import plotly.express as px
from dash.dependencies import Input, Output
from . import ids

METAL_DATA = px.data.medals_long()


def render(app: Dash) -> html.Div:
    @app.callback(Output(ids.BARCHART, "children"), Input(ids.NATION_DROPDOWN, "value"))
    def update_barchart(nations: list[str]) -> html.Div:
        filtered_data = METAL_DATA.query("nation in @nations")

        if filtered_data.shape[0] == 0:
            return html.Div("No data selected")

        fig = px.bar(filtered_data, x="medal", y="count", color="nation", text="nation")
        return html.Div(dcc.Graph(figure=fig), id=ids.BARCHART)

    return html.Div(id=ids.BARCHART)
