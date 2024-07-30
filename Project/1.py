import mysql.connector
import pandas as pd
from mysql.connector import Error 
import random

try:
    connection = mysql.connector.connect(host = "localhost", user = "root", passwd = "Hero1234..", database = "online_retail_store")
except:
    print("Error in connecting to databse\n")

cursor = connection.cursor(buffered=True)

def execute_query(Query):
    try:
        cursor.execute(Query)
        connection.commit()
        return 1
    except Error as err:
        print(err)
        return 0
choice = 0


def app():
    choice = 0
    while True:
        print("*** Welcome to S-Mart ***")
        print("1) Enter as Employee")
        print("2) Enter as Customer")
        print("3) Enter as Supplier")
        print("4) Enter as Delivery Driver")
        print("5) Transactions")
        print("6) Triggers")
        print("7) Queries")
        print("8) Quit")

        choice = int(input("Enter your selection: "))

        if choice==1:
            employee_interface()
        if choice==2: 
            customer_interface()
        if choice==3:
            supplier_interface()
        if choice==4: 
            deliverydriver_interface()
        if choice == 5:
            transaction()
        if choice == 6:
            trigger()
        if choice == 7:
            Queries()
        if choice==8: 
            break

def transaction():
    transaction_new1 = """START TRANSACTION;

    SELECT * FROM customer WHERE Customer_ID=2;
    UPDATE customer SET email = 'WeeWee@Gmail.com' WHERE Customer_ID=2;
    COMMIT;
    """
    transaction_new2 = """START TRANSACTION;

    SELECT Full_Name FROM customer WHERE Customer_ID=2;

    COMMIT;"""
    transaction_new3 = """START TRANSACTION;

    SELECT * FROM customer WHERE Customer_ID=2;
    UPDATE customer SET email = 'JKRowling@Gmail.com' WHERE Customer_ID=2;

    COMMIT;"""
    z = 0
    while z!=4:
        try:
            connection = mysql.connector.connect(host = "localhost", user = "root", passwd = "Hero1234..", database = "online_retail_store")
        except:
            print("Error in connecting to databse\n")

        cursor = connection.cursor(buffered=True)
        print("1) Transaction 1")
        print("2) Transaction 2")
        print("3) Transaction 3")
        print("4) Back\n")
        z = int(input("Enter you selection: "))
        if z == 1:
            print(transaction_new1)
            
            print("\n")
            try:
                cursor.execute("START TRANSACTION;")
                cursor.execute("SELECT * FROM customer WHERE Customer_ID=2;")
                result1 = cursor.fetchall()
                cursor.execute("UPDATE customer SET email = 'WeeWee@Gmail.com' WHERE Customer_ID=2;")
                cursor.execute("SELECT * FROM customer WHERE Customer_ID=2;")
                result2 = cursor.fetchall()
                cursor.execute("COMMIT;")
                connection.commit()
                
                panda1 = []
                panda2 = []
                for i in result1:
                    i = list(i)
                    panda1.append(i)

                columns = ["Customer_ID", "Full_Name", "Email","Customer_Password","Address"]
                df1 = pd.DataFrame(panda1, columns=columns)

                print(df1)
                print("AFTER UPATE\n")
                for i in result2:
                    i = list(i)
                    panda2.append(i)

                columns = ["Customer_ID", "Full_Name", "Email","Customer_Password","Address"]
                df2 = pd.DataFrame(panda2, columns=columns)

                print(df2)
                print("\n")
                print("Transaction1 was successful\n")
            except Error as err:
                print(err)
                connection.rollback()
        elif z == 2:
            print(transaction_new2)
            print("\n")
            try:
                cursor.execute("START TRANSACTION;")
                cursor.execute("SELECT Full_Name FROM customer WHERE Customer_ID=2;")
                result = cursor.fetchall()
                cursor.execute("COMMIT;")
                panda1 = []
                for i in result:
                    i = list(i)
                    panda1.append(i)

                columns = ["Full_Name"]
                df1 = pd.DataFrame(panda1, columns=columns)

                print(df1)
                print("\n")
                print("Transaction2 was successful\n")
            except Error as err:
                print(err)
                connection.rollback()
        elif z == 3:
            print(transaction_new3)
            print("\n")
            try:
                cursor.execute("START TRANSACTION;")
                cursor.execute("SELECT * FROM customer WHERE Customer_ID=2;")
                result1 = cursor.fetchall()
                cursor.execute("UPDATE customer SET email = 'JKRowling@Gmail.com' WHERE Customer_ID=2;")
                cursor.execute("SELECT * FROM customer WHERE Customer_ID=2;")
                result2 = cursor.fetchall()
                cursor.execute("COMMIT;")
                connection.commit()
                panda1 = []
                panda2 = []
                for i in result1:
                    i = list(i)
                    panda1.append(i)

                columns = ["Customer_ID", "Full_Name", "Email","Customer_Password","Address"]
                df1 = pd.DataFrame(panda1, columns=columns)

                print(df1)
                print("AFTER UPATE\n")
                for i in result2:
                    i = list(i)
                    panda2.append(i)

                columns = ["Customer_ID", "Full_Name", "Email","Customer_Password","Address"]
                df2 = pd.DataFrame(panda2, columns=columns)

                print(df2)
                print("\n")
                print("Transaction3 was successful\n")
            except Error as err:
                print(err)
                connection.rollback()
        cursor.close()

