# import pickle
# import numpy as np
# from matplotlib import pyplot as plt
# import matplotlib.colors as mcolors
# from matplotlib.colors import LinearSegmentedColormap, ListedColormap

# cores = list(mcolors.TABLEAU_COLORS.keys())
# cores = [cor.split(':')[-1] for cor in cores]

# def plot_params():
#     # plt.rc('text', usetex=True)
#     plt.rc('font', size=13)
#     plt.rc('xtick', labelsize=11)
#     plt.rc('ytick', labelsize=11)
#     plt.rc('axes', labelsize=14)
#     plt.rc('legend', fontsize=8)
#     plt.rc('lines', linewidth=1.0)
#     plt.rcParams["axes.formatter.limits"] = (-3, 4)
#     # plt.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
#     plt.rcParams['pcolor.shading'] = 'nearest'
# plot_params()

# v = 7
# with open(f'../data/data_read_batches_v{v}_sample5s.pkl', 'rb') as f:
#     data_space_param = pickle.load(f)

# gex = data_space_param['gex']
# amp = data_space_param['amp']
# r = data_space_param['r']
# neighbours = data_space_param['neighbours']
# mean_LOP = data_space_param['mean_LOP']
# mean_GOP = data_space_param['mean_GOP']
# mean_cv = data_space_param['mean_cv']
# mean_freq = data_space_param['mean_freq']
# thresholds = data_space_param['thresholds']
# Coerentes80 = data_space_param['Coerentes80']
# Coerentes90 = data_space_param['Coerentes90']

# mean_LOP_arr = np.array(np.array_split(data_space_param['mean_LOP'], 30))
# mean_GOP_arr = np.array(np.array_split(data_space_param['mean_GOP'], 30))
# mean_cv_arr = np.array(np.array_split(data_space_param['mean_cv'], 30))
# mean_freq_arr = np.array(np.array_split(data_space_param['mean_freq'], 30))
# Coerentes80_arr = np.array(np.array_split(data_space_param['Coerentes80'], 30))
# Coerentes90_arr = np.array(np.array_split(data_space_param['Coerentes90'], 30))

# # axis
# axis_gex = np.array(list(set(gex)))#.astype(int)
# axis_neighbours = np.array(list(set(neighbours)))#.astype(float)
# axis_gex.sort()
# axis_neighbours.sort()


# print(mean_LOP_arr.shape)

# fig, ax = plt.subplots(ncols=3, nrows=2, figsize=(13,7.5))
# fig.set_tight_layout(20)
# fig.suptitle('Rede de 512 neurônios, corrente injetada 170pA, transiente 24s, amostra 1s.')

# tg, ig = np.meshgrid(axis_neighbours, axis_gex)

# ax[0][0].set_title('$\overline{GOP(t)}$')
# hm00 = ax[0][0].pcolor(ig, tg, mean_GOP_arr, cmap='gnuplot', vmin=0, vmax=1)
# cbar00 = fig.colorbar(hm00, ax=ax[0][0])#, cax=cax1, format=formater)
# cbar00.set_label(r'$\overline{GOP}$')

# ax[0][1].set_title('$\overline{\overline{LOP}(t)}$')
# hm01 = ax[0][1].pcolor(ig, tg, mean_LOP_arr, cmap='gnuplot', vmin=0, vmax=1)
# cbar01 = fig.colorbar(hm01, ax=ax[0][1])#, cax=cax1, format=formater)
# cbar01.set_label(r'$\overline{LOP(t)}$')

# ax[0][2].set_title('$\overline{Fr}$')
# hm03 = ax[0][2].pcolor(ig, tg, mean_freq_arr, cmap='gnuplot')
# cbar03 = fig.colorbar(hm03, ax=ax[0][2])#, cax=cax1, format=formater)
# cbar03.set_label(r'Fr (Hz)')

# hm12 = ax[1][0].pcolor(ig, tg, Coerentes80_arr, cmap='gnuplot')
# cbar12 = fig.colorbar(hm12, ax=ax[1][0])#, cax=cax1, format=formater)
# cbar12.set_label(r'Quantidade Elementos')
# ax[1][0].set_title('nº elementos $lop < 0.80$', fontsize=11)


# hm13 = ax[1][1].pcolor(ig, tg, Coerentes90_arr, cmap='gnuplot')
# cbar13 = fig.colorbar(hm13, ax=ax[1][1])#, cax=cax1, format=formater)
# cbar13.set_label(r'Quantidade Elementos')
# ax[1][1].set_title('nº elementos $lop < 0.90$', fontsize=11)

