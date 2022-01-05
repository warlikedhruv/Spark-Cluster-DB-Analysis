# Spark-Cluster-DB-Analysis

## Stand-Alone Cluster in Docker machine

Inside Cluster-Image "build.sh" will build image and compose cluster
### For Linux Machines
```bash
sh build.sh
```
### For Windows Machines with git bash
```bash
bash build.sh
```


## To Run Spark-submit for testing
### For Linux Machines
```commandline
sh job-submit.sh
```

### For Windows Machine with git bash
```commandline
bash job-submit.sh
```
This script will submit the job to spark master and produce the output

This image will make a spark cluster with two workers and one master handling the process. 

localhost:8888 will be for Jupyer Notebook for testing
localhost:8080 will be for master node for spark ui
