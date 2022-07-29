library(spade)
library(methods)
library(umap)
library(dplyr)
library(ggplot2)
library(patchwork)
library(flowCore)
library(magrittr)
library(ggnewscale)
library(scales)
library(PeacoQC)
library(Rtsne)
library(uwot)

spade_downsample <- function(data_file_path, output_dir) {
     # all_channels <- c("Time", "SSC-W", "SSC-H", "SSC-A", "FSC-W", "FSC-H", "FSC-A", "SSC-B-W", "SSC-B-H", "SSC-B-A", "BUV395-A", "LIVE DEAD Blue-A",
     # "BUV563-A", "BUV615-A", "BUV661-A", "BUV805-A", "BV421-A", "eFluor 450-A", "eFluor 506-A", "BV605-A", "BV711-A", "BV785-A",
     # "FITC-A", "PerCP-Cy5.5-A", "PE-A", "PE-Cy5-A", "PE-Cy5.5-A", "PE-Cy7-A", "APC-A", "AF680-A", "APC-Cy7-A", "AF-A")
     # Not run
     ## Load two-parameters sample data included in package
     #data_file_path = paste(installed.packages()["spade","LibPath"],"spade","extdata","SimulatedRawData.fcs",sep=.Platform$file.sep)
     #data_file_path = "C:/Users/Zuhayr/Downloads/776 F SP.fcs"

     # output_dir <- tempdir()
     #
     ## Compute and annotate FCS file with density
     density_file_path <- paste(output_dir,.Platform$file.sep,basename(data_file_path),".density.fcs",sep="")
     SPADE.addDensityToFCS(data_file_path, density_file_path, cols=NULL) #Check which two columns should be used
     #c("FSC-A","SSC-A")

     ## Downsample FCS file based on density
     downsample_file_path <- paste(output_dir,.Platform$file.sep,basename(data_file_path),".density.fcs",sep="")
     SPADE.downsampleFCS(density_file_path, downsample_file_path)
}
spade_build_tree <- function(data_file_path, output_dir)
{
     output_dir <- tempdir()

     cells_file_path <- paste(output_dir,"clusters.fcs",sep="")
     clust_file_path <- paste(output_dir,"clusters.table",sep="")
     graph_file_path <- paste(output_dir,"mst.gml",sep="")
     print(graph_file_path)
     SPADE.FCSToTree(data_file_path, cells_file_path, graph_file_path, clust_file_path, cols=NULL) #cols = NULL selects all channels
     #write_graph(graph_file_path, "C:/Users/Zuhayr/Documents/GitHub/r_background_app/temporary_images/stuff.png", format = "gml")
     #SPADE.FCSToTree(downsample_file_path, cells_file_path, graph_file_path, clust_file_path, cols=c("marker1","marker2"), k = 200, arcsinh_cofactor=NULL, transforms=flowCore::arcsinhTransform(a=0, b=0.2), desired_samples = 50000, comp=TRUE)
}
simple_random_sampling <- function(data_file_path, output_dir, sampling_ceiling = 2)
{
     # output_dir <- tempdir()
     print(data_file_path)
     ff <<- flowCore::read.FCS(data_file_path)
     dsFilt <- sampleFilter(size = sampling_ceiling, filterId="dsFilter")
     result <- filter(ff, dsFilt)
     ff <- Subset(ff, result)
     # print(result)
     # print(ff)
     flowCore::write.FCS(ff, paste(output_dir, "downsampling"))
}



# downsample <- setRefClass("downsample",
#                     fields = list(data_file_path = "character",
#                     channels = "vector"), methods = list(
#                        spade_downsample = function() {
#                             all_channels <- c("Time", "SSC-W", "SSC-H", "SSC-A", "FSC-W", "FSC-H", "FSC-A", "SSC-B-W", "SSC-B-H", "SSC-B-A", "BUV395-A", "LIVE DEAD Blue-A",
#                              "BUV563-A", "BUV615-A", "BUV661-A", "BUV805-A", "BV421-A", "eFluor 450-A", "eFluor 506-A", "BV605-A", "BV711-A", "BV785-A",
#                              "FITC-A", "PerCP-Cy5.5-A", "PE-A", "PE-Cy5-A", "PE-Cy5.5-A", "PE-Cy7-A", "APC-A", "AF680-A", "APC-Cy7-A", "AF-A")
#                             # Not run
#                             ## Load two-parameters sample data included in package
#                             #data_file_path = paste(installed.packages()["spade","LibPath"],"spade","extdata","SimulatedRawData.fcs",sep=.Platform$file.sep)
#                             #data_file_path = "C:/Users/Zuhayr/Downloads/776 F SP.fcs"

#                             output_dir <- tempdir()
#                             #
#                             ## Compute and annotate FCS file with density
#                             density_file_path <- paste(output_dir,.Platform$file.sep,basename(data_file_path),".density.fcs",sep="")
#                             SPADE.addDensityToFCS(data_file_path, density_file_path, cols=NULL) #Check which two columns should be used
#                             #c("FSC-A","SSC-A")

#                             ## Downsample FCS file based on density
#                             downsample_file_path <- paste(output_dir,.Platform$file.sep,basename(data_file_path),".density.fcs",sep="")
#                             SPADE.downsampleFCS(density_file_path, downsample_file_path)
#                        },    
#                        spade_build_tree = function()
#                        {
#                             output_dir <- tempdir()

#                             cells_file_path <- paste(output_dir,"clusters.fcs",sep="")
#                             clust_file_path <- paste(output_dir,"clusters.table",sep="")
#                             graph_file_path <- paste(output_dir,"mst.gml",sep="")
#                             print(graph_file_path)
#                             SPADE.FCSToTree(data_file_path, cells_file_path, graph_file_path, clust_file_path, cols=NULL) #cols = NULL selects all channels
#                             #write_graph(graph_file_path, "C:/Users/Zuhayr/Documents/GitHub/r_background_app/temporary_images/stuff.png", format = "gml")
#                             #SPADE.FCSToTree(downsample_file_path, cells_file_path, graph_file_path, clust_file_path, cols=c("marker1","marker2"), k = 200, arcsinh_cofactor=NULL, transforms=flowCore::arcsinhTransform(a=0, b=0.2), desired_samples = 50000, comp=TRUE)
#                        },
#                        simple_random_sampling = function(sampling_ceiling)
#                        {
#                          output_dir <- tempdir()
                         
#                          ff <<- flowCore::read.FCS(data_file_path)
#                          dsFilt <- sampleFilter(size = sampling_ceiling, filterId="dsFilter")
#                          result <- filter(ff, dsFilt)
#                          ff <- Subset(ff, result)
#                          # print(result)
#                          # print(ff)
#                          write.FCS(ff, "user_data/file.fcs")
#                        }
#                      ))


# downsampling_instance <- downsample(data_file_path = "C:/Users/Zuhayr/Downloads/776 F SP.fcs", channels = c(1, 3, 5:14, 18, 21))
# downsampling_instance$simple_random_sampling(2)

# downsampling_instance$spade_downsample()
# downsampling_instance$spade_build_tree()

######use networkx to visualize
