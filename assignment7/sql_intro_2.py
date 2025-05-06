import sqlite3

import pandas as pd

with sqlite3.connect("../db/lesson.db") as conn:
    sql_statement = """SELECT c.customer_name, o.order_id, p.product_name
    FROM customers c JOIN orders o ON c.customer_id = o.customer_id 
    JOIN line_items li ON o.order_id = li.order_id JOIN products p ON li.product_id = p.product_id;"""
    df = pd.read_sql_query(sql_statement, conn)
    #print(df)
    

with sqlite3.connect("../db/lesson.db") as conn:
    df = pd.read_sql_query("""
        SELECT 
            li.line_item_id,
            li.quantity,
            li.product_id,
            p.product_name,
            p.price
        FROM line_items li
        JOIN products p ON li.product_id = p.product_id
    """, conn)
    
    df['total'] = df['quantity'] * df['price']
    
    print(df.head())
    
    # Group by product_id and aggregate
    product_stats = df.groupby('product_id').agg({
        'line_item_id': 'count',  # Count of orders per product
        'total': 'sum',           # Sum of revenue per product
        'product_name': 'first'   # Get the product name
    }).reset_index()
    
  
    product_stats = product_stats.sort_values('product_name')
    
    print(product_stats.head(5))
    
    product_stats.to_csv('order_summary.csv', index=False)