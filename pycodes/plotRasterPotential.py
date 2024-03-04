import pickle
import numpy as np
import matplotlib.colors as mcolors
import matplotlib.ticker as plticker
import locale
import sys
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')       

from matplotlib import pyplot as plt
import matplotlib.colors as mcolors

def plot_params():
    plt.rc('text', usetex=True)
    plt.rc('font', size=13)
    plt.rc('xtick', labelsize=11)
    plt.rc('ytick', labelsize=11)
    plt.rc('axes', labelsize=14)
    plt.rc('legend', fontsize=8)
    plt.rc('lines', linewidth=1.0)
    plt.rcParams["axes.formatter.limits"] = (-3, 4)
    plt.rcParams['axes.formatter.use_locale'] = True
    plt.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
    plt.rcParams['pcolor.shading'] = 'nearest'
plot_params()

with open('../data/v0_batch0/v0_batch0_data.pkl','rb') as f:
    dados_lop = pickle.load(f)


t = dados_lop['simData']['t']

spkt = dados_lop['simData']['spkt']
spkid = dados_lop['simData']['spkid']

spkid = np.array(spkid)  # Converter para NumPy array
spkts = np.array(spkt)      # Converter para NumPy array
unique_gids = np.unique(spkid)
spkmat = [spkts[spkid == gid] for gid in unique_gids]

cores = list(mcolors.TABLEAU_COLORS.keys())
# id_somas = np.arange(1,100, len(cores))
id_somas = [0,41,61,91]

v_21 = dados_lop['simData']['V_soma']['cell_0']
v_41 = dados_lop['simData']['V_soma']['cell_41']
v_61 = dados_lop['simData']['V_soma']['cell_61']
v_91 = dados_lop['simData']['V_soma']['cell_91']
lista_somas = [v_21, v_41, v_61, v_91]


cm = 1/2.54

fig = plt.figure(figsize=(8*cm, 9*cm))
fig.set_tight_layout(20)
gs = fig.add_gridspec(2, 1, height_ratios=[1,2])

ax0 = fig.add_subplot(gs[0, 0])
ax0.set_title('(A)', loc='left', pad=10, fontsize=12)
ax0.xaxis.set_visible(False)
ax0.set_ylabel('Voltage (mV)', fontsize=10)
ax0.spines['right'].set_visible(False)
ax0.spines['top'].set_visible(False)
ax0.hlines(y = 25, xmin=1900, xmax=2500, linestyles='--', colors='black', linewidth=1, label='limiar')
# ax0.spines['bottom'].set_visible(False)
j = 0
for soma in lista_somas:
    ax0.plot(t, soma, c= cores [j])
    j+=1
    


ax1 = fig.add_subplot(gs[1, 0])
ax1.set_title('(B)', loc='left', pad=10, fontsize=12)
# ax1.xaxis.set_visible(False)
ax1.set_ylabel('$n$-ésimo neuronio', fontsize=10)
ax1.spines['right'].set_visible(False)
ax1.spines['top'].set_visible(False)

j = 0
for i, t_peaks in zip(unique_gids,spkmat):
    if i in id_somas:
        ax1.scatter(y = i + np.zeros(len(t_peaks)), x = t_peaks, color=cores[j], s=10)
        j+=1
    else:
        ax1.scatter(y = i + np.zeros(len(t_peaks)), x = t_peaks, color='black', s=0.5)


ti = 2250
tf = 2450

ax0.set_xlim(ti, tf)
ax1.set_xlim(ti, tf)
ax1.set_xlabel('Tempo (ms)', fontsize=10)
ax1.set_ylim(None, 100)


plt.savefig('exemplo_raster_potencial_1.png', dpi=600, bbox_inches='tight', format='png')
