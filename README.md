# ssh-catalog
This is a simple python3 command-line program used to catalog SSH hosts locally using sqlite3 database.

# installation
Download the release, unpack it and then use pip install.

# usage
After installation you can use 'sshcat' in the terminal. It will create a menu with options. Very simple.
Beside a menu, you can use arguments.
-h, --help (You already know this one.)
-s, --show (this will list entries from the database and ask if you want to connect to any of the SSH hosts.)
-a, --add (This is where you add new entries to the database.)
-m, --modify (Modify existing entries in the database.)
-d, --delete (Deleting a single entry or all entries from the database.)
-b, --backup restore|backup (Creates a backup of the database or restores a backup.

# todo list
* [ ] - Implement sqlite3 database encryption using sqlcipher and pysqlcipher3. 
* [X] - Implement command line arguments.
* [X] - Implement database backup management.
* [ ] - Implement SSH Keys management.