def trigger():
    cursor = connection.cursor(buffered=True)
    Trigger_1 = """
    CREATE TRIGGER send_shipping_notification AFTER UPDATE ON order_
    FOR EACH ROW
    BEGIN
    DECLARE customer_email VARCHAR(100);
    IF OLD.Order_Status != 'Shipped' AND NEW.Order_Status = 'Shipped' THEN
    SELECT customer.Email INTO customer_email
    FROM customer
    WHERE customer.Customer_ID = NEW.Customer_ID;
    SET @message = CONCAT('Dear Customer, your order with Order ID ', NEW.Order_ID, ' has been shipped!');
    INSERT INTO email_notifications (To_Email, Subject_, Message)
    VALUES (customer_email, 'Order Shipped!', @message);
    END IF;
    END """

    Trigger_2 = """
    CREATE TRIGGER update_payment_amount AFTER UPDATE ON order_
    FOR EACH ROW
    BEGIN
        IF NEW.Order_Status = 'Confirmed' AND OLD.Order_Status != 'Confirmed' THEN
            UPDATE payment
            SET Amount = (SELECT SUM(pr.Price * pr.Cart_Quantity) 
                        FROM product pr
                        JOIN contains_ c ON pr.Product_id = c.Product_ID
                        WHERE c.Order_ID = NEW.Order_ID)
            WHERE Order_ID = NEW.Order_ID;
        END IF;
    END;"""
    z = 0
    while z!=3:
        print("1) Trigger 1: Trigger that sends an email notification to the customer when their order status is updated to 'shipped'.")
        print("2) Trigger 2: Trigger to update the payment amount when an order status is changed to 'Confirmed'.")
        print("3) Back\n")
        z = int(input("Enter you selection: "))
        if z == 1:
            print(Trigger_1)
            print("\n")
            # order_id = 78,79
            try:
                cursor.execute(Trigger_1)
                print("Trigger1 was successful\n")
            except Error as err:
                if 'already exists' in str(err):
                    print("Trigger already exists, continuing execution.\n")
                else:
                    print(f"Error creating trigger: {err}")
            x = int(input("Enter the Order_ID whom Order Status you want to change to Shipped: "))
            Query = f"""UPDATE Order_ SET Order_Status = 'Shipped' WHERE Order_ID = {x}"""
            cursor.execute(Query)
            connection.commit()
            
            Query1 = """SELECT * FROM email_notifications"""
            cursor.execute(Query1)
            result = cursor.fetchall()
                
            panda1 = []
            for i in result:
                i = list(i)
                panda1.append(i)

            columns = ["To_Email", "Subject_", "Message"]
            df1 = pd.DataFrame(panda1, columns=columns)

            print(df1)
            print("\n")
        elif z == 2:
            print(Trigger_2)
            print("\n")
            try:
                cursor.execute(Trigger_2)
                print("Trigger2 was successful\n")
            except Error as err:
                if 'already exists' in str(err):
                    print("Trigger already exists, continuing execution.\n")
                else:
                    print(f"Error creating trigger: {err}")

            x = int(input("Enter the Order_ID whom Order Status you want to change to Confirmed: "))
            Query = f"""UPDATE Order_ SET Order_Status = 'Confirmed' WHERE Order_ID = {x}"""
            cursor.execute(Query)
            connection.commit()
            Query1 = f"""SELECT * FROM Payment WHERE Order_ID = {x}"""
            cursor.execute(Query1)
            result = cursor.fetchall()
            panda1 = []
            for i in result:
                i = list(i)
                panda1.append(i)

            columns = ["Payment_Date", "Order_ID", "Amount", "Payment_Status", "Method"]
            df1 = pd.DataFrame(panda1, columns=columns)

            print(df1)
            print("\n")

