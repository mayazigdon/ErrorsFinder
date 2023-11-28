import clipboard
import json
import tkinter as tk
import sys
from tkinter import messagebox
from tkinter import font as tkFont

ALARMS_FILE = "alarms.json"
FILE_PATH = "./assetes/hdmtOScommon.log" #need to modify
IMG_PATH = "./assetes/Intel_logo_PNG5.png"

class Application:

    def __init__(self, window):
        window.geometry("800x600")
        window.title("ErorrsFinder")
        window.configure(bg="#78b9fa")
        window.pack_propagate(False)
        window.resizable(False, False)
        self.menu()


    def loading_errors_to_search(self)->list:
        with open(ALARMS_FILE,'r') as json_file:
            data = json.load(json_file)
        json_file.close()
        alarms_list = data['errors']
        alarms_list = [word.lower() for word in alarms_list]
        json_file.close()
        return alarms_list

    def loading_log(self)->list:
        try:
            with open(FILE_PATH,'r') as file:
                file_content = file.readlines()
                file.close()
        except FileNotFoundError:
            print("file not found")
        return file_content

    def find_errors_in_log(self,file_content:list, alarms_list)->str:
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
        output: dict={}
        number = ''
        for alarm in alarms_list:
            curr_line = []
            output['key word: '+alarm]=["\n"]
            for key, value in lines_dict.items():
                if alarm in value:
                    number = line_number[key].rsplit(',', 1)
                    number = number[-1]
                    if number not in curr_line:
                        output['key word: '+alarm].append(number+" --------------"+lines_dict[key]+"\n")
                        curr_line.append(number)

        return output

    def loading_errors(self):
        file_content = self.loading_log()
        alarms_list = self.loading_errors_to_search()
        global output
        output = self.find_errors_in_log(file_content, alarms_list)


    #GUI
    def show_labels(self):
        self.loading_errors()
        for widget in window.winfo_children():
            widget.pack_forget()

        label_header = tk.Label(window, text="Errors Found In Log Are:", font=("Arial", 16))
        text_widget = tk.Text(window, wrap="word", height=28, width=110)
        text_widget.tag_configure("big", font=("Arial", 16))
        text_widget.tag_configure("small", font=("Arial", 12))
        for key, value in output.items():
            text_widget.insert(tk.END, key, "big")
            for item in value:
                text_widget.insert(tk.END, item, "small")
        button = tk.Button(window, text="Copy To clipBoard ", command=self.copy_to_clipBoard,height=2,width=20)
        button1 = tk.Button(window, text="Back",command=self.menu,height=2,width=6)
        label_header.pack(pady=10)
        text_widget.pack(pady=10)
        button.pack(side=tk.LEFT,padx=180)
        button1.pack(side=tk.LEFT,padx=80)


    def add_search_word(self):
        entry = tk.Entry(window, width=35)
        for widget in window.winfo_children():
            widget.pack_forget()
        button = tk.Button(window, text="Add", command=lambda:self.get_entry_text(entry),height=2,width=8)
        button1 = tk.Button(window, text="New Search", command=self.show_labels,height=2,width=8)
        entry.pack(pady=(200,10),padx=(0,30))
        button.pack(side=tk.LEFT, pady=(0, 300), padx=(305, 0))
        button1.pack(side=tk.LEFT, pady=(0, 300), padx=(20, 0))
        button2 = tk.Button(window, text="Back", command=self.menu,height=1,width=5)
        button2.pack(side=tk.RIGHT, padx=50,pady=(0,100))


    def copy_to_clipBoard(self):
        str_output = ""
        for key,value in output.items():
            str_output+=key
            for item in value:
                str_output+=item
                str_output+="\n"
        clipboard.copy(str_output)

    def get_entry_text(self,entry):
        entered_text = entry.get()
        with open(ALARMS_FILE, 'r') as json_file:
            data = json.load(json_file)
        json_file.close()
        alarm_list = self.loading_errors_to_search()
        if not entered_text:
            messagebox.showinfo("massage", "Please Enter A Search Word")
            return
        if entered_text.lower() in alarm_list:
            messagebox.showinfo("massage","This Search Word Is Already Exist")
            return
        else:
            data['errors'].append(entered_text)
            updated_json = json.dumps(data)
            with open(ALARMS_FILE, 'w') as json_file_w:
                json_file_w.write(updated_json)

    def menu(self):
        button = tk.Button(window, text="Start", command=self.show_labels, height=2, width=20)
        button2 = tk.Button(window, text="Add A New Search Word", command=self.add_search_word, height=2, width=20)
        button3 = tk.Button(window, text="Remove A Search Word", command=self.remove_search_word, height=2, width=20)
        for widget in window.winfo_children():
            widget.pack_forget()
        bold_font = tkFont.Font(family="Courier", size=30, weight="bold")
        label_header = tk.Label(window, text="Key Word Search ", font=bold_font, bg="#78b9fa")
        label_header.pack(padx=(30, 0), pady=(80, 10))
        button.pack(padx=20, pady=(50, 0))
        button2.pack(side=tk.LEFT,pady=(0, 220), padx=(250, 0))
        button3.pack(side=tk.LEFT,pady=(0, 220), padx=(20, 0) )


    def remove_search_word(self):
        entry = tk.Entry(window, width=35)
        for widget in window.winfo_children():
            widget.pack_forget()
        entry.pack(pady=(200, 15))
        button = tk.Button(window, text="Delete", command=lambda:self.delete(entry),height=2,width=8)
        button.pack()
        button1 = tk.Button(window, text="Back", command=self.menu,height=1,width=5)
        button1.pack(side=tk.RIGHT, padx=50,pady=(0,100))


    def delete(self,entry):
        entered_text = entry.get()
        entered_text = entered_text.lower()
        with open(ALARMS_FILE, 'r') as json_file:
            data = json.load(json_file)
        json_file.close()
        alarm_list = self.loading_errors_to_search()
        if not entered_text:
            messagebox.showinfo("massage", "Please Enter A Search Word")
            return
        if entered_text.lower() not in alarm_list:
            messagebox.showinfo("massage", "Search Word Dont Exist")
            return
        data['errors'] = [item for item in data['errors']if item.lower() != entered_text]
        updated_json = json.dumps(data)
        with open(ALARMS_FILE, 'w') as json_file_w:
            json_file_w.write(updated_json)
        messagebox.showinfo("massage", "key word Deleted Succesfully")


if __name__ == "__main__":
    window = tk.Tk()
    app = Application(window)
    window.iconbitmap('./assetes/logo.ico')
    bg_image = tk.PhotoImage(file=IMG_PATH)
    resized_image = bg_image.subsample(14, 14)
    bg_label = tk.Label(window, image=resized_image, bg="#78b9fa")
    bg_label.place(relx=0.27, rely=0.6, relwidth=0.5, relheight=0.5)
    window.mainloop()

