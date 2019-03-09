#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os, sys, datetime
try:
    from tkinter import *
except ImportError:  #Python 2.x
    PythonVersion = 2
    from Tkinter import *
    from tkFont import Font
    from ttk import *
    #Usage:showinfo/warning/error,askquestion/okcancel/yesno/retrycancel
    from tkMessageBox import *
    #Usage:f=tkFileDialog.askopenfilename(initialdir='E:/Python')
    #import tkFileDialog
    #import tkSimpleDialog
else:  #Python 3.x
    PythonVersion = 3
    from tkinter.font import Font
    from tkinter.ttk import *
    from tkinter.messagebox import *
    #import tkinter.filedialog as tkFileDialog
    #import tkinter.simpledialog as tkSimpleDialog    #askstring()

class Application_ui(Frame):
    #这个类仅实现界面生成功能，具体事件处理代码在子类Application中。
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.title('todolist')
        self.master.geometry('353x539')
        self.createWidgets()
        

    def createWidgets(self):
        self.top = self.winfo_toplevel()

        self.style = Style()

        self.inputVar = StringVar(value='')
        self.input = Entry(self.top, text='Text1', textvariable=self.inputVar, font=('宋体',10))
        self.input.place(relx=0.023, rely=0.015, relwidth=0.955, relheight=0.076)

        self.task_listVar = StringVar(value='')
        self.task_listFont = Font(font=('宋体',10))
        self.task_list = Listbox(self.top, listvariable=self.task_listVar, font=self.task_listFont)
        self.task_list.place(relx=0.023, rely=0.119, relwidth=0.955, relheight=0.764)

        self.style.configure('delete.TButton',font=('宋体',10))
        self.delete = Button(self.top, text='delete', command=self.delete_Cmd, style='delete.TButton')
        self.delete.place(relx=0.476, rely=0.905, relwidth=0.207, relheight=0.061)

        self.style.configure('add.TButton',font=('宋体',10))
        self.add = Button(self.top, text='add', command=self.add_Cmd, style='add.TButton')
        self.add.place(relx=0.181, rely=0.905, relwidth=0.207, relheight=0.061)




class Application(Application_ui):
    #这个类实现具体的事件处理回调函数。界面生成代码在Application_ui中。
    def __init__(self, master=None):
        Application_ui.__init__(self, master)
        #关闭窗口提示
        self.master.protocol("WM_DELETE_WINDOW", self.closeWindow)
        #保存未完成任务
        self.master.bind('<Control-s>', self.save)
        self.undo_file_name="undo.txt"
        self.done_file_name="done.txt"
        self.taskListInit()


    def closeWindow(self):
        #关闭窗口提示
        ans = askyesno(title='Warning', message="是否已经保存？")
        if ans:
            #这里可以调用保存功能
            self.master.destroy()
        else:
            return

    def taskListInit(self):
        #初始化任务列表，将上次关机齐纳未完成的任务读入,有bug,后期考虑存储格式为json？
        if os.path.exists(self.undo_file_name):
            with open(self.undo_file_name, 'r', encoding='utf-8') as f:
                for not_ok_task in f.readlines():
                    if not_ok_task:
                        self.task_list.insert(0, not_ok_task.strip())

    def delete_Cmd(self, event=None):
        #完成任务存入文件
        okTask = self.task_list.get(ACTIVE)
        # print(okTask)
        if len(okTask) > 1:
            #删除的时候从undo里删除，并转存至done
            with open(self.undo_file_name, 'r+', encoding='utf-8') as f:
                undo_list = f.readlines()
            for not_ok_task in undo_list:
                #由于\n问题的存在，需要在从文件读取时进行处理
                if not_ok_task.strip() == okTask:
                    # print(not_ok_task)
                    undo_list.remove(not_ok_task)
            with open(self.undo_file_name, 'w', encoding='utf-8') as f:
                # print(undo_list)
                for not_ok_task in undo_list:
                    f.write(not_ok_task)

            now_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            okTask = now_time + '  完成任务:  ' + okTask.strip()
            print(okTask)
            self.saveToFile(okTask ,self.done_file_name)
        self.task_list.delete(ACTIVE)


    def add_Cmd(self, event=None):
        #添加的时候放入未完成文件
        self.task = self.input.get()
        #输入为空不处理
        if len(self.task) > 1:
            self.task_list.insert(0, self.task)
            #存了需要删除
            self.saveToFile(self.task, self.undo_file_name)
        #清空输入框
        self.input.delete(0, END)

    def saveToFile(self ,task, file_name):
        #追加模式
        with open(file_name,'a',encoding='utf-8') as f:
            f.write(task+'\n')

    def save(self, event):
        #bug
        print("save")


if __name__ == "__main__":
    top = Tk()
    Application(top).mainloop()
    try: top.destroy()
    except: pass