def Queries():
    v = 0
    while(v != 3):
        print("1) Normal Queries")
        print("2) OLAP Queries")
        print("3) Back")
        v = int(input("Enter your selection: "))
        if(v == 2):
            OLAP_Query_1 = """
            SELECT p.Product_ID, YEAR(STR_TO_DATE(o.Order_Date, '%d/%m/%Y')) AS Order_Year, SUM(p.cart_quantity * p.price) AS Total_Revenue
            FROM Product p
            JOIN contains_ c ON p.product_id = c.product_id
            JOIN order_ o ON c.order_id = o.order_id
            WHERE o.order_status = 'shipped'
            GROUP BY Order_Year,p.product_id WITH ROLLUP
            ORDER BY p.product_id, Order_Year DESC;"""

            OLAP_Query_2 = """
            SELECT 
            MONTH(STR_TO_DATE(o.Order_Date, '%d/%m/%Y')) AS Month_,
            o.Customer_ID, 
            SUM(p.cart_quantity * p.price) AS Total_Revenue,
            COUNT(distinct o.Order_ID) AS Total_Orders
            FROM 
            order_ o
            JOIN product p ON p.Customer_ID = o.Customer_ID
            GROUP BY 
            Month_, customer_id WITH ROLLUP
            ORDER BY 
            Month_, Customer_ID;"""

            OLAP_Query_3 = """
            SELECT p.Order_ID, SUM(pr.Price * pr.Cart_Quantity) AS Amount, p.Payment_Status, p.Method
            FROM payment p
            JOIN order_ o ON p.Order_ID = o.Order_ID
            JOIN contains_ c ON o.Order_ID = c.Order_ID
            JOIN product pr ON c.Product_ID = pr.Product_id
            GROUP BY p.Payment_Status, p.Method, p.Order_ID WITH ROLLUP;"""

            OLAP_Query_4 = """
            SELECT c.Full_Name, SUM(p.Price * p.Cart_Quantity) as Total
            FROM customer c
            INNER JOIN order_ o ON c.Customer_ID = o.Customer_ID
            INNER JOIN contains_ co ON o.Order_ID = co.Order_ID
            INNER JOIN product p ON co.Product_ID = p.Product_id
            INNER JOIN supplies s ON p.Product_id = s.Product_ID
            INNER JOIN supplier su ON s.Supplier_ID = su.Supplier_ID
            INNER JOIN payment pm ON o.Order_ID = pm.Order_ID
            WHERE su.Supplier_ID = 1 AND pm.Method = "Credit Card"
            GROUP BY c.Customer_ID ;"""

            y = 0
            while y!=5:
                print("1) Calculate total revenue generated by each product in each year and also for all years")
                print("2) Revenue generated each month with total orders in that particular month wrt particular customer")
                print("3) Payment Amount Rollup by Method and Status, Including Subtotal and Grand Total")
                print("4) Find the total of each customer who has purchased products supplied by a supplier with the ID 1 and paid using the method 'Credit Card'")
                print("5) Back\n")
                y = int(input("Enter you selection: "))
                if y == 1:
                    print(OLAP_Query_1)
                    print("\n")
                    try:
                        cursor.execute(OLAP_Query_1)
                        result = cursor.fetchall()
                        print("Query1 was successful\n")
                    except:
                        print("Error")

                    panda1 = []
                    for i in result:
                        i = list(i)
                        panda1.append(i)

                    columns = ["Product_ID", "Order_Year", "Total_Revenue"]
                    df1 = pd.DataFrame(panda1, columns=columns)

                    print(df1)
                    print("\n")
                elif y == 2:
                    print(OLAP_Query_2)
                    print("\n")
                    try:
                        cursor.execute(OLAP_Query_2)
                        result = cursor.fetchall()
                        print("Query2 was successful\n")
                    except:
                        print("Error")

                    panda1 = []
                    for i in result:
                        i = list(i)
                        panda1.append(i)

                    columns = ["Month_", "Customer_ID", "Total_Revenue", "Total_Orders"]
                    df1 = pd.DataFrame(panda1, columns=columns)

                    print(df1)
                    print("\n")
                elif y == 3:
                    print(OLAP_Query_3)
                    print("\n")
                    try:
                        cursor.execute(OLAP_Query_3)
                        result = cursor.fetchall()
                        print("Query3 was successful\n")
                    except:
                        print("Error")

                    panda1 = []
                    for i in result:
                        i = list(i)
                        panda1.append(i)

                    columns = ["Order_ID", "Amount", "Paymnet_Status", "Method"]
                    df1 = pd.DataFrame(panda1, columns=columns)

                    print(df1)
                    print("\n")
                elif y == 4:
                    print(OLAP_Query_4)
                    print("\n")
                    try:
                        cursor.execute(OLAP_Query_4)
                        result = cursor.fetchall()
                        print("Query4 was successful\n")
                    except:
                        print("Error")

                    panda1 = []
                    for i in result:
                        i = list(i)
                        panda1.append(i)

                    columns = ["Full_Name", "Total"]
                    df1 = pd.DataFrame(panda1, columns=columns)

                    print(df1)
                    print("\n")
        if(v==1):
            cursor = connection.cursor(buffered=True)
            Query_1 = """ 
            SELECT p.Product_ID, SUM(p.cart_quantity * p.price) AS Total_Revenue
            FROM Product p
            JOIN contains_ c ON p.product_id = c.product_id
            JOIN order_ o ON c.order_id = o.order_id
            WHERE o.order_status = 'shipped'
            GROUP BY p.product_id
            ORDER BY total_revenue DESC; """
            Query_2 = """
            SELECT c.Customer_ID, SUM(p.Price * p.Cart_Quantity) AS TotalValue
            FROM customer c
            JOIN order_ o ON c.Customer_ID = o.Customer_ID
            JOIN contains_ co ON o.Order_ID = co.Order_ID
            JOIN product p ON co.Product_ID = p.Product_ID
            GROUP BY c.Customer_ID
            ORDER BY TotalValue DESC
            LIMIT 5;"""
            Query_3 = """SELECT p.ProductName, SUM(p.Cart_Quantity) AS TotalQuantity
            FROM product p
            JOIN contains_ c ON p.Product_id = c.Product_ID
            JOIN order_ o ON c.Order_ID = o.Order_ID
            WHERE STR_TO_DATE(o.Order_Date, '%d/%m/%Y') BETWEEN STR_TO_DATE('01/01/2022', '%d/%m/%Y') AND STR_TO_DATE('31/12/2022', '%d/%m/%Y')
            GROUP BY p.Product_id
            ORDER BY TotalQuantity DESC;"""
            Query_4 = """SELECT p.ProductName
            FROM product p
            LEFT JOIN contains_ c ON p.Product_id = c.Product_ID
            LEFT JOIN order_ o ON c.Order_ID = o.Order_ID
            WHERE (o.Order_Date IS NULL OR STR_TO_DATE(o.Order_Date, '%d/%m/%Y') NOT BETWEEN STR_TO_DATE('01/01/2022', '%d/%m/%Y') AND STR_TO_DATE('31/12/2022', '%d/%m/%Y'));"""
            Query_5 = """UPDATE inventory i
            SET i.Reorder = 'True'
            WHERE i.Inventory_ID IN (
                SELECT p.Inventory_ID
                FROM product p
                WHERE p.Inventory_Quantity < 10
            );"""
            Query_6 = """SELECT s.Full_Name, AVG(p.Price) AS Average_Price
            FROM supplier s
            JOIN supplies sp ON s.Supplier_ID = sp.Supplier_ID
            JOIN product p ON sp.Product_ID = p.Product_id
            GROUP BY s.Supplier_ID;"""
            Query_7 = """SELECT c.Customer_ID, COUNT(DISTINCT od.Product_ID) AS NumProductsOrdered
            FROM customer c
            JOIN order_ o ON c.Customer_ID = o.Customer_ID
            JOIN contains_ od ON o.Order_ID = od.Order_ID
            GROUP BY c.Customer_ID;"""
            Query_8 = """SELECT p.product_id
            FROM product p
            LEFT JOIN contains_ oi ON p.product_id = oi.product_id
            WHERE oi.product_id IS NULL;"""
            Query_9 = """SELECT p.product_id, SUM(p.cart_quantity) AS total_quantity
            FROM product p
            JOIN contains_ oi ON p.product_id = oi.product_id
            GROUP BY p.product_id
            ORDER BY total_quantity DESC;"""
            Query_10 = """SELECT *
            FROM customer
            WHERE Customer_ID IN (
            SELECT Order_.Customer_ID
            FROM order_
            INNER JOIN (
                SELECT Order_.Order_ID, SUM(Cart_Quantity * Price) AS Order_Total
                FROM contains_
                INNER JOIN product ON contains_.Product_ID = product.Product_id
                INNER JOIN order_ ON contains_.Order_ID = order_.Order_ID
                WHERE order_.Order_Status = 'shipped'
                GROUP BY Order_.Order_ID
            ) AS order_total ON order_.Order_ID = order_total.Order_ID
            WHERE Order_Total > (
                SELECT AVG(Order_Total)
                FROM (
                SELECT order_.Order_ID, SUM(Cart_Quantity * Price) AS Order_Total
                FROM contains_
                INNER JOIN product ON contains_.Product_ID = product.Product_id
                INNER JOIN order_ ON contains_.Order_ID = order_.Order_ID
                WHERE order_.Order_Status = 'shipped'
                GROUP BY order_.Order_ID
                ) AS order_total_avg
            )
            );"""
            x = 0
            while x!=11:
                print("1) Show revenue generated by each product")
                print("2) Top 5 Customer")
                print("3) Cacluate a decreasing order product which has been most purchased between two dates using date format dd/mm/yyyy")
                print("4) Select all the products that have not been ordered between two dates")
                print("5) Update the inventory reorder flag for all products that have less than 10 units in stock")
                print("6) Average price of products supplied by each supplier")
                print("7) Number of Distinct Products Ordered")
                print("8) Products that haven't been ordered")
                print("9) Total quantity a particular product has been ordered")
                print("10) Show all customers who have made an order with a total value greater than the average total value of all orders")
                print("11) Back\n")
                x = int(input("Enter you selection: "))
                if x == 1:
                    print(Query_1)
                    print("\n")
                    try:
                        cursor.execute(Query_1)
                        result = cursor.fetchall()
                        print("Query1 was successful\n")
                    except:
                        print("Error")

                    panda1 = []
                    for i in result:
                        i = list(i)
                        panda1.append(i)

                    columns = ["Product_ID", "Total_Revenue"]
                    df1 = pd.DataFrame(panda1, columns=columns)

                    print(df1)
                    print("\n")

                elif x == 2:
                    print(Query_2)
                    print("\n")
                    try:
                        cursor.execute(Query_2)
                        result = cursor.fetchall()
                        print("Query2 was successful\n")
                    except:
                        print("Error")

                    panda2 = []
                    for i in result:
                        i = list(i)
                        panda2.append(i)

                    columns = ["Customer_ID", "TotalValue"]
                    df2 = pd.DataFrame(panda2, columns=columns)

                    print(df2)
                    print("\n")
                elif x == 3:
                    print(Query_3)
                    print("\n")
                    try:
                        cursor.execute(Query_3)
                        result = cursor.fetchall()
                        print("Query3 was successful\n")
                    except:
                        print("Error")

                    panda2 = []
                    for i in result:
                        i = list(i)
                        panda2.append(i)
                    columns = ["ProductName", "Total_Quantity"]
                    df2 = pd.DataFrame(panda2, columns=columns)

                    print(df2)
                    print("\n")
                elif x == 4:
                    print(Query_4)
                    print("\n")
                    try:
                        cursor.execute(Query_4)
                        result = cursor.fetchall()
                        print("Query4 was successful\n")
                    except:
                        print("Error")

                    panda2 = []
                    for i in result:
                        i = list(i)
                        panda2.append(i)

                    columns = ["ProductName"]
                    df2 = pd.DataFrame(panda2, columns=columns)

                    print(df2)
                    print("\n")
                elif x == 5:
                    print(Query_5)
                    print("\n")
                    try:
                        cursor.execute(Query_5)
                        result = cursor.fetchall()
                        print("Query5 was successful\n")
                    except:
                        print("Error")

                    panda2 = []
                    for i in result:
                        i = list(i)
                        panda2.append(i)
                    columns = [""]
                    df2 = pd.DataFrame(panda2, columns=columns)

                    print(df2)
                    print("\n")
                elif x == 6:
                    print(Query_6)
                    print("\n")
                    try:
                        cursor.execute(Query_6)
                        result = cursor.fetchall()
                        print("Query6 was successful\n")
                    except:
                        print("Error")

                    panda2 = []
                    for i in result:
                        i = list(i)
                        panda2.append(i)
                    columns = ["FullName", "Average_Price"]
                    df2 = pd.DataFrame(panda2, columns=columns)

                    print(df2)
                    print("\n")
                elif x == 7:
                    print(Query_7)
                    print("\n")
                    try:
                        cursor.execute(Query_7)
                        result = cursor.fetchall()
                        print("Query7 was successful\n")
                    except:
                        print("Error")

                    panda2 = []
                    for i in result:
                        i = list(i)
                        panda2.append(i)
                    columns = ["Customer_ID", "NumProductsOrdered"]
                    df2 = pd.DataFrame(panda2, columns=columns)

                    print(df2)
                    print("\n")
                elif x == 8:
                    print(Query_8)
                    print("\n")
                    try:
                        cursor.execute(Query_8)
                        result = cursor.fetchall()
                        print("Query8 was successful\n")
                    except:
                        print("Error")

                    panda2 = []
                    for i in result:
                        i = list(i)
                        panda2.append(i)
                    columns = ["Product_ID"]
                    df2 = pd.DataFrame(panda2, columns=columns)

                    print(df2)
                    print("\n")
                elif x == 9:
                    print(Query_9)
                    print("\n")
                    try:
                        cursor.execute(Query_9)
                        result = cursor.fetchall()
                        print("Query9 was successful\n")
                    except:
                        print("Error")

                    panda2 = []
                    for i in result:
                        i = list(i)
                        panda2.append(i)
                    columns = ["Product_ID", "Total_Quantity"]
                    df2 = pd.DataFrame(panda2, columns=columns)

                    print(df2)
                    print("\n")
                elif x == 10:
                    print(Query_10)
                    print("\n")
                    try:
                        cursor.execute(Query_10)
                        result = cursor.fetchall()
                        print("Query10 was successful\n")
                    except:
                        print("Error")

                    panda2 = []
                    for i in result:
                        i = list(i)
                        panda2.append(i)
                    columns = ["Customer_ID", "FullName", "Email", "Customer_Password","Address"]
                    df2 = pd.DataFrame(panda2, columns=columns)

                    print(df2)
                    print("\n")

