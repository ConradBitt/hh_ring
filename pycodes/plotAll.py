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
    freq_mean = data['freq_bar'].mean()
    cv = data['cv'].mean()
    t_peaks = data['t_peaks']
    phases = data['phases']
    t_phase = data['t_phase']

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
    fr = '$\overline{Fr} = '+f'{freq_mean:.1f}$'+'Hz\n\n'
    cv_mean = '$\overline{CV}='+f'{cv:.2f}'.replace('.',',')+'$\n\n' 

    infos = raio+g+i+fr+cv_mean
    ax[1][1].annotate(infos.replace('.',','), xy = (0,0), xytext=(0,-1), fontsize=10)
    ax[1][1].yaxis.set_visible(False)
    ax[1][1].xaxis.set_visible(False)
    ax[1][1].spines['right'].set_visible(False)
    ax[1][1].spines['left'].set_visible(False)
    ax[1][1].spines['top'].set_visible(False)
    ax[1][1].spines['bottom'].set_visible(False)

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

folder = '../regioes_v3_batch1/'

caminhos = [
    'v3_batch1_17_23_data_regiao_V.pkl',
    'v3_batch1_27_20_data_regiao_II.pkl'
]

for p in caminhos:
    plotAll(folder+p)
