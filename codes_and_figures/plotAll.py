import pickle
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.ticker as plticker
from matplotlib.colors import LinearSegmentedColormap, ListedColormap
import locale
import latex
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')       

cores = list(mcolors.TABLEAU_COLORS.keys())
cores = [cor.split(':')[-1] for cor in cores]

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

from numba import jit
@jit(nopython=True)
def isi_cv_freq(tpeaks, ti=0,tf=-1):
    """
    Calcula o inter-spike-interval (ISI) de uma lista de tspikes.

    Args:
        tpeaks (list of arrays): A lista contendo n-arrays com o tempo em que ocorre os spikes.

    Returns:
        tupla: uma tupla contendo as seguintes matrizes:
             - isi_bar (numpy.ndarray): Matriz de ISIs médios para cada neurônio.
             - cv (numpy.ndarray): Matriz de coeficiente de variação (CV) dos ISIs para cada neurônio.
             - freq_bar (numpy.ndarray): Matriz de frequências médias de disparo (em Hz) para cada neurônio.
    """
    num_neurons = len(tpeaks)
    isi_bar = np.zeros(num_neurons)
    cv = np.zeros(num_neurons)
    freq_bar = np.zeros(num_neurons)
    
    for i in range(num_neurons):    
        nspikes = tpeaks[i][(tpeaks[i] > ti) & (tpeaks[i] < tf)]
        isis = np.empty(len(tpeaks[i]) - 1, dtype=np.float64)
        for j in range(len(tpeaks[i]) - 1):
            isis[j] = tpeaks[i][j + 1] - tpeaks[i][j]

        isi_bar[i] = np.mean(isis)
        freq_bar[i] = (1 / isi_bar[i]) * 1e3  # Convert ISI to firing frequency (Hz)
        cv[i] = np.std(isis) / isi_bar[i]
    
    return isi_bar, cv, freq_bar

