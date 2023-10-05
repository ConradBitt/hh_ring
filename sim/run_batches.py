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
gex = np.round(np.arange(2.2,6.2,0.2) * 1e-4, 6)
# external current
# i_ext = np.round(np.linspace(0.7, 0.9, 12), 3)
# currents = np.array_split(i_ext, 4)

n_cons_network = np.arange(25, 45,1)
ncons = np.array_split(n_cons_network, 5)

batch = 1
v = 7
delta_max = 5
print(f'Grid: {len(n_cons_network)} x {len(gex)}\n\n')
inicio = time.time()
for g in gex:
    inicio_batch = time.time()
    for conn in ncons:
        inicio_subbatch = time.time()
        # os.system(f'python3 batch.py {v} {batch} {g:.7f} ' + f'{conn}')
        for c in range(len(conn)):
            os.system(f'python3 preprocessing.py {v} {batch} {c} {delta_max}')


        # print(f'python3 batch.py {v} {batch} {g:.7f} ' + f'{conn}')
        batch+=1
        fim_subbatch = time.time()
        print(f'Tempo batch:\t{fim_subbatch - inicio_subbatch:.3f}s')

    fim_batch = time.time()
    print(f'Tempo batch:\t{fim_batch - inicio_batch:.3f}s')
final = time.time()

print(f'Simulação: {final - inicio}')
        


