#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#       Tasks 1.0 - Organize your tasks.
#       
#       Copyright 2011 Dimos Poupos <dimospoupos@gmail.com>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
#       

try:
    import sqlite3
except ImportError:
    exit("Please install sqlite3 module for python to run this program.")

from os.path import *
from os import getenv
from os import system
from os import mkdir

settings = {
    'path' : '%s/.tasks/' % ( getenv('HOME') ),
    'database' : 'tasks.db'
}

def sizeof_db(number):
    """Convert KiloBytes to other unit of measurement."""
    int(number)
    for x in ['bytes','KB','MB','GB','TB']:
        if number < 1024.0:
            return "%3.2f %s" % (number, x)
        number = number / 1024.0
    return '(Error: Not Found!)'

class Database:
    
    """Interaction with the database."""
    
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.db_name = db_name
    
    def create_table(self):
        self.cursor.execute('CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY,\
        task VARCHAR, status INTEGER)')
        self.connection.commit()
    
    def add_task(self):
        text = raw_input("The task: ")
        self.cursor.execute('INSERT INTO tasks VALUES (null, ?, ?)', (text, 0))
        self.connection.commit()
    
    def delete_task(self, task_id):
        command = 'DELETE FROM tasks WHERE id=%d' % (task_id)
        self.cursor.execute(command)
        self.connection.commit()
    
    def edit_task(self, task_id, field, value):
        try:
            int(value)
            command = 'UPDATE tasks SET {0}={1} WHERE id={2}'.format(field, value, task_id)
        except:
            command = "UPDATE tasks SET {0}='{1}' WHERE id={2}".format(field, value, task_id)
        self.cursor.execute(command)
        self.connection.commit()
    
    def all_completed(self):
        self.cursor.execute('SELECT * FROM tasks WHERE status=1')
        for row in self.cursor:
            print "Task %d - %s" % (row[0], row[1])
        return 0
    
    def all_todo(self):
        self.cursor.execute('SELECT * FROM tasks WHERE status=0')
        for row in self.cursor:
            print "Task %d - %s" % (row[0], row[1])
    
    def all_tasks(self):
        self.cursor.execute('SELECT * FROM tasks')
        for row in self.cursor:
            if row[2] == 1:
                status = "completed"
            else:
                status = "uncompleted"
            print "Task %d - %s (%s)" % (row[0], row[1], status )
    
    def tasks_len(self):
        i = 0
        self.cursor.execute('SELECT * FROM tasks')
        for i in self.cursor:
            pass
        try:
            return i[0]
        except TypeError:
            return 0
    
    def db_info(self, all_tasks_len):
        size = sizeof_db(getsize(self.db_name))
        print """All tasks: %d
Database's path: %s
Database file size: %s
        """ % ( all_tasks_len,
                self.db_name,
                size
        )
    
    def close_connection(self):
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

def first_time():
    if not exists(settings['path']) and not exists(settings['path'] + settings['database']):
        mkdir(settings['path'])
        return 1
    else:
        return 0

def check_id(db, task_id):
    if task_id == 'q':
        menu(db)
    try:
        task_id = int(task_id)
        return 0
    except:
        print "Please insert a valid task id."
        return 1

def menu(db):
    system("clear")
    
    actions = {
        '0' : exit_program,
        '1' : add_menu,
        '2' : markc_menu,
        '3' : edit_menu,
        '4' : delete_menu,
        '5' : info_menu,
        '6' : all_menu,
    }
    
    print "--- Todo ---\n"
    if db.tasks_len() == 0:
        print "(There are no tasks!)"
    else:
        db.all_todo()
    print "\n--- Completed ---\n"
    if db.tasks_len() == 0:
        print "(There are no tasks!)"
    else:
        db.all_completed()
    print """\n\
----------------------------------------------------------
| Actions: 1) Add task 2) Mark as completed 3) Edit task |
|          4) Delete task 5) Database info 6) All tasks  |
|          0) Exit                                       |
----------------------------------------------------------
    """
    choice = raw_input("> ")
    while choice not in ['0', '1', '2', '3', '4', '5', '6']:
        print "Please choose a valid action:"
        choice = raw_input("('q' to exit) > ")
        if choice == 'q':
            exit_program(db)
            
    actions[str(choice)](db)

def add_menu(db):
    system("clear")
    print "--- Add task ---"
    db.add_task()
    system("clear")
    print "Task added."
    print "1) Return to main menu 2) Exit program"
    choice = int(raw_input("> "))
    if choice == 1:
        menu(db)
    elif choice == 2:
        exit_program(db)

def markc_menu(db):
    system("clear")
    print "--- Mark as completed ---"
    print "Uncompleted tasks: \n"
    if db.tasks_len() == 0:
        print "There are no tasks!"
    else:
        db.all_todo()
    print ("\nInsert the id of task you want:")
    task_id = int(raw_input("> "))
    while check_id(db, task_id) == 1:
        task_id = raw_input("('q' to exit) > ")
        if task_id != 'q':
            int(task_id)
        elif task_id == 'q':
            exit_program(db)
    db.edit_task(task_id, 'status', 1)
    system("clear")
    print "Task marked as completed."
    print "1) Return to main menu 2) Exit program"
    choice = int(raw_input("> "))
    if choice == 1:
        menu(db)
    elif choice == 2:
        exit_program(db)

def edit_menu(db):
    system("clear")
    print "--- Edit task ---"
    print "All tasks: \n"
    if db.tasks_len() == 0:
        print "(There are no tasks!)"
    else:
        db.all_tasks()
    print ("\nInsert the id of task you want to edit:")
    task_id = int(raw_input("> "))
    while check_id(db, task_id) == 1:
        task_id = raw_input("('q' to exit) > ")
        if task_id != 'q':
            int(task_id)
        elif task_id == 'q':
            exit_program(db)
    system("clear")
    print "Give the text of new task:"
    value = raw_input("> ")
    db.edit_task(task_id, 'task', value)
    system("clear")
    print "Task edited."
    print "1) Return to main menu 2) Exit program"
    choice = int(raw_input("> "))
    if choice == 1:
        menu(db)
    elif choice == 2:
        exit_program(db)

def delete_menu(db):
    system("clear")
    print "--- Delete task ---"
    print "All tasks: \n"
    if db.tasks_len() == 0:
        print "(There are no tasks!)"
    else:
        db.all_tasks()
    print ("\nInsert the id of task you want to delete:")
    task_id = int(raw_input("> "))
    while check_id(db, task_id) == 1:
        task_id = raw_input("('q' to exit) > ")
        if task_id != 'q':
            int(task_id)
        elif task_id == 'q':
            exit_program(db)
    db.delete_task(task_id)
    system("clear")
    print "Task deleted."
    print "1) Return to main menu 2) Exit program"
    choice = int(raw_input("> "))
    if choice == 1:
        menu(db)
    elif choice == 2:
        exit_program(db)

def info_menu(db):
    system("clear")
    print "--- Database's informarions ---\n"
    db.db_info(db.tasks_len())
    raw_input("\nPress <Enter> to return to main menu...")
    menu(db)

def all_menu(db):
    system("clear")
    print "--- All tasks ---\n"
    if db.tasks_len() == 0:
        print "(There are no tasks!)"
    else:
        db.all_tasks()
    raw_input("\nPress <Enter> to return to main menu...")
    menu(db)

def exit_program(db):
    db.close_connection()
    exit(0)

def main():
    if first_time() == 1:
        db = Database(settings['path'] + settings['database'])
        db.create_table()
    else:
        db = Database(settings['path'] + settings['database'])
    menu(db)
    exit(0)

if __name__ == '__main__':
    main()
