import tkinter as tk
from tkinter import  font
from tkinter.messagebox import askyesno
from tkinter import messagebox
from tkinter  import *
from PIL import ImageTk, Image
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from segmentationGUI import main
from mqqtpub import run
import threading
import os
from second_window import prog_bar
from progessBarClass import progess_bar_class
# ===========================Button Actions===============================================
def popup():
    response = messagebox.askyesno("Neutral Network Training","Do you want to start training")
    if response == 1:
        print('Answer is Yes')
        prog_bar()
    else:
        print('Answer is not')

def start_mqtt_thread(x):
    global long_thread
    long_thread = threading.Thread(target=run,kwargs={'loop_trigger': x})
    long_thread.start()
# ===========================GUI Settings===============================================
root = ttk.Window()
root.title('RetroVision Control Panel')
root.resizable(0, 0)
root.style.theme_use('cosmo') # Use or set this theme
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=3)
root.configure()
# style
font_style = font.Font(family='Roboto', size=22,weight='bold')
myFont = font.Font(size=33)
#  Footer
copyright = u"\u00A9"
status_frame =tk.Frame(root)
status_frame.grid(row=100,column=0,columnspan=5,)
status = Label(status_frame, text="Copyright "+ copyright + " RetroVision, 2022",relief=SUNKEN,bd=1)
status.grid(row=0,column=0,pady=10)
#=======================Title and Logo===================================
username_label = ttk.Label(root, text="RetroVision",font=('times', 42, 'bold', 'italic'))
username_label.grid(column=0, row=0, sticky=tk.W, padx=20, pady=20)
logo = (Image.open("eye.png"))
logo = logo.resize((65, 60), Image.ANTIALIAS)
logo = ImageTk.PhotoImage(logo)
image_label = ttk.Label(root, image=logo)
username_entry = ttk.Entry(root)
image_label.grid(column=1, row=0, sticky=tk.E, padx=5, pady=5)
#=======================Buttons===================================
#   Button R1C1
print(os.path.abspath(os.path.dirname(__file__)) + "\images\camera.png")

camera = PhotoImage(file=r"C:\Users\ASAD\Desktop\Digi Project\Gui\images\camera.png")
camera = camera.subsample(4, 4)
Load_RetroVision = Button(root,command=main,image = camera,compound=LEFT)
Load_RetroVision.grid(column=0, row=1, sticky=tk.W, padx=20, pady=40)
#   Button R1C2
nn_image = PhotoImage(file=r"C:\Users\ASAD\Desktop\Digi Project\Gui\images\nn.png")
nn_image = nn_image.subsample(4, 4)
Neural_Network=Button(root,image = nn_image,compound=LEFT,command=popup)
Neural_Network.grid(column=1, row=1, sticky=tk.E, padx=20, pady=40)
#   Button R2C2
vv_image = PhotoImage(file=r"C:\Users\ASAD\Desktop\Digi Project\Gui\images\visualization.png")
vv_image = vv_image.subsample(4, 4)
visualization = Button(root,image=vv_image,font=font_style,command=lambda:start_mqtt_thread(True))
visualization.grid(column=0, row=2, sticky=tk.W, padx=20, pady=40)
# MQTT Button row 2
settings_image = PhotoImage(file=r"C:\Users\ASAD\Desktop\Digi Project\Gui\images\settings.png")
settings_image = settings_image.subsample(4, 4)
Settings = Button(root,image=settings_image)
Settings.grid(column=1, row=2, sticky=tk.E, padx=20, pady=40)
#=======================action on exit window===================================
def confirm():
    ans = askyesno(title='Exit', message="Do you want to close the window?")
    if ans:
        root.destroy()
        run(False)  # to kill thread of mqtt
        print('mqqt terminated')
root.protocol("WM_DELETE_WINDOW",confirm)
root.mainloop()

