import os
import pickle
import numpy as np

v = 3
n_batchs = 128
n_subbatchs = 8

space_param = {
        'gex': np.zeros(n_batchs * n_subbatchs),
        'amp': np.zeros(n_batchs * n_subbatchs),
        'neighbours': np.zeros(n_batchs * n_subbatchs),
        'mean_GOP': np.zeros(n_batchs * n_subbatchs),
        'mean_LOP': np.zeros(n_batchs * n_subbatchs),
        'mean_freq': np.zeros(n_batchs * n_subbatchs),
        'mean_cv': np.zeros(n_batchs * n_subbatchs),
}

# Cria dicionário 
with open(f'../data/space_param_V{v}.pkl', 'wb') as handle:
    pickle.dump(space_param, handle, protocol=pickle.HIGHEST_PROTOCOL)
i = 0
for batch in range(1,n_batchs + 1):
    for subbatch in range(0, n_subbatchs):
        os.system(f'python3 readpickle.py {v} {batch} {subbatch} {i}')
        i+=1