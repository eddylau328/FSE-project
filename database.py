import sqlite3
from operator import itemgetter
from itertools import groupby
import datetime
import ntpath
import os


class DateTime:
    def __init__(self):
        pass

    def get_current_time(self):
        currentDT = datetime.datetime.now()
        return currentDT.strftime("%Y-%m-%d %H:%M:%S")


class Data:
    def __init__(self, **kwargs):
        self.name = kwargs.get('name', None)
        self.obj_id = kwargs.get('filepath', None)
        self.filepath = kwargs.get('filepath', None)
        self.filename = kwargs.get('filename', None)
        self.category = kwargs.get('category', None)
        self.creator = kwargs.get('creator', None)
        self.description = kwargs.get('description', None)
        self.last_modify =  kwargs.get('last_modify', None)
        self.create_date = kwargs.get('create_date', None)

    def set(self, **kwargs):

        modify_set = self.modify(**kwargs)

        self.name = modify_set.get('name')
        self.filepath = modify_set.get('filepath')
        self.filename = modify_set.get('filename')
        self.category = modify_set.get('category')
        self.creator = modify_set.get('creator')
        self.create_date = modify_set.get('create_date')
        self.last_modify = modify_set.get('last_modify')
        self.description = modify_set.get('description')

    def get(self, *args):
        get_dict = {}
        if (len(args) > 1):
            for field in args:
                if (field == "name"):
                    get_dict[field] = self.name
                elif (field == "obj_id"):
                    get_dict[field] = self.obj_id
                elif (field == "filepath"):
                    get_dict[field] = self.filepath
                elif (field == "filename"):
                    get_dict[field] = self.filename
                elif (field == "category"):
                    get_dict[field] = self.category
                elif (field == "creator"):
                    get_dict[field] = self.creator
                elif (field == "description"):
                    get_dict[field] = self.description
                elif (field == "last_modify"):
                    get_dict[field] = self.last_modify
                elif (field == "create_date"):
                    get_dict[field] = self.create_date
            return get_dict
        elif (len(args) == 1):
            for field in args:
                if (field == "name"):
                    return self.name
                elif (field == "obj_id"):
                    return self.obj_id
                elif (field == "filepath"):
                    return self.filepath
                elif (field == "filename"):
                    return self.filename
                elif (field == "category"):
                    return self.category
                elif (field == "creator"):
                    return self.creator
                elif (field == "description"):
                    return self.description
                elif (field == "last_modify"):
                    return self.last_modify
                elif (field == "create_date"):
                    return self.create_date
        else:
            return {'name': self.name, 'obj_id':self.obj_id, 'filepath': self.filepath, 'filename': self.filename, 'category': self.category, 'creator': self.creator, 'description': self.description, 'last_modify':self.last_modify, 'create_date':self.create_date}

    def modify(self, **kwargs):
        modify_set = {
            'name' : kwargs.get('name', self.name),
            'filepath' : kwargs.get('filepath', self.filepath),
            'filename' : kwargs.get('filename', self.filename),
            'category' : kwargs.get('category', self.category),
            'creator' : kwargs.get('creator', self.creator),
            'create_date' : kwargs.get('create_date', self.create_date),
            'last_modify' : kwargs.get('last_modify', self.last_modify),
            'description' : kwargs.get('description', self.description)
        }

        if (modify_set.get('description', None) != None):
            if (modify_set.get('description').replace(" ", "") != ""):
                modify_set['description'] = modify_set.get('description').strip()

        return modify_set


class SQL:
    def __init__(self, sql, target=None):
        self.command = sql
        self.target = target

class SQL_Solution:
    def __init__(self, is_procedure_search):
        self.steps = []
        self.procedure_search = is_procedure_search

    def add_step(self, step):
        self.steps.append(step)

    # step_num is assumed to be started from 1 to ...
    def get_step(self, step_num=None, state=None):
        if (step_num != None):
            return self.steps[step_num - 1]
        else:
            if (state == "current"):
                return self.steps[-1]
            elif (state == "previous"):
                return self.steps[-2]
            elif (state == "start"):
                return self.steps[0]
            else:
                return None

    def get_num_of_steps(self):
        return len(self.steps)


class SQL_Step:
    def __init__(self, step_type, step_num, sql ,keyword, method, select_field, compare_field, order_field):
        # step_num is started from 1 to ...
        self.step_num = step_num
        self.step_type = step_type
        self.sql = sql
        self.keyword = keyword
        self.method = method
        self.select_field = select_field
        self.compare_field = compare_field
        self.order_field = order_field

