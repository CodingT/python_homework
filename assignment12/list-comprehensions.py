import pandas as pd

df = pd.read_csv("../csv/employees.csv")

# print(df)

employee_names = [f"{row['first_name']} {row['last_name']}" for _, row in df.iterrows()]
print(employee_names)

names_with_e = [name for name in employee_names if "e" in name.lower()]
print(names_with_e)
