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









quality_control <- setRefClass("quality_control", fields = list(file = "character", 
                       channels = "vector"), methods = list(
                       format_fcs = function()
                       {
                           file <- flowCore::read.FCS(file)
                           file <- RemoveMargins(ff=file, channels=channels, output="frame")
                           #first compensate
                           file <- flowCore::compensate(file, flowCore::keyword(file)$SPILL)
                           #then transform
                           #file <- flowCore::transform(file, flowCore::estimateLogicle(file, colnames(flowCore::keyword(file)$SPILL))) #################################################
                           #file <- flowCore::transform(file, flowCore::estimateLinear(file, colnames(flowCore::keyword(file)$SPILL))) #################################################
                           #file <- ""

                        # Read files
                        # fs <- flowCore::read.FCS(file)
                        # print(length(fs))
                        # print(length(col(fs)))
                        # fs.spill = spillover(fs,
                        # unstained = length(fs),   # unstained is the last file
                        # stain_match = "ordered") 
                        # round(fs.spill, 3)
                        # matplot(asinh(t(fsApply(fs, each_col, median))/150), typ = "l", lwd = rep(c(2, 5), times = c(14,1)), xlab = "Channels", ylab = "asinh(intensity/150)")
                       },    
                       run_QC = function()
                       {
                           file <- flowCore::read.FCS(file)
                           PeacoQC_res <- PeacoQC(file, channels="all", determine_good_cells="all", save_fcs=TRUE)
                       }
                     ))

