import requests
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import dash_auth
from users import VALID_USERNAME_PASSWORD_PAIRS


app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.DARKLY])

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

header = html.Div("NSSP DATA", className="h2 p-2 text-white bg-primary text-center")



app.layout = dbc.Container(
    [
        header,
    ],
)


if __name__ == '__main__':
    app.run_server(debug=True)

# url = "https://essence.syndromicsurveillance.org/nssp_essence/api/timeSeries?endDate=9Feb2021&medicalGrouping=injury&percentParam=noPercent&geographySystem=hospitaldhhsregion&datasource=va_hospdreg&detector=probrepswitch&startDate=11Nov2020&timeResolution=daily&medicalGroupingSystem=essencesyndromes&userId=455&aqtTarget=TimeSeries"

# r = requests.get(url=URL, auth=(username, password))