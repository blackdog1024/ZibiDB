# -*- coding: utf-8 -*-
import os
import shutil
from ZibiDB.core.table import Table
import pickle
import sys
import pandas as pd

class Database():
    def __init__(self, name):
        self.tables = {}
        self.name = name
        #self.create_dir(self.name)

    # Display all tables
    def display(self):
        for table in self.tables:
            print (table)
    
    # Save the whole database as a binary file
    def save(self):
        database = self.name.replace(';', '').lower()
        _database = sys.argv[0]      
        _database = _database[:-11] + 'database/'

        # If the database directory is exist, pass
        if not os.path.exists(_database):
            os.makedirs(_database)

        # If the database is exist, rewrite
        if os.path.exists(_database + database):
            file = open(_database + database, "wb+")
            pickle.dump(self, file)
            file.close()
            print('PASS: Database %s is saved.' % database)
            return

        # If the database is not exist, create and PASS
        elif not os.path.exists(_database + database):
            file = open(_database + database, "wb+")
            pickle.dump(self, file)
            file.close()
            print('PASS: Database %s is created.' % database)
            return

        else:
            raise Exception('ERROR: Invalid command.')

    def drop_database(self):
        database = self.name.replace(';', '').lower()
        _database = sys.argv[0]      
        _database = _database[:-11] + 'database/'
        # If there is no database, pass
        if not os.path.exists(_database):
            raise Exception('ERROR: No any databases')

        # If the database exists, drop and PASS
        if os.path.exists(_database + database):
            os.remove(_database + database)
            print('PASS: Database %s is dropped.' % database)
            return

        # If the database doesnt exist, ERROR
        elif not os.path.exists(_database + database):
            raise Exception('ERROR: Database %s doesnt exist.' % database)

        else:
            raise Exception('ERROR: Invalid command.')

    # Add new table to dabase
    def add_table(self, attrls, info):
        self.tables[info['name']] = Table(attrls, info)

    # Drop exit table from database
    def drop_table(self, name):
        if name not in self.tables.keys():
            raise Exception("Table %s doesn't exist" % name)
        del self.tables[name]
        print ('Table %s is dropped' % name)

    def join_table(self, table1, table2, attr):
        df1 = pd.DataFrame(table1.data)
        df2 = pd.DataFrame(table2.data)
        info = {'name': '', 'attrs': [], 'primary': '', 'foreign': []}
        df = pd.merge(df1, df2, on=attr)
        attrs = df.columns.tolist()
        table = Table(attrs, info)
        return table

    