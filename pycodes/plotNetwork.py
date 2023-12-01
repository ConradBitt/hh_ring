import pickle
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.font_manager
import os
import sys

def plot_params():
    # plt.rc('text', usetex=True)
    plt.rc('font', size=13)
    plt.rc('xtick', labelsize=11)
    plt.rc('ytick', labelsize=11)
    plt.rc('axes', labelsize=14)
    plt.rc('legend', fontsize=8)
    plt.rc('lines', linewidth=1.0)
    plt.rcParams["axes.formatter.limits"] = (-3, 4)
    # plt.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
    plt.rcParams['mathtext.fontset'] = 'cm'
    plt.rcParams['font.family'] = 'STIXGeneral'

plot_params()

v = str(sys.argv[1])
batch = sys.argv[2]
batch_number = 'batch'+str(batch.zfill(4))
subbatch = sys.argv[3]
subbatch_number = '0_'+str(subbatch)
# file = f'../data3/v{v}_{batch_number}/v{v}_{batch_number}_{subbatch_number}'
folder = f'../data/v{v}_{batch_number}/'
file = f'../data/v{v}_{batch_number}/v{v}_{batch_number}_0'

# file = f'../data/v{v}_batch{batch}/v{v}_batch{batch}_0_{subbatch}'
# file = f'../data/v0_batch0/v0_batch0'
print('~~ Plot Raster, LOP, Phase and GOP.')
print(f'Reading: "{file}"')

with open(file+'_data.pkl', 'rb') as f:
    data = pickle.load(f)

cellNumber = data['simConfig']['cellNumber']
gex = data['simConfig']['gex']
amp = data['simConfig']['IClamp0']['amp'] * 1000
neighbours = data['simConfig']['n_neighbors']
freq_mean = data['freq_bar'].mean()
coresPerNode = data['simConfig']['coresPerNode']

neuronsPerCore = int(cellNumber)/int(coresPerNode)

infos = f'{neuronsPerCore} neuronios por core'

x = np.zeros(cellNumber)
z = np.zeros(cellNumber)

for i, cell in enumerate(data['net']['cells']):
    x[i] = cell['tags']['x']
    z[i] = cell['tags']['z']

cm = 1/2.54  # centimeters in inches

f, ax = plt.subplots(figsize=(12*cm, 12*cm))
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.scatter(x,z, s=0.5, color='black')
ax.set_xlabel('$X$  $(\mu m)$')
ax.set_ylabel('$Z$  $(\mu m)$')
ax.set_title(infos, fontsize=11, loc='left', pad=20)

print('->'+f'../AnalysisV{v}_n{len(x)}_{gex}Scm2_{amp:.1f}pA_r{neighbours/cellNumber:.2f}neigh_{int(freq_mean)}Hz.png')
plt.savefig(folder+f'NetWorkV{v}_n{len(x)}_{gex}Scm2_{amp:.1f}pA_r{neighbours/cellNumber:.2f}neigh_{int(freq_mean)}Hz.png', dpi=600, bbox_inches='tight', format='png')
