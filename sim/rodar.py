""" Expanse components
System Component                    Configuration
0   AMD Rome Standard Compute Nodes  AMD Rome Standard Compute Nodes
1                        Node count                              728
2                       Clock speed                         2.25 GHz
3                        Cores/node                              128
4                         DRAM/node                           256 GB
5                         NVMe/node                             1 TB
6   NVIDIA V100 GPU Nodes            NVIDIA V100 GPU Nodes
7                        Node count                               52
8                    CPU cores/node                               40
9                          CPU Type                        6248 Xeon
10                  CPU Clock speed                          2.5 GHz
11                    CPU DRAM/node                           384 GB
12                        GPUs/node                                4
13                         GPU Type                        V100 SMX2
14                       Memory/GPU                            32 GB
15                        NVMe/node                           1.6 TB
16  Large-memory AMD Rome Nodes      Large-memory AMD Rome Nodes
17                       Node count                                4
18                      Clock speed                         2.25 GHz
19                       Cores/node                              128
20                        DRAM/node                             2 TB
21                  SSD memory/node                           3.2 TB
22                  Storage Systems                  Storage Systems
23                     File systems                     Lustre, Ceph
24                   Lustre Storage                            12 PB
25                     Ceph Storage                             7 PB
"""

import os

rodar = """#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=128
#SBATCH --time=01:30:00
#SBATCH --partition=compute
#SBATCH --account=TG-IBN140002
#SBATCH --export=ALL
#SBATCH --mail-user=conrad.bittencourt@gmail.com
#SBATCH --mail-type=end


"""

resolution_space_param = 32
v = 2
##########
# demora mas funciona
# é mais eficiente splitar as chamadas rodar.sh em lotes
#~~~~~>> "mpiexec -n 1 nrniv -python -mpi init.py" funciona com 1 nodo e 128 tasks
##########
init = lambda i, j: f'mpiexec -n 1 nrniv -python -mpi init.py simConfig=../data/v{v}_batch1/v{v}_batch1_{i}_{j}_cfg.json netParams=../data/v{v}_batch1/v{v}_batch1_netParams.py'
preprocessing = lambda i, j: f'mpiexec -n 1 python3 preprocessing.py {v} {i} {j}'

for i in range(resolution_space_param):
    for j in range(resolution_space_param):
        # rodar += f'{init(i, j)} && {preprocessing(i,j)} &\n'
        rodar += f'{preprocessing(i,j)} &\n'

rodar = rodar[:-3]  # Remove the trailing '&&'
with open('rodar.sh', 'w+') as rodar_sh:
    rodar_sh.writelines(rodar)
print(rodar)
os.system('sbatch rodar.sh')


