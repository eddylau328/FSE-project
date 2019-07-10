import tkinter as tk
import tkinter.ttk as ttk
import database as db
import random
from tkinter import filedialog
import sys


class GUI:
    def __init__(self, os_platform):
        if (os_platform == "OS X"):

            self.filter_checkbutton_fontsize = 12

            # Modify FILES POPUP WINDOW CONSTANT
            self.modify_listbox_width = 28
            self.modify_width = 900
            self.modify_height = 500
            self.modify_leftframe_wraplength = 200
            self.modify_leftframe_width = 30
            self.modify_leftframe_font = 12
        elif (os_platform == "Windows"):

            self.filter_checkbutton_fontsize = 9

            # Modify FILES POPUP WINDOW CONSTANT
            self.modify_listbox_width = 40
            self.modify_width = 900
            self.modify_height = 500
            self.modify_leftframe_wraplength = 200
            self.modify_leftframe_width = 32
            self.modify_leftframe_font = 9


def get_platform():
    platforms = {
        'darwin' : 'OS X',
        'win32' : 'Windows'
    }
    if (sys.platform not in platforms):
        return sys.platform

    return platforms[sys.platform]
'''
if get all
    [0] => name
    [1] => filepath
    [2] => category
    [3] => creator
    [4] => description
    [5] => create date
    [6] => last modify
'''


