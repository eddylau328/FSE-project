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
            self.modify_height = 550
            self.modify_leftframe_wraplength = 165
            self.modify_leftframe_width = 30
            self.modify_leftframe_font = ('Arial', 12)

            # Click Treeviews POPUP WINDOW CONSTANT
            self.treeview_popup_font = ('Arial', 12)
            self.treeview_popup_width = 400
            self.treeview_popup_height = 400
            self.treeview_popup_padx = 10
            self.treeview_popup_pady = 5
            self.treeview_popup_labelframe_padx = 10
            self.treeview_popup_labelframe_pady = 10
            self.treeview_popup_data_wraplength = 260

            # main frame settings constant
            self.main_frame_outside_padx = 5
            self.main_frame_outside_pady = 20
            self.main_frame_inline_padx = 5
            self.main_frame_inline_pady = 5

            # treeview column width
            self.treeview_width_title = 150
            self.treeview_width_filename = 200
            self.treeview_width_creator = 80
            self.treeview_width_last_modify = 100
            self.treeview_width_category = 320

            # search entry width
            self.main_frame_search_entry_width = 80

            # select category window
            self.select_category_window_width = 300
            self.select_category_window_height = 300

            self.screen_width = 0
            self.screen_height = 0

            # this limits the select_category_window
            self.select_category_window_row_limit = 6

        elif (os_platform == "Windows"):

            self.filter_checkbutton_fontsize = 9

            # Modify FILES POPUP WINDOW CONSTANT
            self.modify_listbox_width = 40
            self.modify_width = 900
            self.modify_height = 500
            self.modify_leftframe_wraplength = 220
            self.modify_leftframe_width = 32
            self.modify_leftframe_font = ('Arial', 9)

            # Click Treeviews POPUP WINDOW CONSTANT
            self.treeview_popup_font = ('Arial', 10)
            self.treeview_popup_width = 340
            self.treeview_popup_height = 400
            self.treeview_popup_padx = 12
            self.treeview_popup_pady = 5
            self.treeview_popup_labelframe_padx = 10
            self.treeview_popup_labelframe_pady = 10
            self.treeview_popup_data_wraplength = 190

            # main frame settings constant
            self.main_frame_outside_padx = 5
            self.main_frame_outside_pady = 15
            self.main_frame_inline_padx = 5
            self.main_frame_inline_pady = 5

            # treeview column width
            self.treeview_width_title = 150
            self.treeview_width_filename = 200
            self.treeview_width_creator = 80
            self.treeview_width_last_modify = 115
            self.treeview_width_category = 350

            # search entry width
            self.main_frame_search_entry_width = 68

            # select category window
            self.select_category_window_width = 400
            self.select_category_window_height = 230

            self.screen_width = 0
            self.screen_height = 0

            # this limits the select_category_window
            self.select_category_window_row_limit = 6


def get_platform():
    platforms = {
        'darwin' : 'OS X',
        'win32' : 'Windows'
    }
    if (sys.platform not in platforms):
        return sys.platform

    return platforms[sys.platform]

