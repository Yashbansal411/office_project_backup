from operator import itemgetter
import json
import time


def input_to_list(name):
    with open(name) as f:
        l = []
        for line in f:
            l.append(json.loads(line))
        return l


def list_to_file(list3):
    with open('Testingfiles/output_50L.txt','w') as f:
        for i in list3:
            i = str(i)
            i = i.replace(" ","")
            if i != '\n':
                i = i+'\n'
            f.write(i)


def main_code(file1_address,file2_address):
    list1 = input_to_list(file1_address) #1L 2000 sec.
    list2 = input_to_list(file2_address)
    sorted_list1 = sorted(list1, key=itemgetter('raw_log_time'))
    sorted_list2 = sorted(list2, key=itemgetter('raw_log_time'))
    list3 = main_func(sorted_list1, sorted_list2)
    list_to_file(list3)
    return list3

