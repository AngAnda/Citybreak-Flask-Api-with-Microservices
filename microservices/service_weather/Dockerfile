FROM microskel

ADD . /opt/service_weather
WORKDIR /opt/service_weather

RUN pip install -r requirements.txt
ENV REDIS_HOST=redis-db
ENV REDIS_PORT=6379
ENV REDIS_PASSWORD=yourpassword

CMD ["python", "service_weather.py"]
