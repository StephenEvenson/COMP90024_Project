#!/bin/sh
whoami
while :
  do
    /data/app/wait-for-it.sh "$NLP_HOST":"$NLP_PORT" --timeout=5
    # shellcheck disable=SC2181
    if [ $? -eq 0 ]; then
      # shellcheck disable=SC2039
      echo -e "\033[42;34m nlp_server is ok \033[0m"
      python mastodon_harvester.py
      break
    else
      sleep 5
    fi
  done