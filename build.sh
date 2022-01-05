# -- Software Stack Version

SPARK_VERSION="3.0.0"
HADOOP_VERSION="2.7"
JUPYTERLAB_VERSION="2.1.5"

# -- Building the Images

docker build \
  --no-cache \
  -f ./Cluster-Image/Cluster-Base-Image.Dockerfile \
  -t cluster-base .

docker build \
  --no-cache \
  --build-arg spark_version="${SPARK_VERSION}" \
  --build-arg hadoop_version="${HADOOP_VERSION}" \
  -f ./Cluster-Image/Spark-Base-Image.Dockerfile \
  -t spark-base .

docker build \
  --no-cache \
  -f ./Cluster-Image/Spark-Master-Image.Dockerfile \
  -t spark-master .

docker build \
  --no-cache \
  -f ./Cluster-Image/Spark-Worker-Image.Dockerfile \
  -t spark-worker .

docker build \
  --build-arg spark_version="${SPARK_VERSION}" \
  --build-arg jupyterlab_version="${JUPYTERLAB_VERSION}" \
  -f ./Cluster-Image/jupyterlab.Dockerfile \
  -t jupyterlab .


docker-compose up