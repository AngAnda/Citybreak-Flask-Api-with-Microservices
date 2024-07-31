FROM microskel

ADD . /opt/service_events
WORKDIR /opt/service_events

RUN pip install -r requirements.txt

CMD ["python", "service_events.py"]
