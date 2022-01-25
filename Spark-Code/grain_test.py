from pyspark.sql import SparkSession
import os
from pyspark.sql.functions import col, array, when, array_remove, lit
import pyspark.sql.functions as f
import argparse

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
    # conditions_ = [when(original_table_df[c] != target_table_df[c], str(c)).otherwise("")
    #                for c in original_table_df.columns if c != primary_key]

    # select_expr = [
    #     col(primary_key),
    #     *[target_table_df[c] for c in target_table_df.columns if c != primary_key],
    #     array_remove(array(*conditions_), "").alias("column_names")
    # ]
    #
    # original_table_df.join(target_table_df, primary_key).select(*select_expr).show(original_table_df.count())

    columns = original_table_df.columns
    df3 = original_table_df.alias("d1").join(target_table_df.alias("d2"), f.col("d1.id") == f.col("d2.id"), "left")

    for name in columns:
        df3 = df3.withColumn(name + "_temp", f.when(f.col("d1." + name) != f.col("d2." + name), f.lit(name)))

    df3.withColumn("column_names", f.concat_ws(",", *map(lambda name: f.col(name + "_temp"), columns))).select("d1.*",
                                                                                                               "column_names").show(original_table_df.count())

def compare_2(original_table_df, target_table_df, primary_key):
    new_column_name_list_1 = list(map(lambda x: "Expected_"+x, original_table_df.columns))
    df_Expected = original_table_df.toDF(*new_column_name_list_1)

    new_column_name_list_2 = list(map(lambda x: "Actual_" + x, target_table_df.columns))
    df_Actual = target_table_df.toDF(*new_column_name_list_2)

    # these are the fields you want to compare
    df_cobined = df_Actual.join(df_Expected, (df_Actual.Actual_id == df_Expected.Expected_id))
    col_names = df_Actual.schema.names
    df_cobined.show(30)
    col_names = original_table_df.schema.names
    to_compare = [c for c in original_table_df.columns if c != "id"]
    df_new = df_cobined.select(
        "Actual_"+primary_key,
        f.array([
            f.when(
                f.col("Actual_" + c) != f.col("Expected_" + c),
                f.struct(
                    f.col("Actual_"+c).alias("Actual_value"),
                    f.col("Expected_" + c).alias("Expected_value"),
                    f.lit("Actual_"+ c).alias("Field")
                )
            ).alias(c)
            for c in to_compare
        ]).alias("temp")
    ) \
        .select("id", f.explode("temp")) \
        .dropna() \
        .select("id", "col.*")
    df_new.show()

def main(source_table_config,target_table_config ):
    """

    :param source_table_config: Dict with db connections
    :param target_table_config: Dict with db connections
    :return: None
    """
    mysql_path = "/usr/bin/spark-3.0.0-bin-hadoop2.7/mysql-connector-java-8.0.27.jar"
    spark = SparkSession \
        .builder \
        .appName('test') \
        .master('local[*]') \
        .enableHiveSupport() \
        .config("spark.driver.extraClassPath", mysql_path) \
        .getOrCreate()

    source_df = create_df(spark, source_table_config)
    target_df = create_df(spark, target_table_config)
    compare_df(source_df, target_df, primary_key="id")
    compare_2(source_df, target_df, primary_key="id")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--SourceHostName', type=str, required=True)
    parser.add_argument('--SourcePort', type=str, required=True)
    parser.add_argument('--SourceDatabase', type=str, required=True)
    parser.add_argument('--SourceTableOrQuery', type=str, required=True)
    parser.add_argument('--SourceUser', type=str, required=True)
    parser.add_argument('--SourcePassword', type=str, required=True)

    parser.add_argument('--TargetHostName', type=str, required=True)
    parser.add_argument('--TargetPort', type=str, required=True)
    parser.add_argument('--TargetDatabase', type=str, required=True)
    parser.add_argument('--TargetTableOrQuery', type=str, required=True)
    parser.add_argument('--TargetUser', type=str, required=True)
    parser.add_argument('--TargetPassword', type=str, required=True)
    args = parser.parse_args()
    source_table_config = {"hostname": args.SourceHostName, "port": args.SourcePort, "database": args.SourceDatabase,
                           "table_or_query": args.SourceTableOrQuery, "user": args.SourceUser, "password":args.SourcePassword}
    target_table_config = {"hostname": args.TargetHostName, "port": args.TargetPort, "database": args.TargetDatabase,
                           "table_or_query": args.TargetTableOrQuery, "user": args.TargetUser, "password": args.TargetPassword}

    main(source_table_config, target_table_config)
