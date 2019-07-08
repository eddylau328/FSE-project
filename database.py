import sqlite3
from operator import itemgetter
from itertools import groupby

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
                category text
            )""")
        self.conn.commit()
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
        command = '''INSERT INTO files_table (name,filepath,category) VALUES (?,?,?)'''
        file_obj = (kwargs.get('name', None), kwargs.get('filepath', None), kwargs.get('category', None))
        sql = SQL(command, file_obj)
        self.sql_insert(sql)

    def get_all_data(self):
        # extract all data from the database
        command = '''SELECT * FROM files_table'''
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
                self.c.execute(sql.command,sql.target)
        return self.c.fetchall(), sql

    def get_filter(self, categoryList, method):
        if (method == 'union'):
            logic = "or"
        elif (method == 'intersect'):
            logic = "and"
        else:
            return
        sql = '''SELECT * FROM files_table WHERE'''
        target = ()
        count = 0
        for category in categoryList:
            sql = sql + ''' category LIKE ? '''
            if (count < len(categoryList)-1):
                sql = sql + logic
            count += 1
            target = target + ('%' + category + '%',)
        sql = SQL(sql, target)
        return self.sql_search(sql)

    def get_relate(self, keyword):
        command = '''SELECT * FROM files_table WHERE name LIKE ? COLLATE NOCASE'''
        target = ('%' + keyword + '%',)
        sql = SQL(command, target)
        return self.sql_search(sql)

    def get_exact(self, keyword):
        command = '''SELECT * FROM files_table WHERE name=? COLLATE NOCASE'''
        target = (keyword,)
        sql = SQL(command, target)
        return self.sql_search(sql)

    def sort(self, dataset, reverse=None):
        if (reverse == None):
            dataset.sort(key=itemgetter(2, 0))
        else:
            dataset.sort(key=itemgetter(2, 0), reverse=reverse)
        return dataset

    def get(self, search, keyword=None, method=None):
        if (search == "all"):
            result, sql = self.get_all_data()
            step = SQL_Step(step_type="Search all", step_num=self.sql_steps.get_num_of_steps()+1, sql=sql)
            self.sql_steps.add_step(step)
            return self.sort(result)
        elif (search == "relate"):
            result, sql = self.get_relate(keyword)
            step = SQL_Step(step_type="Search related keyword", step_num=self.sql_steps.get_num_of_steps()+1, sql=sql)
            self.sql_steps.add_step(step)
            return self.sort(result)
        elif (search == "exact"):
            result, sql = self.get_exact(keyword)
            step = SQL_Step(step_type="Search exact keyword", step_num=self.sql_steps.get_num_of_steps()+1, sql=sql)
            self.sql_steps.add_step(step)
            return self.sort(result)
        elif (search == "filter"):
            if (keyword == None):
                return []
            elif (keyword == []):
                return []
            else:
                if (method == None):
                    return []
                else:
                    result, sql = self.get_filter(keyword, method)
                    step = SQL_Step(step_type="Filter", step_num=self.sql_steps.get_num_of_steps()+1, sql=sql)
                    self.sql_steps.add_step(step)
                    return self.sort(result)

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

    def __del__(self):
        print("Disconnected to the database")
