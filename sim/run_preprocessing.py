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

# coupling of elements
gex =  [round(1e-5*vv, 6) for vv in range(6,36,1)]
n_cons_network = [vv for vv in range(2,62,2)]
ncons = np.array_split(n_cons_network, 6)

batch = 1
v = 3
delta_max = 5

for g in gex:
    for conn in ncons:
        for subbatch in range(len(conn)):
            os.system(f'python3 preprocessing.py {v} {batch} {subbatch} {delta_max}')
                    
        batch+=1
