# Note: This script lists the commands to run the container
#       In short, you should run the first group of commands on your computer,
#       and run the second and thrid group of commands inside the container.
#

# on your computer: pull the image and start the container
docker pull robbinyang/container-scheduling:v2
docker run --name cs4296_serverless -it -d --previleged=true robbinyang/container-scheduling:v1 /sbin/init
docker exec -it cs4296_serverless /bin/bash

# inside the container: update source code
cd /home/tianxia/depsched
git remote add github https://github.com/robbin647/cs4296_project.git
git pull github main

# inside the container: run simulation
/home/tianxia/run_simulator.sh 

# inside the container: visualize the result
export PYTHONPATH="/home/tianxia/SOFTWARE/depsched_pyenv/lib/python3.10/site-packages:$PYTHONPATH"
python3 /home/tianxia/depsched/cdf_plot.py
