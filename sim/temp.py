import re
import time 
import numpy as np
# arquivos_nao_lidos = """batch1_18_0_data
# batch1_18_1_data
# batch1_18_2_data
# batch1_19_1_data
# batch1_30_0_data"""

# arquivos_faltando = [(int(b[0]), int(b[1]))for b in [re.findall('\d+',s[6:]) for s in arquivos_nao_lidos.split('\n')]]

arquivos = [(i,j) for i in range(32) for j in range(32)]


rodar = """#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=128
#SBATCH --time=02:30:00
#SBATCH --partition=compute
#SBATCH --account=TG-IBN140002
#SBATCH --export=ALL
#SBATCH --mail-user=conrad.bittencourt@gmail.com
#SBATCH --mail-type=end


"""
v = 3
init = lambda i, j: f'mpiexec -n 1 nrniv -python -mpi init.py simConfig=../data/v{v}_batch1/v{v}_batch1_{i}_{j}_cfg.json netParams=../data/v{v}_batch1/v{v}_batch1_netParams.py'
preprocessing = lambda i, j: f'mpiexec -n 1 python3 preprocessing.py {v} {i} {j}'


lotes = np.array_split(arquivos,64)

rodar_lote = len(lotes)*[rodar]

for indice_lote, lote in enumerate(lotes):
    for l in lote:
        i, j = l
        rodar_lote[indice_lote] += f'{init(i,j)} && {preprocessing(i,j)} &\n'
    rodar_lote[indice_lote] = rodar_lote[indice_lote][:-3]

import os


for indice_lote,rodar in enumerate(rodar_lote):
    with open(f'rodar{indice_lote}.sh', 'w+') as rodar_sh:
        rodar_sh.writelines(rodar)
    print(rodar)
    # os.system(f'sbatch rodar{indice_lote}.sh')
    # time.sleep(3600)