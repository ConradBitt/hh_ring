"""
batch.py 

Influence if slow potassium and Ca channels in bistable firing patterns using NetPyNE

Contributors: protachevicz@gmail.com, fernandodasilvaborges@gmail.com
"""

from netpyne.batch import Batch
from netpyne import specs
import numpy as np
import sys

try:
    from __main__ import cfg  # import SimConfig object with params from parent module
except:
    from cfg import cfg

# ----------------------------------------------------------------------------------------------
# Custom
# ----------------------------------------------------------------------------------------------
def custom():
    params = specs.ODict()
    
    # params[('seeds', 'conn')] =  [1] 
    # params[('IClamp0', 'amp')] = [0.08, 0.10, 0.12] 
    # params[('gex')] = [round(1e-5*vv, 6) for vv in range(20,34,2)]
    # params[('n_neighbors')] = [vv for vv in range(20, 55,5)]

    # params[('gex')] = [np.round(1e-5*vv, 6) for vv in range(2,66,5)]  # 32 elements
    # params[('n_neighbors')] = [vv for vv in range(2,66,5)]  # 32 elements

    params[('gex')] = [float(sys.argv[3])]
    arg_conns = [value.replace('[','').replace(']','').replace(',','').replace("'",'') for value in sys.argv[4:]]
    params[('n_neighbors')] = np.array([int(value) for value in arg_conns if value != '']).astype('int64')

    b = Batch(params=params, netParamsFile='netParams.py', cfgFile='cfg.py')

    return b

# ----------------------------------------------------------------------------------------------
# Run configurations
# ----------------------------------------------------------------------------------------------
def setRunCfg(b, type='mpi_bulletin'):
    if type=='mpi_bulletin' or type=='mpi':
        b.runCfg = {'type': 'mpi_bulletin', 
            'script': 'init.py', 
            'skip': True}

    elif type=='mpi_direct':
        b.runCfg = {'type': 'mpi_direct',
            'cores': 20,
            'script': 'init.py',
            'mpiCommand': 'mpiexec', # i7  --use-hwthread-cpus
            'skip': True}

    elif type=='mpi_direct2':
        b.runCfg = {'type': 'mpi_direct',
            'mpiCommand': 'mpirun -n 12 ./x86_64/special -mpi -python init.py', # --use-hwthread-cpus
            'skip': True}

    elif type=='hpc_slurm_gcp':
        b.runCfg = {'type': 'hpc_slurm',
            'allocation': 'default',
            'walltime': '24:00:00',
            'nodes': 1,
            'coresPerNode': 80,
            'email': 'conrad.bittencourt@gmail.com',
            'folder': '/home/ext_conrad.bittencourt_gmail_/S1_mouse/sim/',
            'script': 'init.py',
            'mpiCommand': 'mpirun',
            'skipCustom': '_raster.png'}
        
    elif type == 'hpc_slurm_Expanse':
        b.runCfg = {'type': 'hpc_slurm',
                    'allocation': 'TG-IBN140002',
                    'partition': 'compute',
                    'walltime': '00:30:00',
                    'nodes': 1,
                    # 'coresPerNode': 20,
                    'coresPerNode': int(cfg.coresPerNode),
                    # 'email': 'conrad.bittencourt@gmail.com',
                    'folder': '/home/fborges/hh_ring/sim/',
                    'script': 'init.py',
                    'mpiCommand': 'mpirun',
                    'custom': '#SBATCH --mem=249325M\n#SBATCH --export=ALL\n#SBATCH --partition=compute',
                    'skip': True}
        
    elif type == 'hpc_slurm_Expanse_debug':
        b.runCfg = {'type': 'hpc_slurm',
                    'allocation': 'TG-IBN140002',
                    'partition': 'debug',
                    'walltime': '1:00:00',
                    'nodes': 1,
                    'coresPerNode': 64,
                    'email': 'conrad.bittencourt@gmail.com',
                    'folder': '/home/fborges/hh_ring/sim/',
                    'script': 'init.py',
                    'mpiCommand': 'mpirun',
                    'custom': '#SBATCH --mem=249325M\n#SBATCH --export=ALL\n#SBATCH --partition=debug',
                    'skip': True}

# ----------------------------------------------------------------------------------------------
# Main code
# ----------------------------------------------------------------------------------------------
if __name__ == '__main__': 
    b = custom() #
    # 
    version_number = sys.argv[1]
    batch_number = sys.argv[2]
    batch_number = batch_number.zfill(4) # fill string with zeros.

    b.batchLabel = f'v{version_number}_batch{batch_number}' #cfg.simLabel  # default: 'v0_batch0'
        
    cfg.simLabel = b.batchLabel
    b.saveFolder = '../data/'+b.batchLabel
    b.method = 'grid'
    setRunCfg(b, 'hpc_slurm_Expanse')     # setRunCfg(b, 'mpi_bulletin')
    b.run() # run batch

# if __name__ == '__main__': 
#     b = custom() #

#     b.batchLabel = 'v1_batch4'  
#     b.saveFolder = '../data/'+b.batchLabel
#     b.method = 'grid'
#     setRunCfg(b, 'hpc_slurm_Expanse') # hpc_slurm_Expanse  setRunCfg(b, 'hpc_slurm_Cineca_debug') # setRunCfg(b, 'hpc_slurm_Expanse')
#     b.run() # run batch
