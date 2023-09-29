# hh_ring

## Getting Started
### Prerequisites

This repository has dependencies with languages C and Python (version to be defined). It is advisable to [create a unique python virtual environment](https://docs.python.org/3.10/library/venv.html) to use the necessary packages. If you prefer, you can use [conda enviroment](https://conda.io/projects/conda/en/latest/user-guide/index.html). This project relies on Open MPI, an open-source Message Passing Interface implementation, for parallel computing tasks. You can install Open MPI using the package manager specific to your operating system.

After creating the environment, packages can be installed in the standard way from the Python Package Index (PyPI).

You can see the individual version of each package in the [requirements.txt](requirements.txt) file.

Some results are shown via [Jupyter Notebook](https://jupyter.org/install), so it's important to have it installed.

### Installation

1. Create a virtual enviroment with [venv](https://docs.python.org/3.10/library/venv.html) python package or [conda](https://conda.io/projects/conda/en/latest/user-guide/index.html). Activate the virtual enviroment and install packages with pip:

        pip install -r requirements.txt
        
2. For parallel computing install MPI: [Quick start: Installing Open MPI](https://docs.open-mpi.org/en/v5.0.x/installing-open-mpi/quickstart.html)


## How to Use
First, in the “simulations_one_cell” or “simulations_network” folder, run “nrnivmodl” in the terminal to compile the NEURON files. This must only be done once.

# First Result
![img](https://github.com/ConradBitt/hh_ring/blob/main/data/v0_batch0/v0_batch0_raster.png)
