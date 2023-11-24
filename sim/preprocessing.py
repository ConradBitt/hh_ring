"""
preprocessing.py

Script python to calculate the metrics.

    - This script has the function of reading a .pkl file from a netpyne simulation
    containing the spkid and spkt of the neurons. From these lists, the phase, CV,
    firing rate, GOP and LOP are calculated.

params: 
    - python3 preprocessing.py version batch_number subbatch_number delta_neighbours

Contributors: conrad.bittencourt@gmail.com, fernandodasilvaborges@gmail.com
"""

import sys
import pickle
import numpy as np
import metrics
import datetime

# read variables of file
v = str(sys.argv[1])
batch = sys.argv[2]
batch_number = 'batch'+str(batch.zfill(4))
subbatch = sys.argv[3]
subbatch_number = '0_'+str(subbatch)
delta = int(sys.argv[4])
file = f'../data/v{v}_{batch_number}/v{v}_{batch_number}_{subbatch_number}'

# file = f'../data/v1_batch0/v1_batch0'
delta = 5

now = datetime.datetime.now()
print(f'\n~~ Start pre processing {now}')
print(f'~ Read file: {file}')
with open(file+'_data.pkl', 'rb') as f:
    data = pickle.load(f)

step = data['simConfig']['recordStep']
n_neighbors = data['simConfig']['n_neighbors']
cellNumber = data['simConfig']['cellNumber']
r = n_neighbors / cellNumber
data['r'] = r
print(f'Cell number: {cellNumber} \t n_neighbors: {n_neighbors} \t r: {r}')
print(f"time simulation: {data['simConfig']['duration']}ms\n")

ti = -2500
tf = -500
print(f"\ntime sample metrics: {tf - ti}ms\n")

spkid = data['simData']['spkid']
spkt = data['simData']['spkt']

print('~ Computing phase')
spkmat, t_range = metrics.calculate_t_range(spkinds = spkid, spkts=spkt, step=10)
t_range, phases = metrics.calculate_phases(spkmat, t_range, ti=ti, tf=tf)

data['t_phase'] = t_range
data['phases'] = phases
data['spkmat'] = spkmat

print('~ ISI, CV and FR')
isi_bar, cv, freq_bar = metrics.isi_cv_freq(spkmat)
data['isi_bar'] = isi_bar
data['cv'] = cv
data['freq_bar'] = freq_bar

print('~ Computing GOP')
gop = np.zeros(phases.shape[1])
for i, spatial_phase in enumerate(phases.T):
    gop[i] = metrics.kuramoto_param_global_order(spatial_phase)
data['GOP'] = gop

print('~ Computing LOP:')
deltas = np.arange(delta, delta+1, 1)
print(f' -- deltas: {deltas}')
lops = {}
for d in deltas:
    print(f'--> d: {d}')
    lop = np.zeros_like(phases.T)
    for i, spatial_phase in enumerate(phases.T):
        lop[i] = metrics.kuramoto_param_local_order(spatial_phase, delta=d)
    lops[d] = lop.T
data['LOP_delta'] = lops

print('~ Counting LOP under threshold:')
thresholds = [0.75, 0.85, 0.95, 1.]
n_coerentes = metrics.countNeuronsUnderThr(lops[delta], thresholds)
data['Count_LOP_Under_Trh'] = {}
for i, thr in enumerate(thresholds):
    print(f'threshold: {thr} - count: {n_coerentes[i]}')
    data['Count_LOP_Under_Trh'][thr] = n_coerentes[i]

metrics.get_size(file+'_data.pkl')
print(f'~ Dump pickle file: {file}\n')
with open(file+'_data.pkl', 'wb') as handle:
    pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
metrics.get_size(file+'_data.pkl')

now = datetime.datetime.now()
print(f'Finish preprocessing: {now}')

