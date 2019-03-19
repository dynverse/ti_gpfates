#!/usr/local/bin/python

import dynclipy
task = dynclipy.main()
# task = dynclipy.main(
#   ["--dataset", "/code/example.h5", "--output", "/mnt/output"],
#   "/code/definition.yml"
# )

import pandas as pd
import numpy as np
import json
import sys
from GPfates import GPfates

import time
checkpoints = {}

#   ____________________________________________________________________________
#   Load data                                                               ####
end_n = task["priors"]["end_n"]

p = task["parameters"]

expression = task["expression"]
expression = expression[(expression > p["log_expression_cutoff"]).sum(1) >= p["min_cells_expression_cutoff"]]
if expression.shape[0] == 0:
  raise ValueError("Expression preprocessing filtered out all cells")

checkpoints["method_afterpreproc"] = time.time()

#   ____________________________________________________________________________
#   Infer trajectory                                                        ####
cellinfo = pd.DataFrame({"cell_id":expression.index.tolist()}, index = expression.index.tolist())
m = GPfates.GPfates(cellinfo, expression.T)

# dimensionality reduction
m.dimensionality_reduction()
m.store_dr(dims=range(p["ndim"])) # store the dr in the sample table (m.s), so it can be used in the gplvm

# infer pseudotime
m.infer_pseudotime(s_columns=["bgplvm_" + str(i) for i in range(p["ndim"])]) # use the first two components to infer pseudotime

# model different fates
m.model_fates(C=end_n)

checkpoints["method_aftermethod"] = time.time()

#   ____________________________________________________________________________
#   Process and save output                                                 ####
# pseudotime
pseudotime = m.s.pseudotime.reset_index()
pseudotime.columns = ["cell_id", "pseudotime"]

# dimred
dimred = pd.DataFrame(m.dr_models["bgplvm"].X.mean[:,:].tolist())
dimred["cell_id"] = m.s.pseudotime.index.tolist()

# progressions
end_state_probabilities = pd.DataFrame(m.fate_model.phi)
end_state_probabilities["cell_id"] = m.s.pseudotime.index.tolist()

# save
dataset = dynclipy.wrap_data(cell_ids = m.s.pseudotime.index)
dataset.add_end_state_probabilities(
  end_state_probabilities = end_state_probabilities,
  pseudotime = pseudotime
)
dataset.add_timings(timings = checkpoints)
dataset.write_output(task["output"])