class Show_Data_Package:
    def __init__(self, frame):
        self.data = db.Data()
        self.GUI = GUI(get_platform())
        # name title label
        self.name_title = tk.Label(frame, text="Name :", font=('Arial', self.GUI.modify_leftframe_font))
        # name entry id
        self.name_entry_id = tk.StringVar()
        self.name_entry_id.set("")
        self.name_entry = tk.Entry(frame, textvariable=self.name_entry_id, font=('Arial', self.GUI.modify_leftframe_font), width=self.GUI.modify_leftframe_width)

        # creator title label
        self.creator_title = tk.Label(frame, text="Creator :", font=('Arial', self.GUI.modify_leftframe_font))

        # creator label
        self.creator_id = tk.StringVar()
        self.creator_id.set("")
        self.creator_label = tk.Label(frame, textvariable=self.creator_id, font=('Arial', self.GUI.modify_leftframe_font), wraplength=self.GUI.modify_leftframe_width, justify="left", width=0)

        # category title label
        self.category_title = tk.Label(frame, text="Category :", font=('Arial', self.GUI.modify_leftframe_font))
        # category entry id
        self.category_id = tk.StringVar()
        self.category_id.set("")
        self.category_label = tk.Label(frame, textvariable=self.category_id, font=('Arial', self.GUI.modify_leftframe_font), wraplength=self.GUI.modify_leftframe_wraplength, justify="left", width=0)

        # filepath label
        self.filename_title = tk.Label(frame, text="Filename", font=('Arial', self.GUI.modify_leftframe_font))

        # current filepath id
        self.current_filename_id = tk.StringVar()
        self.current_filename_id.set("")
        self.current_filename_entry = tk.Entry(frame, textvariable=self.current_filename_id, font=('Arial', self.GUI.modify_leftframe_font), width=self.GUI.modify_leftframe_width)

        # filepath label
        self.filepath_title = tk.Label(frame, text="Filepath", font=('Arial', self.GUI.modify_leftframe_font))

        # current filepath id
        self.current_filepath_id = tk.StringVar()
        self.current_filepath_id.set("")
        self.current_filepath = tk.Label(frame, textvariable=self.current_filepath_id, font=('Arial', self.GUI.modify_leftframe_font), wraplength=self.GUI.modify_leftframe_wraplength, justify="left", width=0)

        # description title label
        self.description_title = tk.Label(frame, text="Description :", font=('Arial', self.GUI.modify_leftframe_font))

        # description entry id
        self.description_text = tk.Text(frame, font=('Arial', self.GUI.modify_leftframe_font), height=10, width=self.GUI.modify_leftframe_width)

    # row, column is start from corner
    def show_name(self, row, column):
        self.name_title.grid(row=row, column=column, sticky="W", padx=5, pady=8)
        self.name_entry.grid(row=row, column=column + 1, sticky="W", padx=5, pady=8)

    # row, column is start from corner
    def show_creator(self, row, column):
        self.creator_title.grid(row=row, column=column, sticky="WN", padx=5, pady=8)
        self.creator_label.grid(row=row, column=column + 1, sticky="WN", padx=5, pady=8)

    # row, column is start from corner
    def show_category(self, row, column):
        self.category_title.grid(row=row, column=column, sticky="W", padx=5, pady=8)
        self.category_label.grid(row=row, column=column + 1, sticky="W", padx=5, pady=8)

    # row, column is start from corner
    def show_filename(self, row, column):
        self.filename_title.grid(row=row, column=column, sticky="WN", padx=5, pady=8)
        self.current_filename_entry.grid(row=row, column=column + 1, sticky="WN", padx=5, pady=8)

    # row, column is start from corner
    def show_filepath(self, row, column):
        self.filepath_title.grid(row=row, column=column, sticky="WN", padx=5, pady=8)
        self.current_filepath.grid(row=row, column=column + 1, sticky="WN", padx=5, pady=8)

    # row, column is start from corner
    def show_description(self, row, column):
        self.description_title.grid(row=row, column=column, sticky="WN", padx=5, pady=8)
        self.description_text.grid(row=row, column=column + 1, sticky="W", padx=5, pady=8)

    def set(self, **kwargs):
        name = kwargs.get('name', None)
        creator = kwargs.get('creator', None)
        category = kwargs.get('category', None)
        filename = kwargs.get('filename', None)
        filepath = kwargs.get('filepath', None)
        description = kwargs.get('description', None)
        self.data.set(name=name, creator=creator, category=category, filename=filename, filepath=filepath, description=description)
        self.name_entry_id.set(name)
        self.creator_id.set(creator)
        self.category_id.set(category)
        self.current_filename_id.set(filename)
        self.current_filepath_id.set(filepath)
        # clear the content in the description text box
        self.description_text.delete('1.0', 'end')
        if (description != None):
            self.description_text.insert("end", description)

    def compare_value(self):
        dataset = self.data.get()
        isSame = True
        if (dataset['name'] != self.name_entry_id.get()):
            print("pass1")
            isSame = False
        if (dataset['filename'] != self.current_filename_id.get()):
            print("pass2")
            isSame = False
        if (dataset['filepath'] != self.current_filepath_id.get()):
            print("pass3")
            isSame = False
        if (dataset['category'] != self.category_id.get()):
            print("pass4")
            isSame = False
        if (dataset['description'].replace(" ", "") != self.description_text.get("1.0", "end-1c").replace(" ","")):
            print("'"+dataset['description']+"'")
            print("'"+self.description_text.get("1.0", "end")+"'")
            isSame = False
        return isSame


class Root:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Files Search Engine")
        self.window_width = 1360
        self.window_height = 800
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        x_coor = (self.screen_width / 2) - (self.window_width / 2)
        y_coor = (self.screen_height / 2) - (self.window_height / 2)
        self.root.geometry("%dx%d+%d+%d" % (self.window_width, self.window_height, x_coor, y_coor))


class Checkbutton:
    def __init__(self, root, name, row, column, fontsize):
        self.value_id = tk.IntVar(value=1)
        self.category = name
        self.checkbutton = tk.Checkbutton(root, text=name, variable=self.value_id, font=('Arial', fontsize))
        self.checkbutton.grid(row=row, column=column, sticky="W")


