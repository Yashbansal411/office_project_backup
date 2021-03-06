def stringsFile1(fileName):
    l = []  # create empty list
    with open(fileName, 'r') as f:
        for line in f:
            l.append(line)
        f.close()
    return l

def func(list1,list2):
    list3 = ['\n']*(len(list1))
    lastInsertedIndex = -1
    indexList2 = 0
    for i in list2:
        if i in list1:
            try:
                index = list1.index(i,lastInsertedIndex+1,len(list1)-1)
                list3[index] = i
                lastInsertedIndex = index
            except ValueError:
                continue

        else:
             if indexList2 == len(list2)-1:
                 if list3[len(list3)-1] == '\n':
                    list3[len(list3)-1] = i.rstrip('\n') + '<mismatch>\n'
                 else :
                     list3.append(i.rstrip('\n') + '<mismatch>\n')
             else:
                 try:
                    list3[lastInsertedIndex+1] = i.rstrip('\n') + '<mismatch>\n'
                 except IndexError:
                    list3.append(i.rstrip('\n') + '<mismatch>\n')
                 lastInsertedIndex += 1
        indexList2 += 1
    return list3


def listToFile(list3):
    with open('output.txt','w') as f:
        for i in list3:
            f.write(i)
        f.close()

list1 = stringsFile1('./file1.txt')
list2 = stringsFile1('./file2.txt')
list3 = func(list1,list2)
print(list3)
listToFile(list3)