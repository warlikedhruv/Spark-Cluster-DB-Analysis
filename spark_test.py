# from pyspark.sql import SparkSession
# import os
#
#
# def connect_to_sql(spark, jdbc_hostname, jdbc_port, database, data_table, username, password):
#     jdbc_url = "jdbc:mysql://{0}:{1}/{2}".format(jdbc_hostname, jdbc_port, database)
#
#     connection_details = {
#         "user": username,
#         "password": password,
#         "driver": "com.mysql.cj.jdbc.Driver",
#     }
#
#     df = spark.read.jdbc(url=jdbc_url, table=data_table, properties=connection_details)
#     return df
#     # print("os path", os.getcwd())
#     # mysql_path = os.getcwd() + "/mysql-connector-java-5.1.34.jar"
#     # print("MY SQL PATh", mysql_path)
#     # print("ABS PATH", os.path.abspath(os.getcwd()))
#     # if os.path.exists(mysql_path):
#     #     print("SQL PATH EXISTS")
#     # else:
#     #     print("SQL PATH DOES NOT EXISTS")
#     # return None
#
#
#
# if __name__ == '__main__':
#     mysql_path = os.getcwd() + "/mysql-connector-java-5.1.34.jar"
#     spark = SparkSession \
#         .builder \
#         .appName('test') \
#         .master('local[*]') \
#         .enableHiveSupport() \
#         .config("spark.driver.extraClassPath", mysql_path) \
#         .getOrCreate()
#
#     df = connect_to_sql(spark, 'localhost', '3306', 'AMS', 'crew', 'root', 'password')

import os

import pyspark # only run after findspark.init()
from pyspark.sql import SparkSession
from pyspark import SparkConf, SparkContext

# SUBMIT_ARGS = "--packages mysql:" + os.getcwd()+ "/mysql-connector-java:5.1.34 pyspark-shell"
# os.environ["PYSPARK_SUBMIT_ARGS"] = SUBMIT_ARGS
# conf = SparkConf()
spark = SparkSession.builder.getOrCreate()

dataframe_mysql = spark.read.format("jdbc").options(
    url="jdbc:mysql://db.cs.dal.ca:3306/dhruvkumar",
    driver = "com.mysql.cj.jdbc.Driver",
    dbtable = "company",
    user="dhruvkumar",
    password="Wp6CRupcXtdqWnW96CQXKcMcD").load()

dataframe_mysql.show()