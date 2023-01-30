import io
import os
import tkinter
from json import JSONDecodeError
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import ttkbootstrap as ttk
import cv2
import PIL.ImageTk
from PIL import Image
import Section
import json


# Loads a Config for GUI Settings. If there is no config, it takes basic values and saves a config as soon as an image
# is being loaded.
def loadGUIConfig():
    # Path is script path + name of the config File.
    path = os.path.abspath(os.path.dirname(__file__)) + "\GUIConfig.json"
    # Try to read the data from the JSON File
    try:
        with io.open(path, 'r') as f:
            data = json.load(f)
            data_list = list(data.values())
            width = data_list[0]
            height = data_list[1]
            screen_width = data_list[2]
            screen_height = data_list[3]
            # If there is no background image path in the config, return without it
            if len(data_list) == 4:
                return width, height, screen_width, screen_height, None
            # If a path exists return width, height and the path
            background_path = data_list[4]
            return width, height, screen_width, screen_height, background_path

    # If the config file exists, but it is empty use default values. They are getting saved as soon as an image
    # is being loaded.
    except JSONDecodeError:
        screen_width, screen_height = get_curr_screen_geometry()
        print(screen_width, screen_height)
        width = 1280
        height = 720

        return width, height, screen_width, screen_height, None

    # If the config file does not exist, create a new file and use default values. They are getting saved as soon as
    # an image is being loaded.
    except FileNotFoundError:
        with io.open(path, 'w'):
            pass
        screen_width, screen_height = get_curr_screen_geometry()
        width = 1280
        height = 720
        return width, height, screen_width, screen_height, None


# Creation of Main GUI Class
def callback_lostfocus(event, element):
    element.unbind("<Return>")
    element.unbind("<Right>")
    element.unbind("<Left>")


class GUI:

    def __init__(self):
        # First off all values are getting reset.

        self.rectangle = None
        self.win2 = None
        self.isdoubleclicked = False
        self.canvas_height = 0
        self.canvas_width = 0
        self.btnNewRectPressed = False
        self.currentIndex = 0
        self.image_coordinates = []
        self.rectangles = {}
        self.sections = {}
        self.reset()

        # Then we create the main window. It uses the width and height provided by the config file.
        self.window = tkinter.Toplevel()
        self.window.geometry(str(GUIWIDTH) + "x" + str(GUIHEIGHT) + "+"
                             + str(int(SCREENWIDTH / 2 - ((GUIWIDTH + 350) / 2))) + "+"
                             + str(int(SCREENHEIGHT / 2 - GUIHEIGHT / 2)))
        self.window.title("ConfigGUI")
        self.window.resizable(False, False)
        self.window.lift()
        self.window.attributes('-topmost', 1)
        self.window.attributes('-topmost', 0)
#        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        # A canvas gets created to contain the image later on.
        self.canvas = Canvas(self.window, width=self.canvas_width, height=self.canvas_height)
        self.canvas.grid(row=0, column=1, rowspan=20, padx=30)
        self.canvas.bind('<Double-Button-1>', self.mousedoubleclick)

        # If a path exists in the config file the image is automatically getting selected.
        if BACKGROUND_PATH is not None:
            background_img = cv2.cvtColor(cv2.imread(BACKGROUND_PATH), cv2.COLOR_BGR2RGB)
            background_img = cv2.resize(background_img, (self.canvas_width, self.canvas_height))

            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(background_img))
            self.canvas.create_image(0, 0, image=self.photo, anchor=NW)

        # +++++++++++++++++++++++++++++++++++++ START OF BUTTONS ++++++++++++++++++++++++++++++++++++++++++++++++++

        # Creating a button to create new rectangles.
        self.btn_New_Rect = ttk.Button(self.window, text="New Rectangle", width=20, command=self.btnNewRect)
        self.btn_New_Rect.config(style='info.TButton')
        self.btn_New_Rect.grid(row=4, column=0, padx=30)

        # Creating a button to save segments
        self.btn_Save = ttk.Button(self.window, text="Save Config", width=20, command=self.btnSave)
        self.btn_Save.config(style='info.TButton')
        self.btn_Save.grid(row=3, column=0, padx=30)

        # Creating a button to load segments
        self.btn_Load = ttk.Button(self.window, text="Load Config", width=20, command=self.btnLoad)
        self.btn_Load.config(style='info.TButton')
        self.btn_Load.grid(row=2, column=0, padx=30)

        # Creating a button to load an image.
        self.btn_loadImage = ttk.Button(self.window, text="Load Image", width=20, command=self.loadBackgroundImage)
        self.btn_loadImage.config(style='info.TButton')
        self.btn_loadImage.grid(row=1, column=0, padx=30)

        # Creating a button to create a new Project
        self.btn_new = ttk.Button(self.window, text="New", width=20, command=self.btnNew)
        self.btn_new.config(style='info.TButton')
        self.btn_new.grid(row=0, column=0, padx=30)

        # +++++++++++++++++++++++++++++++++++++ END OF BUTTONS ++++++++++++++++++++++++++++++++++++++++++++++++++++

        self.lbl_mousePos = ttk.Label(self.window, text=" \n ")
        self.lbl_mousePos.grid(row=0, column=3)

        # Main process to keep the window alive.
        self.window.mainloop()

