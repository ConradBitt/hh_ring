import pickle
import numpy as np
import os
import metrics2

n_batchs = 36
n_subbatchs = 4
gex = np.zeros(n_batchs * n_subbatchs)
amp = np.zeros(n_batchs * n_subbatchs)
r = np.zeros(n_batchs * n_subbatchs)
neighbours = np.zeros(n_batchs * n_subbatchs)

mean_LOP = np.zeros(n_batchs * n_subbatchs)
mean_GOP = np.zeros(n_batchs * n_subbatchs)

mean_cv = np.zeros(n_batchs * n_subbatchs)
mean_freq = np.zeros(n_batchs * n_subbatchs)

thresholds = np.arange(0.7, 0.99,0.05)

Coerentes75 = np.zeros(n_batchs * n_subbatchs)
Coerentes80 = np.zeros(n_batchs * n_subbatchs)
Coerentes85 = np.zeros(n_batchs * n_subbatchs)
Coerentes90 = np.zeros(n_batchs * n_subbatchs)
Coerentes95 = np.zeros(n_batchs * n_subbatchs)

i = 0
v = 7
for batch in range(1,n_batchs + 1):
    for subbatch in range(0, n_subbatchs):
        b = 'batch'+str(batch).zfill(4)
        file = f'../data_non_otm/v7_{b}/v7_{b}_0_{subbatch}_data.pkl'

        with open(file, 'rb') as f:
            data = pickle.load(f)
        gex[i] = data['simConfig']['gex']
        amp[i] = data['simConfig']['IClamp0']['amp']
        neighbours[i] = data['simConfig']['n_neighbors']
        r[i] = data['r']

        mean_GOP[i] = data['GOP'].mean()
        mean_LOP[i] = data['LOP_delta'][5].mean(axis=1).mean()

        coerentes = data['analise_media_lops'][2][1:]
        
        Coerentes75[i] = coerentes[0]
        Coerentes80[i] = coerentes[1]
        Coerentes85[i] = coerentes[2]
        Coerentes90[i] = coerentes[3]
        Coerentes95[i] = coerentes[4]
        
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
    'Coerentes75':Coerentes75,
    'Coerentes80':Coerentes80,
    'Coerentes85':Coerentes85,
    'Coerentes90':Coerentes90,
    'Coerentes95':Coerentes95,
}

print(f'~ Dump pickle file: \n')
with open('data_read_batches_v7.pkl', 'wb') as handle:
    pickle.dump(dados, handle, protocol=pickle.HIGHEST_PROTOCOL)