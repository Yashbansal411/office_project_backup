from python:3.8

RUN  apt-get update

RUN mkdir -p /app/logs

WORKDIR /app

COPY requirment.txt /app

RUN pip3 install -r requirment.txt

COPY . /app

EXPOSE 8080

ENTRYPOINT ["python3"]

CMD ["count_substring.py"]
