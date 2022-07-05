library(methods)
library(umap)
# library(dplyr)
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
library(ggplot2)
library(factoextra)
library(tensorflow)
library(grappolo)
library(parallel)
library(MASS)
library(vizier)
library(RColorBrewer)
library(rlang)
numCores <- detectCores()
set.seed(42)


#####################################################################################################
# Principal Component Analysis
#####################################################################################################

scree_plot <- setRefClass("scree_plot", fields = list(path = "character"), methods = list(
                       graph_scree = function()
                       {
                         #    # x <- read.FCS(file, transformation=FALSE)
                         #    # summary(x)
                            file <- flowCore::read.FCS(path)
                            data <- exprs(file)
                            print(nrow(data))
                            print(ncol(data))
                            results <- prcomp(data, scale = FALSE)
                         #    print(head(results[1:5, 1:5]))
                            #calculate total variance explained by each principal component
                            var_explained = results$sdev^2 / sum(results$sdev^2)

                            #create scree plot
                            scree <- qplot(c(1:33), var_explained) + 
                              geom_line() + 
                              xlab("Principal Component") + 
                              ylab("Variance Explained") +
                              ggtitle("Scree Plot") +
                              ylim(0, 1)

                            print(scree)

                         # res.pca <- princomp(matrix1, cor = FALSE, scores = FALSE)
                         # print(fviz_eig(res.pca))

                       }
                     ))

# scree_instance <- scree_plot(path = "C:/Users/Zuhayr/Documents/GitHub/all_together/static/PeacoQC_results/fcs_files/776 F SP_QC.fcs")
# scree_instance$graph_scree()

graph_scree <- function(path)
                       {
                         #    # x <- read.FCS(file, transformation=FALSE)
                         #    # summary(x)
                            file <- flowCore::read.FCS(path)
                            data <- flowCore::exprs(file)
                            print(nrow(data))
                            print(ncol(data))
                            results <- prcomp(data, scale = FALSE)
                         #    print(head(results[1:5, 1:5]))
                            #calculate total variance explained by each principal component
                            var_explained = results$sdev^2 / sum(results$sdev^2)

                            #create scree plot
                            scree <- qplot(c(1:33), var_explained)+
                              geom_line()+
                              xlab("Principal Component")+
                              ylab("Variance Explained") +
                              ggtitle("Scree Plot") +
                              ylim(0, 1)

                            print(scree)

                         # res.pca <- princomp(matrix1, cor = FALSE, scores = FALSE)
                         # print(fviz_eig(res.pca))

                       }

#####################################################################################################
#  Rtsne - tSNE
#####################################################################################################

# library(Rtsne)

# iris_unique <- unique(iris) # Remove duplicates
# set.seed(42) # Sets seed for reproducibility
# tsne_out <- Rtsne(as.matrix(iris_unique[,1:4])) # Run TSNE
# #plot(tsne_out$Y,col=iris_unique$Species,asp=1) # Plot the result

library(Rtsne)

Rtsne_analysis <- setRefClass("Rtsne_analysis", fields = list(path = "character"), methods = list(
                       Rtsne_func = function()
                       {
                         start_time <- Sys.time()
                         file <- flowCore::read.FCS(path)
                        #  data <- data.frame(matrix(exprs(file)))
                         data <- file[exprs]
                         print(data)
                         data <- data[1:10]
                         print(typeof((data)))
                        #  l <- data.frame(data)
                        #  thing <- typeof(data.frame(matrix(unlist(l), nrow=length(l), byrow=TRUE)))
                         
                         
                         analyzed_data <- Rtsne(data, check_duplicates = FALSE)
                         # print(analyzed_data)
                         graph <- ggplot(analyzed_data, aes(color = "red")) + 
                            geom_point(aes(x=x, y=y)) #, color=col
                        print(graph)
                        end_time <- Sys.time()
                        print(end_time - start_time)
                       }
                     ))

# Rtsne_instance <- Rtsne_analysis(path = "C:/Users/Zuhayr/Documents/GitHub/all_together/static/PeacoQC_results/fcs_files/776 F SP_QC.fcs")
# Rtsne_instance$Rtsne_func()

#####################################################################################################
#  umap - Uniform Manifold Approximation and Projection (UMAP)
#####################################################################################################


# fcsFile <- "C:/Users/Zuhayr/Downloads/776 F SP.fcs"

# x  <- read.FCS(filename = fcsFile, truncate_max_range = FALSE)
# x
# matrixFormat <- exprs(x)
# matrixShort <- head(matrixFormat, -1429593)
# #matrixShort

