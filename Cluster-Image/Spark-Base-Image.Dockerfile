FROM cluster-base

# -- Layer: Apache Spark

ARG spark_version=3.0.0
ARG hadoop_version=2.7

#install Spak Cluster
RUN apt-get update -y && \
    apt-get install -y curl && \
    curl https://archive.apache.org/dist/spark/spark-${spark_version}/spark-${spark_version}-bin-hadoop${hadoop_version}.tgz -o spark.tgz && \
    tar -xf spark.tgz && \
    mv spark-${spark_version}-bin-hadoop${hadoop_version} /usr/bin/ && \
    mkdir /usr/bin/spark-${spark_version}-bin-hadoop${hadoop_version}/logs && \
    rm spark.tgz

RUN apt update -y && \
    apt install -y git && \
    apt-get install wget && \
    wget https://dev.mysql.com/get/Downloads/Connector-J/mysql-connector-java-8.0.27.tar.gz -O mysql-connector.tar.gz && \
    tar -xf mysql-connector.tar.gz && \
    mv mysql-connector-java-8.0.27/mysql-connector-java-8.0.27.jar /usr/bin/spark-${spark_version}-bin-hadoop${hadoop_version}/jars/ && \
    rm -r mysql-connector-java-8.0.27 && \
    rm mysql-connector.tar.gz

#Git Code Fetch
RUN git clone https://github.com/warlikedhruv/Spark-Cluster-DB-Analysis.git && \
    mv Spark-Cluster-DB-Analysis/Spark-Code /usr/bin/spark-${spark_version}-bin-hadoop${hadoop_version}/ && \
    rm -r Spark-Cluster-DB-Analysis


ENV SPARK_HOME /usr/bin/spark-${spark_version}-bin-hadoop${hadoop_version}
ENV SPARK_MASTER_HOST spark-master
ENV SPARK_MASTER_PORT 7077
ENV PYSPARK_PYTHON python3

# -- Runtime

WORKDIR ${SPARK_HOME}