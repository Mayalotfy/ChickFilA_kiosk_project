import psycopg2
from datetime import datetime
import Summary
from psycopg2.extensions import adapt
# Define a function to get the current timestamp

from flask import Flask
app = Flask(__name__)

def get_timestamp():
    """
    Returns the current timestamp as a formatted string.
    """
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def get_todaydate():
    """
    Returns the current date as a formatted string.
    """
    current_date = datetime.now()
    return current_date.strftime("%m/%d/%Y")

def db_connection():
    """
    This function creates a connection to a PostgreSQL database with the given
    credentials and returns the connection object.

    Returns:
        psycopg2.extensions.connection: The connection object for the database
    """
    conn = psycopg2.connect(
        host="csce-315-db.engr.tamu.edu",
        database="csce315331_iota",
        user="csce315331_iota_master",
        password="IOTA"
    )
    return conn

def get_ordernumber():
    """
    Retrieves the latest order number from the orderhistory table in the database, increments it by 1,
    and returns the new order number. If there is an error finding the order number, a message is printed
    and the function returns 0000 as the order number.
    """
    ordernumber =0000
    conn = db_connection()
    cur = conn.cursor()
    cur.execute("SELECT ordernumber FROM orderhistory ORDER BY ordernumber DESC LIMIT 1")
    resultSet = cur.fetchall()
    if resultSet:
        ordernumber = resultSet[0][0]+1
    else:
        print("Error finding ordernumber.")
    cur.close()
    conn.close()
    return ordernumber

def getCategoryNamesFromDatabase():
    """
    Retrieves a list of distinct category names from the items table in the database and returns the list.
    """
    categoryNames = []
    conn = db_connection()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT category FROM items")
    resultSet = cur.fetchall()
    for row in resultSet:
            categoryNames.append(row[0])
    cur.close()
    conn.close()
    return categoryNames

def getItemsfromcategory(Category):
    """
    Retrieves a list of item names from the items table in the database that belong to the specified category,
    and returns the list.
    
    Parameters:
    Category (str): The category of items to retrieve.
    """
    ItemsNames = []
    conn = db_connection()
    cur = conn.cursor()
    cur.execute("SELECT item FROM items WHERE category = %s", (Category,))
    resultSet = cur.fetchall()
    for row in resultSet:
            ItemsNames.append(row[0])
    cur.close()
    conn.close()
    return ItemsNames

def get_ingredients_from_item(item):
    """
    Retrieves a list of ingredients that are used in the specified item from the ingredientslist table in the
    database and returns the list.
    
    Parameters:
    item (str): The name of the item to retrieve the ingredients for.
    """
    items_names = []
    conn = db_connection()
    cur = conn.cursor()
    query = "SELECT Ingredient FROM ingredientslist WHERE Item = %s"
    cur.execute(query, (item,))
    resultSet = cur.fetchall()
    for row in resultSet:
                items_names.append(row[0])
    cur.close()
    conn.close()
    return items_names

def get_add_value(extra_category, item):
    """
    Retrieves the additional/remove value for the specified extra category and item from the extras table in the database,
    and returns the value.
    
    Parameters:
    extra_category (str): The category of the extra to retrieve the value for.
    item (str): The name of the item that the extra is associated with.
    """
    value = 0
    conn = db_connection()
    cur = conn.cursor()
    query = "SELECT add FROM extras WHERE ExtraCategory = %s AND Item = %s"
    cur.execute(query, (extra_category, item))
    result_set = cur.fetchall()
    if result_set:
        value = result_set[0][0]
    cur.close()
    conn.close()
    return value

def add_to_history(newOrder):
    """
    Adds the items in the cart of the newOrder object to the orderhistory table in the database, along with the
    customization and price of each item.
    
    Parameters:
    newOrder (Order): The order object containing the cart items to add to the order history.
    """
    conn = db_connection()
    cur = conn.cursor()
    for key in newOrder.cartItem:
        for value in newOrder.cartItem[key]:
            cur.execute("SELECT id FROM orderhistory ORDER BY id DESC LIMIT 1")
            resultSet = cur.fetchall()
            num=resultSet[0][0] + 1
            customization = '{{{}}}'.format(','.join(['"{}"'.format(x) for x in value]))
            query = "INSERT INTO orderhistory (id, ordernumber, date, time, items, customization, price) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}');".format(
                num,
                newOrder.ordernumber,
                get_todaydate(),
                get_timestamp(),
                key,
                customization,
                str(round(newOrder.getPrice(key,value),2))
            )   
            print(query)
            cur.execute(query)
            conn.commit()

    cur.close()
    conn.close()
    return

def add_to_ztable(newOrder):
    """
    Adds the items in the cart of the newOrder object to the ztable table in the database, along with the
    customization and price of each item.
    
    Parameters:
    newOrder (Order): The order object containing the cart items to add to the ztable.
    """
    conn = db_connection()
    cur = conn.cursor()
    
    for key in newOrder.cartItem:
        for value in newOrder.cartItem[key]:
            cur.execute("SELECT COUNT(*) FROM ztable")
            result = cur.fetchone()
            if result[0] == 0:
                num = 1
            else:
                cur.execute("SELECT id FROM ztable ORDER BY id DESC LIMIT 1")
                resultSet = cur.fetchall()
                num = resultSet[0][0] + 1

            customization = '{{{}}}'.format(','.join(['"{}"'.format(x) for x in value]))
            query = "INSERT INTO ztable (id, ordernumber, date, time, items, customization, price) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(
                num,
                newOrder.ordernumber,
                get_todaydate(),
                get_timestamp(),
                key,
                customization,
                str(round(newOrder.getPrice(key,value),2))
            )   
            print(query)
            cur.execute(query)
            conn.commit()

    cur.close()
    conn.close() 
    return

def add_ingredient(item):
    """
    Increments the quantity of the specified ingredient in the ingredients table in the database by 1.
    
    Parameters:
    item (str): The name of the ingredient to increment the quantity of.
    """
    conn = db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE ingredients SET Quantitiesperday = Quantitiesperday + 1 WHERE Ingredients = %s", (item,))
    conn.commit()
    cur.close()
    conn.close()

def remove_ingredient(item):
    """
    Decrements the quantity of the specified ingredient in the ingredients table in the database by 1.
    
    Parameters:
    item (str): The name of the ingredient to decrement the quantity of.
    """
    conn = db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE ingredients SET Quantitiesperday = Quantitiesperday - 1 WHERE Ingredients = %s", (item,))
    conn.commit()
    cur.close()
    conn.close()