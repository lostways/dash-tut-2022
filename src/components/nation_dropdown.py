from dash import Dash, html, dcc
from . import ids


def render(app: Dash) -> html.Div:
    all_nations = ["Sount Korea", "China", "Canada"]

    return html.Div(
        children=[
            html.H6("Nation"),
            dcc.Dropdown(
                id=ids.NATION_DROPDOWN,
                options=[{"label": nation, "value": nation} for nation in all_nations],
                value=all_nations,
                multi=True,
            ),
            html.Button(
                id=ids.NATION_BUTTON,
                className="dropdown-button",
                children=["Select All"],
            ),
        ]
    )
