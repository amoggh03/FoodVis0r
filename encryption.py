import sqlite3
from cryptography.fernet import Fernet

# Generate a key for encryption
key = Fernet.generate_key()
cipher = Fernet(key)

# Encrypt a value
def encrypt_value(value):
    return cipher.encrypt(value.encode())

# Decrypt a value
def decrypt_value(encrypted_value):
    return cipher.decrypt(encrypted_value).decode()

# Connect to SQLite database
conn = sqlite3.connect('my_encrypted_database.db')
cursor = conn.cursor()

# Create table dynamically based on user_database
for column_name, values in user_database.items():
    cursor.execute(f'CREATE TABLE IF NOT EXISTS {column_name} (value BLOB)')  # Use BLOB for binary data

    # Encrypt and insert values into the table
    for value in values:
        encrypted_value = encrypt_value(value)
        cursor.execute(f'INSERT INTO {column_name} (value) VALUES (?)', (encrypted_value,))

# Commit changes
conn.commit()

# Get a list of tables in the database
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Display tables and their encrypted contents
for table in tables:
    table_name = table[0]
    print(f"Table: {table_name}")
    
    # Fetch rows from the table
    cursor.execute(f"SELECT * FROM {table_name};")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

# Close connection
conn.close()