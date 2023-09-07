import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pathlib
from datetime import datetime, date, timedelta
from xbbg import blp
import os
import hvplot.pandas
import holoviews as hv 
from holoviews import opts
hv.extension('bokeh')
import win32com.client as win32
from sklearn.preprocessing import StandardScaler
from scipy.stats.mstats import winsorize
from bokeh.palettes import Category10

name_list = ['S&P 500','S&P Small Cap', 'S&P Mid 400 Cap', 'Russell 3000 Large Cap',
 'Nikkei 225', 'MSCI Japan Large Index',
 ' MSCI Japan Mid index',
  'MSCI Japan Small Index', 'MSCI Europe',  'MSCI European Large Cap Index',
 'MSCI European Mid Cap Index', 
 'MSCI European Small Cap Index', 'FTSE100', 

  'S&P/ASX 200',
 'S&P/ASX Midcap 50 Index','S&P/ASX Small Ordinaries Index' ,'MSCI Australia Minimum Volatility Index' ,
 'MSCI Australia Value Index', 'MSCI Australia Growth Index',
 'MSCI Australia Quality' ,'MSCI Australia Small Cap'  ,

'MSCI Emerging Markets index' ,'MSCI AC Asia Pacific Excluding Japan Index', 'ShangHai Composite' ,

 'MSCI ACWI Index' ,'MSCI World Quality net Total Return USD Index' ,'MSCI World Value Index (USD)' ,'MSCI World Growth Index', 
 'MSCI World Minimum Volatility Index (USD)', 
 'MSCI World Momentum Total Return Index (USD)', 'MSCI World Large Cap Index', 
 'MSCI World Mid Cap Index', 'MSCI World Small Cap Index', 'FTSE All-World EX US Index (USD)', 'MSCI EAFE Index', 'Global ex-Aus Agriculture AUD']


data = ['SPX Index', 'sml index', 'mid Index','ray Index', 'NKY Index', 'MXJPLC Index', 
'MXJPMC Index', 'MXJPSC Index', 'MXEU Index', 'mxeulc index','mxeumc index','mxeusc index', 'ukx index',

 'ASa51 Index' , 'asa34 index' , 'asa38 index','M5AUVOA Index', 'MXAU000V Index' , 'MXAU000G Index', 'm1auqu Index','MXAUSC Index',

'mxef index','MXAPJ Index','shcomp index',

'mxwd index', 'm1woqu index','mxwo000v Index','MXWo000G Index','M1WOMVOL INDEX','M1WOMOM Index', 				
'mxwolc index', 'mxwomc index', 'mxwosc index','FTAW02 Index', 'MXEA Index','NQXAUHAN Index']


def check_what_isnt_there(data, output_df):
    # Convert the lists to sets for faster membership checking
    set1 = set(output_df)
    set2 = set(data)

    names_in_list1_not_in_list2 = set1.difference(set2)
    names_in_list2_not_in_list1 = set2.difference(set1)

    names_in_list1_not_in_list2 = list(names_in_list1_not_in_list2)
    names_in_list2_not_in_list1 = list(names_in_list2_not_in_list1)

    return names_in_list2_not_in_list1

def px_to_10y_sales(df):
    for country in df.columns.get_level_values(0).unique():
        country_df = df[country] # accessing data for particular country column
        result = country_df['px_last'] / country_df['trail_12m_sales_per_sh'].rolling(window=120).mean()
        df[(country, 'prices_to_10y_sales')] = result
    return df

def winsorize(clean):
    capped_dfs = []

    for col in clean.columns:
        x95 = np.percentile(clean[col], 95)
        x5 = np.percentile(clean[col], 5)
        
        capped_values = []
        for value in clean[col]:
            if value > x95:
                capped_values.append(x95)
            elif value < x5:
                capped_values.append(x5)
            else:
                capped_values.append(value)
        
        capped_series = pd.Series(capped_values, index=clean.index, name=col)
        capped_dfs.append(capped_series) # makes a list of df's
    capped_df = pd.concat(capped_dfs, axis=1) # stretches the list of df's into a wide DF
    return capped_df

def agg_z(df):
    z = (df-df.mean())/df.std()
    agg_z = z.groupby(level=0, axis=1).mean() # groups by aggregating level 1
    return agg_z

    # z = StandardScaler().fit_transform(df)
    # z = pd.DataFrame(z, columns=df.columns, index = df.index)
    # agg_z = z.groupby(level=0, axis=1).mean() # groups by aggregating level 1
    #return agg_z



def df_construct(z_scored_winsorized_df):
    result_dfs = {} # we're making a dictionairy full of df's

    for col in z_scored_winsorized_df.columns:
        average = z_scored_winsorized_df[col].mean()
        stddev = z_scored_winsorized_df[col].std()

        new_df = pd.DataFrame({
            'Value': z_scored_winsorized_df[col],
            'Average': average,
            '+1 STD': average + stddev,
            '+2 STD': average + stddev*2,
            '-1 STD': average - stddev,
            '-2 STD': average - stddev*2
        })
        new_df = new_df.dropna(axis=0)
        result_dfs[col] = new_df
    
    return result_dfs


def graphing(dfs_dict):
    graphs = {}

    # Iterate through the DataFrames in the result_dfs dictionary
    for key, df in dfs_dict.items():
        graph = df.hvplot.line(
            x='index',  # Assuming the index represents time
            y=['Value', 'Average', '+1 STD', '+2 STD','-1 STD', '-2 STD'],
            xlabel='Time',
            ylabel='Z-score',
            title=f'Z-Score Aggregated Valuation: {key} - {date.today()}',
            grid=True,
            width=900,
            height=500,
            fontsize={'title': '15pt'},
            line_dash=['solid', 'solid', 'dashed', 'dashed', 'dashed', 'dashed'],
            color=["#22A6A3", "#595959", "#A5A5A5","#A5A5A5","#A5A5A5","#A5A5A5"],
            legend=('bottom')
        )

        # Store the graph in the graphs dictionary
        graphs[key] = graph
    return graphs