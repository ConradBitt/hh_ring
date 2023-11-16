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
# gex = [19*1e-5]
# n_cons_network = [vv for vv in range(22,42,2)]
# ncons = np.array_split(n_cons_network, 2)


# batch = 81
# v = 1

# coupling of elements
gex = [20*1e-5]
n_cons_network = [vv for vv in range(22,32,2)]
ncons = np.array_split(n_cons_network, 1)


batch = 87
v = 1
delta_max = 5

for g in gex:
    for conn in ncons:
        os.system(f'ipython batch.py {v} {batch} {g:.7f} ' + f'{conn}')
        time.sleep(60) # sleep by 1 minute 20 seconds
        batch+=1