class Show_Data_Package:
    def __init__(self, frame):

        # frame
        self.root = frame

        # checkbuttons list
        self.checkbuttons = []

        # used to compare
        self.data = db.Data()
        # used to compare
        self.new_data = db.Data()

        # this contains which data leftframe is actually showing
        self.selected_index = None

        # name title label
        self.name_title = tk.Label(frame, text="Title :", font=GUI.modify_leftframe_font)
        # name entry id
        self.name_entry_id = tk.StringVar()
        self.name_entry_id.set("")
        self.name_entry = tk.Entry(frame, textvariable=self.name_entry_id, font=GUI.modify_leftframe_font, width=GUI.modify_leftframe_width)

        # creator title label
        self.creator_title = tk.Label(frame, text="Creator :", font=GUI.modify_leftframe_font)

        # creator label
        self.creator_id = tk.StringVar()
        self.creator_id.set("")
        self.creator_label = tk.Entry(frame, textvariable=self.creator_id, font=GUI.modify_leftframe_font, width=GUI.modify_leftframe_width)

        # category title label
        self.category_title = tk.Label(frame, text="Category :", font=GUI.modify_leftframe_font)
        # category entry id
        self.category_id = tk.StringVar()
        self.category_id.set("")
        self.category_label = tk.Button(frame, textvariable=self.category_id, font=GUI.modify_leftframe_font, wraplength=GUI.modify_leftframe_wraplength, justify="left", width=30, command=self.select_category_button)

        # filepath label
        self.filename_title = tk.Label(frame, text="Filename", font=GUI.modify_leftframe_font)

        # current filepath id
        self.current_filename_id = tk.StringVar()
        self.current_filename_id.set("")
        self.current_filename_entry = tk.Entry(frame, textvariable=self.current_filename_id, font=GUI.modify_leftframe_font, width=GUI.modify_leftframe_width)

        # filepath label
        self.filepath_title = tk.Label(frame, text="Filepath", font=GUI.modify_leftframe_font)

        # current filepath id
        self.current_filepath_id = tk.StringVar()
        self.current_filepath_id.set("")
        self.current_filepath = tk.Label(frame, textvariable=self.current_filepath_id, font=GUI.modify_leftframe_font, wraplength=GUI.modify_leftframe_wraplength, justify="left", width=0)

        # description title label
        self.description_title = tk.Label(frame, text="Description :", font=GUI.modify_leftframe_font)

        # description entry id
        self.description_text = tk.Text(frame, font=GUI.modify_leftframe_font, height=10, width=GUI.modify_leftframe_width)

        # create date title
        self.last_modify_title = tk.Label(frame, text="Last Modify :", font=GUI.modify_leftframe_font)
        self.last_modify_id = tk.StringVar()
        self.last_modify_id.set("")
        self.last_modify = tk.Label(frame, textvariable=self.last_modify_id, font=GUI.modify_leftframe_font, wraplength=GUI.modify_leftframe_wraplength, justify="left", width=0)

        # create date title
        self.create_date_title = tk.Label(frame, text="Create Date :", font=GUI.modify_leftframe_font)
        self.create_date_id = tk.StringVar()
        self.create_date_id.set("")
        self.create_date = tk.Label(frame, textvariable=self.create_date_id, font=GUI.modify_leftframe_font, wraplength=GUI.modify_leftframe_wraplength, justify="left", width=0)


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

    # row, column is start from corner
    def show_last_modify(self, row, column):
        self.last_modify_title.grid(row=row, column=column, sticky="WN", padx=5, pady=8)
        self.last_modify.grid(row=row, column=column + 1, sticky="W", padx=5, pady=8)

    # row, column is start from corner
    def show_create_date(self, row, column):
        self.create_date_title.grid(row=row, column=column, sticky="WN", padx=5, pady=8)
        self.create_date.grid(row=row, column=column + 1, sticky="W", padx=5, pady=8)


    def set(self, index, **kwargs):
        title = kwargs.get('title', None)
        creator = kwargs.get('creator', None)
        category = kwargs.get('category', None)
        filename = kwargs.get('filename', None)
        filepath = kwargs.get('filepath', None)
        description = kwargs.get('description', None)
        last_modify = kwargs.get('last_modify', None)
        create_date = kwargs.get('create_date', None)
        self.selected_index = index
        self.data.set(**kwargs)
        self.new_data.set(**kwargs)

        if (title != None):
            self.name_entry_id.set(title)
        else:
            self.name_entry_id.set("")
        if ( creator != None):
            self.creator_id.set(creator)
        else:
            self.creator_id.set("")
        if (category != None):
            self.category_id.set(category)
        else:
            self.category_id.set("...")
        if (filename != None):
            self.current_filename_id.set(filename)
        else:
            self.current_filename_id.set("")
        if (filepath != None):
            self.current_filepath_id.set(filepath)
        else:
            self.current_filepath_id.set("")
        if (create_date != None):
            self.create_date_id.set(create_date)
        else:
            self.create_date_id.set("")
        if (last_modify != None):
            self.last_modify_id.set(last_modify)
        else:
            self.last_modify_id.set("")

        # clear the content in the description text box
        self.description_text.delete('1.0', 'end')
        if (description != None):
            self.description_text.insert("end", description)

    def update_new_data(self):
        #  dataset -> made need some corrections
        dataset = {
            'title' : self.name_entry_id.get(),
            'filepath' : self.current_filepath_id.get(),
            'filename' : self.current_filename_id.get(),
            'category' : self.category_id.get(),
            'creator' : self.creator_id.get(),
            'description' : self.description_text.get("1.0", "end-1c"),
            'create_date' : self.create_date_id.get(),
            'last_modify' : db.DateTime().get_current_time()
        }
        self.new_data.set(**dataset)

    def compare_value(self):
        dataset = self.data.get()
        newdataset = self.new_data.get()
        isSame = True
        if (dataset['title'] != newdataset['title']):
            isSame = False
        if (dataset['creator'] != newdataset['creator']):
            isSame = False
        if (dataset['filename'] != newdataset['filename']):
            isSame = False
        if (dataset['filepath'] != newdataset['filepath']):
            isSame = False
        if (dataset['category'] != newdataset['category']):
            isSame = False
        if (dataset['description'] != newdataset['description']):
            isSame = False
        return isSame


    def reset(self):
        self.selected_index = None
        self.name_entry_id.set("")
        self.current_filename_id.set("")
        self.current_filepath_id.set("")
        self.category_id.set("")
        self.creator_id.set("")
        self.description_text.delete("1.0", "end")
        self.create_date_id.set("")
        self.last_modify_id.set("")
        self.data = db.Data()
        self.new_data = db.Data()


    def select_category_button(self):
        new_window = self.create_window(GUI.select_category_window_width, GUI.select_category_window_height)
        labelframe = tk.LabelFrame(new_window, text="Category")
        labelframe.pack(side="top", fill=tk.X, padx=5, pady=2)
        categories = database.get_category()
        current_category_list = self.category_id.get().split(",")
        row = 0
        column = 0
        for category in database.get_category():
            if (row == GUI.select_category_window_row_limit):
                column += 1
                row = 0
            self.add_checkbutton(labelframe, category[0], row=row, column=column, fontsize=GUI.filter_checkbutton_fontsize)
            self.checkbuttons[-1].set(0)
            if (category[0] in current_category_list):
                self.checkbuttons[-1].set(1)
            row += 1
        update_button = tk.Button(new_window, text="Update", command=self.update_category)
        update_button.pack(side="bottom", pady=2)

    def update_category(self):
        new_category_list = []
        for checkbutton in self.checkbuttons:
            if (checkbutton.get() == 1):
                new_category_list.append(checkbutton.category)
        self.category_id.set(",".join(new_category_list))


    def create_window(self, w, h):
        new_window = tk.Toplevel(self.root)
        x_coor = (GUI.screen_width / 2) - (w / 2)
        y_coor = (GUI.screen_height / 2) - (h / 2)
        new_window.geometry("%dx%d+%d+%d" % (w, h, x_coor, y_coor))
        return new_window

    def add_checkbutton(self, root, name, row, column, fontsize):
        self.checkbuttons.append(Checkbutton(root, name=name, row=row, column=column, fontsize=fontsize, padx=2, pady=2))


