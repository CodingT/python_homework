import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

#TASK 2

db_path = "./db/lesson.db"

with sqlite3.connect("../db/lesson.db") as conn:
    print("Database created and connected successfully.")

    cursor = conn.cursor()

    # conn.execute("PRAGMA foreign_keys = 1")

    query = """
    SELECT o.order_id, SUM(p.price * li.quantity) AS total_price
    FROM orders o
    JOIN line_items li ON o.order_id = li.order_id
    JOIN products p ON li.product_id = p.product_id
    GROUP BY o.order_id
    ORDER BY o.order_id;
    """

    
    df = pd.read_sql_query(query, conn)


def cumulative(row):
   totals_above = df['total_price'][0:row.name+1]
   return totals_above.sum()

df['cumulative'] = df.apply(cumulative, axis=1)
df['cumulative'] = df['total_price'].cumsum()

print(df.head())

df.plot(x='order_id', y='cumulative', kind='line', marker='o')

plt.title("Cumulative Revenue by Order ID")
plt.xlabel("Order ID")
plt.ylabel("Cumulative Revenue")
plt.grid(True)
plt.tight_layout()

plt.show()
