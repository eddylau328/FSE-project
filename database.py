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

    def add_category(self, new_category):
        currentCategory = self.get_category()
        for category in currentCategory:
            if (new_category.casefold() == category[0].casefold()):
                print("Already have this category")
                return
        with self.conn:
            self.c.execute("INSERT INTO category_list VALUES (:category)", {'category': new_category.casefold()})

    def get_category(self):
        with self.conn:
            self.c.execute("SELECT * FROM category_list")
            return self.c.fetchall()

    def add(self, **kwargs):
        # connection to the database
        with self.conn:
            # add data to the database
            self.c.execute("INSERT INTO files_table VALUES (:name, :filepath, :category)",
                           {
                               'name': kwargs.get('name', None),
                               'filepath': kwargs.get('filepath', None),
                               'category': kwargs.get('category', None)
                           })

    def get_all_data(self):
        # connection to the database
        with self.conn:
            # extract all data from the database
            self.c.execute("SELECT * FROM files_table")
            return self.c.fetchall()

    def get_filter(self, categoryList, method):
        # connection to the database
        resultList = []
        for category in categoryList:
            with self.conn:
                self.c.execute("SELECT * FROM files_table WHERE category LIKE ?", ('%' + category + '%',))
                resultList.append(self.c.fetchall())

        s = set()
        if (method == "union"):
            for result in resultList:
                s = s.union(set(result))
        elif (method == "intersect"):
            if (len(resultList) > 0):
                s = set(resultList[0])
            for i in range(1, len(resultList)):
                s = s.intersection(set(resultList[i]))
        else:
            return []
        return list(s)

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