#(((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((( SUPPLIER ))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))
def supplier_interface():
    choice = 0
    while True:
        print("*** Welcome to S-Mart ***")
        print("1) Register")
        print("2) Login")
        print("3) Go Back\n")

        choice = int(input("Enter your selection: "))

        if choice==1:
            register_Supplier()
        if choice==2: 
            login_Supplier()
        if choice==3:
            break

def register_Supplier():
    Supplier_Name = input("Enter your Full Name: ")
    Supplier_Address = input("Enter your address: ")
    Supplier_PhoneNumber = int(input("Enter your PhoneNumber: "))
    Supplier_Email = input("Enter your Email: ")
    cursor.execute("SELECT MAX(Supplier_ID) FROM Supplier")
    max_id = cursor.fetchone()[0]
    new_id = max_id + 1 if max_id else 1
    Query = f"""INSERT INTO Supplier(Supplier_ID,Full_Name, Address, Phone_Number, Email) VALUES {new_id,Supplier_Name, Supplier_Address, Supplier_PhoneNumber, Supplier_Email}"""
    result = execute_query(Query)
    if(result):
        print("Registration successful!!")
        print("Supplier added successfully with ID:", new_id)
    # 

def login_Supplier():
    Supplier_ID = int(input("Enter your Supplier ID: "))
    Supplier_Pass = input("Enter your password: ")
    print("\n")
    Query = f"""SELECT * FROM SUPPLIER WHERE SUPPLIER_ID = {Supplier_ID}"""
    cursor.execute(Query)
    result = cursor.fetchall()
    if len(result) == 0:
        print("Wrong details")
    else:
        print(f"Welcome Supplier {result[0][1]}")

    WantToSupply = -1
    print("Do you want to add products to inventory?")
    print("1) Yes")
    print("2) No")
    # product information , add in product table , add in supplies
    WantToSupply = int(input("Enter your selection: "))
    if(WantToSupply == 1):
        print("Enter the details about the Product you want to add")
        Product_Name = input("Enter Product Name: ")
        Product_Desc = input("Enter Product Description: ")
        Product_Availability = input("Availability of Product(Available or Not Available): ")
        Product_Price = int(input("Enter price of Product: "))
        Inventory_Id = int(input("Enter the Inventory ID: "))
        Product_Quantity = int(input("Enter Inventory Quantity: "))
        cursor.execute("SELECT MAX(Product_ID) FROM Product")
        max_id = cursor.fetchone()[0]
        new_id = max_id + 1 if max_id else 1
        Query1 = f"""INSERT INTO Product(Product_id, Availability, Product_Description, Customer_ID, Inventory_ID, Price, Cart_Quantity, ProductName, Inventory_Quantity) VALUES {new_id, Product_Availability, Product_Desc, 1, Inventory_Id, Product_Price, 0, Product_Name, Product_Quantity}"""
        execute_query(Query1)
        
        Query = f"""INSERT INTO Supplies(Supplier_ID, Product_ID) VALUES {Supplier_ID, new_id}"""
        result = execute_query(Query)
        if(result):
            print("Product added successfully!!")
            print(f"Product ID is: {new_id}")


