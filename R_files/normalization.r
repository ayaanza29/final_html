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



# run_gauss <- function(path, channels = all, output = "/static")
#                        {
#                            fs <- flowCore::read.flowSet(path)
#                            typeof(fs)
#                            gauss_result <- gaussNorm(fs, channels)
#                            return(gauss_result)
#                        }

# all_channels <- c("Time", "SSC-W", "SSC-H", "SSC-A", "FSC-W", "FSC-H", "FSC-A", "SSC-B-W", "SSC-B-H", "SSC-B-A", "BUV395-A", "LIVE DEAD Blue-A",
#                              "BUV563-A", "BUV615-A", "BUV661-A", "BUV805-A", "BV421-A", "eFluor 450-A", "eFluor 506-A", "BV605-A", "BV711-A", "BV785-A",
#                              "FITC-A", "PerCP-Cy5.5-A", "PE-A", "PE-Cy5-A", "PE-Cy5.5-A", "PE-Cy7-A", "APC-A", "AF680-A", "APC-Cy7-A", "AF-A")
# path = "C:/Users/Zuhayr/Documents/GitHub/all_together/static/PeacoQC_results/fcs_files/776 F SP_QC.fcs"
# datr <- run_gauss(path, "BUV395-A")$flowset
# print("helloooooo")
# d2 <- densityplot(~BUV395-A, datr, main="normalized", filter=curv1Filter("BUV395-A"))
# plot(d2, split=c(2,1,2,1), newpage=FALSE)


# library(flowCore)
# data(ITN)
# dat <- transform(ITN, "CD4"=asinh(CD4), "CD3"=asinh(CD3), "CD8"=asinh(CD8))
# lg <- lymphGate(dat, channels=c("CD3", "SSC"), preselection="CD4",scale=1.5)
# dat <- Subset(dat, lg)
# datr <- gaussNorm(dat, "CD8")$flowset
# if(require(flowViz)){
#     d1 <- densityplot(~CD8, dat, main="original", filter=curv1Filter("CD8"))
#     d2 <- densityplot(~CD8, datr, main="normalized", filter=curv1Filter("CD8"))
#     plot(d1, split=c(1,1,2,1))
#     plot(d2, split=c(2,1,2,1), newpage=FALSE)
# }

# all_channels <- c("Time", "SSC-W", "SSC-H", "SSC-A", "FSC-W", "FSC-H", "FSC-A", "SSC-B-W", "SSC-B-H", "SSC-B-A", "BUV395-A", "LIVE DEAD Blue-A",
#                              "BUV563-A", "BUV615-A", "BUV661-A", "BUV805-A", "BV421-A", "eFluor 450-A", "eFluor 506-A", "BV605-A", "BV711-A", "BV785-A",
#                              "FITC-A", "PerCP-Cy5.5-A", "PE-A", "PE-Cy5-A", "PE-Cy5.5-A", "PE-Cy7-A", "APC-A", "AF680-A", "APC-Cy7-A", "AF-A")


# data(ITN)
# dat <- transform(ITN, "CD4"=asinh(CD4), "CD3"=asinh(CD3), "CD8"=asinh(CD8))
# lg <- lymphGate(dat, channels=c("CD3", "SSC"),
# preselection="CD4",scale=1.5)
# dat <- Subset(dat, lg$n2gate)
# datr <- warpSet(dat, "CD8", grouping="GroupID", monwrd=TRUE)
# if(require(flowViz)){
#     d1 <- densityplot(~CD8, dat, main="original", filter=curv1Filter("CD8"))
#     d2 <- densityplot(~CD8, datr, main="normalized", filter=curv1Filter("CD8"))
#     plot(d1, split=c(1,1,2,1))
#     plot(d2, split=c(2,1,2,1), newpage=FALSE)
# }

# library(flowCore)
# data(ITN)
# flowViz::prepanel.xyplot.flowset(ITN, channel.x.name = "CD3", channel.y.name = "CD4")
# dat <- transform(ITN, "CD4"=asinh(CD4), "CD3"=asinh(CD3), "CD8"=asinh(CD8))
# # lg <- lymphGate(dat, channels=c("CD3", "SSC"), preselection="CD4",scale=1.5)
# # dat <- Subset(dat, lg)
# datr <- gaussNorm(dat, "CD8")$flowset
# if(require(flowViz)){
#     d1 <- densityplot(~CD8, dat, main="original")
#     d2 <- densityplot(~CD8, datr, main="normalized")
#     plot(d1, split=c(1,1,2,1))
#     plot(d2, split=c(2,1,2,1), newpage=FALSE)
# }



# library(flowCore)
# fs <- flowCore::read.flowSet("C:/Users/Zuhayr/Documents/GitHub/all_together/static/PeacoQC_results/fcs_files/776 F SP_QC.fcs")
# dat <- transform(fs, "Time"=asinh(Time))
# # lg <- lymphGate(dat, channels=c("CD3", "SSC"), preselection="CD4",scale=1.5)
# # dat <- Subset(dat, lg)
# datr <- gaussNorm(dat, "Time")$flowset
# if(require(flowViz)){
#     d1 <- densityplot(~CD8, dat, main="original")
#     d2 <- densityplot(~CD8, datr, main="normalized")
#     plot(d1, split=c(1,1,2,1))
#     plot(d2, split=c(2,1,2,1), newpage=FALSE)
# }
all_channels <- c("Time", "SSC-W", "SSC-H", "SSC-A", "FSC-W", "FSC-H", "FSC-A", "SSC-B-W", "SSC-B-H", "SSC-B-A", "BUV395-A", "LIVE DEAD Blue-A",
                              "BUV563-A", "BUV615-A", "BUV661-A", "BUV805-A", "BV421-A", "eFluor 450-A", "eFluor 506-A", "BV605-A", "BV711-A", "BV785-A",
                              "FITC-A", "PerCP-Cy5.5-A", "PE-A", "PE-Cy5-A", "PE-Cy5.5-A", "PE-Cy7-A", "APC-A", "AF680-A", "APC-Cy7-A", "AF-A")


fs <- flowCore::read.flowSet("C:/Users/Zuhayr/Documents/GitHub/all_together/static/PeacoQC_results/fcs_files/776 F SP_QC.fcs")
# norm_fun = flowCore::function(fs, all_channels)
flowCore::normalization(parameters = all_channels, normFunction = norm_fun)