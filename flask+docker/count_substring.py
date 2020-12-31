from flask import Flask, request,jsonify
from celery import Celery
from celery.result import AsyncResult
from time import sleep
import json

application = Flask(__name__)
celery = Celery('count_substring', broker='pyamqp://guest@localhost//', backend='rpc://')

@application.route('/')
def hello_world():
    return 'welcome home'


@application.route('/result/<task_id>')
def result(task_id):
    res = AsyncResult(id=task_id, app=celery)

    if res.state == 'PENDING' and res.ready(): # executes when task id is valid but status is pending
        return {"task status": res.state}
    elif res.state == 'PENDING':  #executes when task id is invalid/when someone give random task_id
        return jsonify("task_id not valid")
    elif res.state == "FAILURE":
        return {"task_status": res.state, "reason": str(res.info)}
    else:
        return {"status": res.state, "percent": str(round(res.info.get("percent"), 2)) + "%",
                "occurrence": res.info.get('occurrence'),
                "string": res.info.get('string')}


@application.route('/count/', methods=["POST"])
def count_sub():
    substring = request.args.get('substring')
    req_data = json.loads(request.data.decode())
    string = req_data["string"]
    res = get_value.apply_async(args=(string, substring))
    return {"task_id": res.task_id}


@celery.task(name="count_substring.get_value", bind=True)
def get_value(self, string, substring):
    occurrence_list = []
    string_list = []
    for i in string:
        count = i.count(substring)
        sleep(2)
        occurrence_list.append(count)
        string_list.append(i)
        if count == 0:
            raise Exception("count in one or more string is 0")
        else:
            self.update_state(state="progress", meta={"percent": len(occurrence_list) / len(string) * 100,
                                                      "occurrence": occurrence_list, "string": string_list})

    return {"percent": 100, "occurrence": occurrence_list, "string": string_list}


if __name__ == "__main__":
    application.run(debug=True, host="0.0.0.0",port="5000")