#(((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((( EMPLOYEE ))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))

def employee_interface():
    choice = 0
    while True:
        print("*** Welcome to S-Mart ***")
        print("1) Register")
        print("2) Login")
        print("3) Go Back\n")

        choice = int(input("Enter your selection: "))

        if choice==1:
            register_employee()
        if choice==2: 
            login_employee()
        if choice==3:
            break

def register_employee():
    Employee_Username = input("Enter your Username: ")
    Employee_Pass = input("Enter your Password: ")
    
    cursor.execute("SELECT MAX(Employee_ID) FROM Employee")
    max_id = cursor.fetchone()[0]
    new_id = max_id + 1 if max_id else 1
    Query = f"""INSERT INTO Employee(Employee_ID, Username, Employee_Password) VALUES {new_id,Employee_Username, Employee_Pass}"""
    result = execute_query(Query)
    if(result):
        print("Registration successful!!")
        print("Employee added successfully with ID:", new_id)

    Query1 = """SELECT order_id
    FROM order_
    WHERE NOT EXISTS (
    SELECT *
    FROM manages
    WHERE manages.order_id = order_.order_id
    );"""
    cursor.execute(Query1)
    result = cursor.fetchall()
    x = random.randint(1,20)
    Query2 = f"""INSERT INTO Manages(Order_ID, Inventory_ID, Employee_ID) VALUES {result[0][0], x, new_id}"""
    ans = execute_query(Query2)
    if(ans):
        print(f"You have been assigned Inventory_ID = {x} and Order_ID = {result[0][0]}")


