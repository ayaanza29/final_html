# install.packages("reticulate")
# reticulate::use_python("<redacted>/anaconda3/python.exe")
# # The rest WILL run
# try(reticulate::py_config())
# reticulate::py_config()
# 1+1


library(reticulate)
path_to_python <- "/anaconda/bin/python"
use_python(path_to_python)