# ---------------------------------- START OF GUI RELATED METHODS ------------------------------------------------------

    # Resetting all values that have to be reset.
    def reset(self):
        self.sections = {}
        self.rectangles = {}
        self.image_coordinates = []
        self.currentIndex = 0
        self.btnNewRectPressed = False
        self.canvas_width = int(GUIWIDTH * 0.75)
        self.canvas_height = GUIHEIGHT
        self.isdoubleclicked = False
        self.win2 = None

    # Method to load the background image.
    def loadBackgroundImage(self):
        if self.win2 is not None and self.win2.winfo_exists():
            return
        # Filepath
        initial_path = os.path.abspath(os.path.dirname(__file__))
        # Open a dialog to select a picture (the one that is going to be segmented)
        path = filedialog.askopenfile(mode='r', filetypes=[("Jpg File", "*.jpg"), ("PNG File", "*.png")],
                                      initialdir=initial_path)
        if path is None:
            return

        # Save picture path in the config for the GUI.
        config_path = os.path.abspath(os.path.dirname(__file__)) + "\GUIConfig.json"
        data = {'width': GUIWIDTH, 'height': GUIHEIGHT, 'screen_width': SCREENWIDTH, 'screen_height': SCREENHEIGHT,
                'background_img': path.name}
        with io.open(config_path, 'w', encoding='utf8') as outfile:
            str_ = json.dumps(data, indent=4, sort_keys=False,
                              separators=(',', ': '), ensure_ascii=False)
            outfile.write(str_)

        # Prepare image to be used.
        background_img = cv2.cvtColor(cv2.imread(path.name), cv2.COLOR_BGR2RGB)
        background_img = cv2.resize(background_img, (self.canvas_width, self.canvas_height))

        # Set the picture as image inside the canvas.
        self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(background_img))
        self.canvas.create_image(0, 0, image=self.photo, anchor=NW)

# ---------------------------------- END OF GUI RELATED METHODS --------------------------------------------------------

