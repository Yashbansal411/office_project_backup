from celery import Celery
from time import sleep
app = Celery('celery_task_practice', broker="pyamqp://guest@localhost//", backend='rpc://', task_acks_late=False)


@app.task(name='my_task')
def add(a,b):
    sleep(10)
    return a+b