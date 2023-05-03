import requests
from dash import Dash, html, dcc, Input, Output
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
from datetime import date
import dash_auth
import pandas as pd
from io import StringIO
from users import VALID_USERNAME_PASSWORD_PAIRS, username, password


app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.DARKLY])

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

username= username
password=password
print(username)

header = html.Div("NSSP DATA", className="h2 p-2 text-white bg-primary text-center")

URL = "https://essence.syndromicsurveillance.org/nssp_essence/api/timeSeries?endDate=9Feb2021&medicalGrouping=injury&percentParam=noPercent&geographySystem=hospitaldhhsregion&datasource=va_hospdreg&detector=probrepswitch&startDate=11Nov2020&timeResolution=daily&medicalGroupingSystem=essencesyndromes&userId=455&aqtTarget=TimeSeries"

r = requests.get(url=URL, auth=(username, password))
# print(type(r))

data = r.json()
# print(len(data))
keys = data.keys()
# for key in keys:
#     print(key)

# print(data['timeSeriesData'][0]['count'])

df = pd.DataFrame.from_dict(data['timeSeriesData'])
df.drop(['details', 'altText'], axis=1, inplace=True)
# print(type(data))
# df = pd.DataFrame.from_dict(data)
# df = pd.DataFrame(r['data'])
# df = pd.read_csv(StringIO(r), sep=',')
# df = pd.read_csv(URL)
print(df)
bgcolor = "#f3f3f1"  # mapbox light map land color

template = {"layout": {"paper_bgcolor": bgcolor, "plot_bgcolor": bgcolor}}


def blank_fig(height):
    """
    Build blank figure with the requested height
    """
    return {
        "data": [],
        "layout": {
            "height": height,
            "template": template,
            "xaxis": {"visible": False},
            "yaxis": {"visible": False},
        },
    }

app.layout = dbc.Container(
    [
        header,
        dbc.Row([
            dcc.DatePickerRange(
            id='my-date-picker-range',
            min_date_allowed=date(1995, 8, 5),
            max_date_allowed=date(2017, 9, 19),
            initial_visible_month=date(2017, 8, 5),
            end_date=date(2017, 8, 25)
            ),
        ]),
        dbc.Row([
            dbc.Col([
                dcc.Graph(id='incident-graph', figure=blank_fig(500)),
            ], width=12),
        ])
    ],
)

@app.callback(
    Output('incident-graph', 'figure'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'))
def update_output(start_date, end_date):
    
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df['date'],
        y=df['count']
    ))


    return fig


if __name__ == '__main__':
    app.run_server(debug=True)


# r = requests.get(url=URL, auth=(username, password))