# ---------------------------------- START OF BUTTON METHODS -----------------------------------------------------------

    # Method for the button "New"
    def btnNew(self):
        # "Deactivate" if the 2nd window exists
        if self.win2 is not None and self.win2.winfo_exists():
            return
        # If 2nd window does not exist, reset the window.
        self.reset()
        self.loadBackgroundImage()

    # Method for the button "New Rectangle"
    def btnNewRect(self):
        if self.win2 is not None and self.win2.winfo_exists():
            return
        # If the Button was not pressed already, start in first part, if it was pressed before start in 2nd part.
        # The style gets set, then Leftclick, stop clicking left and moving the mouse get bound (unbound) to methods
        if not self.btnNewRectPressed:
            self.btn_New_Rect.config(style='danger.TButton')
            self.btnNewRectPressed = True

            self.canvas.bind('<Button-1>', self.mousedown)
            self.canvas.bind('<ButtonRelease-1>', self.mouseup)
            self.canvas.bind('<Motion>', self.mousepos)
        else:
            self.btn_New_Rect.config(style='info.TButton')
            self.btnNewRectPressed = False

            self.canvas.unbind('<Button-1>')
            self.canvas.unbind('<ButtonRelease-1>')
            self.canvas.unbind('<Motion>')
            self.lbl_mousePos.config(text=" \n ")

    # Method for the button "Save"
    def btnSave(self):
        if self.win2 is not None and self.win2.winfo_exists():
            return
        data = {}
        # Select all data from the elements List that contains all of our elements
        for i in range(len(self.sections)):
            element = self.sections.get(i)
            out_x1 = element.get_x1()
            out_y1 = element.get_y1()
            out_x2 = element.get_x2()
            out_y2 = element.get_y2()
            out_unit = element.get_unit()
            out_min = element.get_min()
            out_max = element.get_max()
            out_name = element.get_name()
            out_type = element.get_type()
            out_desc = element.get_desc()

            data[out_name] = {'x1': out_x1, 'y1': out_y1, 'x2': out_x2, 'y2': out_y2, 'unit': out_unit,
                              'min': out_min, 'max': out_max, 'type': out_type, 'desc': out_desc}

        # Get path by opening up a file dialog
        initial_path = os.path.abspath(os.path.dirname(__file__))
        path = filedialog.asksaveasfile(mode='w', defaultextension=".json", filetypes=[("Json File", "*.json")],
                                        initialdir=initial_path)
        if path is None:
            return

        # Save the data in a json file
        with io.open(path.name, 'w', encoding='utf8') as outfile:
            str_ = json.dumps(data,
                              indent=4, sort_keys=False,
                              separators=(',', ': '), ensure_ascii=False)
            outfile.write(str_)

    # Method for the Button "Load"
    def btnLoad(self):
        if self.win2 is not None and self.win2.winfo_exists():
            return

        # Get path by opening up a file dialog
        initial_path = os.path.abspath(os.path.dirname(__file__))
        path = filedialog.askopenfile(mode='r', filetypes=[("Json File", "*.json")], initialdir=initial_path)
        if path is None:
            return

        self.currentIndex = len(self.rectangles)
        while self.currentIndex > 0:
            self.canvas.delete(self.rectangles[self.currentIndex - 1])
            self.currentIndex -= 1

        self.reset()

        with io.open(path.name, 'r') as f:
            data = json.load(f)

        # Read data from the selected file and save information in the List
        data_list = list(data.values())
        key_list = list(data.keys())
        for i in range(len(data_list)):
            lst_sections = data_list[i]
            sectionitem = Section.Section(int(lst_sections.get('x1')), int(lst_sections.get('y1')),
                                          int(lst_sections.get('x2')), int(lst_sections.get('y2')),
                                          lst_sections.get('unit'), lst_sections.get('min'),
                                          lst_sections.get('max'), key_list[self.currentIndex],
                                          lst_sections.get('type'), lst_sections.get('desc'))

            self.sections[self.currentIndex] = sectionitem
            self.rectangles[self.currentIndex] = self.canvas.create_rectangle(lst_sections.get('x1'),
                                                                              lst_sections.get('y1'),
                                                                              lst_sections.get('x2'),
                                                                              lst_sections.get('y2'),
                                                                              outline="#ff0000", width=3)
            self.currentIndex += 1

    # Method for the Button "OK" in the 2nd window
    def win2_btnOK(self):

        # Save values from all Textboxes in the List
        self.rectangles[self.currentIndex] = self.rectangle
        self.section.setAllValues(int(self.win2txtx1.get()), int(self.win2txty1.get()),
                                  int(self.win2txtx2.get()), int(self.win2txty2.get()), self.win2txtunit.get(),
                                  self.win2txtmin.get(), self.win2txtmax.get(), self.win2txtsection.get(),
                                  self.win2cmbtype.get(), self.win2txtdesc.get("1.0", "end-1c"))
        self.sections[self.currentIndex] = self.section
        self.win2.destroy()

    # Method for the Button "Cancel" in the 2nd window
    def win2_btnCancel(self):
        self.canvas.delete(self.rectangle)
        # Check if window is opened by "New" or by doubleclicking inside a rectangle
        if self.isdoubleclicked:
            self.rectangle = self.canvas.create_rectangle(float(self.x1), float(self.y1),
                                                          float(self.x2), float(self.y2),
                                                          outline="#ff0000", width=3)
            self.rectangles[self.currentIndex] = self.rectangle
        self.isdoubleclicked = False
        self.win2.destroy()

    # Method was originally planned for a preview Button, it's now used for the rectangle preview with arrow keys
    def win2_btnPreview(self, event):
        self.canvas.delete(self.rectangle)
        self.rectangle = self.canvas.create_rectangle(float(self.win2txtx1.get()), float(self.win2txty1.get()),
                                                      float(self.win2txtx2.get()), float(self.win2txty2.get()),
                                                      outline="#ff0000", width=3)

    # Method for the Button "Delete" in the 2nd window
    def win2_btnDelete(self):
        self.canvas.delete(self.rectangle)
        # Delete the value from the list and from the rectangle list
        for i in range(len(self.sections)):
            if i > self.currentIndex:
                self.sections[i - 1] = self.sections[i]
                self.rectangles[i - 1] = self.rectangles[i]
        del self.sections[len(self.sections) - 1]
        del self.rectangles[len(self.rectangles) - 1]
        self.win2.destroy()

