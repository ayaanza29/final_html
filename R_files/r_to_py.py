from rpy2.robjects.vectors import StrVector
import rpy2.robjects.packages as rpackages
import rpy2.robjects as robjects
import pandas as pd
from rpy2.robjects import pandas2ri as pr
from rpy2 import robjects as ro
import rpy2.robjects.packages as rp
from rpy2.robjects.conversion import localconverter as lc



def get_densmap(url, fcs_path, channels = ""):
    print("hiiiiiiiiiiiiiiiiiiiiiiiiiiii")
    fileName = "clustering_dr.r"
    with lc(ro.default_converter + pr.converter):
        fileName_c = ro.conversion.py2rpy(fileName)
        url_c = ro.conversion.py2rpy(url)
    ro.globalenv['fileName'] = fileName_c
    ro.globalenv['url'] = url_c

    r = robjects.r
    r.source('''R_files/clustering_dr.r''')
    print("whyyyyyyyyyyyyyyyyyyyyyyyyy")
    densvis_umap = robjects.globalenv['densvis_umap']
    print(fcs_path)
    densvis_umap(fcs_path)

    return(url, channels)


def get_denmap(output_path, channels):

    return(output_path)


def get_screeplot(output_path, channels):
    return(output_path)


def get_flowSOM(output_path, channels):
    return(output_path)


def get_uwot(output_path, channels):
    return(output_path)

url = "C:\\Users\\Zuhayr\\Documents\\GitHub\\all_together\\R_files\\clustering_dr.r"
fcs_path = "C:/Users/Zuhayr/Documents/GitHub/all_together/static/PeacoQC_results/fcs_files/776 F SP_QC.fcs"
get_densmap(url, fcs_path)