import os
from tkinter import *
from tkinter import filedialog
from tkinter import font
from tkinter import messagebox
from tkinter.filedialog import askopenfilename

from Rope import *


class TextEditor:
    def __init__(self,root):
        self.root = root
        self.savecount = 0
        self.root.title("Notepad--")
        self.root.geometry("800x800")
        self.filename = None

        self.characters = 0
        self.title = StringVar()
        self.status = StringVar()
        self.status1 = StringVar()

        self.titlebar = Label(self.root,textvariable=self.title,font = ("Helvetica",16,"bold"),relief = GROOVE)
        self.titlebar.pack(side = TOP,fill = Y)
        self.settitle()



        self.statusbar = Label(self.root, textvariable = self.status, font = ("times new roman", 15),relief = GROOVE)

        self.statusbar.pack(side=BOTTOM,fill=BOTH)
        self.status.set("Welcome to Notepad--");


        self.statusbar1= Label(self.root, textvariable = self.status1, anchor = 'sw', font = ("times new roman", 15))
        self.statusbar1.pack(side=BOTTOM, fill=BOTH)

        self.status1.set("words = 0")


        scrol_y=Scrollbar(self.root)

        self.txtarea = Text(self.root, yscrollcommand = scrol_y.set, font=("times new roman", 12),selectbackground = "yellow",selectforeground = "Red",undo=True,fg='black',bg='white')

        self.txt = self.txtarea.get("1.0",END)
        self.words = self.txt.count(" ") + self.txt.count("\n")

        scrol_y.pack(side = RIGHT, fill = Y)
        scrol_y.config(command =self.txtarea.yview)

        self.txtarea.pack(fill=BOTH, expand = 50)


        self.menubar =Menu(self.root, font=("times new roman", 15), activebackground ="yellow")
        self.root.config(menu = self.menubar)

        # Creating File Menu

        self.filemenu=Menu(self.menubar, font = ("times new roman", 12,"bold "), activebackground= "skyblue",tearoff=0)
        self.menubar.add_cascade(label="File", menu = self.filemenu)

        self.filemenu.add_command(label="New", accelerator="Ctrl + N", command =self.newfile)
        self.filemenu.add_command(label="Open", accelerator="Ctrl + O", command=self.openfile)
        self.filemenu.add_command(label="Save", accelerator="Ctrl + S", command=self.savefile)
        self.filemenu.add_command(label="Save As", accelerator="Ctrl + Shift + S", command=self.saveasfile)
        self.filemenu.add_separator()
        self.filemenu.add_command(label = "Exit", command=self.exit)


        self.editmenu =  Menu(self.menubar,font = ("times new roman",12,"bold"),activebackground="skyblue",tearoff=0)
        self.menubar.add_cascade(label="Edit", menu= self.editmenu)


        self.editmenu.add_command(label="Cut",accelerator ="Ctrl + X", command = self.cut)
        self.editmenu.add_command(label="Copy", accelerator ="Ctrl + C", command = self.copy)
        self.editmenu.add_command(label="Paste", accelerator ="Ctrl + V", command = self.paste)

        self.filemenu.add_separator()
        self.shortcuts()


    def settitle(self):
        self.title.set("Notepad-- (Made By Avik)")

    def newfile(self,*args):
        self.txtarea.delete("1.0",END)
        self.filename = None
        self.settitle()
        self.status.set("New File Created")
        self.savecount =0
        self.status1.set("words = 0")


    def openfile(self,*args):
        self.words = 0
        try:
            self.filename = filedialog.askopenfilename(title = "Select file", filetypes= (("Text Files","*.txt")))
            if self.filename!=None:
                self.savecount +=1
                infile = open(self.filename,"r")
                self.txtarea.delete("1.0",END)
                counter = 0

                while True:
                    if counter > 11 and counter%6==0:
                        character = infile.read(6)
                        if not character:
                            break
                        rope,self.characters = rope.insertion(character,self.characters)
                        self.words+=character.count(" ")
                        self.words+=character.count("\n")
                        self.txtarea.insert(END,character)
                    else:
                        character = infile.read(11)
                        if not character:
                            break
                        rope, self.characters = add_first(character)
                        self.words += character.count(" ")
                        self.words += character.count("\n")
                        self.txtarea.insert(END, character)
                    counter+=1
                infile.close()
                self.settitle()
                self.status.set("Opened Successfully")
                self.status1.set(str(self.words)+" words")
        except Exception as e:
            print("Can't Access")

    def saveasfile(self, *args):
        try:
            self.filename= filedialog.asksaveasfilename(title = "Save file as",defaultextension=".txt",initialfile = "Untitled.txt",filetypes = (("Text Files", "*.txt")))
            data = self.txtarea.get("1.0",END)
            outfile = open(self.filename,"w")
            outfile.write(data)
            outfile.close()
            self.settitle()
            self.status.set("Saved Successfully")
        except Exception as e:
            print("Can't Access")



    def savefile(self,*args):
        try:
            if self.savecount !=0:
                if self.filename != None:
                    data=self.txtarea.get("1.0",END)
                    outfile =open(self.filename,"w")
                    outfile.write(data)
                    outfile.close()
                    self.settitle()
                    self.status.set("Saved Successfully")
                    self.status1.set(str(self.words)+" word")
            elif self.savecount==0:
                self.savecount+=1
                self.saveasfile()
        except Exception as e:
            print("Can't access")

    def exit(self,*args):
        self.root.destroy()
    def cut(self,*args):
        self.txtarea.event_generate("<<Cut>>")
    def copy(self,*args):
        self.txtarea.event_generate("<<Copy>>")
    def paste(self,*args):
        self.txtarea.event_generate("<<Paste>>")

    def shortcuts(self,*args):
        self.txtarea.bind("<Control-n>",self.newfile)
        self.txtarea.bind("<Control-o>", self.openfile)
        self.txtarea.bind("<Control-s>", self.savefile)
        self.txtarea.bind("<Control-S>", self.saveasfile)
        self.txtarea.bind("<Control-e>", self.exit)
        self.txtarea.bind("<Control-x>", self.cut)
        self.txtarea.bind("<Control-c>", self.copy)
        self.txtarea.bind("<Control-v>", self.paste)

root = Tk()
TextEditor(root)
root.mainloop()