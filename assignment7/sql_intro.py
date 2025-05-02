import sqlite3

try:
    with  sqlite3.connect("../db/magazines.db") as conn: 
        print("Database created and connected successfully.")
        
        conn.execute("PRAGMA foreign_keys = 1")
        
        cursor = conn.cursor()
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS publishers (
            publisher_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE 
        )
        """)
        
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS magazines (
            magazine_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            publisher_id INTEGER NOT NULL,
            FOREIGN KEY (publisher_id) REFERENCES publishers(publisher_id)
        )
        """)
        
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS subscribers (
            subscriber_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT NOT NULL
        )
        """)
        
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS subscriptions (
            subscription_id INTEGER PRIMARY KEY AUTOINCREMENT,
            subscriber_id INTEGER NOT NULL,
            magazine_id INTEGER NOT NULL,
            expiration_date TEXT NOT NULL,
            FOREIGN KEY (subscriber_id) REFERENCES subscribers(subscriber_id),
            FOREIGN KEY (magazine_id) REFERENCES magazines(magazine_id),
            UNIQUE(subscriber_id, magazine_id)  -- Prevent duplicate subscriptions
        )
        """)
        
        print("Tables created successfully.")      
        
        
except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        
        
def add_publisher(cursor, name):
    try:
        cursor.execute("INSERT INTO publishers (name) VALUES (?)", (name,))
    except sqlite3.IntegrityError:
        print(f"{name} is already in the database.")    
        
        
def add_magazine(cursor, name: str, publisher_id):
    try:
       cursor.execute("INSERT INTO magazines (name, publisher_id) VALUES (?,?)", 
                      (name, publisher_id))
    except sqlite3.IntegrityError as e:
        if "FOREIGN KEY" in str(e):
            print(f"Publisher ID {publisher_id} doesn't exist.")
        else:
            print(f"Magazine '{name}' already exists.")
 
            
def add_subscriber(cursor, name, address):
    try:
        # First check if this exact name+address combination already exists
        cursor.execute("""
            SELECT subscriber_id 
            FROM subscribers 
            WHERE name = ? AND address = ?
        """, (name, address))
        
        if cursor.fetchone():
            print(f"Subscriber '{name}' at address '{address}' already exists.")
            return False
        
        # If not found, insert the new subscriber
        cursor.execute("""
            INSERT INTO subscribers (name, address) 
            VALUES (?, ?)
        """, (name, address))
        return True
        
    except sqlite3.Error as e:
        print(f"Error adding subscriber: {e}")
        return False
        


def add_subscription(cursor, subscriber_id, magazine_id, expiration_date):
    try:
        cursor.execute("""INSERT INTO subscriptions 
                          (subscriber_id, magazine_id, expiration_date) 
                          VALUES (?,?,?)""", 
                       (subscriber_id, magazine_id, expiration_date))
    except sqlite3.IntegrityError as e:
        if "subscriber_id" in str(e):
            print(f"Subscriber ID {subscriber_id} doesn't exist.")
        elif "magazine_id" in str(e):
            print(f"Magazine ID {magazine_id} doesn't exist.")
        else:
            print(f"Subscription already exists for subscriber {subscriber_id} and magazine {magazine_id}.")



with sqlite3.connect("../db/magazines.db") as conn:
    conn.execute("PRAGMA foreign_keys = 1")  # Enable foreign key constraints
    cursor = conn.cursor()

    # Insert sample data
    add_publisher(cursor, "Vogue")
    add_publisher(cursor, "Science Monthly")
    add_publisher(cursor, "People")
    
    add_magazine(cursor, "Python Weekly", 1)
    add_magazine(cursor, "Economist", 4)
    add_magazine(cursor, "Review Now", 3)
    
    add_subscriber(cursor, "Johnson Smith", "123 Mason St")
    add_subscriber(cursor, "Bob Johnson", "456 Oak AveDrive")
    add_subscriber(cursor, "Charlie Shin", "7824 Pine Rd")
    
    add_subscription(cursor, 1, 3, "2026-12-31")
    add_subscription(cursor, 1, 2, "2026-06-30")
    add_subscription(cursor, 2, 4, "2026-01-15")
    add_subscription(cursor, 3, 3, "2025-09-30")

    conn.commit()
    print("Sample magazine data inserted successfully.")
    
    
    
    
    cursor.execute("SELECT * FROM publishers WHERE name = 'Science Monthly'")
    result = cursor.fetchall()
    for row in result:
        print(row)
        
        


with sqlite3.connect("../db/magazines.db") as conn:
    cursor = conn.cursor()
    
    # 1. Get all subscribers
    cursor.execute("SELECT * FROM subscribers")
    print("\nAll Subscribers:")
    for row in cursor.fetchall():
        print(row)
    
    # 2. Get all magazines sorted by name
    cursor.execute("SELECT * FROM magazines ORDER BY name")
    print("\nMagazines Sorted by Name:")
    for row in cursor.fetchall():
        print(row)
    
    # 3. Get magazines for specific publisher
    cursor.execute("""
        SELECT magazines.magazine_id, magazines.name 
        FROM magazines
        JOIN publishers ON magazines.publisher_id = publishers.publisher_id
        WHERE publishers.name = 'Tech Publications'
    """)
    print("\nMagazines by Tech Publications:")
    result = cursor.fetchall()
    for row in result:
        print(row)