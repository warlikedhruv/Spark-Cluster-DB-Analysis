# shellcheck disable=SC2046
export $(grep -v '^#' "$PWD"/.env | xargs)

# shellcheck disable=SC2154
docker exec -it spark-master sh Spark-Code/job-submit-spark.sh \
"$SOURCE_HOST_NAME" "$SOURCE_PORT" \
"$SOURCE_DATABASE" "$SOURCE_TABLE_OR_QUERY" \
"$SOURCE_USER" "$SOURCE_PASSWORD" "$TARGET_HOST_NAME" \
"$TARGET_PORT" "$TARGET_DATABASE" "$TARGET_TABLE_OR_QUERY" \
"$TARGET_USER" "$TARGET_PASSWORD"