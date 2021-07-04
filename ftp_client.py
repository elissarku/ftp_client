from tkinter import *
import tkinter.messagebox as box
from tkinter import scrolledtext,ttk
import io
from os import *
from ftplib import FTP

ftp=0

def connect():
    host=e1.get()
    user=e2.get()
    password=e3.get()
    port=int(e4.get())
    if(len(host)!=0):
        global ftp
        ftp = FTP()
        s=ftp.connect(host,port)
        log(s)
        s=ftp.login(user,password)
        log(s)
        s=ftp.pwd()
        remote_path.delete(0,END)
        remote_path.insert(0,s)
        get_remote_file_list()
    else:
        log('Error: Fill The Fields')

def open_local_folder(event):
    x=local_file_list.curselection()
    file=local_file_list.get(x[0])
    get_local_file_list(file)

def open_remote_folder(event):
    x=remote_file_list.curselection()
    file=remote_file_list.get(x[0])
    ftp.cwd(file)
    s=ftp.pwd()
    remote_path.delete(0,END)
    remote_path.insert(0,s)
    get_remote_file_list()
    
def move_to_remote():
    x=local_file_list.curselection()
    filename=local_file_list.get(x[0])
    local_filename = local_path.get() + "/" + filename
    file = io.open(local_filename, "rb")
    ftp.storbinary('STOR '+filename, file)
    file.close()

def move_to_local():
    x=remote_file_list.curselection()
    filename=remote_file_list.get(x[0])
    local_filename = local_path.get() + "/" + filename
    file = io.open(local_filename, "wb")
    ftp.retrbinary('RETR '+ filename, file.write)
    file.close()
    

def get_remote_file_list():
    files=ftp.nlst()
    remote_file_list.delete(0,END)
    for name in files:
        remote_file_list.insert('end', name)

def get_local_file_list(x):
    if(len(x)>0):
        path=local_path.get()+"/"+x
    else:
        path=local_path.get()
    try:
        files=listdir(path)
        local_path.delete(0,END)
        local_path.insert(0,path)
        local_file_list.delete(0,END)
        for name in files:
            local_file_list.insert('end', name)
    except:
        pass
    
def change_drive(event):
    x=drives['values'][drives.current()]
    local_path.delete(0,END)
    local_path.insert(0,x)
    get_local_file_list('')
    
    
def log(txt):
    status.configure(state='normal')
    status.insert('end',txt)
    status.insert('end','\n')
    status.configure(state='disabled')
    status.see("end")


if __name__ == "__main__" :
    window = Tk()
    window.title('FTP Client')
    window.geometry("800x500")

    connect_frame = Frame(window)
    connect_frame.pack(pady = 5, padx = 10)
    status_frame = Frame(window)
    status_frame.pack(pady = 5, padx = 10)
    files_frame = Frame(window)
    files_frame.pack(pady = 5, padx = 10)
    
    l1 = Label(connect_frame,text = "host: ")
    l2 = Label(connect_frame,text = "username: ")
    l3 = Label(connect_frame,text = "password: ")
    l4 = Label(connect_frame,text = "port: ")

    t1=StringVar()
    t1.set("localhost")
    t2=StringVar()
    t2.set("alesar")
    t3=StringVar()
    t3.set("12345")
    t4=StringVar()
    t4.set("21")
    
    e1 = Entry(connect_frame,textvariable = t1)
    e2 = Entry(connect_frame,textvariable = t2)
    e3 = Entry(connect_frame,textvariable = t3)
    e4 = Entry(connect_frame,textvariable = t4)

    l1.grid(column = 0, row = 0)
    l2.grid(column = 2, row = 0)
    l3.grid(column = 4, row = 0)
    l4.grid(column = 6, row = 0)

    e1.grid(column = 1, row = 0)
    e2.grid(column = 3, row = 0)
    e3.grid(column = 5, row = 0)
    e4.grid(column = 7, row = 0)
    
    b_connect = Button(connect_frame,text = "Connect",command = connect)
    b_connect.grid(column = 8, row = 0)

    status = scrolledtext.ScrolledText(status_frame,wrap = WORD, width = 95, height = 4, state=DISABLED)
    status.pack()

    l5 = Label(files_frame,text = "Local site: ",width=55,anchor=W)
    l6 = Label(files_frame,text = "Remote site: ",width=55,anchor=W)

    l5.grid(column = 0, row = 0)
    l6.grid(column = 1, row = 0)
    

    local_path_frame = Frame(files_frame)
    local_path_frame.grid(column = 0, row = 1)
    
    strvar = StringVar()
    drives = ttk.Combobox(local_path_frame, width = 5, textvariable = strvar)
    drives['values'] = ('C:/','D:/','E:/','F:/')
    drives.current(0)
    drives.bind("<<ComboboxSelected>>", change_drive)

    local_path=Entry(local_path_frame,width=55)

    drives.grid(column = 0, row = 0)
    local_path.grid(column = 1, row = 0)
    
    remote_path=Entry(files_frame,width=64)
    remote_path.grid(column = 1, row = 1)


    local_file_list = Listbox(files_frame,width=64,height=18)
    change_drive(0)
    local_file_list.bind('<Double-1>', open_local_folder)
    local_file_list.grid(column = 0, row = 2)

    remote_file_list = Listbox(files_frame,width=64,height=18)
    remote_file_list.bind('<Double-1>', open_remote_folder)
    remote_file_list.grid(column = 1, row = 2)

    b_move_to_remote = Button(files_frame,text = "Move to Remote Site ->",command = move_to_remote)
    b_move_to_remote.grid(column = 0, row = 3)

    b_move_to_local = Button(files_frame,text = "<- Move to Local Site",command = move_to_local)
    b_move_to_local.grid(column = 1, row = 3)
    
    window.mainloop()

