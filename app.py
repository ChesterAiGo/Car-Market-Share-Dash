from dash import html, dcc, Input, Output
import altair as alt
from vega_datasets import data
import dash_bootstrap_components as dbc
import dash
import plotly.express as px
import pandas as pd
import dash_daq as daq



'''
Define the app and load the data
'''
# Load data here
data = pd.read_csv("./data/data.csv")

# Create the Dash app
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])


'''
Define the frontend
'''

# Define the app layout
app.layout = html.Div([
    html.H1('CarMarketStats - Understand the Current Car Market :)', style={'text-align': 'center', 'border-bottom': '2px dashed', 'padding-bottom': '10px'}),

    html.Div([
        html.Label('Car Market Share Pie Chart (sales in thousands)'),
        dcc.Graph(id='chart', style={'margin-top': '20px'}),
        dcc.RadioItems(
            id='chart-type',
            options=[{'label': 'By Manufacturer (all)', 'value': 'Manufacturer'},
                     {'label': 'By Model (top 10)', 'value': 'Model'}],
            value='Manufacturer',
            labelStyle={'display': 'inline-block', 'margin-right': '50px', 'margin-top': '-30px'},
            style={'text-align': 'center', 'padding-bottom': '-40px', 'margin-bottom': '20px'}
        ),
    ], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center', 'border-bottom': '2px dashed'}),

    html.Div([
        html.Label('Car Sorted by Certain Factor'),
        dcc.Graph(id='bar-chart', style={'margin-top': '20px'}),
        html.Div([
            dcc.Dropdown(
                id='sort-by',
                options=[{'label': 'Price', 'value': 'Price_in_thousands'},
                         {'label': 'Fuel Efficiency', 'value': 'Fuel_efficiency'}],
                value='Price_in_thousands',
                style={'width': '500px', 'justify-content': 'center', 'margin-bottom': '20px'}
            ),
            daq.Slider(
                id='k',
                min=1,
                max=153,
                step=1,
                value=10,
                marks={i: str(i) for i in range(1, 154, 10)},
                size=500
            )
    ])
    ], style={'display': 'flex', 'flex-direction': 'column', 'align-items': 'center',
              'margin-top': '10px', 'border-bottom': '2px dashed', 'padding-bottom': '50px'}),

    html.H5('Copyright @ Chester 2023', style={'text-align': 'center'}),

])

'''
Define the backend
'''

# Piechart
@app.callback(
    dash.dependencies.Output('chart', 'figure'),
    [dash.dependencies.Input('chart-type', 'value')]
)
def update_chart(chart_type):
    if chart_type == 'Manufacturer':
        aggregated = data.groupby('Manufacturer')['Sales_in_thousands'].sum()
        labels = list(aggregated.index)
        values = list(aggregated)
    else:
        top_10_sales = data.sort_values(by='Sales_in_thousands', ascending=False).head(10)
        labels = list(top_10_sales['Manufacturer'] + ': ' + top_10_sales['Model'])
        values = list(top_10_sales['Sales_in_thousands'])

    fig = px.pie(values=values, names=labels)
    return fig

# Barchart
@app.callback(
    dash.dependencies.Output('bar-chart', 'figure'),
    [dash.dependencies.Input('sort-by', 'value'), dash.dependencies.Input('k', 'value')]
)
def update_bar_chart(sort_by, k=10):
    data_sorted = data.sort_values(by=sort_by, ascending=False).head(k)
    data_sorted['agg_name'] = data_sorted['Manufacturer'] + ': ' + data_sorted['Model']
    name_conversion = {"Price_in_thousands": "Price (in thousands USD)", "Fuel_efficiency": "Fuel Efficiency"}
    fig = px.bar(data_sorted, x='agg_name', y=sort_by)
    fig.update_layout(yaxis_title=name_conversion[sort_by])
    return fig


if __name__ == '__main__':
    app.run_server(host='127.0.0.1', port=8050, debug=True)
