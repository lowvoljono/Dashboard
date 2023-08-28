import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
from xbbg import blp
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pathlib
from datetime import datetime, date, timedelta
import hvplot.pandas
import holoviews as hv 
hv.extension('bokeh')
import win32com.client as win32
import streamlit as st
import requests

app = dash.Dash(__name__)

UStickers = ['USGG3M Index', 'USGG6M Index', 'USGG12M Index',
            'USGG2YR Index', 'USGG3Y Index', 'USGG5YR Index',
            'USGG7Y Index', 'USGG10Y Index', 'USGG20Y Index', 'USGG30Y Index']

app.layout = html.Div([
    html.H1("US Yield Curve"),
    dcc.Graph(id='us-yield-curve-graph'),
])

@app.callback(
    Output('us-yield-curve-graph', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_yield_curve(n):
    today = datetime.date.today()
    start_date = (today - datetime.timedelta(days=33)).strftime("%Y-%m-%d")

    UStoday = blp.bdh(tickers=UStickers, flds=['PX_LAST'], start_date=start_date, end_date=today).tail(1)
    UScurvechart = UStoday.transpose()

    figure = {
        'data': [
            {'x': UScurvechart.index, 'y': UScurvechart.iloc[0], 'type': 'line', 'name': 'Today'},
        ],
        'layout': {
            'title': 'US Yield Curve ' + str(datetime.date.today()),
            'xaxis': {'title': 'Maturity'},
            'yaxis': {'title': 'Yield'},
            'grid': True,
            'width': 900,
            'height': 500,
            'font': {'size': 15},
            'line_dash': ['solid'],
        }
    }

    return figure

if __name__ == '__main__':
    app.run_server(debug=True)
