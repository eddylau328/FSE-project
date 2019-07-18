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
        self.title = kwargs.get('title', None)
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

        self.title = modify_set.get('title')
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
                if (field == "title"):
                    get_dict[field] = self.title
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
                if (field == "title"):
                    return self.title
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
            return {'title': self.title, 'obj_id': self.obj_id, 'filepath': self.filepath, 'filename': self.filename, 'category': self.category, 'creator': self.creator, 'description': self.description, 'last_modify': self.last_modify, 'create_date': self.create_date}

    def modify(self, **kwargs):
        modify_set = {
            'title': kwargs.get('title', self.title),
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
    def __init__(self, command, target):
        self.command = command
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
            try:
                return self.steps[step_num - 1]
            except:
                return None
        else:
            if (state == "current"):
                try:
                    return self.steps[-1]
                except:
                    return None
            elif (state == "previous"):
                try:
                    return self.steps[-2]
                except:
                    return None
            elif (state == "start"):
                try:
                    return self.steps[0]
                except:
                    return None
            else:
                return None

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
        elif (search_type == Search_Type.FILTER_RELATE):
            self.step_type = "Filter Relate"
        elif (search_type == Search_Type.FILTER_EXACT):
            self.step_type = "Filter Exact"
        self.search_package = search_package

class Search_Type(Enum):
    SEARCH_ALL = 1
    SEARCH_RELATE = 2
    SEARCH_EXACT = 3
    SEARCH_MIX = 4
    FILTER_RELATE = 5
    FILTER_EXACT = 6

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
                title text,
                filepath text,
                filename text,
                category text,
                creator text,
                description text,
                create_date text,
                last_modify text
            )""")
        self.conn.commit()
        # File title - saves the file title you want to set
        # Filepath - saves the filepath
        # Categories - saves the category of the file
        # Creator - saves the creator name
        # description - descripes what the file is
        # Create date - saves the created date of the object
        # Last Modify - saves the latest update time and date
        self.ALL_FIELDS = ("title", "filepath", "filename","category", "creator", "description", "create_date", "last_modify")
        self.c.execute("""CREATE TABLE if not exists category_list (category text)""")
        self.conn.commit()
        self.sql_history = []
        self.sql_solution = None
        print("Connected to the database")

    # user can add categories for sorting the files
    def add_category(self, new_category):
        if (self.check_category_exist(new_category) == False):
            with self.conn:
                self.c.execute("INSERT INTO category_list VALUES (:category)", {'category': new_category.casefold()})
        else:
            return

    # get the categories designed by the users
    def get_category(self):
        with self.conn:
            self.c.execute("SELECT * FROM category_list")
            return self.c.fetchall()

    def delet_category(self, category):
        with self.conn:
            self.c.excute("DELETE FROM category_list WHERE category=?", (category,))


    def check_category_conflict(self, original):
        with self.conn:
            self.c.execute("SELECT title, filename, category FROM files_table WHERE category LIKE ?", ('%' + original + '%',))
            result = self.c.fetchall()
        if (len(result) > 0):
            return {'conflict_data':result, 'conflict': True}
        else:
            return {'conflict_data':result, 'conflict': False}

    def check_category_exist(self, new_category):
        currentCategory = self.get_category()
        for category in currentCategory:
            if (new_category.casefold() == category[0].casefold()):
                print("Already have this category")
                return True
        return False


    def update_category(self, original, new):
        with self.conn:
            self.c.execute("UPDATE category_list SET category=? WHERE category=?", (new, original))

    # adding files detail to the files_table in the database
    def add(self, **kwargs):
        current_time = DateTime().get_current_time()
        command = '''INSERT INTO files_table (title, filepath, filename, category, creator, description, create_date, last_modify) VALUES (?,?,?,?,?,?,?,?)'''
        file_obj = (kwargs.get('title', None), kwargs.get('filepath', None), kwargs.get('filename', self.extract_filename(kwargs.get('filepath', None), filetype=False)), kwargs.get('category', None), kwargs.get('creator', ""), kwargs.get('description', None), kwargs.get('current_time', current_time), current_time)
        sql = SQL(command=command, target=file_obj)
        self.sql_action(sql)

    def update_data(self, original_filepath, **kwargs):
        # get the id of the orginal data from the database
        command = '''UPDATE files_table SET title = ?, creator = ?, filepath = ?, filename = ?,category = ?, description = ?, last_modify = ? WHERE filepath =?'''
        target = (kwargs.get('title'), kwargs.get('creator'),kwargs.get('filepath'), kwargs.get('filename'),kwargs.get('category'), kwargs.get('description'), DateTime().get_current_time(), kwargs.get('filepath'))
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
            self.c.execute(sql.command, sql.target)
        return self.c.fetchall()

    # used to create the select field command
    def set_select_field_command(self, select_field, previous_sql=None):
        if (select_field == None or select_field == "all"):
            if (previous_sql == None):
                command = '''SELECT * FROM files_table'''
            else:
                command = '''SELECT * FROM ''' + f" ({previous_sql.command}) "
        else:
            count = 0
            command = '''SELECT '''
            for string in select_field:
                if (count < len(select_field) - 1):
                    command = command + string + ''', '''
                else:
                    command = command + string
                count += 1
            if (previous_sql == None):
                command = command + ''' FROM files_table '''
            else:
                command = command + f" FROM ({previous_sql.command}) "
        return command

    def search_package_to_sql(self,search_package, sql_solution):
        search_line = search_package.search_line
        search_method_list = search_package.search_method_list
        select_field = search_package.select_field
        order_field = search_package.order_field

        # this is used to do the procedure search
        if (sql_solution.procedure_search == True):
            # current step is becuz the new step is not yet added
            if (sql_solution.get_step(state="current") == None):
                previous_sql = None
            else:
                previous_sql = sql_solution.get_step(state="current").sql
            # return a sql command that have user's selected fields
            if (previous_sql == None):
                command = self.set_select_field_command(select_field)
            else:
                command = self.set_select_field_command(select_field, previous_sql=previous_sql)
        else:
            command = self.set_select_field_command(select_field)
        target = ()
        space = " "
        case_insensitive = "COLLATE NOCASE"
        if (len(search_line) == 0):
            # as it does not contain any keywords to search, therefore, it is going to get all the data in database
            search_type = Search_Type.SEARCH_ALL
        else:
            command = command + space + "WHERE" + space
            # Filter cannot be invole in mixed search
            if ( Search_Method.EXACT in search_method_list and Search_Method.RELATE in search_method_list):
                # the current searching is mixed search
                search_type = Search_Type.SEARCH_MIX
                if (sql_solution.procedure_search == True):
                    if (previous_sql != None):
                        target = previous_sql.target
                count = 0
                for word in search_line:
                    if (word == "(" or word == ")" or word == "and" or word == "or"):
                        command = command + space + word
                    else:
                        if (search_method_list[count] == Search_Method.EXACT):
                            assign_string = "="
                        else:
                            assign_string = "LIKE"
                        command = command + space + word.field + space + assign_string + space + "?" + space + case_insensitive
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
                    # check whether it is filter or not
                    isFilter = True
                    for word in search_line:
                        if (word != "(" and word != ")" and word != "and" and word != "or"):
                            if (word.field != "category"):
                                isFilter = False
                                break
                    if (isFilter):
                        isRelate = True
                        for word in search_line:
                            if (word == "and"):
                                isRelate = False
                                break
                    if (isFilter == True):
                        if (isRelate == True):
                            search_type = Search_Type.FILTER_RELATE
                        else:
                            search_type = Search_Type.FILTER_EXACT
                    assign_string = "LIKE"

                if (sql_solution.procedure_search == True):
                    if (previous_sql != None):
                        target = previous_sql.target
                for word in search_line:
                    if (word == "(" or word == ")" or word == "and" or word == "or"):
                        command = command + space + word
                    else:
                        command = command + space + word.field + space + assign_string + space + "?" + space + case_insensitive
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


    # append the previous sql_solution to the history and clear the current sql_step and replace it with a new one
    def create_new_search(self, is_procedure_search):
        # when the first beginning of the program, sql_steps is None
        # we add only we finish a steps
        if (self.sql_solution != None):
            self.sql_history.append(self.sql_solution)
        # create a new sql_solution
        self.sql_solution = SQL_Solution(is_procedure_search=is_procedure_search)


    # search_package could be provided, instead of raw_command
    def get(self, raw_command=None, isCount=None, select_field=None, order_field=None, search_package=None, sql=None):
        if (sql == None):
            if (search_package == None):
                if (raw_command==None):
                    raw_command = ""
                if (isCount == None):
                    isCount = False
                search_dict = self.raw_command_to_search_package(raw_command)
                search_line = search_dict.get('search_line')
                search_method_list = search_dict.get('search_method_list')
                new_search_package = Search_Package(search_line=search_line,search_method_list=search_method_list,select_field=select_field,order_field=order_field)
            else:
                new_search_package = search_package
            sql_and_type = self.search_package_to_sql(search_package=new_search_package, sql_solution=self.sql_solution)
            sql = sql_and_type.get('sql')
            search_type = sql_and_type.get('search_type')
        result = self.sql_search(sql)
        if (isCount == True):
            step = SQL_Step(step_num=self.sql_solution.get_num_of_steps()+1, sql=sql, search_package=new_search_package, search_type=search_type)
            self.sql_solution.add_step(step)
        return self.format_dataset_to_dictionary(result, select_field)


    def set_order_command(self, command, select_field, order_field):
        if (select_field == None or select_field == "all"):
            if (order_field == None):
                command = command + ''' ORDER BY category ASC, title ASC'''
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
                if ("category" in select_field and "title" in select_field):
                    command = command + ''' ORDER BY category ASC, title ASC'''
                elif ("category" in select_field):
                    command = command + ''' ORDER BY category ASC'''
                elif ("title" in select_field):
                    command = command + ''' ORDER BY title ASC'''
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
        return self.sql_solution.get_step(step_num=step_num, state=state)

    def clear_sql_history(self):
        self.sql_history = []

    def get_sql_history(self, **kwargs):
        try:
            if ('get_index' in kwargs):
                return len(self.sql_history)-1
            elif ('step_num' in kwargs and 'step_index' in kwargs):
                step_index = kwargs.get('step_index')
                step_num = kwargs.get('step_num')
                return self.sql_history[step_index].get_step(step_num)
            else:
                return self.sql_history[-1]
        except:
            return None

    def extract_filename(self, path, **kwargs):
        if (kwargs.get('filetype', True) == True):
            return ntpath.basename(path)
        else:
            return os.path.splitext(ntpath.basename(path))[0]

    def raw_command_to_search_package(self, raw_command):
        #replace all the space to ,
        space_2_comma = raw_command.replace(" ", ",")
        # this is used to make the command in formatted
        space_2_comma = space_2_comma.replace("[", ",[,")
        space_2_comma = space_2_comma.replace("]", ",],")
        space_2_comma = space_2_comma.replace("=", ",=,")
        space_2_comma = space_2_comma.replace("(", ",(,")
        space_2_comma = space_2_comma.replace(")", ",),")
        space_2_comma = space_2_comma.replace("'", '"')
        while '""' in space_2_comma:
            space_2_comma = space_2_comma.replace('""', '"')

        # may have more than one comma, replace repeat comma to single comma
        comma_2_chunks = space_2_comma
        while (",," in comma_2_chunks):
            comma_2_chunks = comma_2_chunks.replace(",,", ",")

        # make it into chunks in list
        chunks = comma_2_chunks.split(",")
        # remove all the empty string
        while ("" in chunks):
            chunks.pop(chunks.index(""))

        pop_word_list = []
        temp = ""
        start_word_index, end_word_index = 0, 0
        isExactWord = False
        for i in range(0, len(chunks)):
            word = chunks[i]
            if (word[0] == '"' and word[-1] != '"'):
                isExactWord = True
                start_word_index = i

            if (word[0] != '"' and word[-1] == '"'):
                temp = temp + " " + word
                isExactWord = False
                end_word_index = i
                pop_word_list.append({'start':start_word_index, 'end':end_word_index, 'word':temp.strip()})
                temp = ""

            if (isExactWord == True):
                temp = temp + " " +word

        for obj in reversed(pop_word_list):
            start_word_index = obj['start']
            end_word_index = obj['end']
            for i in range(end_word_index,start_word_index-1, -1):
                chunks.pop(i)
            chunks.insert(start_word_index, obj['word'])


        # insert "and" to word and words
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

        # if any "=" sign, format it to a list
        while ("=" in format_chunks):
            index = chunks.index("=")
            # list[first:last], last is not included
            sublist = format_chunks[index-1 : index+2]
            sublist.pop(sublist.index("="))
            for i in range (index-1, index+2):
                format_chunks.pop(index-1)
            format_chunks.insert(index-1, sublist)

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
                        if (word != "and" and word != "or"):
                            sublist = [field, word]
                            split_chunk.append(sublist)
                        else:
                            split_chunk.append(word)
                    record = {'split_chunk':split_chunk, 'index':index}
                    add_list.append(record)
            index += 1

        for obj in reversed(add_list):
            format_chunks.pop(obj.get('index'))
            for chunk in reversed(obj.get('split_chunk')):
                format_chunks.insert(obj.get('index'), chunk)

        # create the search_method_list
        search_line = []
        search_method_list = []
        for word in format_chunks:
            if (word == "(" or word == ")" or word == "and" or word == "or"):
                search_line.append(word)
            else:
                if (type(word) is list):
                    check_word = word[1]
                    if (check_word[0] == '"' and check_word[-1] == '"'):
                        search_method_list.append(Search_Method.EXACT)
                        check_word = check_word[1:len(check_word)-1]
                    else:
                        search_method_list.append(Search_Method.RELATE)
                    search_line.append(Search_Pair(compare_field=word[0], keyword=check_word))
                else:
                    check_word = word
                    if (check_word[0] == '"' and check_word[-1] == '"'):
                        search_method_list.append(Search_Method.EXACT)
                        check_word = check_word[1:len(check_word)-1]
                    else:
                        search_method_list.append(Search_Method.RELATE)
                    search_line.append(Search_Pair(compare_field="title",keyword=check_word))

        return {'search_line':search_line, 'search_method_list':search_method_list}

    # add a directory to the file, currently file directory is "files"
    # "\\" should be adjusted to "/" (Cross-platform problem later should deal with it)
    def get_filepath(self, filename):
        return "files" + "/" + filename

    def __del__(self):
        print("Disconnected to the database")


    # this is used to format all the searching input command into
    # => keyword, compare_field, logic, searching rules, order, etc...
    # => Personal i think this is the hardest
'''
    Situations:

    ** not yet "-keywords" : do not contain this word
    ** not yet "3...8" : range from 3 to 8

    done  " "keywords" " : exact keyword
    done  " word0 word2 " : contains word1 and word2
    done  " word1 and word2"
    done  " word1 or word2" : contains word1 or word2
    done " (word1 or word2) and word3 "
'''
