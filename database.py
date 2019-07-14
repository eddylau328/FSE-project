import sqlite3
import datetime
import ntpath
import os
from enum import Enum


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
        self.last_modify = kwargs.get('last_modify', None)
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
            return {'name': self.name, 'obj_id': self.obj_id, 'filepath': self.filepath, 'filename': self.filename, 'category': self.category, 'creator': self.creator, 'description': self.description, 'last_modify': self.last_modify, 'create_date': self.create_date}

    def modify(self, **kwargs):
        modify_set = {
            'name': kwargs.get('name', self.name),
            'filepath': kwargs.get('filepath', self.filepath),
            'filename': kwargs.get('filename', self.filename),
            'category': kwargs.get('category', self.category),
            'creator': kwargs.get('creator', self.creator),
            'create_date': kwargs.get('create_date', self.create_date),
            'last_modify': kwargs.get('last_modify', self.last_modify),
            'description': kwargs.get('description', self.description)
        }

        if (modify_set.get('description', None) != None):
            if (modify_set.get('description').replace(" ", "") != ""):
                modify_set['description'] = modify_set.get('description').strip()

        return modify_set


class SQL:
    def __init__(self, command, target=None):
        self.command = command
        self.target = target

class SQL_Solution:
    def __init__(self, is_procedure_search):
        self.steps = []
        self.procedure_search = is_procedure_search

    def add_step(self, step):
        self.steps.append(step)

    # step_num is assumed to be started from 1 to ...
    def get_step(self, step_num):
        return self.steps[step_num - 1]

    def get_num_of_steps(self):
        return len(self.steps)


class SQL_Step:
    def __init__(self, step_num, sql, search_package, search_type):
        # step_num is started from 1 to ...
        self.step_num = step_num
        self.sql = sql
        if (search_type == Search_Type.SEARCH_ALL):
            self.step_type = "Search All"
        elif (search_type == Search_Type.SEARCH_RELATE):
            self.step_type = "Search Relate"
        elif (search_type == Search_Type.SEARCH_EXACT):
            self.step_type = "Search Exact"
        elif (search_type == Search_Type.SEARCH_MIX):
            self.step_type = "Mix Search"
        self.search_package

class Search_Type(Enum):
    SEARCH_ALL = 1
    SEARCH_RELATE = 2
    SEARCH_EXACT = 3
    SEARCH_MIX = 4

class Search_Method(Enum):
    EXACT = 1
    RELATE = 2

class Search_Package:
    def __init__(self, search_line ,search_method_list, select_field, order_field):
        self.search_line = search_line
        self.search_method_list = search_method_list
        self.select_field = select_field
        self.order_field = order_field