# ax[1][2].set_title('$\overline{CV}$')
# hm02 = ax[1][2].pcolor(ig, tg, mean_cv_arr, cmap='gnuplot', vmin=0, vmax=1)
# cbar02 = fig.colorbar(hm02, ax=ax[1][2])#, cax=cax1, format=formater)
# cbar02.set_label(r'$CV$')


# ax[0][0].set_ylabel('Nº Conexões')
# ax[1][0].set_ylabel('Nº Conexões')
# ax[1][0].set_xlabel('$g_{ex}$')
# ax[1][1].set_xlabel('$g_{ex}$')
# ax[1][2].set_xlabel('$g_{ex}$')

# plt.savefig('../figures/'+f'SpaceParam_V{v}_5s.png', dpi=600, bbox_inches='tight', format='png')
# plt.show()

import pickle
import numpy as np
from matplotlib import pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.colors import LinearSegmentedColormap, ListedColormap
import locale
# locale.setlocale(locale.LC_ALL, 'de_DE')     

cores = list(mcolors.TABLEAU_COLORS.keys())
cores = [cor.split(':')[-1] for cor in cores]

def plot_params():
    # plt.rc('text', usetex=True)
    plt.rc('font', size=13)
    plt.rc('xtick', labelsize=11)
    plt.rc('ytick', labelsize=11)
    plt.rc('axes', labelsize=14)
    plt.rc('legend', fontsize=8)
    plt.rc('lines', linewidth=1.0)
    plt.rcParams["axes.formatter.limits"] = (-3, 4)
    plt.rcParams['axes.formatter.use_locale'] = True
    # plt.rc('font', **{'family': 'serif', 'serif': ['Computer Modern']})
    plt.rcParams['pcolor.shading'] = 'nearest'
plot_params()

v = 2
resol = 32
with open(f'../data/v{v}_batch1/space_param_v{v}_batch1.pkl', 'rb') as f:
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
fig.suptitle('Rede de 256 neurônios, transiente 24s, amostra 1s,\n $g_{ex} = 250 \\mu S/cm²$')

tg, ig = np.meshgrid(axis_amp[1:], axis_gex[1:])

# ax[0][0].set_title('$\overline{GOP(t)}$')
ax[0][0].set_title('(A)', loc='left',pad=10)
hm00 = ax[0][0].pcolor(ig, tg, mean_GOP_arr, cmap='gnuplot')
cbar00 = fig.colorbar(hm00, ax=ax[0][0])#, cax=cax1, format=formater)
cbar00.set_label(r'$\overline{GOP}$')

# ax[0][1].set_title('$\overline{\overline{LOP}(t)}$')
ax[0][1].set_title('(B)', loc='left',pad=10)
hm01 = ax[0][1].pcolor(ig, tg, mean_LOP_arr, cmap='gnuplot')
cbar01 = fig.colorbar(hm01, ax=ax[0][1])#, cax=cax1, format=formater)
cbar01.set_label(r'$\overline{LOP(t)}$')

# ax[1][0].set_title('$\overline{Fr}$')
ax[1][0].set_title('(C)', loc='left',pad=10)
hm03 = ax[1][0].pcolor(ig, tg, mean_freq_arr, cmap='gnuplot')
cbar03 = fig.colorbar(hm03, ax=ax[1][0])#, cax=cax1, format=formater)
cbar03.set_label(r'Fr (Hz)')

# ax[1][1].set_title('$\overline{CV}$')
ax[1][1].set_title('(D)',loc='left',pad=10)
hm02 = ax[1][1].pcolor(ig, tg, mean_cv_arr, cmap='gnuplot')
cbar02 = fig.colorbar(hm02, ax=ax[1][1])#, cax=cax1, format=formater)
cbar02.set_label(r'$CV$')

# for linha in ax:
#     for coluna in linha:
#         coluna.set_ylim(0.16,0.2)
#         coluna.set_xlim(2e-4,)

ax[0][0].set_ylabel('$I_{ext}$')
ax[1][0].set_ylabel('$I_{ext}$')
ax[1][0].set_xlabel('$g_{ex}$')
ax[1][1].set_xlabel('$g_{ex}$')

plt.savefig(f'../data/v{v}_batch1/'+f'SpaceParam_{v}_neigh_gex.png', dpi=600, bbox_inches='tight', format='png')
plt.show()