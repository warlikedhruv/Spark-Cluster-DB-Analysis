#!/bin/bash

SourceHostName=$1
SourcePort=$2
SourceDatabase=$3
SourceTableOrQuery=$4
SourceUser=$5
SourcePassword=$6
TargetHostName=$7
TargetPort=$8
TargetDatabase=$9
TargetTableOrQuery=${10}
TargetUser=${11}
TargetPassword=${12}

#echo "$SourceHostName"
#echo "$SourcePort"
#echo "$SourceDatabase"
#echo "$SourceTableOrQuery"
#echo "$SourceUser"
#echo "$SourcePassword"
#echo "$TargetHostName"
#echo "$TargetPort"
#echo "$TargetDatabase"
#echo "$TargetTableOrQuery"
#echo "$TargetUser"
#echo "$TargetPassword"

/usr/bin/spark-3.0.0-bin-hadoop2.7/bin/spark-submit \
--jars /usr/bin/spark-3.0.0-bin-hadoop2.7/jars/mysql-connector-java-8.0.27.jar \
--master local[1]  \
/usr/bin/spark-3.0.0-bin-hadoop2.7/Spark-Code/grain_test.py \
--SourceHostName "$SourceHostName" --SourcePort "$SourcePort" \
--SourceDatabase "$SourceDatabase" --SourceTableOrQuery "$SourceTableOrQuery" \
--SourceUser "$SourceUser" --SourcePassword "$SourcePassword" --TargetHostName "$TargetHostName" \
--TargetPort "$TargetPort" --TargetDatabase "$TargetDatabase" --TargetTableOrQuery "$TargetTableOrQuery" \
--TargetUser "$TargetUser" --TargetPassword "$TargetPassword"
