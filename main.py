import json
ALARMS_FILE = "alarms.json"
FILE_PATH = "C:/Users/mzigdon/Documents/logs/hdmtOScommon-3.log"
with open(ALARMS_FILE,'r') as json_file:
    data = json.load(json_file)
    alarms_list = data['errors']
    alarms_list = [word.lower() for word in alarms_list]

try:
    with open(FILE_PATH,'r') as file:
        file_content = file.readlines()
        file.close()
except FileNotFoundError:
    print("file not found")


lines_list:list = []
for line in file_content:
    line = line.lower()
    line = line.strip()
    line = line.rsplit("]",1)
    lines_list.append(line[-1])

#for line in lines_list:
#    for alarm in alarms_list:
#        if alarm in line:
#            print(line)
for alarm in alarms_list:
    print("*********************************************key word:",alarm)
    for line in lines_list:
        if alarm in line:
            print(line)


#for alarm in alarms_list:
#    if alarm in file_content:
#        print(alarm)


