import tkinter as tk
import tkinter.ttk as ttk
import database as db
import random

class Root:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Files Search Engine")
        self.window_width = 1250
        self.window_height = 800
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        x_coor = (self.screen_width / 2) - (self.window_width / 2)
        y_coor = (self.screen_height / 2) - (self.window_height / 2)
        self.root.geometry("%dx%d+%d+%d" % (self.window_width, self.window_height, x_coor, y_coor))


class Checkbutton:
    def __init__(self, root, name, row, column):
        self.value_id = tk.IntVar(value=1)
        self.category = name
        self.checkbutton = tk.Checkbutton(root, text=name, variable=self.value_id, font=('Arial', 12))
        self.checkbutton.grid(row=row, column=column, sticky="W")


class Page(Root):
    def __init__(self):
        Root.__init__(self)
        self.root.grid_rowconfigure(0, minsize=30)
        self.root.grid_columnconfigure(0, minsize=30)
        # Heading
        self.heading = tk.Label(self.root, text="Files Search Engine", font=('Arial', 32), height=1)
        self.heading.grid(row=1, column=1, columnspan=10, sticky="W")
        # skip the line for some spaces
        self.root.grid_rowconfigure(2, minsize=10)
        # search title
        self.search_title = tk.LabelFrame(self.root, text="Search", font=('Arial', 16), height=2)
        self.search_title.grid(row=3, column=1, sticky="W")
        # search label
        self.search_label = tk.Label(self.search_title, text="Keyword :", font=('Arial', 12))
        self.search_label.grid(row=4, column=1, sticky="W")
        # search
        # search_entry_id is the var saves the input string from search_entry
        self.search_entry_id = tk.StringVar()
        self.search_entry = tk.Entry(self.search_title, textvariable=self.search_entry_id, font=('Arial', 12))
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

        # skip the line for some spaces
        self.search_title.grid_rowconfigure(5, minsize=10)

        self.result_title = tk.LabelFrame(self.search_title, text="Results", font=('Arial',16))
        self.result_title.grid(row=6, column=1, rowspan=100, columnspan=10)
        # table
        self.treeview = ttk.Treeview(self.result_title, height=28)
        #self.treeview.grid(row=6, column=1, rowspan=100, columnspan=10)
        self.treeview.pack(side="left", expand=True, fill=tk.Y)
        # set up the columns and headings
        self.treeview["columns"] = ["name", "filepath", "category"]
        self.treeview["show"] = "headings"
        self.treeview.heading("name", text="Name")
        self.treeview.heading("filepath", text="File Path")
        self.treeview.heading("category", text="Category")
        self.treeview.column('name', width=150)
        self.treeview.column('filepath', width=300)
        self.treeview.column('category', width=300)
        # click on the item in treeview
        self.treeview.bind("<Double-1>", self.click_treeview_item)

        # treeview veritcal scroll bar
        self.treeview_vertical_scrollbar = ttk.Scrollbar(self.result_title, orient="vertical")
        self.treeview_vertical_scrollbar.config(command=self.treeview.yview)
        self.treeview.config(yscrollcommand=self.treeview_vertical_scrollbar.set)
        self.treeview_vertical_scrollbar.pack(side="right",fill=tk.Y)

        # skip some x-dir spaces for the treeview and the filter
        self.search_title.grid_columnconfigure(12, minsize=20)

        # filter labelframe
        row = 6
        self.filter_title = tk.LabelFrame(self.search_title, text="Filter", font=('Arial', 16))
        self.filter_title.grid(row=row, column=13, rowspan=100, sticky="W")
        # checkbuttons for the database to sort in category
        self.checkbuttons = []
        row = 0
        column = 0
        for category in database.get_category():
            self.add_checkbutton(self.filter_title, category[0], row=row, column=column)
            row += 1

        self.filter_radiobutton_id = tk.StringVar()
        self.filter_radiobutton_id.set("union")
        # union filter radiobutton
        self.filter_u_radiobutton = tk.Radiobutton(self.filter_title, text="Related", variable=self.filter_radiobutton_id, value="union")
        self.filter_u_radiobutton.grid(row=row, column=column, sticky="W")
        # intersection filter radiobutton
        row += 1
        self.filter_i_radiobutton = tk.Radiobutton(self.filter_title, text="Exact", variable=self.filter_radiobutton_id, value="intersect")
        self.filter_i_radiobutton.grid(row=row, column=column, sticky="W")
        # sort button for the database to perform sorting
        row += 1
        self.filter_button = tk.Button(self.filter_title, text="Filter", font=('Arial', 12), command=lambda: self.filter(self.filter_radiobutton_id.get()))
        self.filter_button.grid(row=row, column=column, sticky="W")

        self.search_title.grid_columnconfigure(14, minsize=20)

        # tab control for changing the page
        self.minor_tab_control = ttk.Notebook(self.search_title, width=200, height=400)
        self.step_tab = ttk.Frame(self.minor_tab_control)
        self.minor_tab_control.add(self.step_tab, text="Steps")
        self.history_tab = ttk.Frame(self.minor_tab_control)
        self.minor_tab_control.add(self.history_tab, text="History")
        self.minor_tab_control.grid(row=7, column=15)

        # used to save the steps the user took
        self.step_listbox = tk.Listbox(self.step_tab)
        self.step_listbox.pack(side="left", fill=tk.BOTH, expand=1)
        # step_scrollbar
        self.step_scrollbar = ttk.Scrollbar(self.step_tab, orient="vertical")
        self.step_scrollbar.config(command=self.step_listbox.yview)
        self.step_listbox.config(yscrollcommand=self.step_scrollbar.set)
        self.step_scrollbar.pack(side="right", fill=tk.Y)

        # new search step
        self.step_new_button = tk.Button(self.step_tab, text="New Search", command=None)
        self.step_new_button.pack(side="bottom")

        # show all the current files inside database
        self.show_table(database.get(search="all"))
        # adding the first step of showing all the current files inside database
        self.add_step()

        print("GUI display is ready")

        # Keep updating the GUI
        self.root.mainloop()

    def create_window(self, w, h):
        new_window = tk.Toplevel(self.root)
        x_coor = (self.screen_width / 2) - (w / 2)
        y_coor = (self.screen_height / 2) - (h / 2)
        new_window.geometry("%dx%d+%d+%d" % (w, h, x_coor, y_coor))
        return new_window

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
        self.step_listbox.insert("end", f"{step.step_num}. {step.step_type}")

    def filter(self, filtertype):
        filterList = []
        for button in self.checkbuttons:
            if (button.value_id.get() == 1):
                filterList.append(button.category)
        self.show_table(database.get(search="filter", keyword=filterList, method=filtertype))
        self.add_step()

    def add_checkbutton(self, root, name, row, column):
        self.checkbuttons.append(Checkbutton(root, name=name, row=row, column=column))

    def search(self, search_method, keyword):
        self.show_table(database.get(search=search_method, keyword=keyword))
        self.add_step()

    def show_table(self, dataset):
        self.treeview.delete(*self.treeview.get_children())
        count = 1
        for data in dataset:
            self.treeview.insert("", "end", f"item{count}", values=(data[0], data[1], data[2]))
            count += 1
        pass

    def __del__(self):
        print("GUI display is closed")


