library(methods)
library(umap)
library(dplyr)
#library(Seurat)
library(ggplot2)
library(patchwork)
library(flowCore)
library(flowViz)
library(magrittr)
library(ggnewscale)
library(scales)
library(PeacoQC)
library(xfun)
library(flowStats)
library(ggcyto)
#library(flowAssist)


run_norm <- function(path, files_vector){ #channels_vector
    print(path)
    print(files_vector)
    files_vector <- c(as.character(files_vector))
    print(files_vector)
    ff <- flowCore::read.flowSet(files = files_vector, path = path)
    #channel_names_normalize <- c("PE-A", "PerCP-Cy5.5-A", "Alexa Fluor 700-A", "BV750-A", "PE-Cy5.5-A")
    print(ff)
    channel_names_normalize <- flowCore::markernames(ff)
    print(channel_names_normalize)
    channel_names_normalize <- names(channel_names_normalize)
    print(channel_names_normalize)
    # ggcyto(file, aes_string(x = "PE-A")) + geom_joy(aes(y = name)) + facet_null()

    print("failing at transform step")
    transform_logicle <- flowCore::estimateMedianLogicle(ff, channels = channel_names_normalize)
    print("step 1")
    transform_set <- flowCore::transform(ff, transform_logicle)
    print("step 2")
    # norm <- gaussNorm(transform_set, channel_names_normalize, max.lms = 1)
    # flow_sub <- (norm[["flowset"]])
    # print(flow_sub)

    #return "42"
    # flowCore::write.FCS(norm, outdir = )
}






if (1<0){

    ff <- flowCore::read.flowSet(files = c("KTX S361.fcs", "KTX S362.fcs", "KTX S363.fcs", "KTX S365.fcs"), path = "C:/Users/Zuhayr/Desktop/GaussNormSamples")
    # channel_names_normalize <- c("PE-A", "PerCP-Cy5.5-A", "Alexa Fluor 700-A", "BV750-A", "PE-Cy5.5-A")
    channel_names_normalize <- c("PE-A", "BV750-A", "PE-Cy5.5-A", "PerCP-Cy5.5-A") #"Alexa Fluor 700-A"
    # print(markernames(file))
    # ggcyto(file, aes_string(x = "PE-A")) + geom_joy(aes(y = name)) + facet_null()
    transform_logicle <- estimateMedianLogicle(ff, channels = channel_names_normalize)
    transform_set <- transform(ff, transform_logicle)

    norm <- gaussNorm(transform_set, channel_names_normalize, max.lms = 1)
    flow_sub <- (norm[["flowset"]])
    print(flow_sub)
    flow_sub <- flow_sub$"KTX S361.fcs"
    print(flow_sub)
    getChannelMarker(flow_sub, "PE-A")
    ggcyto(flow_sub, aes_string(x = "PE-A")) + geom_joy(aes(y = name)) + facet_null()


    # path <- "C:/Users/Zuhayr/Desktop/GaussNormSamples/"
    # channel_names_normalize <- c("PE-A", "PerCP-Cy5.5-A", "Alexa Fluor 700-A", "BV750-A", "PE-Cy5.5-A")
    # filename_vector <- c("KTX S361.fcs", "KTX S362.fcs", "KTX S363.fcs", "KTX S365.fcs")
    # ff_list <- list()
    # fs <- new("flowSet")
    # for (file in filename_vector){
    #     ff <- flowCore::read.FCS(paste(path, file, sep=""))
    #     transform_logicle <- estimateLogicle(ff, channels = channel_names_normalize)
    #     transform_set <- transform(ff, transform_logicle)
    #     print(transform_set)
    #     fs <- rbind2(fs, transform_set)
    #     transform_set <- 0
    #     transform_logicle <- 0
    #     ff <- 0
    # }

    # fs <- new("flowSet", frames = ff_list)
    # flowCore::read.flowSet()
    # as(ff_list,"flowSet")


    #norm <- gaussNorm(fs, channel_names_normalize)


    # append(ff_list, transform_set)
    #transform_set <- flowAssist::DFtoFF(transform_set)  
    #print(transform_set)
    #colnames(transform_set) <- value
}