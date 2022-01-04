from pyspark.sql import SparkSession
import os
def connect_to_sql(
    spark, jdbc_hostname, jdbc_port, database, data_table, username, password
):
    jdbc_url = "jdbc:mysql://{0}:{1}/{2}".format(jdbc_hostname, jdbc_port, database)

    connection_details = {
        "user": username,
        "password": password,
        "driver": "com.mysql.cj.jdbc.Driver",
    }

    df = spark.read.jdbc(url=jdbc_url, table=data_table, properties=connection_details)
    return df

if __name__=='__main__':
    mysql_path = os.getcwd()+ "/mysql-connector-java-5.1.34"
    spark = SparkSession \
        .builder \
        .appName('test') \
        .master('local[*]') \
        .enableHiveSupport() \
        .config("spark.driver.extraClassPath", mysql_path ) \
        .getOrCreate()

    df = connect_to_sql(spark, 'localhost', '3306', 'AMS', 'crew', 'root', 'password')