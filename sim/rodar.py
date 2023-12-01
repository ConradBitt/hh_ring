import os

rodar = """#!/bin/bash
#SBATCH --nodes=1                    # node
#SBATCH --ntasks-per-node=128        # tasks per node
#SBATCH --time=1:00:00               # time limits: 1 hour
#SBATCH --partition=compute
#SBATCH --account=TG-IBN140002
#SBATCH --export=ALL
#SBATCH --mail-user=conrad.bittencourt@gmail.com
#SBATCH --mail-type=end
"""

resolution_space_param = 32 # 32 x 32

command = lambda i, j : f'python init.py simConfig=../data/v1_batch1/v1_batch1_{i}_{j}_cfg.json netParams=../data/v1_batch1/v1_batch1_netParams.py'

for i in range(resolution_space_param):
    for j in range(resolution_space_param):
        rodar += command(i,j) + '\n'

print(rodar)

with open('rodar.sh', 'w+') as rodar_sh:
    rodar_sh.writelines(rodar)

# os.system('sbatch rodar.sh')
