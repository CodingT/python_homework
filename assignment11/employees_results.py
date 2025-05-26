import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

#TASK 1

db_path = "./db/lesson.db"

with sqlite3.connect("../db/lesson.db") as conn:
    print("Database created and connected successfully.")

    cursor = conn.cursor()

    # conn.execute("PRAGMA foreign_keys = 1")

    query = """
    SELECT last_name, SUM(price * quantity) AS revenue
    FROM employees e 
    JOIN orders o ON e.employee_id = o.employee_id 
    JOIN line_items l ON o.order_id = l.order_id 
    JOIN products p ON l.product_id = p.product_id 
    GROUP BY e.employee_id;
    """

    # cursor.execute(query)
    # results = cursor.fetchall()

    # print("\nEmployee Results: ")
    # for last_name, revenue in results:
    #     print(f"Last Name: {last_name}; Revenue: ${revenue:.2f}")
    
    df = pd.read_sql_query(query, conn)
    
    
    
# Sort by revenue for better visualization
df.sort_values("revenue", ascending=False, inplace=True)


plt.figure(figsize=(12, 6))
bars = plt.bar(df["last_name"], df["revenue"], color='skyblue')
plt.title("Revenue by Employee", fontsize=12)
plt.xlabel("Employee Last Name", fontsize=12)
plt.ylabel("Revenue ($)", fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

plt.show()
