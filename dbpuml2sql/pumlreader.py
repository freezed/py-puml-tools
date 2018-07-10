#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------------
# "THE BEER-WARE LICENSE" (Revision 42):
# <martin.groenholdt@gmail.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a beer in return. Martin B. K. Grønholdt
# --------------------------------------------------------------------------------
"""
Name: pumlreader.py
Author: Martin Bo Kristensen Grønholdt.
Since: 2017-08-08

Convert a database diagram written in a subset of PlantUML to SQLite syntax.
"""
from table import Table
import re
import pprint

def lineNormalise(line):
    """
    Utility function to convert string to a known format by:

     * Stripping any whitespaces at the beginning.
     * Converting to lower case.

    :param line: The string to process.
    :return: The processed string.
    """
    # Strip initial whitespaces and lower case the string.
    return (line.lstrip().lower())


def isTable(line):
    """
    Tell if a PlantUML table definition is starting at this line.

    :param line: The line to check.
    :return: True if there is a table definition is starting at this line.
    """
    # Make the string easier to parse.
    line_stripped = lineNormalise(line)

    # Return value.
    ret = False

    # If the line starts with the word table, we have a table definition!
    if line_stripped.startswith('table'):
        ret = True

    # Tell the horrible truth that this code could not find a table.
    return ret


class PUMLReader:
    """
    Class to read, parse, and convert tables from a PlantUML file into SQL
    commands to create them in the database.
    """
    target_keywords = ('class', 'pyk', 'fnk', 'pfk')


    def __init__(self):
        """
        Constructor.
        """
        # All tables en up here.
        self.tables = {}

    def parse(self, lines):
        """
        Parse all lines of a PlantUML file.

        :param lines: The lines in the PlantUML file.
        """
        # Keep count of the current line number.
        i = 0
        # list tables and content
        tables = dict()
        attr_param = list()

        skipped_lines = list()  # DEBUG

        # Loop through all lines.
        for i in range(0, len(lines)):
            line_stripped = lineNormalise(lines[i])
            skip = True

            for keyword in self.target_keywords:

                # Look for keywords at the beginning of the line.
                if line_stripped.startswith(keyword):
                    # print("{} : {}".format(i, line_stripped))  # DEBUG
                    skip = False

                    # Found one, do parse
                    expression = re.search(r'(\w+) (\w+)', line_stripped)
                    if keyword is self.target_keywords[0]:   # class/table
                        # get table name
                        table_name = expression.group(2)

                        # add it in tables if not already in
                        # tables (classes) may be at differant place in a PlantUML file
                        if table_name not in tables:
                            tables[table_name] = list()
                            # print("Table : «{}» ajoutee".format(expression.group(2)))  # DEBUG
                            print("{} : +table «{}»".format(i, table_name))  # DEBUG

                    elif keyword is self.target_keywords[1]:   # primary key
                        # import pdb; pdb.set_trace()
                        # get related table
                        attr_param = (re.sub(r'(pyk\()|\)|,|\n', r' ', line_stripped).strip().split())
                        tables[table_name].extend(attr_param)
                        print("{} :\t«{}» +{}".format(i, table_name, attr_param))  # DEBUG

                    elif keyword is self.target_keywords[2]:   # foreign key
                        # get related table
                        attr_param = (re.sub(r'(fnk\()|\)|,|\n', r' ', line_stripped).strip().split())
                        tables[table_name].extend(attr_param)
                        print("{} :\t«{}» +{}".format(i, table_name, attr_param))  # DEBUG


                    elif keyword is self. target_keywords[3]:   # primary foreign key
                        # get related table
                        attr_param = (re.sub(r'(pfk\()|\)|,|\n', r' ', line_stripped).strip().split())
                        tables[table_name].extend(attr_param)
                        print("{} :\t«{}» +{}".format(i, table_name, attr_param))  # DEBUG

                    else:   # attribute
                        # print(line_stripped)  # DEBUG
                        print("{} : \t«{}» Attribute? {}".format(i, line_stripped))  # DEBUG

            if skip:
                skipped_lines.append(i)

        print("\nNumbers of tables : {}\n".format(len(tables)))
        pp = pprint.PrettyPrinter(indent=4, compact=True)
        print("Scraped data:")
        pp.pprint(tables)  # DEBUG
        print("\nSkipped lines: {}\n".format(skipped_lines))  # DEBUG


    def sql(self):
        """
        Return the SQL command to create the tables.

        :return: SQL command string.
        """
        # Return value.
        ret = ''

        # Variables for figuring out dependencies between tables.
        done = []
        dependencies = {}

        # Run through all tables.
        for table in self.tables.values():
            # Assume no references.
            reference = False

            # Check fields for foreign keys.
            for field in table.fields.values():
                if field['foreign'] is not False:
                    # Add the reference to the dependencies of the table.
                    if table.name not in dependencies.keys():
                        dependencies[table.name] = []
                    dependencies[table.name].append(
                        field['foreign'].split('.')[0])
                    reference = True

            # If the table has no dependencies, just print it.
            if not reference:
                ret += '\n' + table.sql()
                done.append(table.name)

        # Solve dependencies.
        while (len(dependencies) > 0):
            # Run through all dependencies.
            for table, deplist in dependencies.items():
                # Check is some has been solved since the last run.
                for solved in done:
                    if solved in deplist:
                        # Bingo. Remove it.
                        deplist.remove(solved)
                # If there are no more dependencies
                if len(deplist) == 0:
                    # Add thw SQL to the return value,
                    ret += '\n' + self.tables[table].sql()
                    # Add the table name to the solved list.
                    done.append(table)

            # Remove all tables that have had its dependencies solved.
            for solved in done:
                if solved in dependencies.keys():
                    del dependencies[solved]

        return ret
