import pickle
import sys
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.ticker as plticker
from matplotlib.colors import LinearSegmentedColormap, ListedColormap
import locale
from scipy.signal import find_peaks

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')       

from matplotlib.colors import ListedColormap,LinearSegmentedColormap
colors = ["darkorange", "gold", "lawngreen", "lightseagreen","darkgreen"]
cmap_LOP = ListedColormap(colors)

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

with open('../results/data_LOP_potencial.pkl','rb') as f:
    dados_lop = pickle.load(f)

t = dados_lop['t']
t_phase = dados_lop['t_phase']
v_soma1 = dados_lop['v_soma1']
v_soma2 = dados_lop['v_soma2']
v_soma3 = dados_lop['v_soma3']
v_soma4 = dados_lop['v_soma4']

peaks1, _ = find_peaks(v_soma1, height=0)
peaks2, _ = find_peaks(v_soma2, height=0)
peaks3, _ = find_peaks(v_soma3, height=0)
peaks4, _ = find_peaks(v_soma4, height=0)

t_peaks = [
    peaks1,
    peaks2,
    peaks3,
    peaks4
]

folder = f'../results/'
file = f'v4_batch1_23_29'

# file = f'../data/v{v}_batch{batch}/v{v}_batch{batch}_0_{subbatch}'
# file = f'../data/v0_batch0/v0_batch0'
print('~~ Plot Raster, LOP, Phase and GOP.')
print(f'Reading: "{file}"')

with open(folder+file+'_data.pkl', 'rb') as f:
    data = pickle.load(f)

t_peaks = data['t_peaks']
t_phase = data['t_phase']


cm = 1/2.54

fig = plt.figure(figsize=(15*cm, 9*cm))
gs = fig.add_gridspec(2, 1)
fig.set_tight_layout(20)

ax0 = fig.add_subplot(gs[0, 0])
ax0.set_title('(A)', loc='left', pad=10)
ax0.xaxis.set_visible(False)
ax0.set_ylabel('Voltage (mV)')
ax0.spines['right'].set_visible(False)
ax0.spines['top'].set_visible(False)
ax0.spines['bottom'].set_visible(False)
ax0.plot(t, v_soma4, color='magenta')
ax0.plot(t, v_soma1, color='red')
ax0.plot(t, v_soma2, color='green')
ax0.plot(t, v_soma3, color='blue')
ax0.set_xlim(1500, 4300)

ax1 = fig.add_subplot(gs[1,0])
ax1.spines['right'].set_visible(False)
ax1.spines['top'].set_visible(False)

ax1.set_title('(A)', loc='left', pad=20)
ax1.spines['right'].set_visible(False)
ax1.spines['top'].set_visible(False)
ax1.set_ylabel('$n$-ésimo Neurônio')
ax1.set_xlabel('Tempo (s)')
ax1.set_ylim(0, 20)
ax1.eventplot([event/1000 for event in t_peaks], color='black', linewidths=1,linestyles='-', zorder=3)
ax1.set_xlim(17, 18.5)


for i, t in enumerate(t_peaks):
    ax1.scatter(y = i + np.zeros(len(t_peaks[i])), x = t_peaks[i], s = 1, color='black')


plt.savefig('RasterPotentialPlot.png', dpi=600, bbox_inches='tight', format='png')
