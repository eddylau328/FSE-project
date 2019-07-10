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
    def __init__(self, name=None, filename=None, filepath=None, category=None, creator=None, description=None, create_date=None, last_modify=None):
        self.name = name
        self.filepath = filepath
        self.filename = filename
        self.category = category
        self.creator = creator
        self.description = description
        self.last_modify = last_modify
        self.create_date = create_date

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

    def get(self):
        return {'name': self.name, 'filepath': self.filepath, 'filename': self.filename, 'category': self.category, 'creator': self.creator, 'description': self.description, 'last_modify':self.last_modify, 'create_date':self.create_date}

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
    def __init__(self, step_type, step_num, sql):
        # step_num is started from 1 to ...
        self.step_num = step_num
        self.step_type = step_type
        self.sql = sql


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
        file_obj = (kwargs.get('name', None), kwargs.get('filepath', None), kwargs.get('category', None), kwargs.get('creator', None), kwargs.get('description', None), current_time, current_time)
        sql = SQL(command, file_obj)
        self.sql_insert(sql)

    def update_data(self, orginal_filepath, **kwargs):
        # get the id of the orginal data from the database
        with self.conn:
            self.c.execute("SELECT id FROM files_table WHERE filepath = ?", (orginal_filepath,))
            data_id = self.c.fetchall()[0][0]
        print(data_id)

    def get_all_data(self, select_field=None):
        # extract all data from the database
        if (select_field == None):
            command = '''SELECT name, filepath, creator, last_modify, category FROM files_table'''
        else:
            count = 0
            command = '''SELECT '''
            for string in select_field:
                if (count < len(select_field) - 1):
                    command = command + string + ''', '''
                else:
                    command = command + string
            command = command + ''' FROM files_table '''
        sql = SQL(command)
        return self.sql_search(sql)

    def sql_insert(self, sql):
        # connection to the database
        with self.conn:
            if (sql.command != None and sql.target != None):
                self.c.execute(sql.command, sql.target)
            elif (sql.command != None):
                self.c.execute(sql.command)
            else:
                return

    def sql_search(self, sql):
        # connection to the database
        with self.conn:
            if (sql.target == None):
                self.c.execute(sql.command)
            else:
                self.c.execute(sql.command, sql.target)
        return {'data': self.c.fetchall(), 'sql': sql}

    def get_filter(self, categoryList, method):
        if (method == 'union'):
            logic = "or"
        elif (method == 'intersect'):
            logic = "and"
        else:
            return
        sql = ''''''
        target = None
        if (categoryList != []):
            sql = '''SELECT name, filepath, creator, last_modify, category FROM files_table WHERE'''
            target = ()
            count = 0
            for category in categoryList:
                sql = sql + ''' category LIKE ? '''
                if (count < len(categoryList) - 1):
                    sql = sql + logic
                count += 1
                target = target + ('%' + category + '%',)
        sql = SQL(sql, target)
        return self.sql_search(sql)

    def get_relate(self, keyword):
        command = '''SELECT name, filepath, creator, last_modify, category FROM files_table WHERE name LIKE ? COLLATE NOCASE'''
        target = ('%' + keyword + '%',)
        sql = SQL(command, target)
        return self.sql_search(sql)

    def get_exact(self, keyword, select_field=None, compare_field=None):
        command = ''''''
        target = ()
        if (select_field == None):
            command = '''SELECT name, filepath, creator, last_modify, category FROM files_table'''
        elif (select_field == "all"):
            command = '''SELECT * FROM files_table'''

        if (compare_field == None):
            command = command + ''' WHERE name=? COLLATE NOCASE'''
            target = (keyword,)
        else:
            for string in compare_field:
                command = command + ''' WHERE ''' + string + '''=? COLLATE NOCASE'''
            for word in keyword:
                target = target + (word,)
        print(command)
        print(target)
        sql = SQL(command, target)
        return self.sql_search(sql)

    def sort(self, dataset, reverse=None, select_field=None):
        if (reverse == None):
            if (select_field == None):
                dataset.sort(key=itemgetter(4, 0))
            else:
                if ("category" in select_field and "name" in select_field):
                    dataset.sort(key=itemgetter(select_field.index("category"), select_field.index("name")))
                else:
                    return dataset
        else:
            if (select_field == None):
                dataset.sort(key=itemgetter(4, 0), reverse=reverse)
            else:
                if ("category" in select_field and "name" in select_field):
                    dataset.sort(key=itemgetter(select_field.index("category"), select_field.index("name")), reverse=reverse)
                else:
                    return dataset
        return dataset

    # search is the method it used to search
    # isCount is whether it needs to count a step
    # keyword should be a list to saves the word you need to search
    # method is the way it used to do sorting, union or intersection
    # select_field is the field you want the database to return
    # compare field is the field you want the database to compare your keyword to which column
    def get(self, search, isCount, keyword=None, method=None, select_field=None, compare_field=None):
        if (search == "all"):
            result = self.get_all_data(select_field=select_field)
            if (isCount == True):
                step = SQL_Step(step_type="Search all", step_num=self.sql_steps.get_num_of_steps() + 1, sql=result.get('sql'))
                self.sql_steps.add_step(step)
            return self.sort(result.get('data'), select_field=select_field)
        elif (search == "relate"):
            result = self.get_relate(keyword)
            if (isCount == True):
                step = SQL_Step(step_type="Search related keyword", step_num=self.sql_steps.get_num_of_steps() + 1, sql=result.get('sql'))
                self.sql_steps.add_step(step)
            return self.sort(result.get('data'), select_field=select_field)
        elif (search == "exact"):
            result = self.get_exact(keyword, select_field=select_field, compare_field=compare_field)
            if (isCount == True):
                step = SQL_Step(step_type="Search exact keyword", step_num=self.sql_steps.get_num_of_steps() + 1, sql=result.get('sql'))
                self.sql_steps.add_step(step)
            return self.sort(result.get('data'), select_field=select_field)
        elif (search == "filter"):
            if (keyword == None):
                return []
            else:
                if (method == None):
                    return []
                else:
                    result = self.get_filter(keyword, method)
                    if (isCount == True):
                        step = SQL_Step(step_type="Filter", step_num=self.sql_steps.get_num_of_steps() + 1, sql=result.get('sql'))
                        self.sql_steps.add_step(step)
                    return self.sort(result.get('data'), select_field=select_field)

    def print(self, dataset=None):
        if (dataset == None):
            for data in self.get_all_data():
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
    def get_filepath(self, filename):
        return "files" + "/" + filename

    def __del__(self):
        print("Disconnected to the database")
