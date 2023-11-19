import json
import tkinter as tk
#import UI as ui

ALARMS_FILE = "alarms.json"
FILE_PATH = "C:/Users/mzigdon/Documents/logs/hdmtOScommon-3.log"

def loading_errors_to_search()->list:
    with open(ALARMS_FILE,'r') as json_file:
        data = json.load(json_file)
        alarms_list = data['errors']
        alarms_list = [word.lower() for word in alarms_list]
        return alarms_list

def loading_log()->list:
    try:
        with open(FILE_PATH,'r') as file:
            file_content = file.readlines()
            file.close()
    except FileNotFoundError:
        print("file not found")
    return file_content

def find_errors_in_log(file_content:list, alarms_list)->str:
    count=0
    line_number = {}
    lines_dict: dict ={}

    #parsing file for 2 dicts
    for line in file_content:
        line = line.lower()
        line = line.strip()
        line = line.rsplit("]",1)
        lines_dict[count]=line[-1]
        line_number[count] = line[0]
        count += 1

    #looking up for any alarms in file
    output: str = ""
    number = ''
    for alarm in alarms_list:
        curr_line = []
        output += " \nkey word: " + alarm + "\n"
        for key, value in lines_dict.items():
            if alarm in value:
                number = line_number[key].rsplit(',', 1)
                number = number[-1]
                if number not in curr_line:
                    output += number
                    output += " --------------"
                    output += lines_dict[key]
                    output += "\n"
                    curr_line.append(number)

    return output

file_content = loading_log()
alarms_list = loading_errors_to_search()
output = find_errors_in_log(file_content, alarms_list)

#GUI
def show_labels():
    label_header.pack()
    text_widget.pack(pady=10)

    #label_main.pack()



    #label = tk.Label(window,text =data, font=("Arial",12),justify="left", wraplength=700)

window = tk.Tk()
text_widget = tk.Text(window, wrap="word", height=30, width=60)
text_widget.tag_configure("big", font=("Arial", 14))
text_widget.tag_configure("small", font=("Arial", 8))
for word in output:
    text_widget.insert(tk.END, word, "big")
    text_widget.insert(tk.END, word, "small")
window.geometry("800x900")
window.title("ErorrsFinder")
window.configure(bg='lightblue')
window.iconbitmap('./assetes/logo.ico')
button = tk.Button(window, text="Start",command=show_labels)

label_header = tk.Label(window, text="errors found in log are:", font=("Arial",16))



button.pack(padx=20,pady=80)
#label_main = make_label(output)

window.mainloop()

