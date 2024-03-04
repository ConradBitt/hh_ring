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


# path = str(input('Path of file: '))
path = '../results_spaceparams/space_param_v2_batch1_2.pkl'

file = path.split('/')[-1]

# file = f'space_param_v{v}_batch1'
resol = 32
with open(path, 'rb') as f:
    data_space_param = pickle.load(f)

# cellNumber = data_space_param['infosNetWork']['cellNumber']
# amp = data_space_param['infosNetWork']['amp']
# neuronsPerCore = data_space_param['infosNetWork']['neuronsPerCore']
# coresPerNode = data_space_param['infosNetWork']['coresPerNode']

gex = data_space_param['gex']
neighbours = data_space_param['neighbours']
amp = data_space_param['amp']
mean_LOP = data_space_param['mean_LOP']
mean_GOP = data_space_param['mean_GOP']
mean_cv = data_space_param['mean_cv']
mean_freq = data_space_param['mean_freq']

mean_LOP_arr = np.array(np.array_split(data_space_param['mean_LOP'], resol))
mean_GOP_arr = np.array(np.array_split(data_space_param['mean_GOP'], resol))
mean_cv_arr = np.array(np.array_split(data_space_param['mean_cv'],resol))
mean_freq_arr = np.array(np.array_split(data_space_param['mean_freq'], resol))

# axis
axis_gex = np.array(list(set(gex)))#.astype(int)
axis_amp = np.array(list(set(amp)))
axis_neighbours = np.array(list(set(neighbours)))#.astype(float)
axis_gex.sort()
axis_amp.sort()
axis_neighbours.sort()


print(mean_LOP_arr.shape)

fig, ax = plt.subplots(ncols=2, nrows=2, figsize=(8,6))
fig.set_tight_layout(20)
# fig.suptitle('Rede de 256 neurônios, transiente 24s, amostra 1s,\n $g_{ex} = 250 \\mu S/cm²$')

# tg, ig = np.meshgrid(axis_neighbours[1:]/256, axis_gex[1:]*1e2)
tg, ig = np.meshgrid(axis_amp[1:]*1000, axis_gex[1:]*1e2)

# ax[0][0].set_title('$\overline{GOP(t)}$')
ax[0][0].set_title('(A)', loc='left',pad=10)
hm00 = ax[0][0].pcolor(ig, tg, mean_GOP_arr, cmap='gnuplot')
cbar00 = fig.colorbar(hm00, ax=ax[0][0])#, cax=cax1, format=formater)
cbar00.ax.set_title(r'$\langle GOP \rangle$')

# ax[0][1].set_title('$\overline{\overline{LOP}(t)}$')
ax[0][1].set_title('(B)', loc='left',pad=10)
hm01 = ax[0][1].pcolor(ig, tg, mean_LOP_arr, cmap='gnuplot')
cbar01 = fig.colorbar(hm01, ax=ax[0][1])#, cax=cax1, format=formater)
cbar01.ax.set_title(r'$\langle LOP \rangle$')

# ax[1][0].set_title('$\overline{Fr}$')
ax[1][0].set_title('(C)', loc='left',pad=10)
hm03 = ax[1][0].pcolor(ig, tg, mean_freq_arr, cmap='gnuplot')
cbar03 = fig.colorbar(hm03, ax=ax[1][0])#, cax=cax1, format=formater)
cbar03.ax.set_title(r'$\overline{Fr}$')

# ax[1][1].set_title('$\overline{CV}$')
ax[1][1].set_title('(D)',loc='left',pad=10)
hm02 = ax[1][1].pcolor(ig, tg, mean_cv_arr, cmap='gnuplot')
cbar02 = fig.colorbar(hm02, ax=ax[1][1])#, cax=cax1, format=formater)
cbar02.ax.set_title(r'$\overline{CV}$')

# step_y = plticker.MultipleLocator(base=0.05) # this locator puts ticks at regular intervals
# step_x = plticker.MultipleLocator(base=0.05)
for linha in ax:
    for coluna in linha:
