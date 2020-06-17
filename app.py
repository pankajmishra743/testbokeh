from flask import Flask, jsonify, render_template, request, flash, redirect
import numpy as np

import xlrd
import json
import random
import pandas as pd
import seaborn as sns
import geopandas as gpd
import matplotlib.pyplot as plt

from bokeh.io import curdoc, output_notebook
from bokeh.models import Slider, HoverTool
from bokeh.layouts import widgetbox, row, column
from bokeh.io import output_notebook, show, output_file
from bokeh.plotting import figure
from bokeh.models import GeoJSONDataSource, LinearColorMapper, ColorBar
from bokeh.palettes import brewer
from bokeh.embed import components



app = Flask(__name__)

# Load the MapWithData Data Set
sns.set_style('dark')
with open('YearWiseJsonFiles/2017_data_with_map.json') as f_2017:
    data_2017 = json.load(f_2017)
with open('YearWiseJsonFiles/2018_data_with_map.json') as f_2018:
    data_2018 = json.load(f_2018)
with open('YearWiseJsonFiles/2019_data_with_map.json') as f_2019:
    data_2019 = json.load(f_2019)

Years = ['2017', '2018', '2019']

def getMMR(data, current_year):
    # Create the plot
    #Input GeoJSON source that contains features for plotting.
    geosource = GeoJSONDataSource(geojson = json.dumps(data))
    #Define a sequential multi-hue color palette.
    palette = brewer['YlGnBu'][8]
    #Reverse color order so that dark blue is highest value.
    palette = palette[::-1]
    #Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors. Input nan_color.
    color_mapper = LinearColorMapper(palette = palette, low = 0, high = 400, nan_color = '#d9d9d9')
    #Define custom tick labels for color bar.
    tick_labels = {'0': '0', '50': '50', '100':'100', '150':'150', '200':'200', '250':'250', '300':'300', '350':'350', '400':'400'}
    #Add hover tool
    hover_MMR = HoverTool(tooltips = [ ('Year','@Year'),('State/UT','@State'),('Maternal Mortality Rate', '@MMR')])
    #Create color bar. 
    color_bar = ColorBar(color_mapper=color_mapper, label_standoff=7,width = 400, height = 20, border_line_color=None,location = (0,0), orientation = 'horizontal', major_label_overrides = tick_labels)
    #Create figure object for MMR.
    p_MMR = figure(title = 'Maternal Mortality Rate - ' + str(current_year), plot_height = 600 , plot_width = 450, toolbar_location = None, tools = [hover_MMR])
    p_MMR.xgrid.grid_line_color = None
    p_MMR.ygrid.grid_line_color = None
    p_MMR.axis.visible = False
    #Add patch renderer to figure. 
    p_MMR.patches('xs','ys', source = geosource,fill_color = {'field' :'MMR', 'transform' : color_mapper}, line_color = 'black', line_width = 0.25, fill_alpha = 1)
    #Specify layout
    p_MMR.add_layout(color_bar, 'below')
    curdoc().add_root(p_MMR)
    return(p_MMR)
    
def getIMR(data, current_year):
    # Create the plot
    #Input GeoJSON source that contains features for plotting.
    geosource = GeoJSONDataSource(geojson = json.dumps(data))
    #Define a sequential multi-hue color palette.
    palette = brewer['YlGnBu'][8]
    #Reverse color order so that dark blue is highest value.
    palette = palette[::-1]
    #Instantiate LinearColorMapper that linearly maps numbers in a range, into a sequence of colors. Input nan_color.
    color_mapper = LinearColorMapper(palette = palette, low = 0, high = 56, nan_color = '#d9d9d9')
    #Define custom tick labels for color bar.
    tick_labels = {'0': '0', '7': '7', '14':'14', '21':'21', '28':'28', '35':'35', '42':'42', '49':'49', '56':'56'}
    #Add hover tool
    hover_IMR = HoverTool(tooltips = [ ('Year','@Year'),('State/UT','@State'),('Infant Mortality Rate', '@IMR')])
    #Create color bar. 
    color_bar = ColorBar(color_mapper=color_mapper, label_standoff=7,width = 400, height = 20, border_line_color=None,location = (0,0), orientation = 'horizontal', major_label_overrides = tick_labels)
    #Create figure object for IMR.
    p_IMR = figure(title = 'Infant Mortality Rate - ' + str(current_year), plot_height = 600 , plot_width = 450, toolbar_location = None, tools = [hover_IMR])
    p_IMR.xgrid.grid_line_color = None
    p_IMR.ygrid.grid_line_color = None
    p_IMR.axis.visible = False
    #Add patch renderer to figure. 
    p_IMR.patches('xs','ys', source = geosource,fill_color = {'field' :'IMR', 'transform' : color_mapper}, line_color = 'black', line_width = 0.25, fill_alpha = 1)
    #Specify layout
    p_IMR.add_layout(color_bar, 'below')
    curdoc().add_root(p_IMR)
    return(p_IMR)



# Index page
@app.route('/')
def index():
    data = ""
    # Determine the selected feature
    current_year = request.args.get("Year")
    if ((current_year == "2017") or (current_year == None)) :
        current_year = 2017
        data = data_2017
    elif current_year == "2018" :
        current_year = 2018
        data = data_2018
    elif current_year == "2019" :
        current_year = 2019
        data = data_2019
   
    # Embed plot into HTML via Flask Render
    script, div = components(getMMR(data, current_year))
    script1, div1 = components(getIMR(data, current_year))
    return render_template("myindex.html", script=script, div=div, script1=script1, div1=div1,
        Years=Years,  current_year=current_year)

# With debug=True, Flask server will auto-reload 
# when there are code changes
if __name__ == '__main__':
    app.run(port=5000, debug=True)