class Root:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Files Search Engine")
        self.window_width = 1360
        self.window_height = 800
        GUI.screen_width = self.root.winfo_screenwidth()
        GUI.screen_height = self.root.winfo_screenheight()
        x_coor = (GUI.screen_width / 2) - (self.window_width / 2)
        y_coor = (GUI.screen_height / 2) - (self.window_height / 2)
        self.root.geometry("%dx%d+%d+%d" % (self.window_width, self.window_height, x_coor, y_coor))


class Checkbutton:
    def __init__(self, root, name, row, column, fontsize, padx=None, pady=None):
        self.value_id = tk.IntVar(value=1)
        self.category = name
        self.checkbutton = tk.Checkbutton(root, text=name, variable=self.value_id, font=('Arial', fontsize))
        if (padx != None and pady != None):
            self.checkbutton.grid(row=row, column=column, sticky="W", padx=padx, pady=pady)
        else:
            self.checkbutton.grid(row=row, column=column, sticky="W")

    def set(self, value):
        self.value_id.set(value)

    def get(self):
        return self.value_id.get()

class Page(Root):
    def __init__(self):
        Root.__init__(self)

        # Heading
        self.heading = tk.Label(self.root, text="Files Search Engine", font=('Arial', 32), height=1)
        self.heading.grid(row=1, column=1, columnspan=10, sticky="W",padx=GUI.main_frame_outside_padx, pady=GUI.main_frame_outside_pady)

        # creator of the program
        self.inventor_of_program = tk.Label(self.root, text="Created by Eddy Lau", font=('Arial', 10), fg="grey")
        self.inventor_of_program.grid(row=5, column=1, sticky="E")

        # search title
        self.search_title = tk.LabelFrame(self.root, text="Search", font=('Arial', 16), height=2)
        self.search_title.grid(row=3, column=1, sticky="W", padx=GUI.main_frame_outside_padx)
        # search label
        self.search_label = tk.Label(self.search_title, text="Keyword :", font=('Arial', 14))
        self.search_label.grid(row=4, column=1, sticky="W", padx=GUI.main_frame_inline_padx, pady=GUI.main_frame_inline_pady)
        # search
        # search_entry_id is the var saves the input string from search_entry
        self.search_entry_id = tk.StringVar()
        self.search_entry = tk.Entry(self.search_title, textvariable=self.search_entry_id, font=('Arial', 14), width=GUI.main_frame_search_entry_width)
        self.search_entry.grid(row=4, column=2, sticky="W", padx=GUI.main_frame_inline_padx, pady=GUI.main_frame_inline_pady)

        # search button
        self.search_button = tk.Button(self.search_title, text="Search", font=('Arial', 12), command=self.search)
        self.search_button.grid(row=4, column=3, sticky="W", pady=GUI.main_frame_inline_pady)

        # bind the [enter button], which make it more easy to input search
        self.search_entry.bind('<Return>', lambda event: self.search())

        # add button
        self.add_button = tk.Button(self.search_title, text="Add / Delete / Modify Files", command=lambda: self.add_delete_modify_files())
        self.add_button.grid(row=4, column=12, sticky="W", padx=GUI.main_frame_inline_padx, pady=GUI.main_frame_inline_pady)

        self.result_title = tk.LabelFrame(self.search_title, text="Results", font=('Arial', 16))
        self.result_title.grid(row=5, column=1, rowspan=100, columnspan=10, padx=GUI.main_frame_inline_padx, pady=GUI.main_frame_inline_pady)
        # table
        self.treeview = ttk.Treeview(self.result_title, height=28, selectmode="browse")
        #self.treeview.grid(row=6, column=1, rowspan=100, columnspan=10)
        self.treeview.pack(side="left", expand=True, fill=tk.Y)
        # set up the columns and headings
        self.treeview["columns"] = ["title", "filename", "creator", "last_modify", "category"]
        self.treeview["show"] = "headings"
        self.treeview.heading("title", text="Title")
        self.treeview.heading("filename", text="File Name")
        self.treeview.heading("creator", text="Creator")
        self.treeview.heading("last_modify", text="Last Modify")
        self.treeview.heading("category", text="Category")
        self.treeview.column('title', width=GUI.treeview_width_title)
        self.treeview.column('filename', width=GUI.treeview_width_filename)
        self.treeview.column('creator', width=GUI.treeview_width_creator)
        self.treeview.column('last_modify', width=GUI.treeview_width_last_modify)
        self.treeview.column('category', width=GUI.treeview_width_category)
        # click on the item in treeview
        self.treeview.bind("<Double-1>", self.click_treeview_item)

        # treeview veritcal scroll bar
        self.treeview_vertical_scrollbar = ttk.Scrollbar(self.result_title, orient="vertical")
        self.treeview_vertical_scrollbar.config(command=self.treeview.yview)
        self.treeview.config(yscrollcommand=self.treeview_vertical_scrollbar.set)
        self.treeview_vertical_scrollbar.pack(side="right", fill=tk.Y)

        # filter labelframe
        row = 10
        self.filter_title = tk.LabelFrame(self.search_title, text="Filter", font=('Arial', 16))
        self.filter_title.grid(row=row, column=12, rowspan=100, sticky="W", padx=GUI.main_frame_inline_padx, pady=GUI.main_frame_inline_pady)
        # checkbuttons for the database to sort in category
        self.checkbuttons = []
        row = 0
        column = 0
        for category in database.get_category():
            if (row == GUI.select_category_window_row_limit):
                column += 1
                row = 0
            self.add_checkbutton(self.filter_title, category[0], row=row, column=column, fontsize=GUI.filter_checkbutton_fontsize)
            row += 1

        row, column = 7, 0
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

        # tab control for changing the page
        self.minor_tab_control = ttk.Notebook(self.search_title, width=400, height=250)
        self.step_tab = ttk.Frame(self.minor_tab_control)
        self.minor_tab_control.add(self.step_tab, text="Steps")
        self.history_tab = ttk.Frame(self.minor_tab_control)
        self.minor_tab_control.add(self.history_tab, text="History")
        self.minor_tab_control.grid(row=9, column=12, padx=GUI.main_frame_inline_padx, pady=GUI.main_frame_inline_pady)

        # history
        # it saves the step num, index in the history_listbox, and the corresponding steps it refer to
        self.history_steps_list = []
        self.history_listbox = tk.Listbox(self.history_tab, selectmode="single")
        # clear all history steps
        self.history_clear_button = tk.Button(self.history_tab, text="Clear History", command=lambda: self.click_clear_history())
        self.history_clear_button.pack(side="bottom", fill=tk.X)
        # pack the history listbox at last
        self.history_listbox.pack(side="left", fill=tk.BOTH, expand=1)

        # history_scrollbar
        self.history_scrollbar = ttk.Scrollbar(self.history_tab, orient="vertical")
        self.history_scrollbar.config(command=self.history_listbox.yview)
        self.history_listbox.config(yscrollcommand=self.history_scrollbar.set)
        self.history_scrollbar.pack(side="right", fill=tk.Y)

        # add clicking event in step_listbox
        self.history_listbox.bind('<Double-1>', self.click_history_listbox_item)

        # procedure search checkbutton value
        self.step_procedure_search_id = tk.IntVar()
        self.step_procedure_search_id.set(0)
        # used to save the steps the user took
        self.step_listbox = tk.Listbox(self.step_tab, selectmode="single")
        # new search step
        self.step_new_button = tk.Button(self.step_tab, text="New Search", command=lambda: self.click_new_search(self.step_procedure_search_id, self.step_listbox, self.checkbuttons, self.search_entry_id))

        # procedure search checkbutton
        self.step_procedure_search_checkbutton = tk.Checkbutton(self.step_tab, text="Procedure Search", variable=self.step_procedure_search_id, font=('Arial', 12))
        self.step_procedure_search_checkbutton.pack(side="bottom", fill=tk.X)
        self.step_new_button.pack(side="bottom", fill=tk.X)
        self.step_listbox.pack(side="left", fill=tk.BOTH, expand=1)
        # step_scrollbar
        self.step_scrollbar = ttk.Scrollbar(self.step_tab, orient="vertical")
        self.step_scrollbar.config(command=self.step_listbox.yview)
        self.step_listbox.config(yscrollcommand=self.step_scrollbar.set)
        self.step_scrollbar.pack(side="right", fill=tk.Y)

        # add clicking event in step_listbox
        self.step_listbox.bind('<Double-1>', self.click_step_listbox_item)

        # this is start at the beginning of the program
        # show all the current files inside database
        # adding the first step of showing all the current files inside database
        self.click_new_search(self.step_procedure_search_id, self.step_listbox, self.checkbuttons, self.search_entry_id)
        # use to save the temporary objects
        self.temporary_obj_list = []
        # use to save the current_objects_list, but only need to save filepath as it can retrieve from database
        self.current_filepath_list = []

        print("GUI display is ready")

        # Keep updating the GUI
        self.root.mainloop()


    def click_clear_history(self):
        print("Clear all history steps")
        self.history_listbox.delete(0, "end")
        self.history_steps_list = []
        database.clear_sql_history()


    def click_history_listbox_item(self,event):
        click_index = self.history_listbox.curselection()[0]
        for step_data in self.history_steps_list:
            # first ensure that the user click the history step but not the titles
            if (click_index == step_data.get('index')):
                step_index = step_data.get('step_index')
                step_num = step_data.get('step_num')
                step = database.get_sql_history(step_index=step_index, step_num=step_num)
                self.show_table(database.get(isCount=False, sql=step.sql))

    def update_history(self):
        if (database.get_sql_history() != None):
            sql_solution = database.get_sql_history()
            # add the title first
            if (sql_solution.procedure_search):
                self.history_listbox.insert("end", "--------------------------------------")
                self.history_listbox.insert("end", "Procedural Search")
            else:
                self.history_listbox.insert("end", "--------------------------------------")
                self.history_listbox.insert("end","Non-Procedural Search")
            # loop through the sql_solution
            for step in sql_solution.steps:
                # append the current
                self.history_steps_list.append({'index':self.history_listbox.index("end"), 'step_index':database.get_sql_history(get_index=True), 'step_num':step.step_num})
                self.history_listbox.insert("end", f"{step.step_num}. {step.step_type}")
            self.history_listbox.select_set(tk.END)
        print(self.history_steps_list)


    # this is the event when the user click the new search button
    def click_new_search(self, step_procedure_search_id, step_listbox, checkbuttons, search_entry_id):
        value = step_procedure_search_id.get()
        if (value == 1):
            is_procedure_search = True
            listbox_title = "Procedural Search"
        else:
            is_procedure_search = False
            listbox_title = "Non-Procedural Search"

        database.create_new_search(is_procedure_search=is_procedure_search)
        step_listbox.delete(0, "end")
        step_listbox.insert("end", listbox_title)

        self.update_history()
        self.show_table(database.get(isCount=True))
        self.add_step()
        # all filter button is reset to original
        for button in checkbuttons:
            button.set(1)
        # clear the search field
        search_entry_id.set("")


    def create_window(self, w, h):
        new_window = tk.Toplevel(self.root)
        x_coor = (GUI.screen_width / 2) - (w / 2)
        y_coor = (GUI.screen_height / 2) - (h / 2)
        new_window.geometry("%dx%d+%d+%d" % (w, h, x_coor, y_coor))
        return new_window


    # Add / delete / modify files Window
    def add_delete_modify_files(self):
        new_window = self.create_window(GUI.modify_width, GUI.modify_height)


        # frame is used to contain everything
        right_frame = tk.LabelFrame(new_window, text="")
        right_frame.pack(side="left", fill=tk.Y)

        # skip some spaces in both dir in right_frame
        right_frame.grid_rowconfigure(0, minsize=10)
        right_frame.grid_columnconfigure(0, minsize=10)

        change_title = tk.Label(right_frame, text="Temporary", font=('Arial', 12))
        change_title.grid(row=1, column=1)

        change_listbox = tk.Listbox(right_frame, selectmode="extended", width=GUI.modify_listbox_width, height=25)
        change_listbox.grid(row=2, column=1, rowspan=25)

        current_title = tk.Label(right_frame, text="Current Database", font=('Arial', 12))
        current_title.grid(row=1, column=3)

        current_listbox = tk.Listbox(right_frame, selectmode="extended", width=GUI.modify_listbox_width, height=25)
        current_listbox.grid(row=2, column=3, rowspan=25)
        for data in database.get(select_field=['filepath']):
            self.current_filepath_list.append(data.get('filepath'))
            current_listbox.insert("end", f"{database.extract_filename(data.get('filepath'))}")

        # browse button is used to browse file to open in change_listbox
        browse_button = tk.Button(right_frame, text="Browse file", font=('Arial', 12), command=lambda: self.click_browse(new_window, change_listbox))
        browse_button.grid(row=28, column=1, columnspan=2, sticky="W")

        # left frame is the frame to contains the data of the file
        left_frame = tk.LabelFrame(new_window, text="")
        left_frame.pack(side="right", fill=tk.Y)
        # hide it first
        left_frame.pack_forget()

        data_package = Show_Data_Package(left_frame)
        data_package.show_name(row=0, column=1)
        data_package.show_creator(row=1, column=1)
        data_package.show_category(row=2, column=1)
        data_package.show_filename(row=3, column=1)
        data_package.show_filepath(row=4, column=1)
        data_package.show_description(row=5, column=1)
        data_package.show_last_modify(row=6, column=1)
        data_package.show_create_date(row=7, column=1)
        # delete button is used to delete file in change_listbox
        delete_button = tk.Button(right_frame, text="Delete file", font=('Arial', 12), command=lambda: self.click_delete(left_frame, data_package, change_listbox))
        delete_button.grid(row=28, column=1, sticky="E")

        # update button is used to update the data of the file
        update_button = tk.Button(left_frame, text="Update", font=('Arial', 12), command=lambda: self.click_update(data_package))
        update_button.grid(row=8, column=1, columnspan=3, pady=10)
        update_button.grid_forget()
        # save button is used to save the data currently
        save_button = tk.Button(left_frame, text="Save", font=('Arial', 12), command=lambda: self.click_save(data_package, change_listbox))
        save_button.grid(row=8, column=1, columnspan=3, pady=10)
        save_button.grid_forget()

        # binding the double click event to the current listbox
        # search_filename -> get it from the curselection from the current_listbox
        current_listbox.bind('<Double-1>', lambda event, left_frame=left_frame, update_button=update_button, save_button=save_button, listbox=current_listbox, data_package=data_package: self.click_current_listbox_item(event, left_frame, update_button, save_button, listbox, data_package))

        # binding the double click event to the current listbox
        # search_filename -> get it from the curselection from the current_listbox
        change_listbox.bind('<Double-1>', lambda event, left_frame=left_frame, update_button=update_button, save_button=save_button, listbox=change_listbox, data_package=data_package: self.click_change_listbox_item(event, left_frame, update_button, save_button, listbox, data_package))

        # move left / right button is used to shift things to database or delete things to database
        move_in_button = tk.Button(right_frame, text="=>", width=2, height=1, command=lambda: self.click_move_in(left_frame, data_package, change_listbox, current_listbox))
        move_in_button.grid(row=13, column=2, padx=5)
        move_out_button = tk.Button(right_frame, text="<=", width=2, height=1, command=lambda: self.click_move_out(left_frame, data_package, change_listbox, current_listbox))
        move_out_button.grid(row=14, column=2, padx=5)

        # closing new_window event which is clearing all the obj inside self.temporary_obj_list
        new_window.protocol("WM_DELETE_WINDOW", lambda: self.close_add_delete_modify_files_window(new_window))


    # this is used to clear out all the things inside the temporary obj list
    def close_add_delete_modify_files_window(self, new_window):
        for obj in self.temporary_obj_list:
            print(obj['data'].get())
        self.temporary_obj_list = []
        self.current_filepath_list = []
        new_window.destroy()


    def click_current_listbox_item(self, event, left_frame, update_button, save_button, listbox, data_package):
        # show the left_frame
        left_frame.pack(side="right", fill=tk.Y)

        update_button.grid(row=8, column=1, columnspan=3, pady=10)
        save_button.grid_forget()

        data_package.reset()

        selected_index = listbox.index(listbox.curselection())
        # get the selecting item in current database listbox
        current_path = self.current_filepath_list[selected_index]
        data = database.get(isCount=False,raw_command=f"filepath='{current_path}'")
        # ensure the file got a file, otherwise report error
        try:
            data = data[0]
        except:
            data = {}
            print("Data missing")

        dataDict = {
            'title': data.get('title', None),
            'category': data.get('category', None),
            'filename': database.extract_filename(data.get('filepath', None), filetype=False),
            'filepath': data.get('filepath', None),
            'creator': data.get('creator', None),
            'description': data.get('description', None),
            'create_date': data.get('create_date', None),
            'last_modify': data.get('last_modify', None)
        }

        data_package.set(selected_index ,**dataDict)


    def click_change_listbox_item(self, event, left_frame, update_button, save_button, listbox, data_package):
        # show the left_frame
        left_frame.pack(side="right", fill=tk.Y)

        # show the save button
        save_button.grid(row=8, column=1, columnspan=3, pady=10)
        update_button.grid_forget()

        data_package.reset()

        # get the selecting item in current database listbox
        selected_index = listbox.index(listbox.curselection())
        # get the selected item from the temporary obj list
        selected_dict = self.temporary_obj_list[selected_index]

        # Show the data by sending the data to data_package.set() methods
        #print(selected_dict.get('data').get())
        data_package.set(selected_index ,**selected_dict.get('data').get())


    def click_move_in(self, left_frame, data_package, change_listbox, current_listbox):
        # close the left_frame
        left_frame.pack_forget()
        data_package.reset()

        # move the item from change listbox to current listbox

        remove_index_list = []
        remove_num = 0
        # used to count the number of remove items and remove items index
        for selected_item in change_listbox.curselection():
            remove_num += 1
            remove_index_list.append(change_listbox.index(selected_item))

        # delete item in from current listbox
        for delete_item in range(0, remove_num):
            change_listbox.delete(change_listbox.curselection()[0])
        change_listbox.select_clear(0, "end")

        # add data to the database
        for index in remove_index_list:
            selected_dict = self.temporary_obj_list[index]
            if (selected_dict['type'] == "new"):
                # it takes kwargs, database.Data().get return dictionary
                database.add(**selected_dict['data'].get())
            elif (selected_dict['type'] == "old"):
                obj_id = selected_dict['data'].get("obj_id")
                database.update_data(obj_id, **selected_dict['data'].get())

        # put the filename to the current_listbox
        for index in remove_index_list:
            selected_dict = self.temporary_obj_list[index]
            filepath = selected_dict['data'].get("filepath")
            filename = database.extract_filename(filepath, filetype=True)
            current_listbox.insert("end", f"{filename}")
            self.current_filepath_list.append(filepath)

        # delete obj in temporary_obj_list, in reverse way it will disorganise the structure
        for index in sorted(remove_index_list, reverse = True):
            self.temporary_obj_list.pop(index)

        # ensure it update when there is something added
        if (remove_num > 0):
            # highlight the add items
            start = current_listbox.index("end") - remove_num
            current_listbox.selection_set( start, "end")

            # update treeview after you removing something in database
            self.show_table(database.get())



    def click_move_out(self, left_frame, data_package, change_listbox, current_listbox):
        # close the left_frame
        left_frame.pack_forget()
        data_package.reset()

        # move the item from current listbox to change listbox
        delete_item = 0
        remove_path_index_list = []
        for selected_item in current_listbox.curselection():
            delete_item += 1
            # get the item in current_listbox
            selected_filename = current_listbox.get(selected_item)
            remove_path_index_list.append(current_listbox.index(selected_item))
            current_path = self.current_filepath_list[current_listbox.index(selected_item)]
            data = database.get(raw_command=f"filepath='{current_path}'")

            # ensure the file got a file, otherwise report error
            try:
                data = data[0]
            except:
                data = {}
                print("Data missing")

            dataDict = {
                'title': data.get('title', None),
                'category': data.get('category', None),
                'filename': database.extract_filename(data.get('filepath', None), filetype=False),
                'filepath': data.get('filepath', None),
                'creator': data.get('creator', None),
                'description': data.get('description', None),
                'create_date': data.get('create_date', None),
                'last_modify': data.get('last_modify', None)
            }

            change_listbox.insert("end", f"{selected_filename}")
            self.temporary_obj_list.append({ 'data':db.Data(**dataDict),'type':"old"})

        # delete item in from current listbox
        for delete_item in range(0, delete_item):
            current_listbox.delete(current_listbox.curselection()[0])

        # delete filepath in current_filepath_list, in reverse way it will disorganise the structure
        for delete_index in sorted(remove_path_index_list, reverse = True):
            self.current_filepath_list.pop(delete_index)

        current_listbox.select_clear(0, "end")


    # click browse to browse files
    def click_browse(self, window, change_listbox):
        window.filename = filedialog.askopenfilenames(title="Select file(s)")
        window.deiconify()
        for filepath in window.filename:
            filename = database.extract_filename(filepath)
            # get the latest index for the inserting
            change_listbox.insert("end", f"(New) {filename}")
            self.temporary_obj_list.append({'data':db.Data(filename=database.extract_filename(filepath, filetype=False), filepath=filepath),'type':"new"})


    # click delete files in change_listbox
    def click_delete(self, left_frame, data_package, change_listbox):
        left_frame.grid_forget()
        data_package.reset()
        # saves the index to remove items in self.temporary_obj_list
        remove_index_list = []
        remove_num = 0

        # used to count the number of remove items and remove items index
        for selected_item in change_listbox.curselection():
            remove_num += 1
            remove_index_list.append(change_listbox.index(selected_item))

        # delete item in from current listbox
        for delete_item in range(0, remove_num):
            change_listbox.delete(change_listbox.curselection()[0])
        change_listbox.select_clear(0, "end")

        # delete data from database
        for index in remove_index_list:
            # "old" is the data from the database
            if (self.temporary_obj_list[index].get('type') == "old"):
                delete_file_path = self.temporary_obj_list[index]['data'].get("obj_id")
                database.delete_data(delete_file_path)

        # delete obj in temporary_obj_list
        for index in sorted(remove_index_list, reverse = True):
            self.temporary_obj_list.pop(index)

        # update treeview after you removing something in database
        self.show_table(database.get())



    # click save button (it should be saving temporary, not in the database)
    def click_save(self, data_package, listbox):
        print("click save")
        data_package.update_new_data()
        # retrieving the selected index from data package
        selected_index = data_package.selected_index
        self.temporary_obj_list[selected_index]['data'].set(**data_package.new_data.get())
        print(self.temporary_obj_list[selected_index]['data'].get())

    # click update button
    def click_update(self, data_package):
        print("click update")
        # before comparing value update the new data set, if anything in the Entry is different
        data_package.update_new_data()

        # return True then no different, return False then have difference
        if (data_package.compare_value() == False):
            # have difference, needs to update the database
            # obj_id is the original filepath, it may want to change the filepath
            database.update_data(original_filepath=data_package.data.get('obj_id'), **data_package.new_data.get())
            self.show_table(database.get())


    def click_treeview_item(self, event):
        new_window = self.create_window(GUI.treeview_popup_width, GUI.treeview_popup_height)

        labelframe = tk.LabelFrame(new_window, text="Detail Information", font=GUI.treeview_popup_font)
        #labelframe.grid(row=0,column=0, padx=GUI.treeview_popup_labelframe_padx, pady=GUI.treeview_popup_labelframe_pady)
        labelframe.pack(fill=tk.BOTH, expand=1, side="top", padx=GUI.treeview_popup_labelframe_padx, pady=GUI.treeview_popup_labelframe_pady)
        # name title label
        name_title = tk.Label(labelframe, text="Title :", font=GUI.treeview_popup_font)
        name_title.grid(row=0, column=0, sticky="WN", padx=GUI.treeview_popup_padx, pady=GUI.treeview_popup_pady)
        # creator
        creator_title = tk.Label(labelframe, text="Creator :", font=GUI.treeview_popup_font)
        creator_title.grid(row=1, column=0, sticky="WN", padx=GUI.treeview_popup_padx, pady=GUI.treeview_popup_pady)
        # category title label
        category_title = tk.Label(labelframe, text="Category :", font=GUI.treeview_popup_font)
        category_title.grid(row=2, column=0, sticky="WN", padx=GUI.treeview_popup_padx, pady=GUI.treeview_popup_pady)
        # filename title label
        filename_title = tk.Label(labelframe, text="Filename :", font=GUI.treeview_popup_font)
        filename_title.grid(row=3, column=0, sticky="WN", padx=GUI.treeview_popup_padx, pady=GUI.treeview_popup_pady)
        # filepath title label
        filepath_title = tk.Label(labelframe, text="Filepath :", font=GUI.treeview_popup_font)
        filepath_title.grid(row=4, column=0, sticky="WN", padx=GUI.treeview_popup_padx, pady=GUI.treeview_popup_pady)
        # description title label
        # category title label
        description_title = tk.Label(labelframe, text="Description :", font=GUI.treeview_popup_font)
        description_title.grid(row=5, column=0, sticky="WN", padx=GUI.treeview_popup_padx, pady=GUI.treeview_popup_pady)
        # last modify title
        last_modify_title = tk.Label(labelframe, text="Last Modify :", font=GUI.treeview_popup_font)
        last_modify_title.grid(row=6, column=0, sticky="WN", padx=GUI.treeview_popup_padx, pady=GUI.treeview_popup_pady)
        # create date title
        create_date_title = tk.Label(labelframe, text="Create Date :", font=GUI.treeview_popup_font)
        create_date_title.grid(row=7, column=0, sticky="WN", padx=GUI.treeview_popup_padx, pady=GUI.treeview_popup_pady)

        selected_item_filepath = self.treeview.selection()[0]
        data = database.get(raw_command=f"filepath='{selected_item_filepath}'")[0]
        # name data
        name_id = tk.StringVar()
        name_id.set(data.get('title'))
        name = tk.Label(labelframe, textvariable=name_id, font=GUI.treeview_popup_font, wraplength=GUI.treeview_popup_data_wraplength, justify="left")
        name.grid(row=0, column=1, sticky="WN", padx=GUI.treeview_popup_padx, pady=GUI.treeview_popup_pady)
        # creator data
        creator_id = tk.StringVar()
        creator_id.set(data.get('creator'))
        creator = tk.Label(labelframe, textvariable=creator_id, font=GUI.treeview_popup_font,wraplength=GUI.treeview_popup_data_wraplength, justify="left")
        creator.grid(row=1, column=1, sticky="WN", padx=GUI.treeview_popup_padx, pady=GUI.treeview_popup_pady)
        # category data
        category_id = tk.StringVar()
        category_id.set(data.get('category'))
        category = tk.Label(labelframe, textvariable=category_id, font=GUI.treeview_popup_font, wraplength=GUI.treeview_popup_data_wraplength, justify="left")
        category.grid(row=2, column=1, sticky="WN", padx=GUI.treeview_popup_padx, pady=GUI.treeview_popup_pady)
        # filename data
        filename_id = tk.StringVar()
        filename_id.set(data.get('filename'))
        filename = tk.Label(labelframe, textvariable=filename_id, font=GUI.treeview_popup_font,wraplength=GUI.treeview_popup_data_wraplength, justify="left")
        filename.grid(row=3, column=1, sticky="WN", padx=GUI.treeview_popup_padx, pady=GUI.treeview_popup_pady)
        # filepath data
        filepath_id = tk.StringVar()
        filepath_id.set(data.get('filepath'))
        filepath = tk.Label(labelframe, textvariable=filepath_id, font=GUI.treeview_popup_font,wraplength=GUI.treeview_popup_data_wraplength, justify="left")
        filepath.grid(row=4, column=1, sticky="WN", padx=GUI.treeview_popup_padx, pady=GUI.treeview_popup_pady)
        # description data
        description_id = tk.StringVar()
        description_id.set(data.get('description'))
        description = tk.Label(labelframe, textvariable=description_id, font=GUI.treeview_popup_font,wraplength=GUI.treeview_popup_data_wraplength, justify="left")
        description.grid(row=5, column=1, sticky="WN", padx=GUI.treeview_popup_padx, pady=GUI.treeview_popup_pady)
        # last modify data
        last_modify_id = tk.StringVar()
        last_modify_id.set(data.get('last_modify'))
        last_modify = tk.Label(labelframe, textvariable=last_modify_id, font=GUI.treeview_popup_font,wraplength=GUI.treeview_popup_data_wraplength, justify="left")
        last_modify.grid(row=6, column=1, sticky="WN", padx=GUI.treeview_popup_padx, pady=GUI.treeview_popup_pady)
        # create date data
        create_date_id = tk.StringVar()
        create_date_id.set(data.get('create_date'))
        create_date = tk.Label(labelframe, textvariable=create_date_id, font=GUI.treeview_popup_font,wraplength=GUI.treeview_popup_data_wraplength, justify="left")
        create_date.grid(row=7, column=1, sticky="WN", padx=GUI.treeview_popup_padx, pady=GUI.treeview_popup_pady)


    def add_step(self):
        step = database.get_sql_step(state="current")
        print(step.step_type)
        self.step_listbox.select_clear(0, tk.END)
        self.step_listbox.insert("end", f"{step.step_num}. {step.step_type}")
        self.step_listbox.select_set(tk.END)


    # event is trigger by double clicking the self.step_listbox item
    def click_step_listbox_item(self, event):
        # receive the index which the user select, it is tuple
        index = self.step_listbox.curselection()[0]
        if (index != 0):
            # index is equal to the step num
            # there is no step zero
            step = database.get_sql_step(step_num=index)
            # use the step.sql to get back the data you search before
            result = database.get(isCount=False, sql=step.sql)
            self.show_table(result)

    # filter out different category
    def filter(self, filtertype):
        filterList = []
        for button in self.checkbuttons:
            if (button.get() == 1):
                filterList.append(button.category)
        field = "category"
        if (filtertype == "union"):
            logic = "or"
        elif (filtertype == "intersect"):
            logic = "and"
        count = 0
        search_line = []
        search_method_list = []
        for category in filterList:
            search_line.append(db.Search_Pair(keyword=category, compare_field=field))
            search_method_list.append(db.Search_Method.RELATE)
            if (count < len(filterList)-1):
                search_line.append(logic)
            count += 1
        search_package = db.Search_Package(search_line=search_line, search_method_list=search_method_list, select_field="all",order_field=None)
        # keyword => list
        self.show_table(database.get(search_package=search_package, isCount=True))
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


    def search(self):
        raw_command = self.search_entry_id.get()
        self.show_table(database.get(raw_command=raw_command, isCount=True))
        self.add_step()


    def show_table(self, dataset):
        self.treeview.delete(*self.treeview.get_children())
        count = 1
        for data in dataset:
            # treeview.insert(parent id, index, iid, values)
            self.treeview.insert("", "end", f"{data.get('filepath')}" , values=(data.get('title'), data.get('filename'), data.get('creator'), data.get('last_modify'), data.get('category')))
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

