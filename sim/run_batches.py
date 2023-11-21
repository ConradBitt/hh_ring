"""
run_batches.py

Script python to run n-th batches 

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
# info networks
n = cfg.cellNumber


# coupling of elements
gex = [round(1e-5*vv, 6) for vv in range(6,56,1)]
p = np.arange(0.01, 0.502,0.01)
n_cons_network = (n * p).astype(int)
ncons = np.array_split(n_cons_network, 10)

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
        time.sleep(80)
        batch+=1

batch = 1
for g in gex:
    for conn in ncons:
        for subbatch in range(len(conn)):
            os.system(f'python3 preprocessing.py {v} {batch} {subbatch} {delta_max}')         
        batch+=1
