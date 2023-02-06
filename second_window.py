# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from tkinter import *
from tkinter import Tk, Frame, Label
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import time
import threading


def print_hi():
    # Use a breakpoint in the code line below to debug your script.
    window = Tk()
    mainframe = Frame(window, bg="red")
    mainframe.pack(fill="both", expand=True)
    # horizontal
    label = Label(mainframe, text="Horizontal Frame Example", bg="black", fg="white", padx=5, pady=5)
    label.config(font=("Arial", 18))
    label.pack(fill="x")
    horizontal_frame = Frame(mainframe)

    Button_1 = Button(horizontal_frame, text="Item 1 in Horizontal", bg="red", fg="white", padx=10, pady=10)
    Button_1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    Button_2 = Button(horizontal_frame, text="Item 2 in Horizontal", bg="red", fg="white", padx=10, pady=10)
    Button_2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
    Button_3 = Button(horizontal_frame, text="Item 3 in Horizontal", bg="red", fg="white", padx=10, pady=10)
    Button_3.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")
    Button_4 = Button(horizontal_frame, text="Item 4 in Horizontal", bg="red", fg="white", padx=10, pady=10)
    Button_4.grid(row=0, column=3, padx=10, pady=10, sticky="nsew")

    horizontal_frame.grid_columnconfigure(0, weight=1)
    horizontal_frame.grid_columnconfigure(1, weight=1)
    horizontal_frame.grid_columnconfigure(2, weight=1)
    horizontal_frame.grid_columnconfigure(3, weight=1)
    horizontal_frame.pack(fill="x")

    # end horizontal
    # grid data
    run_labeling = Button(mainframe, text="run_labeling", bg="black", fg="white", padx=5, pady=5,
                          command=lambda: my_fun(True))
    run_labeling.config(font=("Arial", 18))
    run_labeling.pack()
    # run_labeling.pack(fill="x")
    training = Label(mainframe, text="training.....", bg="black", fg="white", padx=5, pady=5)
    label.config(font=("Arial", 18))
    label.pack(fill="x")


    # Create an object of tkinter ImageTk


    # status bar
    # Create a Label Widget to display the text or Image
    prg1 = ttk.Progressbar(mainframe, orient=HORIZONTAL,
                           value=1, length=300, mode='determinate', )
    prg1.pack(padx=5, pady=5, side=BOTTOM, fill='x')

    grid_frame = Frame(mainframe)
    grid_frame.pack(fill="x")
    def bar_init(var):
        # first layer of isolation, note var being passed along to the self.start_bar function
        # target is the function being started on a new thread, so the "bar handler" thread
        print('in  bar_init')
        start_bar_thread = threading.Thread(target=start_bar, args=(var,))
        # start the bar handling thread
        start_bar_thread.start()

    def start_bar( var):
        # the load_bar needs to be configured for indeterminate amount of bouncing
        prg1.config(mode='indeterminate', maximum=100, value=0)
        # 8 here is for speed of bounce
        prg1.start(8)
        # start the work-intensive thread, again a var can be passed in here too if desired
        work_thread = threading.Thread(target=work_task, args=(var,))
        work_thread.start()
        # close the work thread
        work_thread.join()
        # stop the indeterminate bouncing
        prg1.stop()
        # reconfigure the bar so it appears reset
        prg1.config(value=0, maximum=0)

    def work_task(wait_time):
        for x in range(wait_time):
           time.sleep(0.001)

    def bar_stop(wait_time):
        prg1.pack_forget()

        prg1.stop()


    button = Button(window, text="download",command=lambda: bar_init(250000)).pack()
    button = Button(window, text="stop",command=lambda: bar_stop(250000)).pack()

    mainframe.mainloop()




# Press the green button in the gutter to run the script.
def prog_bar():

    print_hi()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
