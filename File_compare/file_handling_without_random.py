import json
dic = {"id":"333l","raw_log_time":8,"evt_order":0,"user":"abc"}
json_obj = json.dumps(dic)

with open('files_for_test_exec_time/file1_40000.txt','w') as f:
    num = 40000
    while(num):
        #data = str(dic)+'\n'
        #data.replace("'",'"')
        json_obj = json.dumps(dic)
        f.write(json_obj+'\n')
        num = num - 1