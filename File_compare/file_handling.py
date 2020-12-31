import random,json
dic = {"id":"333l","raw_log_time":8,"evt_order":0,"user":"abc"}
list_of_name = []
list_of_id = []
for i in range(1000):
    list_of_name.append('change'+str(i))  # create list of different names
    list_of_id.append('id'+str(i))  # create list of random id's
#print(list_of_name[940])
#print(list_of_id[940])
list_of_dict = []
for i in range(150):  # run for create input size.
    raw_log_time = random.randint(1, 1500)  # generate random number
    dic = {"id": "333l", "raw_log_time": 8, "evt_order": 0, "user": "abc"}
    dic["raw_log_time"] = raw_log_time
    dic["id"] = list_of_id[random.randint(0,999)]
    dic["user"] = list_of_name[random.randint(0,999)]
    list_of_dict.append(dic)

with open('Testingfiles/file2_150L.txt','w') as f:
    for i in list_of_dict:
        json_obj = json.dumps(i)
        f.write(json_obj + '\n')



