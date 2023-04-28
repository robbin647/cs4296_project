# Clustering Trick on Handling User Requests in Cloud Computing
## CS4296 Group Porject

## Our artifact

We implemented a container scheduling algorithm featuring request clustering, as
an improvement to the [**dependency scheduling**](https://www.usenix.org/system/files/hotedge20_paper_fu.pdf) algorithm proposed by Fu et al. [1].
In experimenting with our scheduler, we also adpted a Python-based [simulator](https://github.com/depsched/sim) authored by them,
to whom we should give the most credit.

[1] Fu, S., Mittal, R., Zhang, L. and Ratnasamy, S., 2020, June. Fast and Efficient Container Startup at the Edge via Dependency Scheduling. In HotEdge.

## How to use our artifact

Please see the [run_container.sh](./run_container.sh) script for commands to download the readily built container
from the docker hub repo and to initiate simulation in our container.

Once the simulation finishes, please run the [cdf_plot.py](./cdf_plot.py) Python script *in the container* to obtain a latency CDF graph of the four algorithms (monkey, kube, dep, req-cluster) used in the simulation.

## Sample simulation result
Please refer [here](https://drive.google.com/file/d/1PDHoBa4pW9wwuImOo599P91JvHw7bGDs/view?usp=share_link) for a sample of simulation result running our and other three sheduling algorithms.