class Database:
    def __init__(self):
        # make connection to the database
        self.conn = sqlite3.connect(":memory:")
        self.c = self.conn.cursor()

        # if not exists, it will prevent error
        self.c.execute("""CREATE TABLE if not exists
            files_table (
                name text,
                filepath text,
                category text,
                creator text,
                description text,
                create_date text,
                last_modify text
            )""")
        self.conn.commit()
        # File Name - saves the file name you want to set
        # Filepath - saves the filepath
        # Categories - saves the category of the file
        # Creator - saves the creator name
        # description - descripes what the file is
        # Create date - saves the created date of the object
        # Last Modify - saves the latest update time and date
        self.ALL_FIELDS = ("name", "filepath", "category", "creator", "description", "create_date", "last_modify")
        self.c.execute("""CREATE TABLE if not exists category_list (category text)""")
        self.conn.commit()
        self.sql_history = []
        self.sql_steps = SQL_Solution(is_procedure_search=False)
        print("Connected to the database")

    # user can add categories for sorting the files
    def add_category(self, new_category):
        currentCategory = self.get_category()
        for category in currentCategory:
            if (new_category.casefold() == category[0].casefold()):
                print("Already have this category")
                return
        with self.conn:
            self.c.execute("INSERT INTO category_list VALUES (:category)", {'category': new_category.casefold()})

    # get the categories designed by the users
    def get_category(self):
        with self.conn:
            self.c.execute("SELECT * FROM category_list")
            return self.c.fetchall()

    # adding files detail to the files_table in the database
    def add(self, **kwargs):
        current_time = DateTime().get_current_time()
        command = '''INSERT INTO files_table (name, filepath, category, creator, description, create_date, last_modify) VALUES (?,?,?,?,?,?,?)'''
        file_obj = (kwargs.get('name', None), kwargs.get('filepath', None), kwargs.get('category', None), kwargs.get('creator', None), kwargs.get('description', None), kwargs.get('current_time',current_time), current_time)
        sql = SQL(command, file_obj)
        self.sql_action(sql)


    def update_data(self, original_filepath, **kwargs):
        # get the id of the orginal data from the database
        command = '''UPDATE files_table SET name = ?, filepath = ?, category = ?, description = ?, last_modify = ? WHERE filepath =?'''
        target = (kwargs.get('name'), kwargs.get('filepath'), kwargs.get('category'), kwargs.get('description'), DateTime().get_current_time(), kwargs.get('filepath'))
        sql = SQL(command, target)

        self.sql_action(sql)

    def delete_data(self, original_filepath):
        command = '''DELETE FROM files_table WHERE filepath = ?'''
        target = (original_filepath,)
        sql = SQL(command, target)
        self.sql_action(sql)

    # can insert, can delete, can update
    def sql_action(self, sql):
        # connection to the database
        with self.conn:
            self.c.execute(sql.command, sql.target)

    def sql_search(self, sql):
        # connection to the database
        with self.conn:
            if (sql.target == None):
                self.c.execute(sql.command)
            else:
                self.c.execute(sql.command, sql.target)
        return {'data': self.c.fetchall(), 'sql': sql}

    def get_filter(self, categoryList, method, select_field, order_field):
        if (method == 'union'):
            logic = "or"
        elif (method == 'intersect'):
            logic = "and"
        else:
            return

        # return the select field command
        command = self.set_select_field_command(select_field)
        target = ()
        count = 0
        if (len(categoryList) > 0):
            command = command + ''' WHERE '''
        for category in categoryList:
            command = command + ''' category LIKE ? '''
            if (count < len(categoryList) - 1):
                command = command + logic
            count += 1
            target = target + ('%' + category + '%',)

        command = self.set_order_command(command, select_field, order_field)
        print(command)
        sql = SQL(command, target)
        return self.sql_search(sql)

    # used to create the select field command
    def set_select_field_command(self, select_field):
        if (select_field == None or select_field == "all"):
            command = '''SELECT * FROM files_table'''
        else:
            count = 0
            command = '''SELECT '''
            for string in select_field:
                if (count < len(select_field) - 1):
                    command = command + string + ''', '''
                else:
                    command = command + string
                count += 1
            command = command + ''' FROM files_table '''
        return command

    def get_all_data(self, select_field, compare_field, order_field):
        # extract all data from the database
        command = self.set_select_field_command(select_field)
        command = self.set_order_command(command, select_field, order_field)
        sql = SQL(command)
        return self.sql_search(sql)

    def get_exact_or_relate(self, search, keyword, select_field, compare_field, order_field):
        command = self.set_select_field_command(select_field)
        target = ()

        if (compare_field == None):
            if (search == "exact"):
                command = command + ''' WHERE name=? COLLATE NOCASE'''
                target = (keyword,)
            elif (search == "relate"):
                command = command + ''' WHERE name LIKE ? COLLATE NOCASE'''
                target = ('%' + keyword + '%',)
        else:
            if (search == "exact"):
                if (len(compare_field) > 0):
                    command = command + ''' WHERE '''
                count = 0
                for string in compare_field:
                    command = command + string + ''' =? COLLATE NOCASE '''
                    if (count < len(compare_field) - 1):
                        command = command + ''' and '''
                    count += 1
                for word in keyword:
                    target = target + (word,)
            elif (search == "relate"):
                if (len(compare_field) > 0):
                    command = command + ''' WHERE '''
                for string in compare_field:
                    command = command + string + ''' LIKE ? COLLATE NOCASE '''
                    if (count < len(compare_field) - 1):
                        command = command + ''' or '''
                    count += 1
                for word in keyword:
                    target = target + ('%' + word + '%',)

        command = self.set_order_command(command, select_field, order_field)
        sql = SQL(command, target)
        return self.sql_search(sql)

    def set_order_command(self, command, select_field, order_field):
        if (select_field == None or select_field == "all"):
            if (order_field == None):
                command = command + ''' ORDER BY category ASC, name ASC'''
            else:
                command = command + ''' ORDER BY '''
                count = 0
                for field in order_field:
                    if (count < len(order_field) - 1):
                        command = command + ''' ''' + field + ''' ASC, '''
                    else:
                        command = command + ''' ''' + field + ''' ASC '''
        else:
            if (order_field == None):
                if ("category" in select_field and "name" in select_field):
                    command = command + ''' ORDER BY category ASC, name ASC'''
                elif ("category" in select_field):
                    command = command + ''' ORDER BY category ASC'''
                elif ("name" in select_field):
                    command = command + ''' ORDER BY name ASC'''
                elif ("filepath" in select_field):
                    command = command + ''' ORDER BY filepath ASC'''
            else:
                command = command + ''' ORDER BY '''
                count = 0
                for field in order_field:
                    if (field in select_field):
                        if (count < len(order_field)-1):
                            command = command + ''' ''' + field + ''' ASC, '''
                        else:
                            command = command + ''' ''' + field + ''' ASC '''
                    count += 1
        return command

    # this is used to format all the get results set into dictionary type object
    def format_dataset_to_dictionary(self, dataset, select_field):
        new_dataset = []
        for obj in dataset:
            dict_obj = {}
            if (select_field == "all" or select_field == None):
                for field in self.ALL_FIELDS:
                    # as self.ALL_FIELDS is in order with the column, therefore it can get the correct column
                    dict_obj[field] = obj[self.ALL_FIELDS.index(field)]
            else:
                index = 0
                for field in select_field:
                    dict_obj[field] = obj[index]
                    index += 1
            new_dataset.append(dict_obj)
        return new_dataset

    # search is the method it used to search
    # isCount is whether it needs to count a step
    # keyword should be a list to saves the word you need to search
    # method is the way it used to do sorting, union or intersection
    # select_field is the field you want the database to return
    # compare field is the field you want the database to compare your keyword to which column
    # order field is the field you want to sort
    def get(self, search, isCount, keyword=None, method=None, select_field=None, compare_field=None, order_field=None):
        if (search == "all"):
            result = self.get_all_data(select_field=select_field,compare_field=compare_field,order_field=order_field)
            if (isCount == True):
                step = SQL_Step(step_type="Search all", step_num=self.sql_steps.get_num_of_steps() + 1, sql=result.get('sql'),keyword=keyword, method=method, select_field=select_field, compare_field=compare_field, order_field=order_field)
                self.sql_steps.add_step(step)
            return self.format_dataset_to_dictionary(result.get('data'), select_field=select_field)
        elif (search == "relate" or search == "exact"):
            result = self.get_exact_or_relate(search, keyword, select_field=select_field, compare_field=compare_field, order_field=order_field)
            if (isCount == True):
                if (search == "relate"):
                    step_type = "Search related keyword"
                elif (search == "exact"):
                    step_type = "Search exact keyword"
                step = SQL_Step(step_type=step_type, step_num=self.sql_steps.get_num_of_steps() + 1, sql=result.get('sql'),keyword=keyword, method=method, select_field=select_field, compare_field=compare_field, order_field=order_field)
                self.sql_steps.add_step(step)
            return self.format_dataset_to_dictionary(result.get('data'), select_field=select_field)
        elif (search == "filter"):
            if (keyword == None):
                return []
            else:
                if (method == None):
                    return []
                else:
                    result = self.get_filter(keyword, method, select_field, order_field)
                    if (isCount == True):
                        if (method == "union"):
                            step_type = "Filter Related"
                        elif (method == "intersect"):
                            step_type = "Filter Exact"
                        step = SQL_Step(step_type=step_type, step_num=self.sql_steps.get_num_of_steps() + 1, sql=result.get('sql'),keyword=keyword, method=method, select_field=select_field, compare_field=compare_field, order_field=order_field)
                        self.sql_steps.add_step(step)
                    return self.format_dataset_to_dictionary(result.get('data'), select_field=select_field)


    def print(self, dataset=None):
        if (dataset == None):
            for data in self.get(search="all", isCount=False):
                print(data)
        else:
            for data in dataset:
                print(data)

    def get_sql_step(self, step_num=None, state=None):
        return self.sql_steps.get_step(step_num, state)

    def get_sql_history(self):
        return self.sql_history

    def extract_filename(self, path, **kwargs):
        if (kwargs.get('filetype', True) == True):
            return ntpath.basename(path)
        else:
            return os.path.splitext(ntpath.basename(path))[0]

    # add a directory to the file, currently file directory is "files"
    # "\\" should be adjusted to "/" (Cross-platform problem later should deal with it)
#    def get_filepath(self, filename):
#        return "files" + "/" + filename


    def __del__(self):
        print("Disconnected to the database")
