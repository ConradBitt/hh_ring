#!/bin/bash
#SBATCH --nodes=1                    # node
#SBATCH --ntasks-per-node=128   # tasks per node
#SBATCH --time=22:00:00               # time limits: 1 hour
#SBATCH --partition=compute
#SBATCH --account=TG-IBN140002
#SBATCH --export=ALL
#SBATCH --mail-user=conrad.bittencourt@gmail.com
#SBATCH --mail-type=end

python init.py simConfig=../data/v1_batch1/v1_batch1_0_1_cfg.json netParams=../data/v1_batch1/v1_batch1_netParams.py
python init.py simConfig=../data/v1_batch1/v1_batch1_0_2_cfg.json netParams=../data/v1_batch1/v1_batch1_netParams.py
python init.py simConfig=../data/v1_batch1/v1_batch1_1_1_cfg.json netParams=../data/v1_batch1/v1_batch1_netParams.py
python init.py simConfig=../data/v1_batch1/v1_batch1_1_2_cfg.json netParams=../data/v1_batch1/v1_batch1_netParams.py
