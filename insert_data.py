import sqlite3
from datetime import datetime

def insert_query_data(query_title):
    # Get the current time when the query was executed
    execution_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Connect to the SQLite database
    conn = sqlite3.connect('HistoryTracking.db')
    cursor = conn.cursor()
    
    # Insert data into the Details table
    cursor.execute('''
    INSERT INTO Details (title_of_query, time_of_execution)
    VALUES (?, ?)
    ''', (query_title, execution_time))
    
    # Commit changes and close the connection
    conn.commit()
    conn.close()
    print(f"Query '{query_title}' inserted into the database at {execution_time}")
