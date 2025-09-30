import sqlite3

# Connect to SQLite database (creates file if it doesn't exist)
conn = sqlite3.connect('bloodbank.db')
c = conn.cursor()

# Create table for appointments
c.execute('''
CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullName TEXT NOT NULL,
    age INTEGER NOT NULL,
    bloodGroup TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT NOT NULL,
    appointmentDate TEXT NOT NULL,
    comments TEXT
)
''')

conn.commit()
conn.close()
print("Database and table ready!")
