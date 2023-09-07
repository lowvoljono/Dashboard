import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pathlib
from datetime import datetime, date, timedelta
from xbbg import blp
import os
import hvplot.pandas
import holoviews as hv 
hv.extension('bokeh')
import win32com.client as win32
import streamlit as st
import requests

UStickers =['USGG3M Index','USGG6M Index', 'USGG12M Index', 
            'USGG2YR Index', 'USGG3Y Index', 'USGG5YR Index', 
            'USGG7Y Index','USGG10Y Index','USGG20Y Index','USGG30Y Index']

EUtickers =['GTEUR3M Govt','GTEUR6M Govt', 'GTEUR1Y Govt', 
            'GTEUR2Y Govt', 'GTEUR3Y Govt', 'GTEUR5Y Govt', 
            'GTEUR7Y Govt','GTEUR10Y Govt','GTEUR20Y Govt','GTEUR30Y Govt']

AUtickers =['GTAUD3M Govt', 'GTAUD1Y Govt', 
            'GTAUD2Y Govt', 'GTAUD3Y Govt', 'GTAUD5Y Govt', 
            'GTAUD7Y Govt','GTAUD10Y Govt','GTAUD20Y Govt','GTAUD30Y Govt']

#establish times to pull data

today = datetime.today() - timedelta(days = 3)
three = today - timedelta(days = 6)
week = today - timedelta(days = 10)
month = today - timedelta(days = 33)
formatted_date = today.strftime("%Y-%m-%d")

#US Yield Curve

UStoday = blp.bdh(tickers = UStickers, flds=['PX_LAST'], start_date='2022-01-01', end_date=today).tail(1)
USthree = blp.bdh(tickers = UStickers, flds=['PX_LAST'], start_date='2022-01-01', end_date=three).tail(1)
USweek = blp.bdh(tickers = UStickers, flds=['PX_LAST'], start_date='2022-01-01', end_date=week).tail(1)
USmonth = blp.bdh(tickers = UStickers, flds=['PX_LAST'], start_date='2022-01-01', end_date=month).tail(1)

UScurve = pd.concat([UStoday, USthree, USweek, USmonth], axis = 0)
UScurve.columns = UScurve.columns.droplevel(1) 
UScurve = UScurve.rename(
    index = {UScurve.index[0]: 'Today', UScurve.index[1]: 'Three Days', UScurve.index[2]: 'Week', UScurve.index[3]: 'Month'}) 
UScurve = UScurve.rename(columns={
    UScurve.columns[0]: '3m',
    UScurve.columns[1]: '6m',
    UScurve.columns[2]: '12m',
    UScurve.columns[3]: '2y',
    UScurve.columns[4]: '3y',
    UScurve.columns[5]: '5y',
    UScurve.columns[6]: '7y',
    UScurve.columns[7]: '10y',
    UScurve.columns[8]: '20y',
    UScurve.columns[9]: '30y'})

UScurvechart = UScurve.transpose()


USchart = UScurvechart.hvplot.line(
    xlabel = 'Maturity',
    ylabel = 'Yield',
    title = 'US Yield Curve ' + str(date.today()),
    grid=True, width = 900, height = 500, fontsize = {'title': '15pt'},
    line_dash = ['solid', 'dashed', 'dashed', 'dashed'],
    color = ["#22A6A3","#595959","#A5A5A5","#D9D9D9"],
    legend = ('top_right')
)

US_chart_file_path = f"C:/Users/Admin/Documents/Automation/yc_charts/US_Yield_Curve_{formatted_date}.png"

US_curve_source = ColumnDataSource(data=UScurvechart)
US_chart = figure(x_axis_label='Maturity', y_axis_label='Yield', title='US Yield Curve ' + str(date.today()),
                  width=900, height=500, tools='', x_range=UScurvechart.index.tolist())
US_chart.line(x='index', y='Today', line_width=2, source=US_curve_source, legend_label='Today', line_color="#22A6A3")
US_chart.line(x='index', y='Three Days', line_width=2, source=US_curve_source, legend_label='Three Days', line_dash='dashed', line_color="#595959")
US_chart.line(x='index', y='Week', line_width=2, source=US_curve_source, legend_label='Week', line_dash='dashed', line_color="#A5A5A5")
US_chart.line(x='index', y='Month', line_width=2, source=US_curve_source, legend_label='Month', line_dash='dashed', line_color="#D9D9D9")
US_chart.legend.location = "top_right"

# Display the chart using Streamlit's bokeh_chart function
st.bokeh_chart(US_chart)