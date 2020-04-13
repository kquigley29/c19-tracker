import csv, sqlite3


def upload_to_db(database, table_name, csv_file_name):
    connection_ = sqlite3.connect(database)
    cursor_ = connection_.cursor()
    cursor_.execute("CREATE TABLE " + table_name + " (col1, col2);") # use your column names here

    with open(csv_file_name,'rb') as fin: # `with` statement available in 2.5+
        # csv.DictReader uses first line in file for column headings by default
        dr = csv.DictReader(fin) # comma is default delimiter
        to_db = [(i['col1'], i['col2']) for i in dr]

    cur.executemany("INSERT INTO t (col1, col2) VALUES (?, ?);", to_db)
    con.commit()
    con.close()


upload_to_db('tracker.db', 'treatments')