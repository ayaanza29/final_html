import pandas as pd
import numpy as np
import harmonypy as hm


meta_data = pd.read_csv("data/meta.tsv.gz", sep = "\t")
vars_use = ['dataset']


data_mat = pd.read_csv("data/pcs.tsv.gz", sep = "\t")
data_mat = np.array(data_mat)

# Run Harmony

ho = hm.run_harmony(data_mat, meta_data, vars_use)

# Write the adjusted PCs to a new file.
res = pd.DataFrame(ho.Z_corr)
res.columns = ['X{}'.format(i + 1) for i in range(res.shape[1])]
res.to_csv("data/adj.tsv.gz", sep = "\t", index = False)
