from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.io import output_notebook, push_notebook
import streamlit.bokeh_support as st_bokeh

# US Yield Curve Chart
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