class Search_Pair:
    def __init__(self, keyword, compare_field):
        self.keyword = keyword
        self.field = compare_field

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
        file_obj = (kwargs.get('name', None), kwargs.get('filepath', None), kwargs.get('category', None), kwargs.get('creator', None), kwargs.get('description', None), kwargs.get('current_time', current_time), current_time)
        sql = SQL(command=command, target=file_obj)
        self.sql_action(sql)

    def update_data(self, original_filepath, **kwargs):
        # get the id of the orginal data from the database
        command = '''UPDATE files_table SET name = ?, filepath = ?, category = ?, description = ?, last_modify = ? WHERE filepath =?'''
        target = (kwargs.get('name'), kwargs.get('filepath'), kwargs.get('category'), kwargs.get('description'), DateTime().get_current_time(), kwargs.get('filepath'))
        sql = SQL(command=command, target=target)

        self.sql_action(sql)

    def delete_data(self, original_filepath):
        command = '''DELETE FROM files_table WHERE filepath = ?'''
        target = (original_filepath,)
        sql = SQL(command=command, target=target)
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
        return self.c.fetchall()

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

    def search_package_to_sql(self,search_package):
        search_line = search_package.search_line
        search_method_list = search_package.search_method_list
        select_field = search_package.select_field
        order_field = search_package.order_field
        # return a sql command that have user's selected fields
        command = self.set_select_field_command(select_field)
        target = None
        space = " "
        if (len(search_line) == 0):
            # as it does not contain any keywords to search, therefore, it is going to get all the data in database
            search_type = Search_Type.SEARCH_ALL
        else:
            command = command + space + "WHERE" + space
            # Filter cannot be invole in mixed search
            if ( Search_Method.EXACT in search_method_list and Search_Method.RELATE in search_method_list):
                # the current searching is mixed search
                search_type = Search_Type.SEARCH_MIX
                target = ()
                count = 0
                for word in search_line:
                    if (word == "(" or word == ")" or word == "and" or word == "or"):
                        command = command + space + word
                    else:
                        if (search_method_list[count] == Search_Method.EXACT):
                            assign_string = "="
                        else:
                            assign_string = "LIKE"
                        command = command + space + word.field + space + assign_string + space + "?"
                        if (search_method_list[count] == Search_Method.EXACT):
                            target = target + ( word.keyword, )
                        else:
                            target = target + ('%' + word.keyword + '%',)
                        count += 1
            else:
                if (Search_Method.EXACT in search_method_list):
                    # the current searching is exact search
                    search_type = Search_Type.SEARCH_EXACT
                    search_method = Search_Method.EXACT
                    assign_string = "="
                else:
                    # the current searching is related search
                    search_type = Search_Type.SEARCH_RELATE
                    search_method = Search_Method.RELATE
                    assign_string = "LIKE"
                target = ()

                for word in search_line:
                    if (word == "(" or word == ")" or word == "and" or word == "or"):
                        command = command + space + word
                    else:
                        command = command + space + word.field + space + assign_string + space + "?"
                        if (search_method == Search_Method.EXACT):
                            target = target + ( word.keyword, )
                        else:
                            target = target + ('%' + word.keyword + '%',)
        command = self.set_order_command(command, select_field, order_field)
        while ("  " in command):
            command = command.replace("  ", " ")
        print(command)
        print(target)
        return {'sql':SQL(command=command, target=target), 'search_type':search_type}


    def get(self, raw_command, isCount):
        search_dict = self.raw_command_to_search_package(raw_command)
        search_line = search_dict.get('search_line')
        search_method_list = search_dict.get('search_method_list')
        order_field = ['category', 'name']
        select_field = "all"
        search_package = Search_Package(search_line=search_line,search_method_list=search_method_list,select_field=select_field,order_field=order_field)
        sql_and_type = self.search_package_to_sql(search_package)
        sql = sql_and_type.get('sql')
        search_type = sql_and_type.get('search_type')
        result = self.sql_search(sql)
        if (isCount == True):
            step = Step(step_num=self.sql_steps.get_num_of_steps()+1, sql=sql, search_package=search_package, search_type=search_type)
            self.sql_steps.add_step(step)
        return self.format_dataset_to_dictionary(result, select_field)


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
                    count += 1
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
                        if (count < len(order_field) - 1):
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

    def raw_command_to_search_package(self, raw_command):
        #replace all the space to ,
        print(raw_command)
        space_2_comma = raw_command.replace(" ", ",")
        # this is used to make the command in formatted
        space_2_comma = space_2_comma.replace("[", ",[,")
        space_2_comma = space_2_comma.replace("]", ",],")
        space_2_comma = space_2_comma.replace("=", ",=,")
        space_2_comma = space_2_comma.replace("(", ",(,")
        space_2_comma = space_2_comma.replace(")", ",),")
        space_2_comma = space_2_comma.replace('""', '"')
        space_2_comma = space_2_comma.replace("''", "'")
        print(space_2_comma)

        # may have more than one comma, replace repeat comma to single comma
        comma_2_chunks = space_2_comma
        while (",," in comma_2_chunks):
            comma_2_chunks = comma_2_chunks.replace(",,", ",")
        print(comma_2_chunks)
        # make it into chunks in list
        chunks = comma_2_chunks.split(",")
        # remove all the empty string
        while ("" in chunks):
            chunks.pop(chunks.index(""))
        print(chunks)
        #print(chunks)
        insert_index_list = []
        for i in range(0, len(chunks)-1):
            if (chunks[i] == "(" or chunks[i] == "=" or chunks[i] == "or" or chunks[i] == "and" or chunks[i] == "["):
                pass
            else:
                if (chunks[i+1] == "=" or chunks[i+1] == "or" or chunks[i+1] == "and" or chunks[i+1] == ")" or chunks[i+1] == "]"):
                    pass
                else:
                    insert_index_list.append(i+1)

        for index in sorted(insert_index_list, reverse=True):
            chunks.insert(index, "and")
        print(chunks)
        # make list of words into sublist
        format_chunks = chunks
        while ("[" in chunks and "]" in chunks):
            start = chunks.index("[")
            end = chunks.index("]")
            # list[first:last], last is not included
            sublist = format_chunks[start + 1 : end]
            for i in range (start, end+1):
                format_chunks.pop(start)
            format_chunks.insert(start, sublist)
        print(format_chunks)

        # if any "=" sign, format it to a list
        while ("=" in format_chunks):
            index = chunks.index("=")
            # list[first:last], last is not included
            sublist = format_chunks[index-1 : index+2]
            sublist.pop(sublist.index("="))
            for i in range (index-1, index+2):
                format_chunks.pop(index-1)
            format_chunks.insert(index-1, sublist)
        print(format_chunks)

        # format the keyword list back to single form
        add_list = []
        index = 0
        for chunk in format_chunks:
            # check whether it is a field search first
            if (type(chunk) is list):
                # check whether it is a list of words
                field = chunk[0]
                if (type(chunk[1]) is list):
                    word_list = chunk[1]
                    split_chunk = []
                    for word in word_list:
                        if (word is not "and" and word is not "or"):
                            sublist = [field, word]
                            split_chunk.append(sublist)
                        else:
                            split_chunk.append(word)
                    record = {'split_chunk':split_chunk, 'index':index}
                    add_list.append(record)
            index += 1

        for obj in reversed(add_list):
            print(obj['split_chunk'], obj['index'])
            format_chunks.pop(obj.get('index'))
            for chunk in reversed(obj.get('split_chunk')):
                format_chunks.insert(obj.get('index'), chunk)

        print(format_chunks)

        # create the search_method_list
        search_line = []
        search_method_list = []
        for word in format_chunks:
            if (word == "(" or word == ")" or word == "and" or word == "or"):
                search_line.append(word)
            else:
                if (type(word) is list):
                    check_word = word[1]
                    if (check_word[0] == "'" and check_word[-1] == "'"):
                        search_method_list.append(Search_Method.EXACT)
                        check_word = check_word[1:len(check_word)-1]
                    elif(check_word[0] == '"' and check_word[-1] == '"'):
                        search_method_list.append(Search_Method.EXACT)
                        check_word = check_word[1:len(check_word)-1]
                    else:
                        search_method_list.append(Search_Method.RELATE)
                    search_line.append(Search_Pair(compare_field=word[0], keyword=check_word))
                else:
                    check_word = word
                    if (check_word[0] == "'" and check_word[-1] == "'"):
                        search_method_list.append(Search_Method.EXACT)
                        check_word = check_word[1:len(check_word)-1]
                    elif(check_word[0] == '"' and check_word[-1] == '"'):
                        search_method_list.append(Search_Method.EXACT)
                        check_word = check_word[1:len(check_word)-1]
                    else:
                        search_method_list.append(Search_Method.RELATE)
                    search_line.append(Search_Pair(compare_field="name",keyword=check_word))
        print(search_method_list)

        return {'search_line':search_line, 'search_method_list':search_method_list}

    # add a directory to the file, currently file directory is "files"
    # "\\" should be adjusted to "/" (Cross-platform problem later should deal with it)
    def get_filepath(self, filename):
        return "files" + "/" + filename

    def __del__(self):
        print("Disconnected to the database")

    # search is the method it used to search
    # isCount is whether it needs to count a step
    # keyword should be a list to saves the word you need to search
    # method is the way it used to do sorting, union or intersection
    # select_field is the field you want the database to return
    # compare field is the field you want the database to compare your keyword to which column
    # order field is the field you want to sort