def login_employee():
    Employee_ID = int(input("Enter your ID: "))
    Employee_Pass = input("Enter your password: ")
    print("\n")
    Query = f"""SELECT * FROM Employee WHERE Employee_ID = {Employee_ID} AND Employee_Password = '{Employee_Pass}'"""
    cursor.execute(Query)
    result = cursor.fetchall()
    if len(result) == 0:
        print("Wrong details")
    else:
        ins = 0
        while(ins!=3):
            print(f"Welcome Employee {result[0][1]}")
            print("Do you want to see Inventory or Order under this employee?")
            print("1) Inventory")
            print("2) Order")
            print("3) Back")
            ins = int(input("Enter your selection: "))
            if(ins == 2):
                order_under_employee(Employee_ID)
            elif ins == 1:
                inventory_check_by_employee(Employee_ID)
            else:
                return

def order_under_employee(Employee_ID):
    print("All the order under this employee are: ")
    Query = f"""SELECT Order_ID FROM manages WHERE Employee_ID = {Employee_ID}"""
    cursor.execute(Query)
    result = cursor.fetchall()
    panda1 = []
    for i in result:
        i = list(i)
        panda1.append(i)
    columns = ["Order_ID"]
    df1 = pd.DataFrame(panda1, columns=columns)

    print(df1)
    print("\n")


def inventory_check_by_employee(Employee_ID):
    Query = f"""SELECT Inventory_ID FROM manages WHERE Employee_ID = {Employee_ID}"""
    cursor.execute(Query)
    result1 = cursor.fetchall()
    print(f"Inventory under this Employee is {result1[0][0]}")
    
    Query1 = f"""SELECT Reorder FROM inventory WHERE Inventory_ID = {result1[0][0]}"""
    cursor.execute(Query1)
    result = cursor.fetchall()
    print(f"Reorder value for this Inventory is: {result[0][0]}\n")
    # Need for asking inventory_id first 
    if(result[0][0] == 'False'):
        print("Do you want to change Reorder to True?")
        print("1) Yes")
        print("2) No")
        ans = int(input())
        if(ans == 1):
            execute_query(f"""UPDATE inventory SET Reorder = 'True' WHERE Inventory_ID = {result1[0][0]}""")
            print("Reorder successfully set to True")
    else:
        print("Do you want to change Reorder to False?")
        print("1) Yes")
        print("2) No")
        ans = int(input())
        if(ans == 1):
            execute_query(f"""UPDATE inventory SET Reorder = 'False' WHERE Inventory_ID = {result1[0][0]}""")
            print("Reorder successfully set to False")



# Order table print, Inventory check reorder true display

#(((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((( DELIVERYDRIVER ))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))

def deliverydriver_interface():
    choice = 0
    while True:
        print("*** Welcome to S-Mart ***")
        print("1) Register")
        print("2) Login")
        print("3) Go Back\n")

        choice = int(input("Enter your selection: "))

        if choice==1:
            register_delivery_driver()
        if choice==2: 
            login_delivery_driver()
        if choice==3:
            break


