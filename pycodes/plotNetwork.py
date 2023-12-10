import pickle
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.font_manager
import os
import sys

def get_matriz_Adjacência(n, p, numExtraConex = 0):
    conex = np.zeros((n, n))  # acoplamento não-local
    for i in range(n):
        for k in range(i - p, i + p + 1):
            j = k % n  # Utilize o operador de módulo para garantir que j permaneça dentro do intervalo correto
            if i != j:
                conex[i, j] = 1  # Defina 1 para representar a existência de uma aresta

    # Introduzir conexões aleatórias
    conex_smll = np.zeros_like(conex)
    conex_smll += conex

    for linha, conexoes in enumerate(conex_smll):
        for conexExtra in range(numExtraConex):
            idx_nova_conex = np.random.randint(0, n)  # gera índice aleatório de 0 a n
            if idx_nova_conex == 0 or idx_nova_conex == n:
                idx_nova_conex = idx_nova_conex % n

            if conexoes[idx_nova_conex] != 1:
                conexoes[idx_nova_conex] = 1

    # Remover autoconexões
    for i in range(n):
        conex_smll[i, i] = 0

    return conex_smll



def plot_params():
    # plt.rc('text', usetex=True)
    plt.rc('font', size=13)
    plt.rc('xtick', labelsize=11)
    plt.rc('ytick', labelsize=11)
    plt.rc('axes', labelsize=14)
    plt.rc('legend', fontsize=8)
    plt.rc('lines', linewidth=1.0)
    plt.rcParams["axes.formatter.limits"] = (-3, 4)
    plt.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
    plt.rcParams['mathtext.fontset'] = 'cm'
    plt.rcParams['font.family'] = 'STIXGeneral'

plot_params()

v = str(sys.argv[1])
i = str(sys.argv[2])
j = str(sys.argv[3])
folder = f'figuresV2'
file = f'../{folder}/v{v}_batch1_{i}_{j}'

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

adj_matrix = get_matriz_Adjacência(cellNumber, neighbours, 0)

x = np.zeros(cellNumber)
z = np.zeros(cellNumber)

for i, cell in enumerate(data['net']['cells']):
    x[i] = cell['tags']['x']
    z[i] = cell['tags']['z']

cm = 1/2.54  # centimeters in inches

f, ax = plt.subplots(figsize=(12*cm, 12*cm))
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

# Traçar linhas com base na matriz de adjacência
for i in range(len(x)):
    for j in range(len(x)):
        if adj_matrix[i, j] != 0:
            ax.plot([x[i], x[j]], [z[i], z[j]], linestyle='-', color='blue', alpha=0.05)

ax.scatter(x,z, s=5, color='black')
ax.set_xlabel('$X$  $(\mu m)$')
ax.set_ylabel('$Z$  $(\mu m)$')

# ax.set_xlim(40,60)
# ax.set_ylim(0,20)

plt.savefig(file+'_rede.png', dpi=600, bbox_inches='tight', format='png')
