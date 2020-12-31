from count_substring import *
import os

os.system("celery -A count_substring worker -l info -c 4 -f /app/logs/work.log")

tasks_in_progress = collection1.find({'or$': [{'state': 'progress'}, {'exec_start': 'not_yet'}]})
for doc in tasks_in_progress:
    id = doc.get('task_id')
    string = doc.get('input')
    substring = doc.get('substring')
    get_value.apply_async(args=(string, substring, id), task_id=id)


