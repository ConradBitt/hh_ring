import pickle
import numpy as np
import os
import metrics

n_batchs = 128
n_subbatchs = 7
gex = np.zeros(n_batchs * n_subbatchs)
amp = np.zeros(n_batchs * n_subbatchs)
r = np.zeros(n_batchs * n_subbatchs)
neighbours = np.zeros(n_batchs * n_subbatchs)

mean_LOP = np.zeros(n_batchs * n_subbatchs)
mean_GOP = np.zeros(n_batchs * n_subbatchs)

mean_cv = np.zeros(n_batchs * n_subbatchs)
mean_freq = np.zeros(n_batchs * n_subbatchs)

thresholds = [0.80, 0.90, 1.]
coerentes = {}

for thr in thresholds:
    coerentes[thr] = np.zeros(n_batchs * n_subbatchs)

i = 0
v = 5
for batch in range(1,n_batchs + 1):
    for subbatch in range(0, n_subbatchs):
        b = 'batch'+str(batch).zfill(4)
        file = f'../data/v{v}_{b}/v{v}_{b}_0_{subbatch}_data.pkl'

        with open(file, 'rb') as f:
            data = pickle.load(f)
        gex[i] = data['simConfig']['gex']
        amp[i] = data['simConfig']['IClamp0']['amp']
        neighbours[i] = data['simConfig']['n_neighbors']
        r[i] = data['r']

        mean_GOP[i] = data['GOP'].mean()
        mean_LOP[i] = data['LOP_delta'][5].mean(axis=1).mean()

        Count_LOP_Under_Trh = data['Count_LOP_Under_Trh']
        
        for key, value in Count_LOP_Under_Trh.items():
            coerentes[key][i] = value

        
        mean_freq[i] = data['freq_bar']
        mean_cv[i] = np.mean(data['CV'])
        print(f"finish: {gex[i]}S/cm², {amp[i]}nA, {neighbours[i]} conns por neuron, {data['freq_bar']:.2f}Hz \n ~~ {file}\n")
        i += 1
        del data
        

dados = {
    'gex':gex,
    'amp':amp,
    'r':r,
    'neighbours':neighbours,
    'mean_LOP':mean_LOP,
    'mean_GOP':mean_GOP,
    'mean_cv':mean_cv,
    'mean_freq':mean_freq,
    'thresholds':thresholds,
    'Coerentes':coerentes,
}

print(f'~ Dump pickle file: \n')
with open(f'../data/data_read_batches_v{v}_sample1s.pkl', 'wb') as handle:
    pickle.dump(dados, handle, protocol=pickle.HIGHEST_PROTOCOL)