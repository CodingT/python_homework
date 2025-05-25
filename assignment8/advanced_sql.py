import sqlite3

print("SQLite Version: ", sqlite3.sqlite_version)

db_path = "./db/lesson.db"

with sqlite3.connect("../db/lesson.db") as conn:
    print("Database created and connected successfully.")

    cursor = conn.cursor()

    conn.execute("PRAGMA foreign_keys = 1")

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    # Print table names and its records examples
    for table in tables:
        print(table[0])

    print()

    cursor.execute("SELECT * FROM customers LIMIT 3;")
    print("\nCustomers:")
    for row in cursor.fetchall():
        print(row)

    cursor.execute("SELECT * FROM employees LIMIT 3;")
    print("\nEmployees:")
    for row in cursor.fetchall():
        print(row)

    cursor.execute("SELECT * FROM products LIMIT 3;")
    print("\nProducts:")
    for row in cursor.fetchall():
        print(row)

    cursor.execute("SELECT * FROM line_items LIMIT 3;")
    print("\nLine_items:")
    for row in cursor.fetchall():
        print(row)

    cursor.execute("SELECT * FROM orders LIMIT 3;")
    print("\nOrders:")
    for row in cursor.fetchall():
        print(row)

    # TASK 1
    query1 = """
    SELECT o.order_id, SUM(p.price * li.quantity) AS total_price
    FROM orders o
    JOIN line_items li ON o.order_id = li.order_id
    JOIN products p ON li.product_id = p.product_id
    GROUP BY o.order_id
    ORDER BY o.order_id
    LIMIT 5;
    """

    cursor.execute(query1)
    results = cursor.fetchall()

    print("\nTASK 1:")
    for order_id, total_price in results:
        print(f"Order ID: {order_id}, Total Price: ${total_price:.2f}")

    # TASK 2
    query2 = """
    SELECT c.customer_name AS customer_name, AVG(order_totals.total_price) AS average_total_price
    FROM customers c
    LEFT JOIN (
        SELECT o.customer_id AS customer_id_b, SUM(p.price * li.quantity) AS total_price
        FROM orders o
        JOIN line_items li ON o.order_id = li.order_id
        JOIN products p ON li.product_id = p.product_id
        GROUP BY o.customer_id
    ) AS order_totals
    ON c.customer_id = order_totals.customer_id_b
    GROUP BY c.customer_id
    ORDER BY average_total_price DESC;
    """

    cursor.execute(query2)
    results = cursor.fetchall()

    print("\nTASK 2:")
    for customer_name, avg_price in results:
        avg_price = (
            0.00 if avg_price is None else avg_price
        )  # for cuctomers with NO orders
        print(f"Customer: {customer_name}, Average Order Price: ${avg_price:.2f}")

    # TASK 3
    try:
        conn.execute("BEGIN;")

        # customer_id for 'Perez and Sons'
        cursor.execute(
            "SELECT customer_id FROM customers WHERE customer_name = 'Perez and Sons';"
        )
        customer_id = cursor.fetchone()[0]

        # employee_id for 'Miranda Harris'
        cursor.execute(
            "SELECT employee_id FROM employees WHERE first_name = 'Miranda' AND last_name = 'Harris';"
        )
        employee_id = cursor.fetchone()[0]

        # Get 5 least expensive products
        cursor.execute("SELECT product_id FROM products ORDER BY price ASC LIMIT 5;")
        product_ids = [row[0] for row in cursor.fetchall()]

        # Insert the new order and get the order_id
        cursor.execute(
            """
            INSERT INTO orders (customer_id, employee_id, date)
            VALUES (?, ?, date('now'))
            RETURNING order_id;
        """,
            (customer_id, employee_id),
        )
        order_id = cursor.fetchone()[0]

        # Insert line items for the order
        for product_id in product_ids:
            cursor.execute(
                """
                INSERT INTO line_items (order_id, product_id, quantity)
                VALUES (?, ?, ?);
            """,
                (order_id, product_id, 10),
            )

        conn.commit()

        # Verify the line items
        cursor.execute(
            """
            SELECT li.line_item_id, li.quantity, p.product_name
            FROM line_items li
            JOIN products p ON li.product_id = p.product_id
            WHERE li.order_id = ?
            ORDER BY li.line_item_id;
        """,
            (order_id,),
        )
        results = cursor.fetchall()

        print("\nTASK 3:")
        print("Line Items for Order ID:", order_id)
        for line_item_id, quantity, product_name in results:
            print(
                f"Line Item ID: {line_item_id}, Quantity: {quantity}, Product: {product_name}"
            )

    except Exception as e:
        conn.rollback()  # Rollback if error acured
        print(f"Error occurred: {e}")

    # TASK 4
    query4 = """
        SELECT e.first_name, e.last_name, COUNT(o.order_id) AS order_count
        FROM employees e
        JOIN orders o ON e.employee_id = o.employee_id
        GROUP BY e.employee_id
        HAVING COUNT(o.order_id) > 5
        ORDER BY order_count DESC;
    """

    cursor.execute(query4)
    results = cursor.fetchall()

    print("\nTASK 4")
    print("Employees with more than 5 orders:")
    for first_name, last_name, order_count in results:
        print(f"Employee: {first_name} {last_name}, Orders: {order_count}")
