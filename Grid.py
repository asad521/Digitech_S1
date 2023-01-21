# This is a sample Python script.
import tkinter as tk
from tkinter  import *
from PIL import ImageTk, Image

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

def print_hi():
    window = tk.Tk()
    window.title('Login')
    window.geometry("640x480")

    window.resizable(0, 0)

    #devide window
    Header_Frame = Frame(window)
    Header_Frame.pack()
    Fotter_Frame = Frame(window)
    Fotter_Frame.pack(side=BOTTOM)

    heading1 = Label(Header_Frame,text="RetroVision",font=('times', 42, 'bold', 'italic'))
    heading1.grid(row=0,column=0,sticky=tk.W)

    # Load an image in the script
    img = (Image.open("eye2.png"))
    # Resize the Image using resize method
    resized_image = img.resize((50, 55), Image.ANTIALIAS)
    new_image = ImageTk.PhotoImage(resized_image)

    image_label = Label(Header_Frame,image=new_image)
    image_label.grid(row=0,column=1,sticky=tk.E,pady=5,padx=5)






    Fotter_status = Label(Fotter_Frame, text="All right reserved")
    Fotter_status.pack()




    window.mainloop()  # placing window on screen

if __name__ == '__main__':
       print_hi()