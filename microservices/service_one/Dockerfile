FROM microskel

ADD . /opt/service_one
WORKDIR /opt/service_one

RUN pip install -r requirements.txt

CMD ["python", "service_one.py"]
