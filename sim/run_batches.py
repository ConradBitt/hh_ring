"""
run_batches.py

Script python to run n-th batches 

params: 
    - python3 batch.py version batch_number list_Gex list_Iinj

Contributors: conrad.bittencourt@gmail.com, fernandodasilvaborges@gmail.com
"""

import os
import numpy as np
import datetime
import json

# Simulação: 18065.6s

time_stamps = {
    'batches':{},
    'subbatches':{},
}
with open('../data/time_stamps.json', 'w') as fp:
    json.dump(time_stamps, fp)

gex = np.round(np.arange(1.,5.5,0.05) * 1e-4, 6)

# Conns per neuron
n_cons_per_neuron = np.arange(100,10,-1)
ncons = np.array_split(n_cons_per_neuron,15)
batch = 1
v = 8
print(f'Grid: {len(n_cons_per_neuron)} x {len(gex)}\n\n')

for g in gex:
    for conn in ncons:
        os.system(f'python3 batch.py 3 {batch} {g:.5f} ' + f'{conn}')
        for c in range(len(conn)):
            isubbatch = datetime.datetime.now()
            os.system(f'python3 preprocessing.py {v} {batch} {c}')  
            fsubbatch = datetime.datetime.now()

            time_stamps['subbatches'][batch+c] = (fsubbatch - isubbatch).total_seconds()
            with open('../data/time_stamps.json', 'w') as fp:
                json.dump(time_stamps, fp)

            print(f'> Simulation: {batch} / {(len(n_cons_per_neuron) * len(gex)) / len(conn)}')
        batch+=1