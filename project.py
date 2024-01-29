import sqlite3
from datetime import datetime
import sys

DB_FILE = 'ecommerce.db'

def connect_to_database():
    return sqlite3.connect(DB_FILE)

def create_tables():
    with connect_to_database() as conn:
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Customer (
        CustomerID INTEGER PRIMARY KEY AUTOINCREMENT,
        PersonalInfo VARCHAR(255),
        ContactInfo VARCHAR(255),
        AddressInfo VARCHAR(255),
        AccountInfo VARCHAR(255),
        PaymentMethod VARCHAR(255)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Product (
                ProductID INT PRIMARY KEY,
                Name VARCHAR(255),
                Description TEXT,
                Price DECIMAL(10,2),
                QuantityInStock INT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS "Order" (
                OrderID INT PRIMARY KEY,
                CustomerID INT,
                OrderDate DATE,
                TotalAmount DECIMAL(10,2),
                PaymentMethod VARCHAR(255),
                OrderStatus VARCHAR(255),
                FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Supplier (
                SupplierID INT PRIMARY KEY,
                Name VARCHAR(255),
                ContactInfo VARCHAR(255),
                PaymentTerms VARCHAR(255),
                DeliveryTerms VARCHAR(255)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Payment (
                PaymentID INT PRIMARY KEY,
                OrderID INT,
                Amount DECIMAL(10,2),
                DatePaid DATE,
                PaymentMethod VARCHAR(255),
                PaymentStatus VARCHAR(255),
                FOREIGN KEY (OrderID) REFERENCES "Order"(OrderID)
            )
        ''')

def add_customer(personal_info, contact_info, address_info, account_info, payment_method):
    with connect_to_database() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Customer (PersonalInfo, ContactInfo, AddressInfo, AccountInfo, PaymentMethod)
            VALUES (?, ?, ?, ?, ?)
        ''', (personal_info, contact_info, address_info, account_info, payment_method))
        customer_id = cursor.lastrowid

    return customer_id

def add_payment_method(payment_method):
    with connect_to_database() as conn:
        cursor = conn.cursor()
        cursor.execute('INSERT OR IGNORE INTO "Order" (PaymentMethod) VALUES (?)', (payment_method,))

def view_payment_methods():
    with connect_to_database() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT DISTINCT PaymentMethod FROM "Order"')
        payment_methods = cursor.fetchall()
        print("\n--- Payment Methods ---")
        for payment_method in payment_methods:
            print(f"PaymentMethod: {payment_method[0]}")
        print("\n")

def view_customers():
    with connect_to_database() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Customer')
        customers = cursor.fetchall()
        print("\n--- Customers Registered ---")
        for customer in customers:
            print(f"""CustomerID: {customer[0]}, 
            PersonalInfo: {customer[1]}
            ContactInfo: {customer[2]} 
            AddressInfo: {customer[3]} 
            AccountInfo: {customer[4]} 
            PaymentMethod: {customer[5]}""")
        print("\n")

def view_products():
    with connect_to_database() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Product')
        products = cursor.fetchall()
        print("\n--- Products Available ---")
        for product in products:
            print(f"""ProductID: {product[0]}
            Name: {product[1]}
            Description: {product[2]} 
            Price: {product[3]}
            QuantityInStock: {product[4]}""")
        print("\n")

def view_orders():
    with connect_to_database() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM "Order"')
        orders = cursor.fetchall()
        print("\n--- Orders Made ---")
        for order in orders:
            print(f"""OrderID: {order[0]} 
            CustomerID: {order[1]}
            OrderDate: {order[2]} 
            TotalAmount: {order[3]} 
            PaymentMethod: {order[4]} 
            OrderStatus: {order[5]}""")
        print("\n")

def view_suppliers():
    with connect_to_database() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Supplier')
        suppliers = cursor.fetchall()
        print("\n--- Suppliers ---")
        for supplier in suppliers:
            print(f"""SupplierID: {supplier[0]}
            Name: {supplier[1]} 
            ContactInfo: {supplier[2]} 
            PaymentTerms: {supplier[3]}
            DeliveryTerms (Home Delivery or Office Pick-up): {supplier[4]}""")
        print("\n")

def add_product(name, description, price, quantity_in_stock):
    with connect_to_database() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Product (Name, Description, Price, QuantityInStock)
            VALUES (?, ?, ?, ?)
        ''', (name, description, price, quantity_in_stock))

def add_order(customer_id, total_amount, payment_method, order_status):
    with connect_to_database() as conn:
        cursor = conn.cursor()
        order_date = datetime.now().strftime("%Y-%m-%d")
        cursor.execute('''
            INSERT INTO "Order" (CustomerID, OrderDate, TotalAmount, PaymentMethod, OrderStatus)
            VALUES (?, ?, ?, ?, ?)
        ''', (customer_id, order_date, total_amount, payment_method, order_status))
        add_payment_method(payment_method)

def add_supplier(name, contact_info, payment_terms, delivery_terms):
    with connect_to_database() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Supplier (Name, ContactInfo, PaymentTerms, DeliveryTerms)
            VALUES (?, ?, ?, ?)
        ''', (name, contact_info, payment_terms, delivery_terms))

def add_payment(order_id, amount, payment_method, payment_status):
    with connect_to_database() as conn:
        cursor = conn.cursor()
        date_paid = datetime.now().strftime("%Y-%m-%d")
        cursor.execute('''
            INSERT INTO Payment (OrderID, Amount, DatePaid, PaymentMethod, PaymentStatus)
            VALUES (?, ?, ?, ?, ?)
        ''', (order_id, amount, date_paid, payment_method, payment_status))

def main():
    create_tables()

    while True:
        print("\n1. Add Customer")
        print("2. Add Product")
        print("3. Add Order")
        print("4. Add Supplier")
        print("5. Add Payment")
        print("6. View Customers")
        print("7. View Products")
        print("8. View Orders")
        print("9. View Suppliers")
        print("10. View Payment Methods")
        print("11. Exit")

        choice = input("Enter your choice (1-11): ")

        if choice == '1':
            # Get user inputs for customer details
            personal_info = input("Enter PersonalInfo: ")
            contact_info = input("Enter ContactInfo: ")
            address_info = input("Enter AddressInfo: ")
            account_info = input("Enter AccountInfo: ")
            payment_method = input("Enter PaymentMethod: ")
            add_customer(personal_info, contact_info, address_info, account_info, payment_method)

        elif choice == '2':
            # Get user inputs for product details
            name = input("Enter Product Name: ")
            description = input("Enter Product Description: ")
            price = float(input("Enter Product Price: "))
            quantity_in_stock = int(input("Enter Quantity In Stock: "))
            add_product(name, description, price, quantity_in_stock)

        elif choice == '3':
            # Get user inputs for order details
            customer_id = int(input("Enter CustomerID for the order: "))
            total_amount = float(input("Enter Total Amount: "))
            payment_method = input("Enter Payment Method: ")
            order_status = input("Enter Order Status: ")
            add_order(customer_id, total_amount, payment_method, order_status)

        elif choice == '4':
            # Get user inputs for supplier details
            name = input("Enter Supplier Name: ")
            contact_info = input("Enter Supplier ContactInfo: ")
            payment_terms = input("Enter Payment Terms: ")
            delivery_terms = input("Enter Delivery Terms: ")
            add_supplier(name, contact_info, payment_terms, delivery_terms)

        elif choice == '5':
            # Get user inputs for payment details
            order_id = int(input("Enter OrderID for the payment: "))
            amount = float(input("Enter Payment Amount: "))
            payment_method = input("Enter Payment Method: ")
            payment_status = input("Enter Payment Status: ")
            add_payment(order_id, amount, payment_method, payment_status)

        elif choice == '6':
            view_customers()
        elif choice == '7':
            view_products()
        elif choice == '8':
            view_orders()
        elif choice == '9':
            view_suppliers()
        elif choice == '10':
            view_payment_methods()
        elif choice == '11':
            sys.exit("Exiting the application.")
        else:
            print("Invalid choice. Please enter a valid option (1-11).")

if __name__ == "__main__":
    main()
    input("Press Enter to exit")
