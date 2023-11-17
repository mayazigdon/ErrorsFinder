import json
import tkinter as tk

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

count=0
line_number = {}
lines_dict: dict ={}

for line in file_content:
    line = line.lower()
    line = line.strip()
    line = line.rsplit("]",1)
    lines_dict[count]=line[-1]
    line_number[count] = line[0]
    count += 1

number = ''
for alarm in alarms_list:
    curr_line = []
    print("*********************************************key word:",alarm)
    for key, value in lines_dict.items():
        if alarm in value:
            number = line_number[key].rsplit(',', 1)
            number = number[-1]
            if number not in curr_line:
                print(number)
                print(lines_dict[key])
                curr_line.append(number)