file_sep = ""
if (get_platform() == "OS X"):
    file_sep = "/"
elif (get_platform() == "Windows"):
    file_sep = "\\"

database.add(title="D Solar Panel 1", filepath="files"+file_sep+"solar_panel_proposal_4a.txt", category="renewable energy", creator=creators[random.randint(0, 2)], description="Hi This is the D solar panel 1. TESTINGGGGGGGGGGGGGGGGGGGGGGG")
database.add(title="F Solar Panel 1", filepath="files"+file_sep+"solar_panel_proposal_5b.txt", category="renewable energy", creator=creators[random.randint(0, 2)], description="Hi hello world")
database.add(title="E Solar Panel 1", filepath="files"+file_sep+"solar_panel_proposal_6c.txt", category="renewable energy", creator=creators[random.randint(0, 2)], description="HoHo")
database.add(title="C Solar Panel 1", filepath="files"+file_sep+"solar_panel_proposal_1d.txt", category="renewable energy", creator=creators[random.randint(0, 2)])
database.add(title="A Solar Panel 2", filepath="files"+file_sep+"solar_panel_proposal_2e.txt", category="renewable energy", creator=creators[random.randint(0, 2)])
database.add(title="B Solar Panel 3", filepath="files"+file_sep+"solar_panel_proposal_3f.txt", category="secret, vehicle,renewable energy", creator=creators[random.randint(0, 2)])

for i in range(1, 10):
    database.add(title=f"{i} Solar Panel", filepath=f"files{file_sep}solar_panel_proposal_{i}.txt", category="renewable energy", creator=creators[random.randint(0, 2)])

database.add(title="D Smart Lighting", filepath="files"+file_sep+"smart_lighting.pdf", category="smart device")
database.add(title="IAQ Smart Device", filepath="files"+file_sep+"indoor_air_quality_device.pdf", category="smart device,indoor air quality")
database.add(title="Air filter Device", filepath="files"+file_sep+"air_filter_device.pdf", category="indoor air quality")

if (get_platform() == "Windows" or get_platform() == "OS X"):
    GUI = GUI(get_platform())
    gui = Page()
else:
    print("Sorry. The application does not support %s yet." % get_platform())