# ---------------------------------- END OF BUTTON METHODS -------------------------------------------------------------

# ---------------------------------- START OF MOUSE EVENTS -------------------------------------------------------------

    # If Left mouse gets clicked get coordinates of the mouse
    def mousedown(self, event):
        self.image_coordinates = [(event.x, event.y)]

    # If Left mouse stops getting clicked get the 2nd pair of coordinates, also unbind stuff related to "New Rectangle"-
    # Button and create a new section fed with the values of coordinates and open 2nd window.
    def mouseup(self, event):
        self.image_coordinates.append((event.x, event.y))

        self.btn_New_Rect.config(style='info.TButton')
        self.btnNewRectPressed = False

        self.canvas.unbind('<Button-1>')
        self.canvas.unbind('<ButtonRelease-1>')
        self.canvas.unbind('<Motion>')
        self.lbl_mousePos.config(text=" \n ")

        rect_x = self.image_coordinates[0][0]
        rect_y = self.image_coordinates[0][1]
        rect_x2 = self.image_coordinates[1][0]
        rect_y2 = self.image_coordinates[1][1]

        newrect = self.canvas.create_rectangle(rect_x, rect_y, rect_x2, rect_y2, outline="#ff0000", width=3)

        newsection = Section.Section(rect_x, rect_y, rect_x2, rect_y2, "", "", "", "", "", "")
        self.currentIndex = len(self.sections)

        self.createEditWindow(newsection, newrect)

    # Get position of the mouse and post coordinates in a Label
    def mousepos(self, event):
        x = event.x
        y = event.y

        self.lbl_mousePos.config(text="x: " + str(x) + " \ny: " + str(y))

    # Handles what happens when left mouse button gets doubleclicked
    def mousedoubleclick(self, event):
        if self.win2 is not None and self.win2.winfo_exists():
            return
        self.isdoubleclicked = True
        x = event.x
        y = event.y
        # Read the values for the corresponding Section and put them in the 2nd window
        self.currentIndex = len(self.sections)
        for i in range(self.currentIndex):
            section = self.sections[i]
            if section.get_x1() < x < section.get_x2() and section.get_y1() < y < section.get_y2():
                rectangle = self.rectangles.get(i)
                self.currentIndex = i
                self.createEditWindow(section, rectangle)
                return

# ---------------------------------- END OF MOUSE EVENTS ---------------------------------------------------------------

