# =================================================================================
# This script sets up the Little Lemon database.
# It creates the database, tables, and populates them with initial data.
# Reviewers should run this script first to create the necessary environment.
# =================================================================================

import mysql.connector
from mysql.connector import Error

# --- IMPORTANT: UPDATE WITH YOUR MYSQL CREDENTIALS ---
# Define the connection parameters for your MySQL server.
db_config = {
    "user": "your_username",
    "password": "your_password",
    "host": "127.0.0.1"
}
DB_NAME = 'little_lemon_db'

# --- SQL STATEMENTS FOR TABLE CREATION ---
# Using "IF NOT EXISTS" makes the script re-runnable without errors.
# Also defining data types and constraints as per the project description.
TABLES = {}
TABLES['MenuItems'] = """
CREATE TABLE IF NOT EXISTS MenuItems (
    ItemID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(200),
    Type VARCHAR(100),
    Price DECIMAL(10, 2)
);"""

TABLES['Menus'] = """
CREATE TABLE IF NOT EXISTS Menus (
    MenuID INT,
    ItemID INT,
    Cuisine VARCHAR(100),
    PRIMARY KEY (MenuID, ItemID),
    FOREIGN KEY (ItemID) REFERENCES MenuItems(ItemID)
);"""

TABLES['Employees'] = """
CREATE TABLE IF NOT EXISTS Employees (
    EmployeeID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255),
    Role VARCHAR(100),
    Address VARCHAR(255),
    Contact_Number VARCHAR(20),
    Email VARCHAR(255),
    Annual_Salary VARCHAR(100)
);"""

TABLES['Bookings'] = """
CREATE TABLE IF NOT EXISTS Bookings (
    BookingID INT AUTO_INCREMENT PRIMARY KEY,
    TableNo INT,
    GuestFirstName VARCHAR(100) NOT NULL,
    GuestLastName VARCHAR(100) NOT NULL,
    BookingSlot TIME NOT NULL,
    EmployeeID INT,
    FOREIGN KEY (EmployeeID) REFERENCES Employees(EmployeeID)
);"""

TABLES['Orders'] = """
CREATE TABLE IF NOT EXISTS Orders (
    OrderID INT,
    TableNo INT,
    MenuID INT,
    BookingID INT,
    Quantity INT,
    BillAmount DECIMAL(10, 2),
    PRIMARY KEY (OrderID, TableNo),
    FOREIGN KEY (BookingID) REFERENCES Bookings(BookingID),
    FOREIGN KEY (MenuID) REFERENCES Menus(MenuID)
);"""

