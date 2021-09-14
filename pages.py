import tkinter as tk
from tkinter import *
from tkinter import ttk #css for tkinter
from PIL import Image, ImageTk
import time
import datetime #want to date the diary entries
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import sys,os

os.chdir(sys.path[0])

LARGE_FONT=("Times New Roman",12)



class myapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self,*args,**kwargs)

        #tk.Tk.iconbitmap(self,default="myicon.ico") #to add icons
        tk.Tk.wm_title(self, "My app")
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column = 0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):

        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self,parent,controller):

        
        tk.Frame.__init__(self,parent)

        label = tk.Label(self,text="How was your dream today?",font = LARGE_FONT)
        label.pack(pady=30,padx=100)
        e = Text(self, width = 45, borderwidth=5)
        e.place(x=55,y=70, height = 250)

        def writediary():
            y = e.get("1.0",END)
            x = datetime.datetime.now()  #set date and time variable
            str_time = str(x)[11:-7]   #str(x) = 2019-08-21 02:35:24.144516   Here we cut out the fat
            str_day = x.strftime("%A") #day of the week in string format (str f), %A is the weekday option, use %a for month abbreviation, ie tues
            str_date = x.strftime("%d") #numerical date in string format, %d is the date option
            str_month = x.strftime("%B") #month in string format, %B is the month option, use %b for month abbreviation, ie dec
            str_year = str(x.year)

            date_formatted = "[" + str_time + "] " + str_day + ", " + str_month + " " + str_date +", " + str_year + ": \n"
            string1 = date_formatted + y + "\n \n"
                # \n is placed to indicate End of Line

            txtfilename = "my_diary.txt"
            file1 = open( txtfilename, "a" )    #open the text file, append to it 
            file1.write(string1)
            file1.close()

        def cloud():
            text = open('my_diary.txt', mode='r', encoding='utf-8').read()
            stopwords = STOPWORDS

            wc = WordCloud(
                background_color='white',
                stopwords=stopwords,
                height = 300,
                width = 375
                )
            wc.generate(text)
            wc.to_file('wordcloud_output.png')
            controller.show_frame(PageTwo)


        

        button = tk.Button(self, text="SAVE", command = writediary, bg="blue")
        button.place(x=53,y=320, width=375)       

        button1 = tk.Button(self, text="WRITE", command = lambda:controller.show_frame(StartPage),bg="green")
        button1.place(x=53,y=350,width=150)

        button2 = tk.Button(self, text="ENTRIES", command = lambda:controller.show_frame(PageOne), bg="yellow")
        button2.place(x=193,y=350, width=110)

        button3 = tk.Button(self, text="WORDCLOUD", command = cloud, bg="red")
        button3.place(x=293,y=350,width=135)



class PageOne(tk.Frame):

    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self,text="Entries:",font = LARGE_FONT)
        label.pack(pady=30,padx=100)

        Lb = Listbox(self,width=45, height=14)
        Lb.pack(pady=2,padx=100)
        f = open("my_diary.txt","r")
        for x in f:
            Lb.insert(END,x)
        f.close()

        def cloud():
            text = open('my_diary.txt', mode='r', encoding='utf-8').read()
            stopwords = STOPWORDS

            wc = WordCloud(
                background_color='white',
                stopwords=stopwords,
                height = 300,
                width = 375
                )
            wc.generate(text)
            wc.to_file('wordcloud_output.png')
            controller.show_frame(PageTwo)


        button1 = tk.Button(self, text="WRITE", command = lambda:controller.show_frame(StartPage),bg="green")
        button1.place(x=53,y=350,width=150)

        button2 = tk.Button(self, text="ENTRIES", command = lambda:controller.show_frame(PageOne), bg="yellow")
        button2.place(x=193,y=350, width=110)

        button3 = tk.Button(self, text="WORDCLOUD", command = cloud, bg="red")
        button3.place(x=293,y=350,width=135)



class PageTwo(tk.Frame):

    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self,text="Generate Word Cloud:",font = LARGE_FONT)
        label.pack(pady=10,padx=5)

        def update():
            image1 = Image.open('wordcloud_output.png')
            test = ImageTk.PhotoImage(image1)

            label1 = tk.Label(self,image=test)
            label1.image = test

            # Position image
            label1.place(x=55, y=50)

        def cloud():
            text = open('my_diary.txt', mode='r', encoding='utf-8').read()
            stopwords = STOPWORDS

            wc = WordCloud(
                background_color='white',
                stopwords=stopwords,
                height = 300,
                width = 375
                )
            wc.generate(text)
            wc.to_file('wordcloud_output.png')
            controller.show_frame(PageTwo)
            

        
        button0 = ttk.Button(self, text="UPDATE", command = update)
        button0.place(x=330,y=10)     

        button1 = tk.Button(self, text="WRITE", command = lambda:controller.show_frame(StartPage),bg="green")
        button1.place(x=53,y=350,width=150)

        button2 = tk.Button(self, text="ENTRIES", command = lambda:controller.show_frame(PageOne), bg="yellow")
        button2.place(x=193,y=350, width=110)

        button3 = tk.Button(self, text="WORDCLOUD", command = cloud, bg="red")
        button3.place(x=293,y=350,width=135)



        

app = myapp()
app.title("D R E A M   J O U R N A L")
app.geometry('500x400') #Determines window size 

app.mainloop()
