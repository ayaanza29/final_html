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
library(xfun)



# ############## General pipeline for preprocessing and quality control with PeacoQC
# fcsFile <- "C:/Users/Zuhayr/Downloads/776 F SP.fcs"
# ############## Read in raw fcs file
# ##############fileName <- system.file("C:/Users/Zuhayr/Downloads/776 F SP.fcs")
# fileName <- "C:/Users/Zuhayr/Downloads/776 F SP.fcs"
# ##############ff <- flowCore::read.FCS(fileName)
# ff <- flowCore::read.FCS("C:/Users/Zuhayr/Downloads/776 F SP.fcs")

# ############## Define channels where the margin events should be removed
# ############## and on which the quality control should be done
# channels <- c(1, 3, 5:14, 18, 21)

# ##############ff <- RemoveMargins(ff=ff, channels=channels, output="frame")

# ############## Compensate and transform the data

# ############## ff <- flowCore::compensate(ff, flowCore::keyword(ff)$SPILL)


# ############## ff <- flowCore::transform(ff,
# ##############                             flowCore::estimateLogicle(ff,
# ##############                             colnames(flowCore::keyword(ff)$SPILL)))


# #Run PeacoQC
# PeacoQC_res <- PeacoQC(ff, channels,
#                         determine_good_cells="all",
#                         save_fcs=TRUE)

stuff <- function() {
    print("hello")
}


# QC_instance <- quality_control(file = "C:/Users/Zuhayr/Downloads/776 F SP.fcs", channels = all)
# QC_instance$run_QC()

run_QC <- function(location_file, output = "/static") #channels
                       {
                           channels <- c(1, 3, 5:14, 18, 21)
                           file <- flowCore::read.FCS(location_file)
                           #file <- format_fcs(path)
                        #    print("cool")
                           PeacoQC_res <- PeacoQC(file, channels=channels, determine_good_cells="all", save_fcs=TRUE, output_directory = output)
                       }
format_fcs <- function(location_file, channels = "")
                       {
                           read_fcs <- flowCore::read.FCS(location_file)
                           read_fcs <<- RemoveMargins(ff=read_fcs, channels=channels, output="frame")
                           #first compensate
                           read_fcs <<- flowCore::compensate(read_fcs, flowCore::keyword(read_fcs)$SPILL)
                           #then transform
                           read_fcs <<- flowCore::transform(read_fcs, flowCore::estimateLogicle(file, colnames(flowCore::keyword(read_fcs)$SPILL)))
                           read_fcs <<- flowCore::transform(read_fcs, flowCore::estimateLinear(file, colnames(flowCore::keyword(read_fcs)$SPILL)))

                           return(read_fcs)
                       }
# location_file <<- "C:\\Users\\Zuhayr\\Documents\\GitHub\\all_together\\static\\PeacoQC_results\\fcs_files\\776 F SP_QC.fcs"
# format_fcs(location_file)

# quality_control <- setRefClass("quality_control", fields = list(file = "character", 
#                        channels = "vector"), methods = list(
#                        format_fcs = function()
#                        {
#                            file <<- flowCore::read.FCS(file)
#                            file <<- RemoveMargins(ff=file, channels=channels, output="frame")
#                            #first compensate
#                            file <<- flowCore::compensate(file, flowCore::keyword(file)$SPILL)
#                            #then transform
#                            #file <- flowCore::transform(file, flowCore::estimateLogicle(file, colnames(flowCore::keyword(file)$SPILL))) #################################################
#                            #file <- flowCore::transform(file, flowCore::estimateLinear(file, colnames(flowCore::keyword(file)$SPILL))) #################################################
#                            #file <- ""

#                        },    
#                        run_QC = function()
#                        {
#                            file <- flowCore::read.FCS(file)
#                            PeacoQC_res <- PeacoQC(file, channels="all", determine_good_cells="all", save_fcs=TRUE)
#                        }
#                      ))

