import sqlite3

def create_db():
    # Connect to SQLite database (it will create if it doesn't exist)
    conn = sqlite3.connect('HistoryTracking.db')
    
    # Create a cursor object to execute SQL queries
    cursor = conn.cursor()
    
    # Create table if it doesn't exist already
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Details (
        sno INTEGER PRIMARY KEY AUTOINCREMENT,
        title_of_query TEXT NOT NULL,
        time_of_execution TEXT NOT NULL
    )
    ''')
    
    # Commit changes and close the connection
    conn.commit()
    conn.close()
    print("Database and table created successfully!")

# Call the function to create the database and table
create_db()
