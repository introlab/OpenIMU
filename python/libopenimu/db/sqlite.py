'''
 Will contain sqlite driver
'''
import sqlite3
import os
import time


def create_database(filename, name='Unnamed', description='No description available', author='Anonymous'):
    print('creating database : ', filename)

    # Delete the old table
    if os.path.isfile(filename):
        os.remove(filename)

    conn = sqlite3.connect(filename)

    # Create the tables
    qry = open('schema_v1.sql', 'r').read()
    sqlite3.complete_statement(qry)
    conn = sqlite3.connect(filename)
    cursor = conn.cursor()

    try:
        cursor.executescript(qry)
    except Exception as e:
        message = filename + ': ' + str(e)
        print('Error: ', message)
        cursor.close()
        raise


    # Fill some base fields
    try:

        # tabInfos -> file_version (float)
        conn.execute("INSERT INTO tabInfos (file_version) VALUES (1.0)")

        # Get current unix time
        creation_date = time.time()

        # tabDataSet -> name, desc, creation_date, upload_date, author
        conn.execute("INSERT INTO tabDataSet (name, desc, creation_date, upload_date, author) "
                     "VALUES (?,?,?,?,?)", [name, description, creation_date, 0, author])

        conn.commit()

    except Exception as e:
        message = filename + ': ' + str(e)
        print('Insert Error: ', message)

    return conn

"""
Test function
"""
if __name__ == '__main__':
    db = create_database('openimu.db')
    db.commit()
    db.close()