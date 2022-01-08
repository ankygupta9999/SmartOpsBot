#!/bin/sh

# Start rasa server with nlu model
rasa run --enable-api --cors "*"  --debug