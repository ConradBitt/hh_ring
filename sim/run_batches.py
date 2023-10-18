"""
run_batches.py

Script python to run n-th batches 

params: 
    - python3 batch.py version batch_number list_Gex list_Iinj

Contributors: conrad.bittencourt@gmail.com, fernandodasilvaborges@gmail.com
"""

import os
import numpy as np
import time

# Simulação: 18065.6s

# coupling of elements
gex = np.round(np.arange(2.,4.3,0.2) * 1e-4, 6)
# external current
# i_ext = np.round(np.linspace(0.7, 0.9, 12), 3)
# currents = np.array_split(i_ext, 4)

n_cons_network = np.arange(65,5,-5)
ncons = np.array_split(n_cons_network,3)

batch = 1
v = 7
delta_max = 5
print(f'Grid: {len(n_cons_network)} x {len(gex)}\n')
for g in gex:
    for conn in ncons:
        os.system(f'python3 batch.py {v} {batch} {g:.7f} ' + f'{conn}')
        for c in range(len(conn)):
            os.system(f'python3 preprocessing.py {v} {batch} {c} {delta_max}')
            print(f'\n\n ** simulation: {batch+c} / {len(n_cons_network) * len(gex)}.... \n\n')
        batch+=1


