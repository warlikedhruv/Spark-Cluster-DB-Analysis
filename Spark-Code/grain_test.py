from pyspark.sql import SparkSession
import os
from pyspark.sql.functions import col, array, when, array_remove


def connect_to_sql(spark, jdbc_hostname, jdbc_port, database, data_table, username, password):
    """

    :param spark:
    :param jdbc_hostname:
    :param jdbc_port:
    :param database:
    :param data_table:
    :param username:
    :param password:
    :return:
    """
    jdbc_url = "jdbc:mysql://{0}:{1}/{2}".format(jdbc_hostname, jdbc_port, database)

    connection_details = {
        "user": username,
        "password": password,
        "driver": "com.mysql.cj.jdbc.Driver",
    }

    df = spark.read.jdbc(url=jdbc_url, table=data_table, properties=connection_details)
    return df


def create_df(spark, connection_config: dict):
    """

    :param spark:
    :param connection_config:
    :return:
    """
    table_df = connect_to_sql(spark, connection_config['hostname'], connection_config['port'],
                              connection_config['database'],
                              connection_config['table_or_query'], connection_config['user'],
                              connection_config['password'])
    return table_df


def compare_df(original_table_df, target_table_df, primary_key):
    """

    :param original_table_df:
    :param target_table_df:
    :param primary_key:
    :return:
    """
    conditions_ = [when(original_table_df[c] != target_table_df[c], [c,original_table_df[c], target_table_df[c]]).otherwise("") for c in original_table_df.columns if c != primary_key]

    select_expr = [
        col(primary_key),
        *[target_table_df[c] for c in target_table_df.columns if c != primary_key],
        array_remove(array(*conditions_), "").alias("column_names")
    ]

    original_table_df.join(target_table_df, primary_key).select(*select_expr).show(original_table_df.count())


def main():
    """

    :return:
    """
    mysql_path = "/usr/bin/spark-3.0.0-bin-hadoop2.7/mysql-connector-java-8.0.27.jar"
    spark = SparkSession \
        .builder \
        .appName('test') \
        .master('local[*]') \
        .enableHiveSupport() \
        .config("spark.driver.extraClassPath", mysql_path) \
        .getOrCreate()
    source_table_config = {"hostname": "host.docker.internal", "port": "3306", "database": "spark_test_db1",
                           "table_or_query": "dummy_data_1", "user": "root", "password": "password"}
    target_table_config = {"hostname": "host.docker.internal", "port": "3306", "database": "spark_test_db1",
                           "table_or_query": "dummy_data_2", "user": "root", "password": "password"}

    source_df = create_df(spark, source_table_config)
    target_df = create_df(spark, target_table_config)
    compare_df(source_df, target_df, primary_key="id")

if __name__ == '__main__':
    main()
