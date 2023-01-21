import tkinter as tk
from tkinter import ttk
from tkinter import  font
from tkinter.messagebox import askyesno
from tkinter import messagebox
from Grid import print_hi
from tkinter  import *
from PIL import ImageTk, Image


#all button and closing window functions
# trigger on buttons
def popup():
    response = messagebox.askyesno("Neutral Network Training","Do you want to start training")
    if response == 1:
        print('Answer is Yes')
    else:
        print('Answer is not')


# root window
root = tk.Tk()
root.title('RetroVision Control Panel')
root.resizable(0, 0)
#sytle
font_style = font.Font(family='Roboto', size=22,weight='bold')
myFont = font.Font(size=33)
# devide in frame
copyright = u"\u00A9"
status_frame =tk.Frame(root)
status_frame.grid(row=100,column=0,columnspan=5)
status = Label(status_frame, text="Copyright "+ copyright + " RetroVision, 2022",relief=SUNKEN,bd=1)
status.grid(row=0,column=0,pady=10)
# configure the grid
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=3)


# title and logo image row 0
username_label = ttk.Label(root, text="RetroVision",font=('times', 42, 'bold', 'italic'))
username_label.grid(column=0, row=0, sticky=tk.W, padx=20, pady=20)
# Load an image in the script
img = (Image.open("eye2.png"))
# Resize the Image using resize method
resized_image = img.resize((65, 60), Image.ANTIALIAS)
new_image = ImageTk.PhotoImage(resized_image)
image_label = ttk.Label(root, image=new_image)
username_entry = ttk.Entry(root)
image_label.grid(column=1, row=0, sticky=tk.E, padx=5, pady=5)
# Labeling  Button row 1
Labeling = Button(root, text="Label Image",font=font_style,command=print_hi)
Labeling.grid(column=0, row=1, sticky=tk.W, padx=20, pady=40)
# Segmentation Button row 1
Segmentation = Button(root, text="Segmentation",font=font_style)
Segmentation.grid(column=1, row=1, sticky=tk.E, padx=20, pady=40)
# NeuralNetwork Button row 2
TrainNTest = Button(root, text="Train & Test",font=font_style,command=popup)
TrainNTest.grid(column=0, row=2, sticky=tk.W, padx=20, pady=40)
# MQTT Button row 2
mqtt = Button(root, text="Publish values",font=font_style)
mqtt.grid(column=1, row=2, sticky=tk.E, padx=20, pady=40)

#exit window
def confirm():
    ans = askyesno(title='Exit', message="Do you want to close the window?")
    if ans:
        root.destroy()
root.protocol("WM_DELETE_WINDOW",confirm)

root.mainloop()