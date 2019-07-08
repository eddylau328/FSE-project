import sqlite3
from operator import itemgetter
from itertools import groupby


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
        sql = '''INSERT INTO files_table (name,filepath,category) VALUES (?,?,?)'''
        file_obj = (kwargs.get('name', None), kwargs.get('filepath', None), kwargs.get('category', None))
        self.sql_insert(sql, file_obj)

    def get_all_data(self):
        # extract all data from the database
        sql = '''SELECT * FROM files_table'''
        return self.sql_search(sql)

    def sql_insert(self, sql, file_obj):
        # connection to the database
        with self.conn:
            self.c.execute(sql, file_obj)

    def sql_search(self, sql, target=None):
        # connection to the database
        with self.conn:
            if (target == None):
                self.c.execute(sql)
            else:
                self.c.execute(sql,target)
        return self.c.fetchall()

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
        print(sql)
        return self.sql_search(sql,target)

    def get_relate(self, keyword):
        with self.conn:
            self.c.execute("SELECT * FROM files_table WHERE name LIKE ? COLLATE NOCASE", ('%' + keyword + '%',))
            return self.c.fetchall()

    def get_exact(self, keyword):
        with self.conn:
            self.c.execute("SELECT * FROM files_table WHERE name=? COLLATE NOCASE", (keyword,))
            return self.c.fetchall()

    def sort(self, dataset, reverse=None):
        if (reverse == None):
            dataset.sort(key=itemgetter(2, 0))
        else:
            dataset.sort(key=itemgetter(2, 0), reverse=reverse)
        return dataset

    def get(self, search, keyword=None, method=None):
        if (search == "all"):
            return self.sort(self.get_all_data())
        elif (search == "relate"):
            return self.sort(self.get_relate(keyword))
        elif (search == "exact"):
            return self.sort(self.get_exact(keyword))
        elif (search == "filter"):
            if (keyword == None):
                return []
            elif (keyword == []):
                return []
            else:
                if (method == None):
                    return []
                else:
                    return self.sort(self.get_filter(keyword, method))

    def print(self, dataset=None):
        if (dataset == None):
            for data in self.get_all_data():
                print(data)
        else:
            for data in dataset:
                print(data)

    def __del__(self):
        print("Disconnected to the database")
