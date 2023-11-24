"""
run_batches.py

Script python to run n-th batches 

    - When we want to run a parameter space grid in parallel, due to computational limitations,
    it is not possible to grid 100x100 in a single simulation. Therefore, we separate them into batches,
    create lists with the parameters, in this case gex and n_cons_network, and apply the array_split function
    to partition the list into equal parts to pass to the batch.py file. This way it is possible to run countless
    batches to traverse a grid of parameter spaces.

params: 
    - python3 batch.py version batch_number list_Gex list_n_cons_network

Contributors: conrad.bittencourt@gmail.com, fernandodasilvaborges@gmail.com
"""

import os
import numpy as np
import time 

try:
    from __main__ import cfg  # import SimConfig object with params from parent module
except:
    from cfg import cfg

# info resolution of space parameter
resol = 32
n = cfg.cellNumber

# coupling of elements
gex = [round(1e-5*vv, 6) for vv in np.linspace(6,56,resol)]
p = np.linspace(0.0, 0.500,resol)
n_cons_network = (n * p).astype(int)
ncons = np.array_split(n_cons_network, 4)

batch = 1
v = 7
delta_max = 5

# coupling of elements
# gex = [11*1e-5]
# n_cons_network = [vv for vv in range(42,52,2)]
# ncons = np.array_split(n_cons_network, 1)
# batch = 35
# v = 4
# delta_max = 5

for g in gex:
    for conn in ncons:
        os.system(f'ipython batch.py {v} {batch} {g:.7f} ' + f'{conn}')
        time.sleep(140)
        batch+=1

batch = 1
for g in gex:
    for conn in ncons:
        for subbatch in range(len(conn)):
            os.system(f'python3 preprocessing.py {v} {batch} {subbatch} {delta_max}')         
        batch+=1
