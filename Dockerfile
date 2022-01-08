FROM rasa/rasa:2.8.13

COPY app /app
COPY server.sh /app/server.sh

USER root
RUN chmod -R 777 /app
USER 1001

RUN python3 -m pip install --no-cache --upgrade pip && pip3 install spacy 
RUN python -m spacy download en_core_web_sm

RUN rasa train nlu
ENTRYPOINT ["/app/server.sh"]