def register_delivery_driver():
    driver_name= input("Enter your Name: ")
    driver_PhNo = input("Enter your PhoneNumber: ")
    delivery_date = '18/12/2023'
    cursor.execute("SELECT MAX(Driver_ID) FROM deliverydriver")
    max_id = cursor.fetchone()[0]
    new_id = max_id + 1 if max_id else 1
    Query = f"""INSERT INTO deliverydriver(Driver_ID, Full_Name, Phone_Number, Delivery_Date) VALUES {new_id, driver_name, driver_PhNo, delivery_date}"""
    result = execute_query(Query)
    if(result):
        print("Registration successful!!")
        print("Driver added successfully with ID:", new_id)

def login_delivery_driver():
    driver_id = int(input("Enter your ID: "))
    driver_password = input("Enter your Password: ")
    print("\n")
    Query = f"""SELECT * FROM deliverydriver WHERE Driver_ID = {driver_id}"""
    cursor.execute(Query)
    result = cursor.fetchall()
    if len(result) == 0:
        print("Wrong details")
    else:
        print(f"Welcome Driver {result[0][1]}")
    print("Do you want to see all the orders under this Driver?")
    print("1) Yes")
    print("2) No")
    ans = int(input())
    if(ans == 1):
        order_under_driver(driver_id)

def order_under_driver(driver_id):
    print("All the order under this driver are: ")
    Query = f"""SELECT * FROM order_ WHERE Driver_ID = {driver_id}"""
    cursor.execute(Query)
    result = cursor.fetchall()
    panda1 = []
    for i in result:
        i = list(i)
        panda1.append(i)
    columns = ["Order_ID", "Order_Date", "Order_Status","Customer_ID", "Driver_ID"]
    df1 = pd.DataFrame(panda1, columns=columns)

    if(len(result)!=0):
        print(df1)
        print("\n")
        print("Do you want to change Order Status of any of these Orders?")
        print("1) Yes")
        print("2) No")
        ins = input("Enter your selection: ")
        if(ins == '1' or ins == "Yes"):
            change_order_status(driver_id)
    else:
        print("No orders for now!!")


def change_order_status(driver_id):
    order_id = int(input("Enter the Order ID for the order you want to change the status of: "))
    query = f"""SELECT * FROM order_ WHERE Order_ID = %s AND Driver_ID = {driver_id}"""
    cursor.execute(query, (order_id,))
    order = cursor.fetchone()
    if not order:
        print("Invalid Order ID.")
        return
    
    print("Current Status:", order[2])
    print("Select New Status:")
    print("1) Pending")
    print("2) Confirmed")
    print("3) Shipped")
    new_status = input("Enter Option Number: ")
    
    if new_status == '1':
        status = "Pending"
    elif new_status == '2':
        status = "Confirmed"
    elif new_status == '3':
        status = "Shipped"
    else:
        print("Invalid Option.")
        return
    
    query = "UPDATE order_ SET Order_Status = %s WHERE Order_ID = %s"
    cursor.execute(query, (status, order_id))
    connection.commit()
    queryx = f"""SELECT * FROM order_ WHERE Order_ID = {order_id} AND Driver_ID = {driver_id}"""
    cursor.execute(queryx)
    result = cursor.fetchall()
    panda1 = []
    for i in result:
        i = list(i)
        panda1.append(i)
    columns = ["Order_ID", "Order_Date", "Order_Status","Customer_ID", "Driver_ID"]
    df1 = pd.DataFrame(panda1, columns=columns)

    print(df1)
    print("\n")
    print("Order Status Updated Successfully.")


#(((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((((( CUSTOMER ))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))
def customer_interface():
    choice = 0
    while True:
        print("*** Welcome to S-Mart ***")
        print("1) Register")
        print("2) Login")
        print("3) Go Back\n")

        choice = int(input("Enter your selection: "))

        if choice==1:
            register_customer()
        if choice==2: 
            login_customer()
        if choice==3:
            app()


def register_customer():
    c_full_name = input("Enter full name: ")
    c_email = input("Enter email: ")
    c_password = input("Enter password: ")
    c_address = input("Enter address: ")
    x = 0
    query = "SELECT * FROM customer WHERE Full_Name=%s AND Email=%s AND Customer_Password=%s AND Address=%s"
    cursor.execute(query, (c_full_name, c_email, c_password, c_address))
    result = cursor.fetchone()
    if result:
        x = 1
        print("Customer already exists in the database.")
    else:
        # Get the maximum customer ID from the customer table and add 1 to it
        cursor.execute("SELECT MAX(Customer_ID) FROM customer")
        max_id = cursor.fetchone()[0]
        new_id = max_id + 1 if max_id else 1
        
        # Insert the new customer into the customer table with the new ID
        query = "INSERT INTO customer (Customer_ID, Full_Name, Email, Customer_Password, Address) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (new_id, c_full_name, c_email, c_password, c_address))
        connection.commit()

    while x!=1:
        c_phone_number = input("Enter phone number (or 'q' to quit): ")
        if c_phone_number.lower() == 'q':
            break
        else:
            # Insert the phone number into the customer_contact table with the new customer's ID
            query = "INSERT INTO customer_contact (Customer_ID, Phone_Number) VALUES (%s, %s)"
            cursor.execute(query, (new_id, c_phone_number))
            connection.commit()

    # connection.commit()
    if(x!=1):
        print("Customer added successfully with ID:", new_id)
    # go back
    # customer_interface()

