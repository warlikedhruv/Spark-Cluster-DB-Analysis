# Spark-Cluster-DB-Analysis

## Stand-Alone Cluster in Docker machine

Inside Cluster-Image "build.sh" will be used to for image and docker-compose file will be used to run containers
```bash
sh build.sh
```
```bash
docker-compose up
```

This image will make a spark cluster with two workers and one master handling the process. 

localhost:8888 will be for Jupyer Notebook for testing
localhost:8080 will be for master node for spark ui