# umapStuff <- umap(matrixShort, init = "pca")
# umapStuff <- as.data.frame(umapStuff)
# umapStuff_df <- data.frame(umapStuff$layout)
# umapStuff_df <- cbind.data.frame(
#    setNames(as.data.frame(umapStuff_df), c("x", "y")),
#    matrixShort,
#    color = rgb(
#      rescale(matrixShort["SSC-W"]),
#      rescale(matrixShort["SSC-H"]),
#      rescale(matrixShort["FSC-W"]),
#      maxColorValue = 255
#    )
#  )


# thing <- ggplot(umapStuff_df, aes(x = X1, y = X2, color = "red"), inherit.aes = FALSE) + 
#         geom_point() + #
#         scale_color_identity() +
#         new_scale_color() +
#         # shape = NA --> invisible layers +
#         geom_point(aes(color = SSC-W), shape = NA) +
#         scale_color_gradient(low = "black", high = "red") +
#         new_scale_color() +
#         geom_point(aes(color = SSC-H), shape = NA) +
#         scale_color_gradient(low = "black", high = "green") +
#         new_scale_color() +
#         geom_point(aes(color = FSC-W), shape = NA) +
#         scale_color_gradient(low = "black", high = "blue")

# thing
# ggsave("static/images/actual_plot.png")



#####################################################################################################
#  uwot - Uniform Manifold Approximation and Projection (UMAP)
#####################################################################################################

library(uwot)

# embed_img <- function(X, Y, k = 15, ...) {
#   args <- list(...)
#   args$coords <- Y
#   args$x <- X

#   do.call(vizier::embed_plot, args)
# }


uwot_analysis <- setRefClass("scree_plot", fields = list(path = "character"), methods = list(
                       tumap = function() {
                         
                        start_time <- Sys.time()
                         file <- flowCore::read.FCS(path)
                         data <- (Biobase::exprs(file))#[1:10000, ]
                         
                         # print(data)
                         # finished_tumap <- uwot::tumap(data, n_neighbors = 15, verbose = TRUE, init = "spca") # , init = spca
                         finished_tumap <- uwot::umap(data, n_neighbors = 15, min_dist = 0.001, verbose = TRUE, n_threads = 8, target_weight = 0.5, ret_model = TRUE, ret_nn = TRUE)
                         # print(typeof(finished_tumap))
                        #  other <- getElement(finished_tumap, "embedding")
                        #  other <- as.data.frame(other)
                        #  print(other)
                         #print(finished_tumap)
                         finished_tumap <- finished_tumap$embedding
                         #print(finished_tumap)
                         finished_tumap <- as.data.frame(finished_tumap)
                         #print(data)
                         # print(other)
                         # print(finished_tumap)
                         UMAP1 <- unlist(finished_tumap[1])
                         UMAP2 <- unlist(finished_tumap[2])
                        
                        # col_vector <- c("red", "blue", "green", "purple", "brown")
                         graph <- ggplot(finished_tumap, aes(x = UMAP1, y = UMAP2)) + #, color = "red"
                              geom_point(size = 0.5, aes(colour= factor(kmeans(scale(cbind(UMAP1, UMAP2)), centers=8)$cluster))) +
                              scale_colour_brewer('My groups', palette = "Set3") #'Set2'
                              # scale_color_identity() +
                              # new_scale_color() +
                              # shape = NA --> invisible layers +
                              # geom_point(aes(color = SSC-W), shape = NA) +
                              # scale_color_gradient(low = "black", high = "red") +
                              # new_scale_color() +
                              # geom_point(aes(color = SSC-H), shape = NA) +
                              # scale_color_gradient(low = "black", high = "green") +
                              # new_scale_color() +
                              # geom_point(aes(color = FSC-W), shape = NA) +
                              # scale_color_gradient(low = "black", high = "blue")
                        print(graph)
                        ggsave("static/temporary_images/umap_temporary.png", graph)
                         color_col <- data[, "BUV395-A"]
                        #  print(color_col)
                         finished_tumap <- cbind(finished_tumap, color_col)
                         print(finished_tumap[1:10, ])
                         graph2 <- ggplot(finished_tumap, aes(x = UMAP1, y = UMAP2)) + #, color = "red"
                              geom_point(size = 0.5, aes(colour = color_col)) +
                              scale_color_gradient2(low = "blue", mid = "red", high = "white", space = "Lab")
                              # scale_colour_brewer('My groups', palette = "Set3") #'Set2'
                         print(graph2)
                         ggsave("static/temporary_images/umap_temporary_shaded.png", graph2)
                         #print(embed_img(data, finished_tumap, pc_axes = TRUE, equal_axes = TRUE, alpha_scale = 0.5, title = "iris UMAP", cex = 1))
                        end_time <- Sys.time()
                        print(end_time - start_time)
                       }
                     ))

