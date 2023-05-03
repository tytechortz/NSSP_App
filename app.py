import requests
from dash import Dash, html, dcc, Input, Output
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
from datetime import date
import dash_auth
import pandas as pd
from io import StringIO
from users import VALID_USERNAME_PASSWORD_PAIRS, username, password
import datetime
from datetime import date

today = date.today()

app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.DARKLY])

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)




username= username
password=password
print(username)

header = html.Div("NSSP DATA", className="h2 p-2 text-white bg-primary text-center")


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
            # min_date_allowed=date(1995, 8, 5),
            # max_date_allowed=date(2017, 9, 19),
            initial_visible_month=today,
            start_date=date(2023, 1, 1),
            end_date=today
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
    
    start_date_new = datetime.datetime.strptime(start_date, '%Y-%m-%d').strftime('%d%b%Y')
    end_date_new = datetime.datetime.strptime(end_date, '%Y-%m-%d').strftime('%d%b%Y')
    
    URL2 = "https://essence.syndromicsurveillance.org/nssp_essence/api/timeSeries?nonZeroComposite=false&endDate=" + end_date_new + "&startMonth=january&graphOnly=false&geography=co_adams&geography=co_arapahoe&geography=co_boulder&geography=co_broomfield&geography=co_denver&geography=co_douglas&geography=co_el%20paso&geography=co_jefferson&geography=co_la%20plata&geography=co_larimer&geography=co_mesa&geography=co_montezuma&geography=co_pueblo&percentParam=noPercent&patientClass=e&datasource=va_er&startDate=2Oct2022&medicalGroupingSystem=essencesyndromes&userId=3942&aqtTarget=TimeSeries&geographySystem=region&detector=probrepswitch&removeZeroSeries=true&stratVal=ccddCategory&timeResolution=daily&isPortlet=true&ccddCategory=cdc%20coronavirus-dd%20v1&ccddCategory=cli%20cc%20with%20cli%20dd%20and%20coronavirus%20dd%20v2&graphWidth=673&portletId=315894&dateconfig=2"
    r2 = requests.get(url=URL2, auth=(username, password))

    data2 = r2.json()   
    df2 = pd.DataFrame.from_dict(data2['timeSeriesData'])
    df2.drop(['details', 'altText'], axis=1, inplace=True)


    URL = "https://essence.syndromicsurveillance.org/nssp_essence/api/timeSeries?endDate=" + end_date_new + "&medicalGrouping=injury&percentParam=noPercent&geographySystem=hospitaldhhsregion&datasource=va_hospdreg&detector=probrepswitch&startDate=" + start_date_new + "&timeResolution=daily&medicalGroupingSystem=essencesyndromes&userId=455&aqtTarget=TimeSeries"

    r = requests.get(url=URL, auth=(username, password))

    data = r.json()
    
    df = pd.DataFrame.from_dict(data['timeSeriesData'])
    df.drop(['details', 'altText'], axis=1, inplace=True)
    print(df2)
    
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df2['date'],
        y=df2['count'],
        marker = {'color': "red"}
    ))

    fig.update_layout(
        paper_bgcolor="#1f2630",
        plot_bgcolor="#1f2630",
        font=dict(color="#2cfec1"),
    )


    return fig


if __name__ == '__main__':
    app.run_server(debug=True)


# r = requests.get(url=URL, auth=(username, password))