#         # coluna.yaxis.set_major_locator(step_y)
#         # coluna.xaxis.set_major_locator(step_x)
#         # coluna.set_ylim(None,0.36)
        # coluna.set_ylim(0.05,0.4)
        coluna.set_xlim(1.e-2,4.e-2)

ax[0][0].set_ylabel('$I_{ext}$ ($pA$)')
ax[1][0].set_ylabel('$I_{ext}$ ($pA$)')

# ax[0][0].set_ylabel('$r$')
# ax[1][0].set_ylabel('$r$')
ax[1][0].set_xlabel('$g_{ex}$ ($mS/cm²$)')
ax[1][1].set_xlabel('$g_{ex}$ ($mS/cm²$)')


# Anotações: v1 batch1
# ax.annotate('(I)', xy=(xpos,ypox),  color='white', fontsize=24)
# ax[0][0].annotate('(I)', xy=(2.4e-2,0.35),  color='black', fontsize=14)
# ax[0][0].annotate('(II)', xy=(3e-2,0.25),   color='white', fontsize=24)
# ax[0][0].annotate('(III)', xy=(2.4e-2,0.19),  color='black', fontsize=14)
# ax[0][0].annotate('(IV)', xy=(1.89e-2,0.165),color='white', fontsize=14)
# ax[0][0].annotate('(V)', xy=(1.25e-2,0.1),  color='black', fontsize=24)


# ax[0][1].annotate('(I)', xy=(1.25e-1,0.1),  color='black', fontsize=24)
# ax[0][1].annotate('(II)', xy=(3e-1,0.25),  color='black', fontsize=24)
# ax[0][1].annotate('(III)', xy=(2.1e-1,0.15),  color='black', fontsize=14)
# ax[0][1].annotate('(IV)', xy=(2.4e-1,0.19),  color='black', fontsize=14)

# ax[1][0].annotate('(I)', xy=(1.25e-1,0.1), color='white', fontsize=24)
# ax[1][0].annotate('(II)', xy=(3e-1,0.25),  color='black', fontsize=24)
# ax[1][0].annotate('(III)', xy=(2.1e-1,0.15),color='white', fontsize=14)
# ax[1][0].annotate('(IV)', xy=(2.4e-1,0.19),  color='white', fontsize=14)

# ax[1][1].annotate('(I)', xy=(1.25e-1,0.1), color='white', fontsize=24)
# ax[1][1].annotate('(II)', xy=(3e-1,0.25),  color='white', fontsize=24)
# ax[1][1].annotate('(III)', xy=(2.1e-1,0.15),color='white', fontsize=14)
# ax[1][1].annotate('(IV)', xy=(2.4e-1,0.19),  color='white', fontsize=14)

# anotações v2 batch1
ax[0][0].annotate('(I)', xy=(1.25e-2,160),  color='black', fontsize=24)
ax[0][0].annotate('(II)', xy=(1.25e-2,190),  color='black', fontsize=24)
ax[0][0].annotate('(III)', xy=(2.1e-2,190),  color='white', fontsize=24)
ax[0][0].annotate('(IV)', xy=(3.25e-2,190),  color='white', fontsize=24)
ax[0][0].annotate('(V)',
             xytext=(3.e-2,175),           # Coordenadas do ponto de destino
             xy=(3.7e-2,162),                # Coordenadas do texto de anotação
             arrowprops=dict(arrowstyle='->', color='white'),  # Estilo da seta
             fontsize=24,              # Tamanho da fonte
             color='white',             # Cor do texto
            #  bbox=dict(facecolor='yellow', edgecolor='red', boxstyle='round'),  # Estilo do retângulo de fundo
             )
# ax[0][0].annotate('(VI)', xy=(3.35e-1,170), color='white')
ax[0][0].annotate('(VI)', xy=(3.35e-2,152),  color='black', fontsize=18)


plt.savefig(f'{file}.png', dpi=600, bbox_inches='tight', format='png')
plt.show()