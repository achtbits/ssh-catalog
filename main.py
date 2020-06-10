#!/usr/bin/env python3

import sqlite3
import os

def connectdb():
    global conn, cursor
    conn = sqlite3.connect('catalog.db')
    cursor = conn.cursor()

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

#Modify host

def deletehost():
    print("Type the ID of a host you want to remove from the catalog.")
    print("If you want to delete all entries in the catalog, type 'ALL' instead.")
    deleteid = input ("ID: ")
    if deleteid == ("ALL"):
        cursor.execute("DELETE FROM CONNECTIONS")
        conn.commit
        cursor.close
    else:
        cursor.execute("DELETE FROM CONNECTIONS WHERE id = (?)", (deleteid))
        conn.commit()
        cursor.close()

def main():
    connectdb()


    choice ='0'
    while choice =='0':
        #Main menu.
        print("SSH Catalog - 1.0")
        print("1. Show connections") # Show hosts in the catalog and connect to selected host.
        print("2. Add new connection") # Add new host to the catalog.
        print("3. Modify existing connection") # Modify existing host.
        print("4. Delete host from catalog") # Delete host from the catalog.

        choice = input ("Please make a choice: ")

        if choice == "1":
            showhosts()
        elif choice == "2":
            addhost()
        elif choice == "3":
            print("Test 3------------------")
        elif choice == "4":
            deletehost()

        else:
            print("Choice does not exist. Better luck next time!")


main()
