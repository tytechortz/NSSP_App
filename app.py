import requests
from dash import Dash, html, dcc, Input, Output
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
            html.Div(id='output-container-date-picker-range'),
        ]),
    ],
)

@app.callback(
    Output('output-container-date-picker-range', 'children'),
    Input('my-date-picker-range', 'start_date'),
    Input('my-date-picker-range', 'end_date'))
def update_output(start_date, end_date):
    string_prefix = 'You have selected: '
    if start_date is not None:
        start_date_object = date.fromisoformat(start_date)
        start_date_string = start_date_object.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'Start Date: ' + start_date_string + ' | '
    if end_date is not None:
        end_date_object = date.fromisoformat(end_date)
        end_date_string = end_date_object.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'End Date: ' + end_date_string
    if len(string_prefix) == len('You have selected: '):
        return 'Select a date to see it displayed here'
    else:
        return string_prefix


if __name__ == '__main__':
    app.run_server(debug=True)


# r = requests.get(url=URL, auth=(username, password))