def login_customer():
    c_id = input("Enter your customer ID: ")
    c_password = input("Enter your password: ")

    # Check if the customer exists in the customer table
    query = "SELECT * FROM customer WHERE Customer_ID=%s AND Customer_Password=%s"
    cursor.execute(query, (c_id, c_password))
    result = cursor.fetchone()

    if result:
        print("Welcome, ", result[1])
        while True:
            print("\nWhat would you like to do?")
            print("1) Place an order")
            print("2) View your orders")
            print("3) Go back")

            choice = input("Enter your choice (1-3): ")
            if choice == "1":
                place_order(c_id)

            elif choice == "2":
                view_orders(c_id)

            elif choice == "3":
                customer_interface()
            else:
                print("Invalid choice. Please enter a number between 1 and 3.")
    else:
        print("Customer ID or password incorrect.")
        # customer_interface()

def view_orders(c_id):
    query = "SELECT * FROM order_ WHERE Customer_ID = %s"
    cursor.execute(query, (c_id,))
    orders = cursor.fetchall()
    if not orders:
        print("No orders found for customer ID", c_id)
    else:
        print("Orders for customer ID", c_id)
        for order in orders:
            print("Order ID:", order[0])
            print("Order Date:", order[1])
            print("Order Status:", order[2])
            # print("Customer ID:", order[3])
            print("Driver ID:", order[4])
            
            # Join contains_ and product tables to get the products in the order
            query = "SELECT p.ProductName, p.Cart_Quantity, p.Price FROM contains_ c INNER JOIN product p ON c.Product_ID = p.Product_id WHERE c.Order_ID = %s"
            cursor.execute(query, (order[0],))
            products = cursor.fetchall()
            
            print("Products:")
            for product in products:
                print(product[0], "Quantity:", product[1], "Price:", product[2])
            
            print("\n")
# Product_ID = 2,3,5
def place_order(c_id):
    # display all available products
    query = "SELECT * FROM product"
    cursor.execute(query)
    products = cursor.fetchall()
    if not products:
        print("No products available.")
        return

    print("Available products:\n")
    # for product in products:
    #     print("Product ID:", product[0])
    #     print("Product Name:", product[7])
    #     print("Description:", product[2])
    #     print("Price:", product[5])
    #     print("Inventory Quantity:", product[8])
    #     print("\n")

    panda1 = []
    for product in products:
        product_list = [product[0], product[7], product[1], product[2], product[5], product[8]]
        panda1.append(product_list)

        columns = ["Product_ID", "Product_Name", "Availabilty", "Description", "Price", "Inventory Quantity"]
        df1 = pd.DataFrame(panda1, columns=columns)
    print(df1)
    print("\n")

    cart_items = {}
    while True:
        p_id = input("Enter the Product ID you want to add to cart or 'done' to place the order: ")
        if p_id == 'done':
            break
        cursor.execute("UPDATE product SET Customer_ID=%s WHERE Product_id=%s", (c_id, p_id))
        connection.commit()
        cursor.execute("SELECT * FROM product WHERE Product_id=%s AND Customer_ID=%s", (p_id, c_id))
        product = cursor.fetchone()

        quantity = input("Enter the Quantity you want to buy: ")
        quantity = int(quantity)

        if quantity <= 0:
            print("Invalid Quantity")
            continue

        if product[8] < quantity:
            print("Quantity not available in inventory")
            continue

        # if p_id in cart_items:
        #     cart_items[p_id] += quantity
        # else:
        cart_items[p_id] = quantity

        print("Product added to cart.")

    if not cart_items:
        print("No Products added to cart.")
        return

    cursor.execute("SELECT MAX(Order_ID) FROM order_")
    max_order_id = cursor.fetchone()[0]
    if max_order_id:
        order_id = max_order_id + 1
    else:
        order_id = 1

    cursor.execute("SELECT Driver_ID FROM deliverydriver ORDER BY RAND() LIMIT 1")
    driver_id = cursor.fetchone()[0]

    total_amount = 0
    cursor.execute("INSERT INTO order_ (Order_ID, Order_Date, Order_Status, Customer_ID, Driver_ID) VALUES (%s,'07/04/2022', 'Pending', %s, %s)",
                (order_id, c_id, driver_id))
    connection.commit()
    for p_id, quantity in cart_items.items():
        cursor.execute("UPDATE product SET Cart_Quantity=%s, Inventory_Quantity=Inventory_Quantity-%s WHERE Product_id=%s AND Customer_ID=%s",
                    (quantity, quantity, p_id, c_id))
        connection.commit()
        cursor.execute("INSERT INTO contains_ (Order_ID, Product_ID) VALUES (%s, %s)", (order_id, p_id))
        connection.commit()
        cursor.execute("SELECT Price FROM product WHERE Product_id=%s", (p_id,))
        price = cursor.fetchone()[0]
        total_amount += price * quantity

    payment_option = ''
    
    print("Please choose a payment option:")
    print("1. Credit card")
    print("2. Cash on Delivery")
    print("3. Debit Card")
    print("4. PayPal")
    
    choice = int(input())
    if choice == 1:
        payment_option = "Credit card"
    elif choice == 2:
        payment_option = "Cash on Delivery"
    elif choice == 3:
        payment_option = "Debit Card"
    elif choice == 3:
        payment_option = "PayPal"
    
    cursor.execute("INSERT INTO payment (Payment_Date, Order_ID, Amount, Payment_Status, Method) VALUES ('07/04/2022', %s, %s, 'Paid',%s)",
                (order_id, total_amount,payment_option))
    

    # connection.commit()
    print("Order Placed Successfully!")


app()