# uwot_instance <- uwot_analysis(path = "C:/Users/Zuhayr/Documents/GitHub/all_together/static/PeacoQC_results/fcs_files/776 F SP_QC.fcs")
# uwot_instance$tumap()

################### Attempt at Paralleliztion
# system.time({
#   results <- mclapply(file, new_function, mc.Cores = numCores)
# })

#####################################################################################################
#  flowSOM - Automatic Clustering
#####################################################################################################

library(FlowSOM)




auto_cluster <- setRefClass("auto_cluster", fields = list(path = "character"), methods = list(
                       automatic_flow = function()
                       {
                          ff <- flowCore::read.FCS(path)
                          # fSOM <- FlowSOM(ff, compensate = FALSE, transform = FALSE, scale = FALSE, colsToUse = c(9, 12, 14:18), xdim = 7, ydim = 7, nClus = 10)
                          fSOM <- FlowSOM(ff, compensate = FALSE, transform = FALSE, scale = FALSE, xdim = 7, ydim = 7, nClus = 10)

                          #p <- PlotStars(fSOM, background.values = fSOM$metaclustering)
                          p <- PlotStars(fSOM)
                          print(p, newpage = FALSE)

                          # FlowSOMmary(fsom = fSOM, plotFile = "FlowSOMmary.pdf")

                          # print(length(GetClusters(fSOM)))
                          meta <- GetMetaclusters(fSOM)
                          print(length(meta))
                          print("bye")
                          return(meta)
                       }
                     ))

# auto_instance <- auto_cluster(path = "C:/Users/Zuhayr/Documents/GitHub/all_together/static/PeacoQC_results/fcs_files/776 F SP_QC.fcs")
# auto_instance$automatic_flow()

#####################################################################################################
#  densvis - tSNE, UMAP, low dimensionality embeddings
#####################################################################################################
library(FlowSOM)
library(densvis)
# library(reticulate)

densvis_analysis <- setRefClass("scree_plot", fields = list(path = "character"), methods = list(
                       automatic_flow = function()
                       {
                          ff <- flowCore::read.FCS(path)
                          # fSOM <- FlowSOM(ff, compensate = FALSE, transform = FALSE, scale = FALSE, colsToUse = c(9, 12, 14:18), xdim = 7, ydim = 7, nClus = 10)
                          fSOM <- FlowSOM(ff, compensate = FALSE, transform = FALSE, scale = FALSE, xdim = 7, ydim = 7, nClus = 10)

                          #p <- PlotStars(fSOM, background.values = fSOM$metaclustering)
                          p <- PlotStars(fSOM)
                          # print(p, newpage = FALSE)

                          # FlowSOMmary(fsom = fSOM, plotFile = "FlowSOMmary.pdf")

                          # print(length(GetClusters(fSOM)))
                          meta <- GetMetaclusters(fSOM)
                          return(meta)
                       },
                       densvis_umap = function()
                       {
                         start_time <- Sys.time()
                         auto_instance <- auto_cluster(path = "C:/Users/Zuhayr/Documents/GitHub/all_together/static/PeacoQC_results/fcs_files/776 F SP_QC.fcs")
                         meta <- automatic_flow()
                         print(head(meta))
                         meta <- meta[1:1000]
                         file <- flowCore::read.FCS(path)
                         data <- Biobase::exprs(file)
                         print("coooooolio")
                         data <- data[1:1000, ]
                         analyzed_data <- densvis::densmap(data)
                         print(length(meta))
                         
                         cbind(analyzed_data, meta)
                         UMAP1 <- analyzed_data[, 1]
                         UMAP2 <- analyzed_data[, 2]
                         print(length(UMAP1))
                         graph1 <- ggplot(as.data.frame(analyzed_data), aes(x = UMAP1, y = UMAP2)) + #, color = "red"
                              geom_point(size = 4, aes(colour= factor(kmeans(scale(cbind(UMAP1, UMAP2)), centers=10)$cluster))) +
                              scale_colour_brewer('My groups', palette = "Set3") #'Set2'
                         print("hi")
                         ggsave("static/temporary_images/k_means_densvis.png", graph1)
                         graph2 <- ggplot(as.data.frame(analyzed_data), aes(x = UMAP1, y = UMAP2)) + #, color = "red"
                              geom_point(size = 4, aes(colour= factor(meta))) +
                              scale_colour_brewer('My groups', palette = "Set3") #'Set2'
                         ggsave("static/temporary_images/flowsom_densvis.png", graph2)
                         print(graph1)
                         print(graph2)
                         end_time <- Sys.time()
                         print(end_time - start_time)
                       },
                       densvis_tsne = function()
                       {
                         start_time <- Sys.time()
                         file <- flowCore::read.FCS(path)
                         data <- Biobase::exprs(file)
                         data <- data[1:1000, ]
                         analyzed_data <- densvis::densne(data)
                         print(analyzed_data)
                         tSNE1 <- analyzed_data[, 1]
                         tSNE2 <- analyzed_data[, 2]
                         graph <- ggplot(as.data.frame(analyzed_data), aes(x = tSNE1, y = tSNE2)) + #, color = "red"
                              geom_point(size = 0.5, aes(colour= factor(kmeans(scale(cbind(tSNE1, tSNE2)), centers=8)$cluster))) +
                              scale_colour_brewer('My groups', palette = "Set3") #'Set2'
                             
                         print(graph)
                         end_time <- Sys.time()
                         print(end_time - start_time)
                       }
                     ))