'''
    def get(self, search, isCount, search_package):
        if (search == "all"):
            result = self.get_all_data(select_field=search_package.select_field, order_field=search_package.order_field)
            if (isCount == True):
                step = SQL_Step(step_type="Search all", step_num=self.sql_steps.get_num_of_steps() + 1, sql=result.get('sql'), search_package=search_package)
                self.sql_steps.add_step(step)
            return self.format_dataset_to_dictionary(result.get('data'), select_field=search_package.select_field)
        elif (search == "relate" or search == "exact"):
            result = self.get_exact_or_relate(search_pair_list=search_package.search_pair_list, search_method_list=search_package.search_method_list, select_field=search_package.select_field, order_field=search_package.order_field)
            if (isCount == True):
                if (search == "relate"):
                    step_type = "Search related keyword"
                elif (search == "exact"):
                    step_type = "Search exact keyword"
                step = SQL_Step(step_type=step_type, step_num=self.sql_steps.get_num_of_steps() + 1, sql=result.get('sql'), search_package=search_package)
                self.sql_steps.add_step(step)
            return self.format_dataset_to_dictionary(result.get('data'), select_field=search_package.select_field)
        elif (search == "filter"):
            result = self.get_filter(search_pair_list=search_package.search_pair_list, logic_list=search_package.logic_list, select_field=search_package.select_field, order_field=search_package.order_field)
            if (isCount == True):
                step_type = "Filter"
                step = SQL_Step(step_type=step_type, step_num=self.sql_steps.get_num_of_steps() + 1, sql=result.get('sql'), search_package=search_package)
                self.sql_steps.add_step(step)
            return self.format_dataset_to_dictionary(result.get('data'), select_field=select_field)

'''

    # this is used to format all the searching input command into
    # => keyword, compare_field, logic, searching rules, order, etc...
    # => Personal i think this is the hardest
