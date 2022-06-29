#
import json
import uuid
import datetime
import csv

def dbloader(db,filename):
    # open the file for reading
    f = open(filename, "r")
    while True:
        # read a single line
        line = f.readline()
        line = line.rstrip()
        if not line:
            break
        if line[0] == "@":
            junk, dbname = line.split('-')
            line = f.readline()
            line = line.rstrip()
        process = process_line(db,dbname,line)
    # close the pointer to that file
    f.close()
    message = "database has been loaded"
    return render_template('message.html', message=message)



    return