class Page(Root):
    def __init__(self):
        Root.__init__(self)
        # check what os system the user is using
        self.GUI = GUI(get_platform())

        self.root.grid_rowconfigure(0, minsize=30)
        self.root.grid_columnconfigure(0, minsize=20)
        # Heading
        self.heading = tk.Label(self.root, text="Files Search Engine", font=('Arial', 32), height=1)
        self.heading.grid(row=1, column=1, columnspan=10, sticky="W")
        # skip the line for some spaces
        self.root.grid_rowconfigure(2, minsize=10)

        # search title
        self.search_title = tk.LabelFrame(self.root, text="Search", font=('Arial', 16), height=2)
        self.search_title.grid(row=3, column=1, sticky="W")
        # search label
        self.search_label = tk.Label(self.search_title, text="Keyword :", font=('Arial', 14))
        self.search_label.grid(row=4, column=1, sticky="W")
        # search
        # search_entry_id is the var saves the input string from search_entry
        self.search_entry_id = tk.StringVar()
        self.search_entry = tk.Entry(self.search_title, textvariable=self.search_entry_id, font=('Arial', 14))
        self.search_entry.grid(row=4, column=2, sticky="W")

        # search button
        self.search_button = tk.Button(self.search_title, text="Search", font=('Arial', 12), command=lambda: self.search(self.search_method_id.get(), self.search_entry_id.get()))
        self.search_button.grid(row=4, column=3)

        # search method radiobutton
        # search_method_id is the var saves the radio button value
        self.search_method_id = tk.StringVar()
        self.search_method_id.set("relate")
        # relate radio button
        self.relate_radiobutton = tk.Radiobutton(self.search_title, text="Related", variable=self.search_method_id, value="relate")
        self.relate_radiobutton.grid(row=4, column=4, sticky="W")
        # exact radio button
        self.exact_radiobutton = tk.Radiobutton(self.search_title, text="Exact", variable=self.search_method_id, value="exact")
        self.exact_radiobutton.grid(row=4, column=5, sticky="W")

        # add button
        self.add_button = tk.Button(self.search_title, text="Add / Delete Files", command=lambda: self.add_delete_modify_files())
        self.add_button.grid(row=4, column=6, sticky="W")

        # skip the line for some spaces
        self.search_title.grid_rowconfigure(5, minsize=10)

        self.result_title = tk.LabelFrame(self.search_title, text="Results", font=('Arial', 16))
        self.result_title.grid(row=6, column=1, rowspan=100, columnspan=10)
        # table
        self.treeview = ttk.Treeview(self.result_title, height=28)
        #self.treeview.grid(row=6, column=1, rowspan=100, columnspan=10)
        self.treeview.pack(side="left", expand=True, fill=tk.Y)
        # set up the columns and headings
        self.treeview["columns"] = ["name", "filepath", "creator", "last_modify", "category"]
        self.treeview["show"] = "headings"
        self.treeview.heading("name", text="Title")
        self.treeview.heading("filepath", text="File Name")
        self.treeview.heading("creator", text="Creator")
        self.treeview.heading("last_modify", text="Last Modify")
        self.treeview.heading("category", text="Category")
        self.treeview.column('name', width=150)
        self.treeview.column('filepath', width=200)
        self.treeview.column('creator', width=100)
        self.treeview.column('last_modify', width=100)
        self.treeview.column('category', width=300)
        # click on the item in treeview
        self.treeview.bind("<Double-1>", self.click_treeview_item)

        # treeview veritcal scroll bar
        self.treeview_vertical_scrollbar = ttk.Scrollbar(self.result_title, orient="vertical")
        self.treeview_vertical_scrollbar.config(command=self.treeview.yview)
        self.treeview.config(yscrollcommand=self.treeview_vertical_scrollbar.set)
        self.treeview_vertical_scrollbar.pack(side="right", fill=tk.Y)

        # skip some x-dir spaces for the treeview and the filter
        self.search_title.grid_columnconfigure(12, minsize=5)

        # filter labelframe
        row = 6
        self.filter_title = tk.LabelFrame(self.search_title, text="Filter", font=('Arial', 16))
        self.filter_title.grid(row=row, column=13, rowspan=100, sticky="W")
        # checkbuttons for the database to sort in category
        self.checkbuttons = []
        row = 0
        column = 0
        for category in database.get_category():
            self.add_checkbutton(self.filter_title, category[0], row=row, column=column, fontsize=self.GUI.filter_checkbutton_fontsize)
            row += 1

        self.filter_radiobutton_id = tk.StringVar()
        self.filter_radiobutton_id.set("union")
        # union filter radiobutton
        self.filter_u_radiobutton = tk.Radiobutton(self.filter_title, text="Related", variable=self.filter_radiobutton_id, value="union")
        self.filter_u_radiobutton.grid(row=row, column=column, sticky="W")
        # intersection filter radiobutton
        self.filter_i_radiobutton = tk.Radiobutton(self.filter_title, text="Exact", variable=self.filter_radiobutton_id, value="intersect")
        self.filter_i_radiobutton.grid(row=row, column=column + 1, sticky="W")
        # filter button for the database to perform sorting
        row += 1
        self.filter_button = tk.Button(self.filter_title, text="Filter", font=('Arial', 12), command=lambda: self.filter(self.filter_radiobutton_id.get()))
        self.filter_button.grid(row=row, column=column, sticky="W")

        # disable all/ select all button for the checkbox in filter section
        self.filter_select_disable_id = tk.StringVar()
        self.filter_select_disable_id.set("Disable all")
        self.filter_select_disable_button = tk.Button(self.filter_title, textvariable=self.filter_select_disable_id, font=('Arial', 12), command=self.filter_checkbox_select_disable_all, width=10)
        self.filter_select_disable_button.grid(row=row, column=column + 1, sticky="W")

        # skip some x-dir space
        self.search_title.grid_columnconfigure(14, minsize=5)

        # tab control for changing the page
        self.minor_tab_control = ttk.Notebook(self.search_title, width=160, height=400)
        self.step_tab = ttk.Frame(self.minor_tab_control)
        self.minor_tab_control.add(self.step_tab, text="Steps")
        self.history_tab = ttk.Frame(self.minor_tab_control)
        self.minor_tab_control.add(self.history_tab, text="History")
        self.minor_tab_control.grid(row=7, column=15)

        # new search step
        self.step_new_button = tk.Button(self.step_tab, text="New Search", command=None)
        self.step_new_button.pack(side="bottom", fill=tk.X)
        # procedure search checkbutton
        self.step_procedure_search_id = tk.IntVar()
        self.step_procedure_search_id.set(0)
        self.step_procedure_search_checkbutton = tk.Checkbutton(self.step_tab, text="Procedure Search", variable=self.step_procedure_search_id, font=('Arial', 12))
        self.step_procedure_search_checkbutton.pack(side="bottom", fill=tk.X)

        # used to save the steps the user took
        self.step_listbox = tk.Listbox(self.step_tab)
        self.step_listbox.pack(side="left", fill=tk.BOTH, expand=1)
        # step_scrollbar
        self.step_scrollbar = ttk.Scrollbar(self.step_tab, orient="vertical")
        self.step_scrollbar.config(command=self.step_listbox.yview)
        self.step_listbox.config(yscrollcommand=self.step_scrollbar.set)
        self.step_scrollbar.pack(side="right", fill=tk.Y)

        # add clicking event in step_listbox
        self.step_listbox.bind('<Double-1>', self.click_step_listbox_item)
        # show that it is non-procedural search at the starting
        self.step_listbox.insert("end", f"Non-Procedural Search")

        # show all the current files inside database
        self.show_table(database.get(search="all", isCount=True))
        # adding the first step of showing all the current files inside database
        self.add_step()

        # use to save the temporary objects
        self.temporary_obj_list = []

        print("GUI display is ready")

        # Keep updating the GUI
        self.root.mainloop()

    def create_window(self, w, h):
        new_window = tk.Toplevel(self.root)
        x_coor = (self.screen_width / 2) - (w / 2)
        y_coor = (self.screen_height / 2) - (h / 2)
        new_window.geometry("%dx%d+%d+%d" % (w, h, x_coor, y_coor))
        return new_window

    # Add / delete / modify files Window
    def add_delete_modify_files(self):
        new_window = self.create_window(self.GUI.modify_width, self.GUI.modify_height)

        # skip some spaces in both dir
        new_window.grid_rowconfigure(0, minsize=10)
        new_window.grid_columnconfigure(0, minsize=10)

        # frame is used to contain everything
        right_frame = tk.LabelFrame(new_window, text="")
        right_frame.grid(row=1, column=1, rowspan=500)

        # skip some spaces in both dir in right_frame
        right_frame.grid_rowconfigure(0, minsize=10)
        right_frame.grid_columnconfigure(0, minsize=10)

        change_title = tk.Label(right_frame, text="Temporary", font=('Arial', 12))
        change_title.grid(row=1, column=1)

        change_listbox = tk.Listbox(right_frame, width=self.GUI.modify_listbox_width, height=25)
        change_listbox.grid(row=2, column=1, rowspan=25)

        # move left / right button is used to shift things to database or delete things to database
        move_left_button = tk.Button(right_frame, text="=>", width=2, height=1, command=None)
        move_left_button.grid(row=13, column=2, padx=5)
        move_right_button = tk.Button(right_frame, text="<=", width=2, height=1, command=None)
        move_right_button.grid(row=14, column=2, padx=5)

        current_title = tk.Label(right_frame, text="Current Database", font=('Arial', 12))
        current_title.grid(row=1, column=3)

        current_listbox = tk.Listbox(right_frame, width=self.GUI.modify_listbox_width, height=25)
        current_listbox.grid(row=2, column=3, rowspan=25)
        for data in database.get(search="all", isCount=False, select_field=['filepath']):
            current_listbox.insert("end", f"{database.extract_filename(data[0])}")

        browse_button = tk.Button(right_frame, text="Browse file", font=('Arial', 12), command=lambda: self.click_browse(new_window, change_listbox))
        browse_button.grid(row=28, column=1)

        # skip some spaces for the x-dir in right frame
        right_frame.grid_columnconfigure(4, minsize=10)

        # skip some spaces for the x-dir in new_window
        new_window.grid_columnconfigure(2, minsize=10)

        # left frame is the frame to contains the data of the file
        left_frame = tk.LabelFrame(new_window, text="")
        left_frame.grid(row=1, column=3)
        # hide it first
        left_frame.grid_forget()

        data_package = Show_Data_Package(left_frame)
        data_package.show_name(row=0, column=1)
        data_package.show_creator(row=1, column=1)
        data_package.show_category(row=2, column=1)
        data_package.show_filename(row=3, column=1)
        data_package.show_filepath(row=4, column=1)
        data_package.show_description(row=5, column=1)

        # update button is used to update the data of the file
        update_button = tk.Button(left_frame, text="Update", font=('Arial', 12), command=lambda: self.click_update(data_package))
        update_button.grid(row=6, column=1, columnspan=3, pady=10)
        update_button.grid_forget()
        # save button is used to save the data currently
        save_button = tk.Button(left_frame, text="Save", font=('Arial', 12), command=lambda: self.click_save())
        save_button.grid(row=6, column=1, columnspan=3, pady=10)
        save_button.grid_forget()

        # binding the double click event to the current listbox
        # search_filename -> get it from the curselection from the current_listbox
        current_listbox.bind('<Double-1>', lambda event, left_frame=left_frame, update_button=update_button, save_button=save_button, listbox=current_listbox, data_package=data_package: self.click_current_listbox_item(event, left_frame, update_button, save_button, listbox, data_package))

        # binding the double click event to the current listbox
        # search_filename -> get it from the curselection from the current_listbox
        change_listbox.bind('<Double-1>', lambda event, left_frame=left_frame, update_button=update_button, save_button=save_button, listbox=change_listbox, data_package=data_package: self.click_change_listbox_item(event, left_frame, update_button, save_button, listbox, data_package))

        # closing new_window event which is clearing all the obj inside self.temporary_obj_list
        new_window.protocol("WM_DELETE_WINDOW", lambda: self.empty_temporary(new_window))

    # this is used to clear out all the things inside the temporary obj list
    def empty_temporary(self, new_window):
        for obj in self.temporary_obj_list:
            print(obj.filename)
        self.temporary_obj_list = []
        for obj in self.temporary_obj_list:
            print(obj.filename)
        new_window.destroy()

    def click_current_listbox_item(self, event, left_frame, update_button, save_button, listbox, data_package):
        # show the left_frame
        left_frame.grid(row=1, column=3)
        update_button.grid(row=6, column=1, columnspan=3, pady=10)
        save_button.grid_forget()
        # get the selecting item in current database listbox
        search_filename = listbox.get(listbox.curselection())
        current_path = database.get_filepath(search_filename)
        data = database.get(search="exact", isCount=False, keyword=[current_path], select_field="all", compare_field=['filepath'])

        # this is not a good format
        print(database.extract_filename(search_filename, filetype=False))
        dataDict = {
            'name': data[0][0],
            'category': data[0][2],
            'filename': database.extract_filename(search_filename, filetype=False),
            'filepath': data[0][1],
            'creator': data[0][3],
            'description': data[0][4]
        }
        data_package.set(**dataDict)

    def click_change_listbox_item(self, event, left_frame, update_button, save_button, listbox, data_package):
        # show the left_frame
        left_frame.grid(row=1, column=3)
        save_button.grid(row=6, column=1, columnspan=3, pady=10)
        update_button.grid_forget()
        # get the selecting item in current database listbox
        search_filename = listbox.get(listbox.curselection())
        current_path = database.get_filepath(search_filename)

    def click_browse(self, window, change_listbox):
        window.filename = filedialog.askopenfilenames(title="Select file(s)")
        window.deiconify()
        for filename in window.filename:
            filename = database.extract_filename(filename)
            change_listbox.insert("end", f"(New) {filename}")
            self.temporary_obj_list.append(db.Data(filename=filename))

    def click_update(self, data_package):
        print("click update")
        print(data_package.compare_value())

    def click_treeview_item(self, event):
        selectedItem = self.treeview.item(self.treeview.focus())
        new_window = self.create_window(400, 400)
        # skip spaces at the top of the window
        new_window.grid_rowconfigure(0, minsize=30)
        # skip spaces at the left of the window
        new_window.grid_columnconfigure(0, minsize=30)
        # name title label
        name_title = tk.Label(new_window, text="Name :", font=('Arial', 12), height=2)
        name_title.grid(row=1, column=1, sticky="W")
        # filepath title label
        filepath_title = tk.Label(new_window, text="Filepath :", font=('Arial', 12), height=2)
        filepath_title.grid(row=2, column=1, sticky="W")
        # category title label
        category_title = tk.Label(new_window, text="Category :", font=('Arial', 12), height=2)
        category_title.grid(row=3, column=1, sticky="W")

        # skip spaces between the titles and the data
        new_window.grid_columnconfigure(2, minsize=15)
        # name data
        name = tk.Label(new_window, text=selectedItem.get('values')[0], font=('Arial', 12), height=2)
        name.grid(row=1, column=3, sticky="W")
        # filepath data
        filepath = tk.Label(new_window, text=selectedItem.get('values')[1], font=('Arial', 12), height=2)
        filepath.grid(row=2, column=3, sticky="W")
        # category data
        category = tk.Label(new_window, text=selectedItem.get('values')[2], font=('Arial', 12), height=2)
        category.grid(row=3, column=3, sticky="W")

    def add_step(self):
        step = database.get_sql_step(state="current")
        print(step.step_type)
        self.step_listbox.select_clear(0, tk.END)
        self.step_listbox.insert("end", f"{step.step_num}. {step.step_type}")
        self.step_listbox.select_set(tk.END)

    # event is trigger by double clicking the self.step_listbox item
    def click_step_listbox_item(self, event):
        # receive the index which the user select
        index = self.step_listbox.curselection()[0]
        # index is equal to the step num
        sql = database.get_sql_step(step_num=index).sql
        result, _ = database.sql_search(sql)
        self.show_table(database.sort(result))

    # filter out different category
    def filter(self, filtertype):
        filterList = []
        for button in self.checkbuttons:
            if (button.value_id.get() == 1):
                filterList.append(button.category)
        self.show_table(database.get(search="filter", isCount=True, keyword=filterList, method=filtertype))
        self.add_step()

    # disable / select all the checkbutton in the filter section
    def filter_checkbox_select_disable_all(self):
        if (self.filter_select_disable_id.get() == "Disable all"):
            for button in self.checkbuttons:
                button.value_id.set(0)
            self.filter_select_disable_id.set("Select all")
        else:
            for button in self.checkbuttons:
                button.value_id.set(1)
            self.filter_select_disable_id.set("Disable all")

    def add_checkbutton(self, root, name, row, column, fontsize):
        self.checkbuttons.append(Checkbutton(root, name=name, row=row, column=column, fontsize=fontsize))

    def search(self, search_method, keyword):
        self.show_table(database.get(search=search_method, isCount=True, keyword=keyword))
        self.add_step()

    def show_table(self, dataset):
        self.treeview.delete(*self.treeview.get_children())
        count = 1
        for data in dataset:
            self.treeview.insert("", "end", f"item{count}", values=(data[0], database.extract_filename(data[1]), data[2], data[3], data[4]))
            count += 1
        pass

    def __del__(self):
        print("GUI display is closed")


