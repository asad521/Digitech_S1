from tkinter import Tk,Frame,Label
from tkinter  import *
from tkinter import ttk
from PIL import ImageTk, Image
import time

mainwindow=Toplevel()
mainframe=Frame(mainwindow,bg="red")
mainframe.pack(fill="both",expand=True)

#label=Label(mainframe,text="Vertical Frame Example",bg="black",fg="white",padx=5,pady=5)
#label.config(font=("Arial",18))
#label.pack(fill="x")
#vertical layout with data
#verticalFrame=Frame(mainframe,bg="blue")

#item1=Label(verticalFrame,text="Item 1",bg="orange",padx=10,pady=10,fg="white")
#item1.pack(fill="x",padx=10,pady=10)

#item1=Label(verticalFrame,text="Item 2",bg="yellow",padx=10,pady=10,fg="black")
#item1.pack(fill="x",padx=10,pady=10)

#item1=Label(verticalFrame,text="Item 3",bg="green",padx=10,pady=10,fg="white")
#item1.pack(fill="x",padx=10,pady=10)

#verticalFrame.pack(fill="x")
#end vertical

#horizontal
label=Label(mainframe,text="Horizontal Frame Example",bg="black",fg="white",padx=5,pady=5)
label.config(font=("Arial",18))
label.pack(fill="x")
horizontal_frame=Frame(mainframe)

Button_1=Button(horizontal_frame,text="Item 1 in Horizontal",bg="red",fg="white",padx=10,pady=10)
Button_1.grid(row=0,column=0,padx=10,pady=10,sticky="nsew")
Button_2=Button(horizontal_frame,text="Item 2 in Horizontal",bg="red",fg="white",padx=10,pady=10)
Button_2.grid(row=0,column=1,padx=10,pady=10,sticky="nsew")
Button_3=Button(horizontal_frame,text="Item 3 in Horizontal",bg="red",fg="white",padx=10,pady=10)
Button_3.grid(row=0,column=2,padx=10,pady=10,sticky="nsew")
Button_4=Button(horizontal_frame,text="Item 4 in Horizontal",bg="red",fg="white",padx=10,pady=10)
Button_4.grid(row=0,column=3,padx=10,pady=10,sticky="nsew")

horizontal_frame.grid_columnconfigure(0,weight=1)
horizontal_frame.grid_columnconfigure(1,weight=1)
horizontal_frame.grid_columnconfigure(2,weight=1)
horizontal_frame.grid_columnconfigure(3,weight=1)
horizontal_frame.pack(fill="x")

#end horizontal

def my_fun(type): # update the value of progress bar
    GB = 100
    download = 0
    speed = 1
    while(download<GB):
        time.sleep(0.05)
        prg1['value']+=(speed/GB)*100
#        percent.set(str(int((download/GB)*100))+"%")
#        text.set(str(download)+"/"+str(GB)+" GB completed")
        mainframe.update_idletasks()

#grid data
run_labeling=Button(mainframe,text="run_labeling",bg="black",fg="white",padx=5,pady=5,command=lambda:my_fun(True))
run_labeling.config(font=("Arial",18))
run_labeling.pack()
#run_labeling.pack(fill="x")


# Create an object of tkinter ImageTk
img = ImageTk.PhotoImage(Image.open("test.jpg"))
# Create a Label Widget to display the text or Image
label = Label(mainframe, image = img)
label.pack()

#status bar
# Create a Label Widget to display the text or Image
prg1 = ttk.Progressbar(mainframe, orient=HORIZONTAL,
                       value=1, length=300, mode='determinate', )
prg1.pack( padx=5, pady=5,side=BOTTOM,fill='x')




grid_frame=Frame(mainframe)
#for row in range(10):
#    for column in range(10):
#        label=Label(grid_frame,text="Item ",bg="red",fg="white",padx=5,pady=5)
#        print(row)
#        prg1 = ttk.Progressbar(grid_frame, orient=HORIZONTAL,
#                               value=70, length=300, mode='determinate',)
#        if (row==9 and column ==9):

#            prg1.grid(row=row,column=column,padx=5,pady=5,sticky="nsew")
#            grid_frame.grid_columnconfigure(column,weight=1)


grid_frame.pack(fill="x")



mainwindow.mainloop()