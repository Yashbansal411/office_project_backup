import os,shutil

size_of_file = os.stat("./worker_logs/work.log").st_size
print(size_of_file)
if size_of_file > 100:
    with open("./worker_logs/work.log","r") as f:
        with open("backup.txt","a") as f1:
            for line in f:
                f1.write(line)
            f1.close()
        f.close()
        #os.remove('./worker_logs/work.log')
        #os.rmdir('./worker_logs')
        #shutil.rmtree('./worker_logs')
            
            
            
