#!/bin/bash

./bin/spark-submit --jars /usr/bin/spark-3.0.0-bin-hadoop2.7/jars/mysql-connector-java-8.0.27.jar --master local[1]  /usr/bin/spark-3.0.0-bin-hadoop2.7/Spark-Code/grain_test.py