# ---------------------------------- START OF SECOND GUI ---------------------------------------------------------------

    # Create a 2nd GUI with a lot of elements like Labels and Entries (Textboxes)
    def createEditWindow(self, sect, newrect):
        self.win2 = Toplevel(self.window)
        self.win2.geometry("350x" + str(GUIHEIGHT) + "+" + str(int(SCREENWIDTH / 2 - ((GUIWIDTH + 350) / 2) + GUIWIDTH))
                           + "+" + str(int(SCREENHEIGHT / 2 - GUIHEIGHT / 2)))
        self.win2.title("Edit")
        self.win2.resizable(False, False)

        self.win2.columnconfigure(0, weight=1)
        self.win2.columnconfigure(1, weight=8)
        self.win2.protocol("WM_DELETE_WINDOW", self.win2_btnCancel)

        vcmd = (self.canvas.register(self.is_Integer), '%S')

        self.section = sect
        self.rectangle = newrect

        self.x1 = self.section.get_x1()
        self.y1 = self.section.get_y1()
        self.x2 = self.section.get_x2()
        self.y2 = self.section.get_y2()

        self.win2lblx1 = ttk.Label(self.win2, text="x1:")
        self.win2lblx1.grid(row=0, column=0, sticky=ttk.W, padx=5, pady=5)

        self.win2txtx1 = ttk.Entry(self.win2, width=30, validate='key', validatecommand=vcmd)
        self.win2txtx1.grid(row=0, column=1, sticky=ttk.W, padx=5, pady=5)
        self.win2txtx1.insert(0, sect.get_x1())
        self.win2txtx1.bind("<FocusIn>", lambda event: self.callback_focus(event, element=self.win2txtx1))
        self.win2txtx1.bind("<FocusOut>", lambda event: callback_lostfocus(event, element=self.win2txtx1))

        self.win2lbly1 = ttk.Label(self.win2, text="y1:")
        self.win2lbly1.grid(row=1, column=0, sticky=ttk.W, padx=5, pady=5)

        self.win2txty1 = ttk.Entry(self.win2, width=30, validate='key', validatecommand=vcmd)
        self.win2txty1.grid(row=1, column=1, sticky=ttk.W, padx=5, pady=5)
        self.win2txty1.insert(0, sect.get_y1())
        self.win2txty1.bind("<FocusIn>", lambda event: self.callback_focus(event, element=self.win2txty1))
        self.win2txty1.bind("<FocusOut>", lambda event: callback_lostfocus(event, element=self.win2txty1))

        self.win2lblx2 = ttk.Label(self.win2, text="x2:")
        self.win2lblx2.grid(row=2, column=0, sticky=ttk.W, padx=5, pady=5)

        self.win2txtx2 = ttk.Entry(self.win2, width=30, validate='key', validatecommand=vcmd)
        self.win2txtx2.grid(row=2, column=1, sticky=ttk.W, padx=5, pady=5)
        self.win2txtx2.insert(0, sect.get_x2())
        self.win2txtx2.bind("<FocusIn>", lambda event: self.callback_focus(event, element=self.win2txtx2))
        self.win2txtx2.bind("<FocusOut>", lambda event: callback_lostfocus(event, element=self.win2txtx2))

        self.win2lbly2 = ttk.Label(self.win2, text="y2:")
        self.win2lbly2.grid(row=3, column=0, sticky=ttk.W, padx=5, pady=5)

        self.win2txty2 = ttk.Entry(self.win2, width=30, validate='key', validatecommand=vcmd)
        self.win2txty2.grid(row=3, column=1, sticky=ttk.W, padx=5, pady=5)
        self.win2txty2.insert(0, sect.get_y2())
        self.win2txty2.bind("<FocusIn>", lambda event: self.callback_focus(event, element=self.win2txty2))
        self.win2txty2.bind("<FocusOut>", lambda event: callback_lostfocus(event, element=self.win2txty2))

        self.win2lblunit = ttk.Label(self.win2, text="Unit:")
        self.win2lblunit.grid(row=4, column=0, sticky=ttk.W, padx=5, pady=5)

        self.win2txtunit = ttk.Entry(self.win2, width=30)
        self.win2txtunit.grid(row=4, column=1, sticky=ttk.W, padx=5, pady=5)
        self.win2txtunit.insert(0, sect.get_unit())

        self.win2lblmin = ttk.Label(self.win2, text="Min Value:")
        self.win2lblmin.grid(row=5, column=0, sticky=ttk.W, padx=5, pady=5)

        self.win2txtmin = ttk.Entry(self.win2, width=30)
        self.win2txtmin.grid(row=5, column=1, sticky=ttk.W, padx=5, pady=5)
        self.win2txtmin.insert(0, sect.get_min())

        self.win2lblmax = ttk.Label(self.win2, text="Max Value:")
        self.win2lblmax.grid(row=6, column=0, sticky=ttk.W, padx=5, pady=5)

        self.win2txtmax = ttk.Entry(self.win2, width=30)
        self.win2txtmax.grid(row=6, column=1, sticky=ttk.W, padx=5, pady=5)
        self.win2txtmax.insert(0, sect.get_max())

        self.win2lblsection = ttk.Label(self.win2, text="Name of Section:")
        self.win2lblsection.grid(row=7, column=0, sticky=ttk.W, padx=5, pady=5)

        self.win2txtsection = ttk.Entry(self.win2, width=30)
        self.win2txtsection.grid(row=7, column=1, sticky=ttk.W, padx=5, pady=5)
        self.win2txtsection.insert(0, sect.get_name())

        self.win2lbltype = ttk.Label(self.win2, text="Type:")
        self.win2lbltype.grid(row=8, column=0, sticky=ttk.W, padx=5, pady=5)

        self.win2cmbtype = ttk.Combobox(self.win2, width=28)
        self.win2cmbtype['values'] = ('Needle', 'LCD', 'Lamp')
        self.win2cmbtype.grid(row=8, column=1, sticky=ttk.W, padx=5, pady=5)
        self.win2cmbtype.set(sect.get_type())

        self.win2lbldesc = ttk.Label(self.win2, text="Description:")
        self.win2lbldesc.grid(row=9, column=0, sticky=ttk.W, padx=5, pady=5)

        self.win2txtdesc = ttk.Text(self.win2, width=30, height=8)
        self.font = ("Segoe UI", 9, "normal")
        self.win2txtdesc.configure(font=self.font)
        self.win2txtdesc.grid(row=9, column=1, sticky=ttk.W, padx=5, pady=5)
        self.win2txtdesc.insert("end", sect.get_desc())

        self.win2btnok = ttk.Button(self.win2, text="OK", width=28, command=self.win2_btnOK)
        self.win2btnok.grid(row=10, column=1, sticky=ttk.W, padx=5, pady=5)

        self.win2btncancel = ttk.Button(self.win2, text="Cancel", width=28, command=self.win2_btnCancel)
        self.win2btncancel.grid(row=11, column=1, sticky=ttk.W, padx=5, pady=5)

        self.win2btndelete = ttk.Button(self.win2, text="Delete", width=28, command=self.win2_btnDelete)
        self.win2btndelete.grid(row=12, column=1, sticky=ttk.W, padx=5, pady=5)

