library(methods)
library(umap)
library(dplyr)
#library(Seurat)
library(ggplot2)
library(patchwork)
library(flowCore)
#library(flowViz)
library(magrittr)
library(ggnewscale)
library(scales)
library(PeacoQC)

# source("final_format/autonomous_gating.r")
source("R_files/QC.r")
# source("final_format/downsampling.r")
# source("final_format/batch_effect.r")
# source("final_format/dimensionality_reduction.r")
# source("final_format/clustering.r")
# source("final_format/data_visualizations.r")



# path_to_fcs <- readline(prompt = "Enter path to fcs file: ")
# path_to_channels <- readline(prompt = "Enter channels vector: ")
# path_to_channels
# while (file_ext(path_to_fcs) != "fcs" || all(path_to_channels != floor(path_to_channels))) {
#     path_to_fcs <- readline(prompt = "Try again, Please enter a valid path to the fcs file: ")
#     #path_to_channels <- readline(prompt = "Enter channels vector: ")
# }
# # QC_instance <- quality_control(file = path_to_fcs, channels = path_to_channels)
# # QC_instance$run_QC()




QC_instance <- quality_control(file = "C:/Users/Zuhayr/Downloads/776 F SP.fcs", channels = c(1, 3, 5:14, 18, 21))
#QC_instance$format_fcs()
QC_instance$run_QC()


# downsampling_instance <- downsampling(file = "C:/Users/Zuhayr/Downloads/776 F SP.fcs", channels = c(1, 3, 5:14, 18, 21))
# downsampling_instance$spade_downsample()
# downsampling_instance$spade_build_tree()





