FROM rasa/rasa:2.8.13

COPY app /app
COPY server.sh /app/server.sh

RUN pip install spacy
RUN python -m spacy download en_core_web_sm

USER root
RUN chmod -R 777 /app
USER 1001

# RUN python -m venv /opt/venv && \
#   . /opt/venv/bin/activate && pip install spacy  

# make sure we use the virtualenv
# ENV PATH="/opt/venv/bin:$PATH"

# RUN pip install spacy  
# RUN python -m spacy download en_core_web_sm

RUN rasa train nlu
ENTRYPOINT ["/app/server.sh"]