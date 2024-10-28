import pymysql

import pymysql

# 데이터베이스 연결 설정
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='class-password',
                             db='classicmodels',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

# (2) CRUD

## 1. SELECT * FROM
def get_customers():    
    cursor = connection.cursor()
        
    sql = "SELECT * FROM customers"
    cursor.execute(sql)

    customers = cursor.fetchone()
    print("customers: ", customers)
    print("customers: ", customers['customerNumber'])
    print("customers: ", customers['customerName'])
    print("customers: ", customers['country'])
    cursor.close()

## 2. INSERT INTO
def add_customer():
    cursor = connection.cursor()
    
    name = 'jaewon'
    family_name = 'kim'
    sql = f"INSERT INTO customers(customerNumber, customerName, contactLastName) VALUES(1005,'{name}','{family_name}')"
    cursor.execute(sql)
    connection.commit()
    cursor.close() 

# add_customer()

## 3. UPDATE INTO
def update_customer():
    cursor = connection.cursor()

    update_name = 'update_jaewon'
    contactLast_name = 'update_kim'
    sql = f"UPDATE customers SET customerName='{update_name}', contactLastName='{contactLast_name}' WHERE customerNumber=1004"
    cursor.execute(sql)
    connection.commit()
    cursor.close()

# update_customer()

## 4. DELETE FROM
def delete_customer():
    cursor = connection.cursor()

    sql = "DELETE FROM customers WHERE customerNumber=1004"
    cursor.execute(sql)
    connection.commit()
    cursor.close()

delete_customer()