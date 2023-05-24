#!/bin/sh

echo "start backend server"
while :
  do
    /data/app/wait-for-it.sh "$WRITE_DB_PORT":"$WRITE_DB_PORT" --timeout=5
    # shellcheck disable=SC2181
    if [ $? -eq 0 ]; then
      # shellcheck disable=SC2039
      echo -e "\033[42;34m couchdb is ok \033[0m"
      uvicorn uvicorn main:app --host 0.0.0.0 --port 8000 --reload
      break
    else
      sleep 5
    fi
  done