from flask import Flask, request,jsonify
from celery import Celery
from pymongo import MongoClient
from celery.result import AsyncResult
from time import sleep
import json, logging, secrets
logging.basicConfig(filename='/app/logs/test.log',level=logging.INFO)
logger = logging.getLogger(__name__)
application = Flask(__name__)
celery = Celery('count_substring', broker='pyamqp://guest@broker/', backend='rpc://')
connect = MongoClient('mongo', 27017)
db = connect['application_data']
collection1 = db['db']

@celery.task(name="count_substring.get_value", bind=True)
def get_value(self, string, substring, id):
    occurrence_list = []
    string_list = []
    for i in string:
        count = i.count(substring)
        sleep(5)
        occurrence_list.append(count)
        string_list.append(i)
        if count == 0:
            collection1.update_one({'task_id': id}, {
                '$set':  {'state': "FAILED",'exec_start': 'started'}})
            raise Exception("count in one or more string is 0")
        else:
            percent = str(round(len(occurrence_list) / len(string) * 100)) + '%'
            self.update_state(state="progress", meta={"percent": percent,
                                                      "occurrence": occurrence_list, "string": string_list})
            collection1.update_one({'task_id': id}, {
                '$set':  {'state': "progress", 'percentage': percent,
                                    'occurrence': occurrence_list, 'string': string_list,'exec_start': 'not_yet'}})

            logger.info("State of the task is progress, percentage of task completed {percent},"
                        " occurrence is {occur}".format(percent=percent,
                                                        occur=occurrence_list))

    logger.info("State of the task is success, percentage of task completed {percent},"
                " occurrence is {occur}".format(percent="100%",
                                                occur=occurrence_list))
    collection1.update_one({'task_id': id}, {
        '$set':  {'state': "SUCCESS", 'percentage': "100%",
                            'occurrence': occurrence_list, 'string': string_list,'exec_start': 'started'}})

    return {"percent": "100%", "occurrence": occurrence_list, "string": string_list}


@application.route('/')
def hello_world():
    logger.info('hello')
    return 'hello'

@application.route('/result/<task_id>')
def result(task_id):
    res = AsyncResult(id=task_id, app=celery)
    if res.state == 'PENDING' and res.ready(): # executes when task id is valid but status is pending
        logger.info("task status {}".format(res.state))
        return {"task status": res.state}
    elif res.state == 'PENDING':#executes when task id is invalid/when someone give random task_id
        logger.info("task status {}".format(res.state))
        return jsonify("task_id not valid")
    elif res.state == "FAILURE":
        logger.info("task status {} and reason of failure".format(res.state,str(res.info)))
        return {"task_status": res.state, "reason": str(res.info)}
    else:
        logger.info("task status {state} percent of task completed {percent}"
                                " occurrence {occur} string {string}".format(state=res.state,percent=res.info.get("percent"),
                                                                             occur=res.info.get('occurrence'), string=res.info.get('string')))

        return {"status": res.state, "percent": res.info.get("percent"),
                "occurrence": res.info.get('occurrence'),
                "string": res.info.get('string')}


@application.route('/count/', methods=["POST"])
def count_sub():
    substring = request.args.get('substring')
    req_data = json.loads(request.data.decode())
    string = req_data["string"]
    id = secrets.token_urlsafe(16)
    collection1.insert_one({'task_id': id, 'input': string, 'substring': substring, 'exec_start': False})
    get_value.apply_async(args=(string, substring, id), task_id=id)
    logger.info("task id is {}".format(id))
    return {"task_id": id}

if __name__ == "__main__":
    application.run(debug=True,port="5000", host = "0.0.0.0") # host = "0.0.0.0"
