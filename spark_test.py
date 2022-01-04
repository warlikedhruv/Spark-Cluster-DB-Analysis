from pyspark.sql import SparkSession
import os
from pyspark.sql.functions import col, array, when, array_remove

def connect_to_sql(spark, jdbc_hostname, jdbc_port, database, data_table, username, password):
    jdbc_url = "jdbc:mysql://{0}:{1}/{2}".format(jdbc_hostname, jdbc_port, database)

    connection_details = {
        "user": username,
        "password": password,
        "driver": "com.mysql.cj.jdbc.Driver",
    }

    df = spark.read.jdbc(url=jdbc_url, table=data_table, properties=connection_details)

    return df

def compare_df(df1, df2):
    conditions_ = [when(df1[c] != df2[c], str(c)).otherwise("") for c in df1.columns if c != 'id']

    select_expr = [
        col("id"),
        *[df2[c] for c in df2.columns if c != 'id'],
        array_remove(array(*conditions_), "").alias("column_names")
    ]

    df1.join(df2, "id").select(*select_expr).show(truncate = False)


if __name__ == '__main__':
    mysql_path = "/usr/bin/spark-3.0.0-bin-hadoop2.7/mysql-connector-java-8.0.27.jar"
    spark = SparkSession \
        .builder \
        .appName('test') \
        .master('local[*]') \
        .enableHiveSupport() \
        .config("spark.driver.extraClassPath", mysql_path) \
        .getOrCreate()

    df1 = connect_to_sql(spark, 'host.docker.internal', '3306', 'spark_test_db1', 'dummy_data_1', 'root', 'password')
    df2 = connect_to_sql(spark, 'host.docker.internal', '3306', 'spark_test_db1', 'dummy_data_2', 'root', 'password')
    print("DATA FRAME CREATED")
    print(df1.show())
    print(df2.show())
    compare_df(df1, df2)