database = db.Database()
database.add_category("renewable energy")
database.add_category("smart device")
database.add_category("indoor air quality")
database.add_category("hydroelectric")
database.add_category("secret")
database.add_category("Lithium battery")
database.add_category("vehicle")
database.add_category("energy efficiency")
database.add(name="D Solar Panel 1", filepath="files\\solar_panel_proposal_4.txt", category="renewable energy")
database.add(name="F Solar Panel 1", filepath="files\\solar_panel_proposal_5.txt", category="renewable energy")
database.add(name="E Solar Panel 1", filepath="files\\solar_panel_proposal_6.txt", category="renewable energy")
database.add(name="C Solar Panel 1", filepath="files\\solar_panel_proposal_1.txt", category="renewable energy")
database.add(name="A Solar Panel 2", filepath="files\\solar_panel_proposal_2.txt", category="renewable energy")
database.add(name="B Solar Panel 3", filepath="files\\solar_panel_proposal_3.txt", category="renewable energy")

for i in range(1, 200):
    database.add(name=f"{random.randint(1,1000)} Solar Panel", filepath=f"files\\solar_panel_proposal_{random.randint(1,1000)}.txt", category="renewable energy")

database.add(name="Smart Lighting", filepath="files\\smart_lighting.pdf", category="smart device")
database.add(name="IAQ Smart Device", filepath="files\\indoor_air_quality_device.pdf", category="smart device,indoor air quality")
database.add(name="Air filter Device", filepath="files\\air_filter_device.pdf", category="indoor air quality")

# database.print()
gui = Page()
