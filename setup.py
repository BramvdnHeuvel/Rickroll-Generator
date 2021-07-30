import sqlite3
import sys

# ---------------------------------------
# Safety lock: make sure they know what they're doing.
# Override by giving -y as an argument.

if '-y' not in sys.argv:
    safety = ''
    
    while safety.lower() != 'y':
        safety = input("WARNING: This will erase the current database! \nDo you want to proceed? [Y/n] ")

        if safety.lower() == 'n':
            exit()


# ---------------------------------------
# Reset the database

with open('links.db', 'w') as open_file:
    pass

conn = sqlite3.connect('links.db')
c = conn.cursor()

c.execute("""CREATE TABLE "links" ( 
    "link" TEXT NOT NULL, 
    "visits" INTEGER NOT NULL DEFAULT 0, 
    "title" TEXT NOT NULL, 
    "description" TEXT, 
    "image" TEXT, 
    PRIMARY KEY("link")
);""")