# densvis_instance <- densvis_analysis(path = "C:/Users/Zuhayr/Documents/GitHub/all_together/static/PeacoQC_results/fcs_files/776 F SP_QC.fcs")
# densvis_instance$densvis_umap()
# densvis_instance$densvis_tsne()

stuff <- function(file) {
  return(file)
}

automatic_flow <- function(path)
                       {
                          ff <- flowCore::read.FCS(path)
                          # fSOM <- FlowSOM(ff, compensate = FALSE, transform = FALSE, scale = FALSE, colsToUse = c(9, 12, 14:18), xdim = 7, ydim = 7, nClus = 10)
                          fSOM <- FlowSOM(ff, compensate = FALSE, transform = FALSE, scale = FALSE, xdim = 7, ydim = 7, nClus = 10)

                          #p <- PlotStars(fSOM, background.values = fSOM$metaclustering)
                          # p <- PlotStars(fSOM)
                          # print(p, newpage = FALSE)

                          # FlowSOMmary(fsom = fSOM, plotFile = "FlowSOMmary.pdf")

                          # print(length(GetClusters(fSOM)))
                          meta <- GetMetaclusters(fSOM)
                          return(meta)
                       }

densvis_umap <- function(file)
                       {
                         start_time <- Sys.time()
                         meta <- automatic_flow(file)
                         print(head(meta))
                         meta <- meta[1:1000]
                         file <- flowCore::read.FCS(file)
                         data <- Biobase::exprs(file)
                         print("coooooolio")
                         data <- data[1:1000, ]
                         analyzed_data <- densvis::densmap(data)
                         print(length(meta))
                         
                         cbind(analyzed_data, meta)
                         UMAP1 <- analyzed_data[, 1]
                         UMAP2 <- analyzed_data[, 2]
                         print(length(UMAP1))
                         graph1 <- ggplot(as.data.frame(analyzed_data), aes(x = UMAP1, y = UMAP2)) + #, color = "red"
                              geom_point(size = 4, aes(colour= factor(kmeans(scale(cbind(UMAP1, UMAP2)), centers=10)$cluster))) +
                              scale_colour_brewer('My groups', palette = "Set3") #'Set2'
                         print("hi")
                         ggsave("static/temporary_images/k_means_densvis.png", graph1)
                         graph2 <- ggplot(as.data.frame(analyzed_data), aes(x = UMAP1, y = UMAP2)) + #, color = "red"
                              geom_point(size = 4, aes(colour= factor(meta))) +
                              scale_colour_brewer('My groups', palette = "Set3") #'Set2'
                         ggsave("static/temporary_images/flowsom_densvis.png", graph2)
                         print(graph1)
                         print(graph2)
                         end_time <- Sys.time()
                         print(end_time - start_time)
                       }

# meta <- automatic_flow("C:/Users/Zuhayr/Documents/GitHub/all_together/static/PeacoQC_results/fcs_files/776 F SP_QC.fcs")
# print(meta)
densvis_umap("C:/Users/Zuhayr/Documents/GitHub/all_together/static/PeacoQC_results/fcs_files/776 F SP_QC.fcs")