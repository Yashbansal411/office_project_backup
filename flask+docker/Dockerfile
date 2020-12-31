from ubuntu:20.04

RUN apt-get update

RUN  apt-get install -y python3-pip 

WORKDIR /app

COPY . /app

RUN pip3 install flask

RUN pip3 install celery==4.1.1

EXPOSE 5000

ENTRYPOINT ["python3"]

CMD ["count_substring.py"]

RUN celery -A app worker --pool=solo -l info

