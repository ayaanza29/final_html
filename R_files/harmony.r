library(harmony)
library(flowCore)
library(ggplot2)
library(plotly)
library(gapminder)
library(grappolo)
library(CytoDx)
library(Biobase)


# my_harmony_embeddings <- HarmonyMatrix(my_pca_embeddings, meta_data, "dataset", do_pca=FALSE)

# my_harmony_embeddings <- HarmonyMatrix(
#   my_pca_embeddings, meta_data, c("dataset", "donor", "batch_id"),
#   do_pca = FALSE
# )

file <- "C:/Users/Zuhayr/Documents/GitHub/all_together/data_storage/PeacoQC_results/fcs_files/776 F SP_QC.fcs"

file <- flowCore::read.FCS(file)
data(file)

# file$meta_data[1:5,]

# file$scaled_pcs[1:5,]


# convert_fcs(file)
# fcs2DF(file)
# file <- as.data.frame(file)
# file <- exprs(file)

print(file)

pca_matrix = print(file[1,])
print("hi")
meta_data = colnames(file)
my_harmony_embeddings <- HarmonyMatrix(meta_data, vars_use="dataset",do_pca = TRUE)