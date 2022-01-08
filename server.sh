#!/bin/sh

# cd app/
# python -m spacy download en_core_web_sm

if [ -z "$PORT"]
then
  PORT=5005
fi

# Start rasa server with nlu model
rasa run --enable-api --cors "*" -p 5005 --debug