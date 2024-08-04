FROM microskel

ADD . /opt/service_two
WORKDIR /opt/service_two

RUN pip install -r requirements.txt

CMD ["python", "service_two.py"]