def plotAll(path):
    file = path.split('/')[-1].split('.')[0]

    # file = f'space_param_v{v}_batch1'
    resol = 32
    with open(path, 'rb') as f:
        data = pickle.load(f)

    # file = f'../data/v{v}_batch{batch}/v{v}_batch{batch}_0_{subbatch}'
    # file = f'../data/v0_batch0/v0_batch0'
    print('~~ Plot Raster, LOP, Phase and GOP.')
    print(f'Reading: "{file}"')

    cellNumber = data['simConfig']['cellNumber']
    gex = data['simConfig']['gex']*1e3
    amp = data['simConfig']['IClamp0']['amp'] * 1000
    neighbours = data['simConfig']['n_neighbors']
    t_peaks = data['t_peaks']
    _, cv, freq = isi_cv_freq(t_peaks, ti=20000, tf=25000)

    cv_bar = np.mean(cv)
    freq_bar = np.mean(freq)

    phases = data['phases']
    t_phase = data['t_phase']
    Qs = data['Count_LOP_Under_Trh']

    gop = data['GOP']
    lop = data['LOP_delta'][5]

    ti = -201
    tf = -101

    gop_sample = gop[ti:tf]
    lop_sample = lop[:,ti:tf]

    mean_lop = lop_sample.mean(axis=1)
    last_lop = lop_sample[:, -10]

    last_phases = phases[:, -10]
    t_sample = t_phase[ti:tf]

    print(gop.shape, lop.shape, mean_lop.shape, last_lop.shape)


    print(f'Plotting...')
    cm = 1/2.54

    fig, ax = plt.subplots(2,3, figsize=(20*cm,12*cm), gridspec_kw={'width_ratios':[5,1.5,1.5], 'height_ratios': [4,2] })
    np.random.seed(2788590720)
    indices_sorteados = np.random.choice(lop_sample.shape[1], 150)
    n = np.arange(lop_sample.shape[0])
    fig.set_tight_layout(15)
    ax[0][0].set_title('(A)', loc='left', pad=20)
    ax[0][0].spines['right'].set_visible(False)
    ax[0][0].spines['top'].set_visible(False)
    ax[0][0].set_ylabel('$n$-ésimo Neurônio')
    ax[0][0].set_ylim(0, len(t_peaks))
    ax[0][0].set_yticks([0,256])
    ax[0][0].eventplot(t_peaks, color='black')
    ax[0][0].xaxis.set_visible(False)

    ax[0][1].set_title('(B)', loc='left', pad=20)
    ax[0][1].scatter(x = last_phases, y=n, color='green', s = 0.1, label=r'$\phi_n(t)$')
    ax[0][1].set_xticks([0,2*np.pi])
    ax[0][1].set_xticklabels(['0','$2\pi$'])
    ax[0][1].set_xlim(-0.08, 2*np.pi+0.05)
    # ax[0][1].set_xlabel('$\phi$(t)', fontsize=11)
    ax[0][1].spines['right'].set_visible(False)
    ax[0][1].spines['top'].set_visible(False)
    ax[0][1].yaxis.set_visible(False)
    l01 = ax[0][1].legend(loc='center',fontsize="8", 
                    bbox_to_anchor=(0.5, -0.15))
    l01.legendHandles[0]._sizes=[15]

    ax[0][2].set_title('(C)',loc='left', pad=20)
    for lop in lop_sample[:, indices_sorteados].T:
        ax[0][2].scatter(x = lop, y = n, color='blue', alpha=0.005)
    ax[0][2].scatter(x = last_lop, y = n, s = 0.1, color='blue', label=r'$LOP_{n}(t)$')
    ax[0][2].scatter(x = mean_lop, y = n, s = 0.2, color='red', alpha=1, label=r'$\langle LOP_{n} \rangle$')
    ax[0][2].set_xticks([0,1.])
    ax[0][2].set_xlim(-0.05,1.05)
    ax[0][2].spines['right'].set_visible(False)
    ax[0][2].spines['top'].set_visible(False)
    ax[0][2].yaxis.set_visible(False)
    l02 = ax[0][2].legend(loc='center',fontsize="8", 
                    bbox_to_anchor=(0.5, -0.17))
    l02.legendHandles[0]._sizes=[15]
    l02.legendHandles[1]._sizes=[15]


    ax[1][0].set_title('(D)', loc='left', pad=20)
    ax[1][0].plot(t_sample, gop_sample, color='darkred', label='GOP$(t)$')
    ax[1][0].spines['right'].set_visible(False)
    ax[1][0].spines['top'].set_visible(False)
    ax[1][0].set_ylim(-0.05, 1.05)
    ax[1][0].set_ylabel('GOP')
    ax[1][0].set_xlabel('Tempo (s)')
    ax[1][0].legend(loc='upper right')


    raio = '$r = '+f'{neighbours/cellNumber:.4f}'.replace('.',',')+'$\n\n'
    g = '$g_{ex}='+f'{gex/10:.4f} mS/cm^2'.replace('.',',')+'$\n\n'
    i = '$I_{ext}='+f'{amp:.2f}'+'$pA\n\n'
    fr = '$\overline{Fr} = '+f'{freq_bar:.1f}$'+'Hz\n\n'
    cv_mean = '$\overline{CV}='+f'{cv_bar:.2f}'.replace('.',',')+'$\n\n' 

    
    infos = raio+g+i+fr+cv_mean
    ax[1][1].annotate(infos.replace('.',','), xy = (0,0), xytext=(0,-1), fontsize=10)
    ax[1][1].yaxis.set_visible(False)
    ax[1][1].xaxis.set_visible(False)
    ax[1][1].spines['right'].set_visible(False)
    ax[1][1].spines['left'].set_visible(False)
    ax[1][1].spines['top'].set_visible(False)
    ax[1][1].spines['bottom'].set_visible(False)

    qlabel = ''
    for s, q in Qs.items():
        if s<1:
            qlabel += '$'+f'Q({s:.2f})='+f'{int(q)}'.replace('.',',')+'$\n\n' 
    ax[1][2].annotate(qlabel.replace('.',','), xy = (0,0), xytext=(0,-1), fontsize=10)
    ax[1][2].yaxis.set_visible(False)
    ax[1][2].xaxis.set_visible(False)
    ax[1][2].spines['right'].set_visible(False)
    ax[1][2].spines['top'].set_visible(False)
    ax[1][2].spines['left'].set_visible(False)
    ax[1][2].spines['bottom'].set_visible(False)

    for axis in ax[:,0]:
        ti_label = t_sample[0]
        tf_label = t_sample[-1]
        axis.set_xlim(ti_label, tf_label)
        axis.set_xticks([ti_label, tf_label])
        axis.set_xticklabels([f'{lab/1e3:.1f}'.replace('.',',') for lab in [ti_label, tf_label]])

    print('->'+f'{file}')
    # plt.savefig(folder+f'AnalysisV{v}_n{len(n)}_{gex}Scm2_{amp:.1f}pA_r{neighbours/cellNumber:.2f}neigh_{int(freq_mean)}Hz.png', dpi=600, bbox_inches='tight', format='png')
    plt.savefig(f'{file}.png', dpi=600, bbox_inches='tight', format='png')

    print('\n~~')


# v = str(sys.argv[1])
# i = str(sys.argv[2])
# j = str(sys.argv[3])
# folder = f'../figuresV2/'
# file = f'../figuresV2/v{v}_batch1_{i}_{j}'

# path = str(input('Path of file: '))

folder = '../results/v2_batch1/'

caminhos = [
    'v2_batch1_25_6_data_regiao_V_BursteChimera.pkl',
    'v2_batch1_9_28_data_regiao_III_RSeChimera.pkl',
    'v2_batch1_23_26_data_regiao_IV_RSeBustsHighFr.pkl',
    'v2_batch1_2_7_data_regiao_I_RS.pkl','v2_batch1_9_29_data_regiao_III_RSeChimera.pkl',
    'v2_batch1_24_1_data_regiao_V_Burst.pkl','v2_batch1_3_28_data_regiao_II_RSeBust.pkl','v2_batch1_25_5_data_regiao_V_BursteChimera.pkl',
    'v2_batch1_9_27_data_regiao_III_RSeChimera.pkl'
]

for p in caminhos:
    plotAll(folder+p)

folder = '../results/v3_batch1/'
caminhos = [
    'v3_batch1_11_13_data_regiao_III_burst.pkl','v3_batch1_2_7_data_regiao_I.pkl',
    'v3_batch1_11_10_data_regiao_III_chimera.pkl','v3_batch1_11_9_data_regiao_III_RSeBust.pkl',
    'v3_batch1_11_12_data_regiao_III_RS.pkl','v3_batch1_17_15_data_regiao_IV_burst.pkl'
]


for p in caminhos:
    plotAll(folder+p)