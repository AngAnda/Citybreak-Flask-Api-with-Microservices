FROM microskel

ADD . /opt/gateway
WORKDIR /opt/gateway

RUN pip install -r requirements.txt

CMD ["python", "service_gateway.py"]