# ---------------------------------- END OF SECOND GUI -----------------------------------------------------------------

    # Wird aufgerufen, wenn in ein Textfeld geklickt wird
    def callback_focus(self, event, element):
        element.bind("<Return>", self.win2_btnPreview)
        element.bind("<Right>", lambda event: self.inc_1(event, element))
        element.bind("<Left>", lambda event: self.dec_1(event, element))

    # Increase value of textbox by 1
    def inc_1(self, event, element):
        value = int(element.get())
        value += 1
        element.delete(0, END)
        element.insert(0, value)
        self.win2_btnPreview(event)
        return

    # Decrease value of textbox by 1
    def dec_1(self, event, element):
        value = int(element.get())
        value -= 1
        element.delete(0, END)
        element.insert(0, value)
        self.win2_btnPreview(event)
        return

    # Check if entry in textbox is an Integer, if not make a sound
    def is_Integer(self, s):
        if s.isdigit():
            return True
        self.canvas.bell()
        return False

    # Handles what happens by pressing on the "X" of a window
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.window.destroy()
            exit(1)

# Needed to return the width and height of the screen the window is displayed on
def get_curr_screen_geometry():
    root = Tk()
    root.update_idletasks()
    root.attributes('-fullscreen', True)
    root.state('iconic')
    geometry = root.winfo_geometry()
    root.attributes('-fullscreen', False)
    root.state('normal')
    root.destroy()
    geometry = geometry[:-4]
    x = geometry.split("x")
    screen_width, screen_height = int(x.pop(0)), int(x.pop(0))
    return screen_width, screen_height


# Main Method
def main():
    global GUIWIDTH, GUIHEIGHT, SCREENWIDTH, SCREENHEIGHT, BACKGROUND_PATH
    GUIWIDTH, GUIHEIGHT, SCREENWIDTH, SCREENHEIGHT, BACKGROUND_PATH = loadGUIConfig()
    gui = GUI()