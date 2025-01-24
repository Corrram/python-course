import sqlite3

def get_customers(db_path="../../../music.db"):
    """
    Connects to the SQLite database at 'db_path' and reads
    from the 'customers' table. The table has columns:
    FirstName, LastName, Email.

    Returns a list of dictionaries with the keys:
    'FirstName', 'LastName', and 'Email'.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Query the 'customers' table
    cursor.execute("SELECT FirstName, LastName, Email FROM customers")
    rows = cursor.fetchall()

    conn.close()

    # Convert each row to a dictionary
    customers = []
    for row in rows:
        customers.append({
            "FirstName": row[0],
            "LastName": row[1],
            "Email": row[2]
        })
    return customers

if __name__ == '__main__':
    customers = get_customers("../../../music.db")
    for customer in customers:
        print(customer)