from python:3.8

RUN apt-get update

RUN mkdir -p /app/logs/

WORKDIR /app

COPY requirment.txt /app

RUN pip3 install -r requirment.txt

COPY . /app

CMD ["celery", "-A", "count_substring", "worker", "-l", "info", "-c", "4", "-f", "/app/logs/work.log"]
