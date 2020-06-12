#!/usr/bin/env python3

import sqlite3
import os
from os.path import expanduser
import argparse
import shutil

def gatherinfo():
    global dirpath, dbpath, homepath
    dirpath = os.path.dirname(os.path.abspath(__file__))
    dbpath = (dirpath + '/catalog.db')
    homepath = os.path.expanduser("~")

def connectdb():
    global conn, cursor
    #dirpath = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(dirpath + '/catalog.db')
    cursor = conn.cursor()

def backupdb(bor):
    if bor == "backup":
        shutil.copy(dbpath, homepath)
        print("database has been backed up to -> " + homepath + "/catalog.db")
    elif bor == "restore":
        print("Restoring the database from your homefolder. Make sure it's there and named 'catalog.db'")
        print("If you are sure, type yes. if not, move it there before continuing.")
        question = input ("Are you sure?: ")
        if question == "yes":
            shutil.copy(homepath + "/catalog.db", dirpath)
        else:
            print("Invalid input. Aborting database restore.")
    else:
        print("Use either -b, --backup restore|backup")

def showhosts():
    os.system('clear')
    sqlite_select_query = """SELECT * from CONNECTIONS"""
    cursor.execute(sqlite_select_query)
    data = cursor.fetchall()
    print("SSH Catalog contains: ", len(data), " records")
    print("\n")
    for row in data:
        print("ID: ", row[0])
        print("NAME: ", row[1])
        print("IP: ", row[2])
        print("PORT: ", row[3])
        print("USERNAME: ", row[4])
        print("PASSWORD: ", row[5])
        print("\n")
                
    #Search for ID and connecto to host    
    selectid = input ("Type ID of host to create a SSH Session: ")
    sqlite_search_query = """SELECT * from CONNECTIONS where ID like (?)"""
    cursor.execute(sqlite_search_query, selectid)
    result = cursor.fetchall()
    for row in result:
        id = row[0]
        name = row[1]
        ip = row[2]
        port = row[3]
        username = row[4]
        password = row[5]
    cursor.close
    #Connect to SSH host.
    os.system("ssh " + (ip) + " -l " + (username))


def addhost():
    print("Add a new SSH connection to the catalog")
    addname = input ("Name: ")
    addip = input ("IP Address: ")
    addport = input ("Port: ")
    addusername = input ("Username: ")
    addpassword = input ("Password: ")
    cursor.execute("INSERT INTO CONNECTIONS (ID,NAME,IP,PORT,USERNAME,PASSWORD) VALUES (null, ?, ?, ?, ?, ?)", (addname, addip, addport, addusername, addpassword ))
    conn.commit()
    cursor.close()

def modifyhost():
    print("Type the ID of a host you want to modify.")
    modifyid = input ("ID: ")
    sqlite_search_query = """SELECT * from CONNECTIONS where ID like (?)"""
    cursor.execute(sqlite_search_query, modifyid)
    result = cursor.fetchall()
    for row in result:
        id = row[0]
        name = row[1]
        ip = row[2]
        port = row[3]
        username = row[4]
        password = row[5]
    print("Old name: " + name)
    print("Old IP: " + ip)
    print("Old port: " + port)
    print("Old username: " + username)
    print("Old password: " + password)
    print("\n")
    modifyname = input ("Name: ")
    modifyip = input ("IP Address: ")
    modifyport = input ("Port: ")
    modifyusername = input ("Username: ")
    modifypassword = input ("Password: ")
    cursor.execute("UPDATE CONNECTIONS SET NAME=?, IP=?, PORT=?, USERNAME=?, PASSWORD=? WHERE ID=?", (modifyname, modifyip, modifyport, modifyusername, modifypassword, modifyid))
    conn.commit()
    cursor.close()

def deletehost():
    print("Type the ID of a host you want to remove from the catalog.")
    print("If you want to delete all entries in the catalog, type 'ALL' instead.")
    deleteid = input ("ID: ")
    if deleteid == ("ALL"):
        cursor.execute("DELETE FROM CONNECTIONS")
        conn.commit()
        cursor.execute("UPDATE sqlite_sequence SET seq=0 WHERE name='CONNECTIONS'")
        print("Deleted all entries in the database.")
        conn.commit()
        cursor.close()
    else:
        cursor.execute("DELETE FROM CONNECTIONS WHERE id = (?)", (deleteid))
        conn.commit()
        cursor.close()

def main():
    gatherinfo()
    connectdb()
    parser = argparse.ArgumentParser(description='List of argument options', add_help=True, allow_abbrev=False)
    parser.add_argument('-s', '--show', dest='show', action='store_true', help='Show all entries in the catalog and connect.')
    parser.add_argument('-a', '--add', dest='add', action='store_true', help='Add a new host to the catalog.')
    parser.add_argument('-m', '--modify', dest='modify', action='store_true', help='Modify an entry in the catalog')
    parser.add_argument('-d', '--delete', dest='delete', action='store_true', help='Delete an entry in the catalog')
    parser.add_argument('-b', '--backup', dest='backup', action='store', type=str, help='Create or restore a backup of the current database.')
    args = parser.parse_args()

    if args.show:
        showhosts()
    elif args.add:
        addhost()
    elif args.modify:
        modifyhost()
    elif args.delete:
        deletehost()
    elif args.backup:
        backupdb(bor=args.backup)
    else:
        #main menu
        choice ='0'
        while choice =='0':
            print("SSH Catalog - 1.0")
            print("1. Show connections")
            print("2. Add new connection")
            print("3. Modify existing connection")
            print("4. Delete host from catalog")

            choice = input ("Please make a choice: ")

            if choice == "1":
                showhosts()
            elif choice == "2":
                addhost()
            elif choice == "3":
                modifyhost()
            elif choice == "4":
                deletehost()
            else:
                print("Choice does not exist. Better luck next time!")
                cursor.close()
if __name__ == '__main__':
    main()
