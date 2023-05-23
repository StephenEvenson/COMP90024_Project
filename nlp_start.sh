#!/bin/sh

python backend/nlp/abusive_interface.py
python backend/nlp/search_interface.py
python backend/nlp/sentiment_interface.py
whoami
while :
  do
    /data/app/wait-for-it.sh "$COUCHDB_HOST":"$COUCHDB_PORT" --timeout=5
    # shellcheck disable=SC2181
    if [ $? -eq 0 ]; then
      # shellcheck disable=SC2039
      echo -e "\033[42;34m couchdb is ok \033[0m"
      uvicorn backend.nlp.nlp_server:app --host 0.0.0.0 --port 8000 --reload
      break
    else
      sleep 5
    fi
  done