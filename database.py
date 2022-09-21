import sqlite3

# Connect to database
connection_object = sqlite3.connect('test.db')
cursor_object = connection_object.cursor()

# Create table
cursor_object.execute('''
    CREATE TABLE IF NOT EXISTS urls
    (
        short_url TEXT PRIMARY KEY NOT NULL,
        long_url TEXT NOT NULL
    );
    ''')
cursor_object.execute('''
    CREATE UNIQUE INDEX idx_long_url ON urls (long_url);
    ''')                  
connection_object.commit()

# Close the connection
connection_object.close()