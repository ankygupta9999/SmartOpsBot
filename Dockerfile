FROM ubuntu:18.04
ENTRYPOINT []

RUN apt-get update && apt-get install -y python3 python3-pip && python3 -m pip install --no-cache --upgrade pip && pip3 install --no-cache rasa==2.8.13 --use-feature=2020-resolver && pip3 install spacy && python3 -m spacy download "en_core_web_sm"
ADD . /app/
RUN chmod +x /app/start_services.sh
CMD /app/start_services.sh
