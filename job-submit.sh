# shellcheck disable=SC2046
export $(grep -v '^#' .env | xargs)

# shellcheck disable=SC2154
docker exec -it spark-master sh Spark-Code/job-submit-spark.sh \
"$SourceHostName" "$SourcePort" \
"$SourceDatabase" "$SourceTableOrQuery" \
"$SourceUser" "$SourcePassword" "$TargetHostName" \
"$TargetPort" "$TargetDatabase" "$TargetTableOrQuery" \
"$TargetUser" "$TargetPassword"