database = db.Database()

creators = ['Eddy', 'Ken', 'Alan']

database.add_category("renewable energy")
database.add_category("smart device")
database.add_category("indoor air quality")
database.add_category("hydroelectric")
database.add_category("secret")
database.add_category("Lithium battery")
database.add_category("vehicle")
database.add_category("energy efficiency")

database.add(name="D Solar Panel 1", filepath="files/solar_panel_proposal_4.txt", category="renewable energy", creator=creators[random.randint(0, 2)], description="Hi This is the D solar panel 1. TESTINGGGGGGGGGGGGGGGGGGGGGGG")
database.add(name="F Solar Panel 1", filepath="files/solar_panel_proposal_5.txt", category="renewable energy", creator=creators[random.randint(0, 2)], description="Hi hello world")
database.add(name="E Solar Panel 1", filepath="files/solar_panel_proposal_6.txt", category="renewable energy", creator=creators[random.randint(0, 2)], description="HoHo")
database.add(name="C Solar Panel 1", filepath="files/solar_panel_proposal_1.txt", category="renewable energy", creator=creators[random.randint(0, 2)])
database.add(name="A Solar Panel 2", filepath="files/solar_panel_proposal_2.txt", category="renewable energy", creator=creators[random.randint(0, 2)])
database.add(name="B Solar Panel 3", filepath="files/solar_panel_proposal_3.txt", category="renewable energy", creator=creators[random.randint(0, 2)])

for i in range(1, 300):
    database.add(name=f"{random.randint(1,300)} Solar Panel", filepath=f"files/solar_panel_proposal_{random.randint(1,1000)}.txt", category="renewable energy", creator=creators[random.randint(0, 2)])

database.add(name="Smart Lighting", filepath="files/smart_lighting.pdf", category="smart device")
database.add(name="IAQ Smart Device", filepath="files/indoor_air_quality_device.pdf", category="smart device,indoor air quality")
database.add(name="Air filter Device", filepath="files/air_filter_device.pdf", category="indoor air quality")

if (get_platform() == "Windows" or get_platform() == "OS X"):
    gui = Page()
else:
    print("Sorry. The application does not support %s yet." % get_platform())
