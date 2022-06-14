# holoviews.py
from logging.config import IDENTIFIER
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from pickle import TRUE
import numpy as np
import holoviews as hv
#from templates.holoviewsApp import dim, opts
import FlowCal
import panel as pn
import holoviews.operation.datashader as hvds
from holoviews.operation.datashader import datashade, shade, dynspread, spread, rasterize
# from holoviews.plotting.bokeh.callbacks import *
from holoviews.plotting.bokeh import *
from holoviews.operation import decimate
from holoviews.selection import link_selections
from bokeh.events import SelectionGeometry
from matplotlib import cm
import pandas as pd
import numpy as np
from numba import *
hv.extension("bokeh")
from scipy.stats import gaussian_kde
import pickle
import os
from sklearn import cluster, datasets
from sklearn.preprocessing import StandardScaler
from bokeh.models import Button, CustomJS, Div
import http
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from bokeh.plotting import *
from bokeh.models import *
from selenium import webdriver
from time import time
from numba.typed import List
from numba import njit
import multiprocessing as mp
import ast
from PIL import Image
import logging
logging.basicConfig(level=logging.INFO)
import chromedriver_autoinstaller
chromedriver_autoinstaller.install()
browser = webdriver.Chrome()



def loop_numba_parallel(point, points_array = "[(-1000000, -1000000), (1000000, -1000000), (-1000000, 1000000), (1000000, 1000000)]"):
    polygon = Polygon(points_array)
    if (polygon.contains(Point(point))):
        return (point[0], point[1])

#### get away from lists
#### multiprocessing
#### flowcore instead of polygon
#### numpy but can only use numpy optimized functions
#### list compressions
#### built in python


#use numba to speed things up
#add boolean indexes to get faster
#@njit
def loop_numba(polygon, tuples):
    x1 = np.array([])
    y1 = np.array([])
    for point in tuples:
        if (polygon.contains(Point(point))):
            x1 = np.append(x1, point[0])
            y1 = np.append(y1, point[1])
    return (x1, y1)
    # print(x1)
    # print(y1)

def remove_points(x1, y1, selected_x1, selected_y1):
    x1_result = []
    y1_result = []
    index = 0
    for x_point in x1:
        y_point = y1[index]
        if (x_point in selected_x1 and y_point in selected_y1):
            x1_result.append(x_point)
            y1_result.append(y_point)
        index += 1
    return (x1_result, y1_result)

### have to define filter gate in r

def createBokeh(fcs_filtered, channel1 = 'FSC-A', channel2 = 'FSC-H', points_array = "[(-1000000, -1000000), (1000000, -1000000), (-1000000, 1000000), (1000000, 1000000)]", output_path = "static/temporary_images/mark1.png"):
    print(points_array)
    if (points_array != "all"):
        points_array = ast.literal_eval(points_array)
    s = FlowCal.io.FCSData(fcs_filtered)
    x1 = s[:, [channel1]] 
    y1 = s[:, [channel2]]
    combined1 = (np.array(x1)).flatten()
    combined2 = (np.array(y1)).flatten()
    print(combined1, combined2)
    combined = pd.DataFrame({channel1: combined1, channel2: combined2})
    combined = combined.to_numpy().astype(np.float64)
    if (points_array != "all"):
        tuples = [tuple(x) for x in combined]
        # new_array = pd.DataFrame()
        polygon = Polygon(points_array)
        ########################################  regular run
        start = time()
        (x1, y1) = loop_numba(polygon, tuples)
        print(f'Time taken to run regular: {time() - start} seconds')

        ########################################  parallel run
        start = time()
        pool = mp.Pool(mp.cpu_count())
        result = pool.starmap(loop_numba_parallel, [(point, points_array) for point in tuples])
        pool.close()
        print(f'Time taken to run parallel: {time() - start} seconds')
        
        
        new_combined = pd.DataFrame({channel1: x1, channel2: y1})
        new_combined = new_combined.to_numpy().astype(np.float64)
    else:
        new_combined = combined
    

    ropts = dict(tools=["box_select"], height=400, width=400)
    new_points = hv.Points(data=new_combined, kdims=[channel1, channel2]).opts(**ropts)#.opts(fill_color='blue', nonselection_color = "gray", fill_alpha=0.5, size=1, frame_width=400, frame_height=400, tools=["lasso_select", "box_select", "poly_select"])
    new_points.redim(x=hv.Dimension('x', range=(0, 5000000)))
    new_points.redim(y=hv.Dimension('y', range=(0, 5000000)))
    rast_graph1 = (rasterize(new_points)).opts(**ropts).opts(cnorm="log")
    hv.save(rast_graph1, output_path)
    im = Image.open("static/temporary_images/mark1.png")
    print(im.size)
    width, height = im.size
    print(width)
    print(height)
   
    start_crop = 270 + ((width - 800)/2)
    im_crop = im.crop((start_crop, 0, start_crop + 430, 385))
    print(im_crop.size)
    im_crop.save("static/temporary_images/mark1.png", quality=95)
    return "static/temporary_images/mark1.png"