# --- SQL STATEMENTS FOR DATA INSERTION ---
insert_menuitems = "INSERT INTO MenuItems (ItemID, Name, Type, Price) VALUES (1, 'Olives', 'Starters', 5.00), (2, 'Flatbread', 'Starters', 5.50), (3, 'Minestrone', 'Starters', 8.00), (4, 'Tomato Bread', 'Starters', 8.50), (5, 'Falafel', 'Starters', 7.50), (6, 'Hummus', 'Starters', 5.00), (7, 'Greek Salad', 'Mains', 15.00), (8, 'Bean Stew', 'Mains', 12.50), (9, 'Pizza', 'Mains', 15.00), (10, 'Greek Burger', 'Mains', 18.00), (11, 'Kabasa', 'Mains', 17.00), (12, 'Shwarma', 'Mains', 11.50), (13, 'Ice Cream', 'Desserts', 6.00), (14, 'Cheesecake', 'Desserts', 7.00);"
insert_menus = "INSERT INTO Menus (MenuID, ItemID, Cuisine) VALUES (1, 1, 'Greek'), (1, 7, 'Greek'), (1, 10, 'Greek'), (1, 13, 'Greek'), (2, 3, 'Italian'), (2, 9, 'Italian'), (2, 14, 'Italian'), (2, 4, 'Italian'), (3, 5, 'Turkish'), (3, 11, 'Turkish'), (3, 12, 'Turkish'), (3, 6, 'Turkish');"
insert_employees = "INSERT INTO Employees (EmployeeID, Name, Role, Address, Contact_Number, Email, Annual_Salary) VALUES (1, 'Mario Gollini', 'Manager', '724, Parsley Lane, Old Town, Chicago, IL', '351258074', 'Mario.g@littlelemon.com', '70000'), (2, 'Adrian Gollini', 'Assistant Manager', '334, Dill Square, Lincoln Park, Chicago, IL', '351474048', 'Adrian.g@littlelemon.com', '65000'), (3, 'Giorgos Dioudis', 'Head Chef', '879, Sage Street, West Loop, Chicago, IL', '351970582', 'Giorgos.d@littlelemon.com', '50000'), (4, 'Vanessa Tortellini', 'Chef', '345, Rosemary Lane, downtown, Chicago, IL', '351963569', 'Vanessa.t@littlelemon.com', '40000'), (5, 'Diana Pifferi', 'Chef', '156, Thyme Square, downtown, Chicago, IL', '351944802', 'Diana.p@littlelemon.com', '35000'), (6, 'Joanna Cortes', 'Head Waiter', '975, Sage Street, West Loop, Chicago, IL', '351970582', 'Joanna.c@littlelemon.com', '30000');"
insert_bookings = "INSERT INTO Bookings (BookingID, TableNo, GuestFirstName, GuestLastName, BookingSlot, EmployeeID) VALUES (1, 12, 'Anna', 'Iversen', '19:00:00', 1), (2, 12, 'Joakim', 'Iversen', '19:00:00', 1), (3, 19, 'Vanessa', 'Torres', '15:00:00', 3), (4, 15, 'Marcos', 'Romero', '17:30:00', 4), (5, 5, 'Hiroki', 'Yamane', '18:30:00', 2), (6, 8, 'Diana', 'Pinto', '20:00:00', 5);"
insert_orders = "INSERT INTO Orders (OrderID, TableNo, MenuID, BookingID, Quantity, BillAmount) VALUES (1, 12, 1, 1, 2, 86.00), (2, 19, 2, 2, 1, 37.00), (3, 15, 2, 3, 1, 37.00), (4, 5, 3, 4, 1, 40.00), (5, 8, 1, 5, 1, 43.00);"


def setup_database(config):
    """Creates the database, tables, and populates them with data."""
    connection = None
    try:
        # Connect to MySQL Server (without specifying a database)
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()
        print("Successfully connected to MySQL server.")

        # Create database
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME} DEFAULT CHARACTER SET 'utf8'")
        cursor.execute(f"USE {DB_NAME}")
        print(f"Database '{DB_NAME}' created and selected for use.")

        # Clear existing data to make script re-runnable
        print("Clearing existing data...")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        cursor.execute("TRUNCATE TABLE Orders;")
        cursor.execute("TRUNCATE TABLE Bookings;")
        cursor.execute("TRUNCATE TABLE Employees;")
        cursor.execute("TRUNCATE TABLE Menus;")
        cursor.execute("TRUNCATE TABLE MenuItems;")
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        
        # Create tables
        print("Creating tables...")
        for table_name in TABLES:
            cursor.execute(TABLES[table_name])
        print("Tables created successfully.")
        
        # Populate tables
        print("Populating tables...")
        cursor.execute(insert_menuitems)
        cursor.execute(insert_menus)
        cursor.execute(insert_employees)
        cursor.execute(insert_bookings)
        cursor.execute(insert_orders)
        print("Data inserted successfully.")

        connection.commit()
        print("Database setup complete and changes committed.")

    except Error as e:
        print(f"Error during database setup: {e}")
        if connection:
            connection.rollback()
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed.")

if __name__ == '__main__':
    print("--- Starting Little Lemon Database Setup ---")
    setup_database(db_config)
    print("--- Setup script finished. ---")