'''
    Situations:

    "-keywords" : do not contain this word
    "3...8" : range from 3 to 8
    " "keywords" " : exact keyword
    " word1 word2 " : contains word1 and word2
    " word1 or word2" : contains word1 or word2

    1. Enter: "solar"
        keyword = ['solar']
        compare_field = ['name']
        order_field = ['category', 'name']
        logic_field = []

    2. Enter: "solar wind" , "solar, wind" , "[solar, wind]"
        keyword = ['solar', 'wind']
        compare_field = ['name', 'name']
        order_field = ['category', 'name']
        search = [LIKE %word%, LIKE %word%]
        logic_field = [and]

    3. Enter: "solar, filename=wind"
        keyword = ['solar', 'wind']
        compare_field = ['name', 'filename']
        order_field = ['category', 'name']
        search = [LIKE %word%, LIKE %word%]
        logic_field = [and]

    4. Enter: "name=solar or filename=[solar, proposal_1]"
        keyword = ['solar', 'solar', 'proposal_1']
        compare_field =['name', 'filename', 'filename']
        order_field = ['category', 'name']

'''

import random

database = Database()

creators = ['Eddy', 'Ken', 'Alan']

database.add_category("renewable energy")
database.add_category("smart device")
database.add_category("indoor air quality")
database.add_category("hydroelectric")
database.add_category("secret")
database.add_category("Lithium battery")
database.add_category("vehicle")
database.add_category("energy efficiency")

file_sep = "\\"

database.add(name="D Solar Panel 1", filepath="files"+file_sep+"solar_panel_proposal_4a.txt", category="renewable energy", creator=creators[random.randint(0, 2)], description="Hi This is the D solar panel 1. TESTINGGGGGGGGGGGGGGGGGGGGGGG")
database.add(name="F Solar Panel 1", filepath="files"+file_sep+"solar_panel_proposal_5b.txt", category="renewable energy", creator=creators[random.randint(0, 2)], description="Hi hello world")
database.add(name="E Solar Panel 1", filepath="files"+file_sep+"solar_panel_proposal_6c.txt", category="renewable energy", creator=creators[random.randint(0, 2)], description="HoHo")
database.add(name="C Solar Panel 1", filepath="files"+file_sep+"solar_panel_proposal_1d.txt", category="renewable energy", creator=creators[random.randint(0, 2)])
database.add(name="A Solar Panel 2", filepath="files"+file_sep+"solar_panel_proposal_2e.txt", category="renewable energy", creator=creators[random.randint(0, 2)])
database.add(name="B Solar Panel 3", filepath="files"+file_sep+"solar_panel_proposal_3f.txt", category="renewable energy", creator=creators[random.randint(0, 2)])

for i in range(1, 10):
    database.add(name=f"{i} Solar Panel", filepath=f"files{file_sep}solar_panel_proposal_{i}.txt", category="renewable energy", creator=creators[random.randint(0, 2)])

database.add(name="D Smart Lighting", filepath="files"+file_sep+"smart_lighting.pdf", category="smart device")
database.add(name="IAQ Smart Device", filepath="files"+file_sep+"indoor_air_quality_device.pdf", category="smart device,indoor air quality")
database.add(name="Air filter Device", filepath="files"+file_sep+"air_filter_device.pdf", category="indoor air quality")


search = 'solar "panel"( (filepath=[solar_panel_proposal, solar_panel_proposal_6c) or creator=eddy)'

result = database.get(search, isCount=False)
for obj in result:
    print(obj)


#search_dict = database.translate_search_command(search)
#search_line = search_dict.get('search_line')
#search_method_list = search_dict.get('search_method_list')
#order_field = ['category', 'name']
#select_field = "all"
#
#search_package = Search_Package(search_line=search_line,search_method_list=search_method_list,select_field=select_field,order_field=order_field)
#database.transform_to_sql(search_line=search_package.search_line, search_method_list=search_package.search_method_list, select_field=search_package.select_field, order_field=search_package.order_field)

#search_pair_list = [Search_Pair('solar', 'name'),Search_Pair('panel', 'name'),Search_Pair('2014-03-28', 'create_date'),Search_Pair('Eddy', '#creator')]
#search_method_list = [Search_Method.RELATE, Search_Method.RELATE, Search_Method.RELATE, Search_Method.RELATE]
#logic_list = ['(','(','and',')','or',')','or']
#select_field = "all"
#order_field = None
#
#search_package = Search_Package(search_pair_list, search_method_list, logic_list, select_field, order_field)
#
#database.transform_to_sql(search_pair_list, search_method_list, logic_list, select_field, order_field)
