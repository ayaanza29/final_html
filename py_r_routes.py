from flask import Flask, flash, request, redirect, url_for, render_template
import datetime
import os
import subprocess
from werkzeug.utils import secure_filename
#from holo import *
from bokeh.client import pull_session
from bokeh.embed import server_session
from flask import Flask, jsonify, render_template
from flask import send_from_directory
import panel as pn
import rpy2
from rpy2.robjects.vectors import StrVector
import rpy2.robjects.packages as rpackages
import rpy2.robjects
import sys
from rpy2.robjects import pandas2ri as pr
from rpy2 import robjects as ro
import rpy2.robjects as robjects
from rpy2.robjects.conversion import localconverter as lc
#import new_graph_still_image
import time
import logging
logging.basicConfig(level=logging.INFO)
UPLOAD_FOLDER = "C:/Users/Zuhayr/Desktop/Zuhayr_Web_Data"
ALLOWED_EXTENSIONS = {'fcs'}

app = Flask(__name__, static_url_path='/static')
app.config["Upload_Folder"] = UPLOAD_FOLDER

################################################################
#   Java Script Ajax Routes
################################################################

@app.route("/get_peaqo")
def get_peaqo():
    
    fileName = "peaqo.r"
    url = "C:\\Users\\Zuhayr\\Documents\\GitHub\\all_together\\R_files\\peaqo.r"
    with lc(ro.default_converter + pr.converter):
        fileName_c = ro.conversion.py2rpy(fileName)
        url_c = ro.conversion.py2rpy(url)
    ro.globalenv['fileName'] = fileName_c
    ro.globalenv['url'] = url_c

    r = robjects.r
    r.source('R_files\\peaqo.r')

    run_QC = robjects.globalenv['run_QC']
    run_QC('C:\\Users\\Zuhayr\\Documents\\GitHub\\front_end_monochrome\\user_data\\Bob\\Job1\\fcs_files\\776 F SP_QC.fcs', output = 'C:\\Users\\Zuhayr\\Documents\\GitHub\\front_end_monochrome\\user_data\\Bob\\Job1\\')
    return 'C:\\Users\\Zuhayr\\Documents\\GitHub\\front_end_monochrome\\user_data\\Bob\\Job1\\'


@app.route("/new")
def new(): 
    path = request.args.get("path")
    point_list = request.args.get("list_points")
    x_axis = request.args.get("x_axis")
    y_axis = request.args.get("y_axis")

    # if (x_axis != None and y_axis != None):
    #     new_graph_still_image.createBokeh(path, channel1 = x_axis, channel2 = y_axis, points_array = point_list)
    # else:
    #     new_graph_still_image.createBokeh(path, points_array = point_list)

    print("did it update")
    return render_template("new_graph.html")


@app.route("/get_normalize")
def get_normalize():
    channels = request.args.get("channels")

    fileName = "normalize.r"
    url = "C:\\Users\\Zuhayr\\Documents\\GitHub\\all_together\\R_files\\normalize.r"
    with lc(ro.default_converter + pr.converter):
        fileName_c = ro.conversion.py2rpy(fileName)
        url_c = ro.conversion.py2rpy(url)
    ro.globalenv['fileName'] = fileName_c
    ro.globalenv['url'] = url_c

    r = robjects.r
    r.source('R_files\\normalize.r')

    gaussNorm = robjects.globalenv['gaussNorm']
    normalize_peaks_graph = gaussNorm('C:\\Users\\Zuhayr\\Documents\\GitHub\\front_end_monochrome\\user_data\\Bob\\Job1\\fcs_files\\776 F SP_QC.fcs', channels = channels)
    return(normalize_peaks_graph)


@app.route("/get_downsampling")
def get_downsampling():
    path = request.args.get("path")
    channels = request.args.get("channels")

    fileName = "downsample.r"
    url = "C:\\Users\\Zuhayr\\Documents\\GitHub\\all_together\\R_files\\downsample.r"
    with lc(ro.default_converter + pr.converter):
        fileName_c = ro.conversion.py2rpy(fileName)
        url_c = ro.conversion.py2rpy(url)
    ro.globalenv['fileName'] = fileName_c
    ro.globalenv['url'] = url_c

    r = robjects.r
    r.source('R_files\\downsample.r')

    spade_downsample = robjects.globalenv['spade_downsample']
    spade_graph = spade_downsample(path, channels = channels)
    return(spade_graph)


@app.route("/get_clustering_dr")
def get_clustering():
    path = request.args.get("path")
    channels = request.args.get("channels")

    fileName = "clustering_dr.r"
    url = "C:\\Users\\Zuhayr\\Documents\\GitHub\\all_together\\R_files\\clustering_dr.r"
    with lc(ro.default_converter + pr.converter):
        fileName_c = ro.conversion.py2rpy(fileName)
        url_c = ro.conversion.py2rpy(url)
    ro.globalenv['fileName'] = fileName_c
    ro.globalenv['url'] = url_c

    r = robjects.r
    r.source('R_files\\clustering_dr.r')

    spade_downsample = robjects.globalenv['demap']
    spade_graph = spade_downsample(path, channels = channels)
    return(spade_graph)


@app.route("/create_user")
def create_user():
    print("wow")
    email = request.args.get("email")
    password = request.args.get("password")
    print(email)
    print(password)
    return 4
