import csv
import os
import subprocess
from datetime import datetime

#Task 2

def read_employees():
    employees = {}
    rows = []
    try:
        with open('../csv/employees.csv', 'r') as file:
            reader = csv.reader(file)
            header = next(reader) #
            employees['fields'] = header
            for row in reader:
                rows.append(row)
                    
            employees['rows'] = rows
            
        return employees
                       
    except Exception as e:
        print(f"An exception occurred.", {e})



employees = read_employees()
#print(employees)
#print(employees.keys() )
#print(type(employees))


#Task 3
def column_index(field):
  return employees["fields"].index(field)

employee_id_column = column_index('employee_id')


#Task 4
def first_name(row_number):
  col_index = column_index('first_name')
  return employees['rows'][row_number][col_index]

#print(first_name(3))

#Task 5
def employee_find(employee_id):
    def employee_match(row):
        return int(row[employee_id_column]) == employee_id

    matches=list(filter(employee_match, employees["rows"]))
    return matches


#print(employee_find(3))


#Task 6
def employee_find_2(employee_id):
   matches = list(filter(lambda row : int(row[employee_id_column]) == employee_id , employees["rows"]))
   return matches


#Task 7
def sort_by_last_name():
  last_name_index = column_index('last_name')
    
  employees['rows'].sort(key=lambda row: row[last_name_index])

  return employees['rows']


#Task 8
def employee_dict(row):
    employeeDict = {}
    for _ in range(1, len(employees['fields'])): #excluding employe_id
        field = employees['fields'][_]
        value = row[_]
        
        employeeDict[field] = value
    
    return employeeDict

row = employees['rows'][3]
employeeDict = employee_dict(row)
print(employeeDict)


# Task 9
def all_employees_dict():
    all_employeesDict = {}
    employee_id_index = column_index('employee_id')

    for row in employees['rows']:
        employee_id = row[employee_id_index]
        employee = employee_dict(row)
        
        all_employeesDict[employee_id] = employee
    
    return all_employeesDict

#all_employees = all_employees_dict()
#print(all_employees)

#Task 10   

#subprocess.run('export THISVALUE=ABC', shell=True, executable='/bin/zsh')
os.environ['THISVALUE'] = 'ABC'

def get_this_value():
  return os.getenv('THISVALUE')

envValue = get_this_value()
print(envValue)

#Task 11
import custom_module


def set_that_secret(new_secret):
    custom_module.set_secret(new_secret)
    
set_that_secret('******')
print(custom_module.secret)


#Task 12
def csv_to_dict(path):
    with open(path, 'r') as file:
        reader = csv.reader(file)
        fields = next(reader)  # header
        rows = [tuple(row) for row in reader]  # Convert each row to a tuple
    return {'fields': fields, 'rows': rows}

def read_minutes():
    minutes1 = csv_to_dict('../csv/minutes1.csv')
    minutes2 = csv_to_dict('../csv/minutes2.csv')
    return minutes1, minutes2

minutes1, minutes2 = read_minutes()


#Task 13
def create_minutes_set():
    set1 = set(minutes1['rows'])
    set2 = set(minutes2['rows'])
    
    union_set = set1.union(set2) 
    return union_set

minutes_set = create_minutes_set()


#Task 14
def create_minutes_list():
    minutes_list = list(minutes_set)
    
    minutes_list = list(map(lambda x: (x[0], datetime.strptime(x[1], "%B %d, %Y")), minutes_list))
    
    return minutes_list


minutes_list = create_minutes_list()

#print(minutes_list)

#Task 15
def write_sorted_list():
    sorted_list = sorted(minutes_list, key=lambda x: x[1])
    
    converted_list = []
    for item in sorted_list:
        name = item[0]
        date_obj = item[1]
        date_str = date_obj.strftime("%B %d, %Y")
        converted_list.append((name, date_str))
    
    with open('./minutes.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(minutes1['fields'])
        
        for row in converted_list:
            writer.writerow(row)
    
    return converted_list

sorted_converted_list = write_sorted_list()

print("Sorted and Converted List:")
print(sorted_converted_list)