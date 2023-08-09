from flask import Flask, render_template,request, redirect, url_for
import Summary
import time

from datetime import datetime
import psycopg2

from app import app

# Define a function to get the current timestamp
def get_timestamp():
    """
    This function returns timestamp to be saved during login
    
    
    """
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

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


#route for the manager's dashboard page
@app.route('/manager')
@Summary.login_is_required
def manager_dashboard():
    """
    This function calls on the manager_dashboard to be displayed

    Returns:
        render html file to go to the manager's dashboard
    """
    timestamp = get_timestamp()
    return render_template('manager_dashboard.html', timestamp=timestamp)

# routes for each block
@app.route('/items')
@Summary.login_is_required

#@login_is_required
def items():
    """
    This function calls on items to be displayed where it access the database and displays the table items

    Returns:
        render html file to go to the items page
    """
    conn = db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM items ORDER BY ItemId")
    data = cur.fetchall()
    cur.close()
    conn.close()

    # Render the items template
    return render_template('items.html', data=data)

@app.route('/add_item', methods=['POST'])
@Summary.login_is_required

#@login_is_required
def add_item():

    """
    This function is called whenever the manager is trying to add an item by pressing on the button Add Item.
    It needs to connect to the database to insert new item.

    Returns:
        redirect html file to update items page
    """
    # Get the new contact's details from the form
    conn = db_connection()
    cur = conn.cursor()
    id = int(request.form['id'])
    category = request.form['category']
    item = request.form['item']
    price = float(request.form['price'])
    cur.execute("INSERT INTO items (ItemId, Category, Item, Price) VALUES (%s, %s, %s, %s)", (id, category, item, price))

    conn.commit()
    conn.close()
    return redirect(url_for('items'))
    

@app.route('/remove_item', methods=['POST'])
@Summary.login_is_required

#@login_is_required
def remove_item():
    """
    This function is called whenever the manager is trying to remove an item by pressing on the button Remove.
    It needs to connect to the database to remove existing item.

    Returns:
        redirect html file to update items page
    """
    item_id = int(request.form['item_id'])
    conn = db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM items WHERE ItemID = %s", (item_id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('items'))

@app.route('/update_item', methods=['POST'])
@Summary.login_is_required

#@login_is_required
def update_item():
    """
    This function is called whenever the manager is trying to update an item by pressing on the button Update.
    It needs to connect to the database to update the information of existing item.

    Returns:
        redirect html file to update items page
    """
    item_id = int(request.form['item_id'])
    category = request.form['category']
    item = request.form['item']
    price = float(request.form['price'])
    conn = db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE items SET Category = %s, Item = %s, Price = %s WHERE ItemID = %s", (category, item, price, item_id))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('items'))


@app.route('/add_ingredient_item', methods=['POST'])
@Summary.login_is_required

#@login_is_required
def add_ingredient_item():
    """
    This function is called whenever the manager is trying to add a new ingredient to the corresponding item.
    It needs to connect to the database to add the new ingredient in the inventory table

    Returns:
        redirect html file to update items page
    """
    # Get the new contact's details from the form
    conn = db_connection()
    cur = conn.cursor()
    id = int(request.form['id'])
    category = request.form['category']
    ingredient = request.form['ingredient']
    quantity=int(request.form['quantity'])
    full= int(request.form['full'])
    low= int(request.form['low'])
    cur.execute("INSERT INTO ingredients (IngredientsID, categories, ingredients, quantitiesperday , fullstock, lowstock) VALUES (%s, %s, %s, %s, %s, %s)", (id, category, ingredient, quantity, full, low))
    conn.commit()
    conn.close()
    return redirect(url_for('items'))

@app.route('/ingredients')
@Summary.login_is_required

#@login_is_required
def ingredients():
    """
    This function calls on ingredients to be displayed where it access the database and displays the table inventory

    Returns:
        render html file to go to the ingredients page
    """
    conn = db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM ingredients ORDER BY IngredientsID")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('ingredients.html', data=data)

@app.route('/add_ingredient', methods=['POST'])
@Summary.login_is_required

#@login_is_required
def add_ingredient():
    """
    This function is called whenever the manager is trying to add an ingredients by pressing on the button Add Ingredient.
    It needs to connect to the database to insert new ingredient.

    Returns:
        redirect html file to update inventory page
    """
    # Get the new contact's details from the form
    conn = db_connection()
    cur = conn.cursor()
    id = int(request.form['id'])
    category = request.form['category']
    ingredient = request.form['ingredient']
    quantity=int(request.form['quantity'])
    full= int(request.form['full'])
    low= int(request.form['low'])
    cur.execute("INSERT INTO ingredients (IngredientsID, categories, ingredients, quantitiesperday , fullstock, lowstock) VALUES (%s, %s, %s, %s, %s, %s)", (id, category, ingredient, quantity, full, low))
    conn.commit()
    conn.close()
    return redirect(url_for('ingredients'))

@app.route('/remove_ingredient', methods=['POST'])
@Summary.login_is_required

#@login_is_required
def remove_ingredient():
    """
    This function is called whenever the manager is trying to remove an ingredient by pressing on the button Remove Ingredient.
    It needs to connect to the database to remove existing ingredient.

    Returns:
        redirect html file to update inventory page
    """
    ingredient_id = int(request.form['ingredient_id'])
    conn = db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM ingredients WHERE IngredientsID = %s", (ingredient_id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('ingredients'))

@app.route('/update_ingredient', methods=['POST'])
@Summary.login_is_required

#@login_is_required
def update_ingredient():
    """
    This function is called whenever the manager is trying to update an ingredient by pressing on the button Update.
    It needs to connect to the database to update an existing ingredient.

    Returns:
        redirect html file to update inventory page
    """
    ingredient_id = int(request.form['ingredient_id'])
    category = request.form['category']
    ingredient = request.form['ingredient']
    quantity=int(request.form['quantity'])
    full= int(request.form['full'])
    low= int(request.form['low'])
    conn = db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE ingredients SET categories = %s, ingredients = %s, quantitiesperday = %s , fullstock =%s, lowstock = %s WHERE IngredientsID = %s", (category, ingredient, quantity, full, low, ingredient_id))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('ingredients'))


@app.route("/restock")
@Summary.login_is_required

#@login_is_required
def restock():
    """
    This function is called whenever the manager is trying to retrieve the restock report of the inventory where items are low in stock.
    Returns:
        redirect html file to restock report page to display the table
    """
    conn = db_connection()
    cur = conn.cursor()
    cur.execute("SELECT IngredientsId, categories, ingredients, quantitiesperday FROM ingredients GROUP BY IngredientsId HAVING quantitiesperday < lowstock;")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("restock.html", data=data)

@app.route('/restock/complete', methods=['POST'])
@Summary.login_is_required

#@login_is_required
def complete_restock():
    """
    This function is called whenever the manager is trying to restock a certain ingredient if it's low on stock and the button Restock is pressed.
    Returns:
        redirect html file to restock report page to display the table and it shows that 
        the ingredient no longer exists since it has been restocked.
    """
    conn = db_connection()
    cur = conn.cursor()
    id = int(request.form['ingredientId'])
    quantity = int(request.form['quantity'])
    cur.execute("UPDATE ingredients SET quantitiesperday = %s WHERE IngredientsID = %s", (quantity, id))
    conn.commit()
    cur.close()
    conn.close()

    return redirect(url_for('restock'))

@app.route('/excess_sale')
@Summary.login_is_required

#@login_is_required
def excess_sale():
    """
    This function is called whenever the manager is trying to retrieve the excess report of the inventory where items are full in stock.
    Returns:
        redirect html file to excess report page to display the table
    """
    conn = db_connection()
    cur = conn.cursor()
    cur.execute("SELECT ingredientsid, categories, ingredients, quantitiesperday FROM ingredients GROUP BY ingredientsid HAVING quantitiesperday > fullstock*.9")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('excess.html', data=data)

@app.route('/orders')
@Summary.login_is_required

#@login_is_required
def orders():
    """
    This function calls on the order hisory to be displayed where it access the database and displays the table orders

    Returns:
        render html file to go to the orders page
    """
    conn = db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM orderhistory")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('orders.html', data=data)

@app.route('/refund_order', methods=['POST'])
@Summary.login_is_required

#@login_is_required
def refund_order():
    """
    This function is called whenever the manager is trying to refund an order from orderhistory by pressing on the button Refund.
    Returns:
        redirect html file to orderhistory to display the table 
        where the item that has been refunded is added but with a negative price
    """
    conn = db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM orderhistory ORDER BY id DESC LIMIT 1")
    last_id = cur.fetchone()[0]
    
    # increment the last id to get the new id
    new_id = last_id + 1
    current_date = datetime.now().strftime("%m/%d/%Y")
    current_time = datetime.now().strftime("%H:%M:%S")
    order_id = request.form['order_id']
    cur.execute("SELECT * FROM orderhistory WHERE id = %s", (order_id,))
    data = cur.fetchone()
    new_price=-data[6]
    cur.execute("INSERT INTO orderhistory (id,ordernumber, date, time, items, customization, price) VALUES (%s,%s, %s, %s, %s, %s, %s)", (new_id, data[1], current_date, current_time, data[4], data[5], new_price) )
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('orders'))



@app.route('/retrieve-report', methods=['POST'])
@Summary.login_is_required

#@login_is_required
def retrieve_report():
    """
    This function is called whenever the manager is trying to retrieve the sales report from orderhistory 
    where he can see the sales of a certain day.
    Returns:
        redirect html file to sales report page to display the table
    """
    conn = db_connection()
    cur = conn.cursor()
    date = request.form['date']
    start_time = request.form['startTime']
    end_time = request.form['endTime']
    
    # Query the database for the report data using the date and time frame
    cur.execute("SELECT * FROM orderhistory WHERE date = %s AND time BETWEEN %s AND %s", (date, start_time, end_time))
    data = cur.fetchall()
    
    cur.close()
    conn.close()

    # Render the orders template with the retrieved data
    return render_template('sales_report.html', data=data)



@app.route('/employees')
@Summary.login_is_required

#@login_is_required
def employees():
    """
    This function calls on employees to be displayed where it access the database and displays the table employees

    Returns:
        render html file to go to the employees page
    """
    conn = db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM employees ORDER BY EmployeeUIN")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('employees.html', data=data)

@app.route('/add_employee', methods=['POST'])
@Summary.login_is_required

#@login_is_required
def add_employee():
    """
    This function is called whenever the manager is trying to add an employee by pressing on the button Add Employee.
    It needs to connect to the database to insert new employee.

    Returns:
        redirect html file to update employees page
    """
    # Get the new contact's details from the form
    conn = db_connection()
    cur = conn.cursor()
    id = request.form['UIN']
    name = request.form['name']
    number = request.form['number']
    email = request.form['email']
    HoursWorkedPerWeek = int(request.form['HoursWorkedPerWeek'])
    SalaryPerWeek= float(request.form['SalaryPerWeek'])
    cur.execute("INSERT INTO employees (EmployeeUIN, name, PhoneNumber, Email, HoursWorkedPerWeek, SalaryPerWeek) VALUES (%s, %s, %s, %s, %s, %s)", (id, name, number, email, HoursWorkedPerWeek, SalaryPerWeek))
    conn.commit()
    conn.close()
    return redirect(url_for('employees'))


@app.route('/remove_employee', methods=['POST'])
@Summary.login_is_required

#@login_is_required
def remove_employee():
    """
    This function is called whenever the manager is trying to remove an employee by pressing on the button Remove.
    It needs to connect to the database to remove new employee.

    Returns:
        redirect html file to update employees page
    """
    # Connect to database
    employee_id = (request.form['employee_id'])
    conn = db_connection()
    cur = conn.cursor()
    # Delete contact from database
    cur.execute("DELETE FROM employees WHERE EmployeeUIN=%s ::text", (employee_id,))
    conn.commit()

    # Close database connection
    conn.close()
    return redirect(url_for('employees'))

@app.route('/update_employee', methods=['POST'])
@Summary.login_is_required

#@login_is_required
def update_employee():
    """
    This function is called whenever the manager is trying to update the information of an employee by pressing on the button Update.
    It needs to connect to the database to update the information of an existing employee.

    Returns:
        redirect html file to update employees page
    """
    employee_id = (request.form['employee_id'])
    name = request.form['name']
    number = request.form['number']
    email = request.form['email']
    HoursWorkedPerWeek = int(request.form['HoursWorkedPerWeek'])
    SalaryPerWeek= float(request.form['SalaryPerWeek'])
    conn = db_connection()
    cur = conn.cursor()

    cur.execute("UPDATE employees SET name = %s,  PhoneNumber= %s, Email = %s , HoursWorkedPerWeek =%s, SalaryPerWeek = %s WHERE EmployeeUIN = %s", (name, number, email, HoursWorkedPerWeek, SalaryPerWeek, employee_id))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('employees'))


@app.route('/contacts')
@Summary.login_is_required

#@login_is_required
def contacts():
    """
    This function calls on emergency contacts to be displayed where it access the database and displays the table contacts

    Returns:
        render html file to go to the contacts page
    """
    conn = db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM contacts ORDER BY id")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('contacts.html', data=data)

# Define route for adding a new contact
@app.route('/add_contact', methods=['POST'])
@Summary.login_is_required

#@login_is_required
def add_contact():
    """
    This function is called whenever the manager is trying to add a contact by pressing on the button Add Contact.
    It needs to connect to the database to insert new Contact.

    Returns:
        redirect html file to update contacts page
    """
    # Get the new contact's details from the form
    conn = db_connection()
    cur = conn.cursor()
    id = int(request.form['id'])
    name = request.form['name']
    category = request.form['category']
    on_campus_dialing = request.form['on_campus_dialing']
    off_campus_dialing = request.form['off_campus_dialing']
    cur.execute("INSERT INTO contacts (id, name, category, OnCampusDialing, OffCampusDialingl) VALUES (%s, %s, %s, %s, %s)", (id, name, category, on_campus_dialing, off_campus_dialing))
    conn.commit()
    conn.close()
    return redirect(url_for('contacts'))

@app.route('/remove_contact', methods=['POST'])
@Summary.login_is_required

#@login_is_required
def remove_contact():
    """
    This function is called whenever the manager is trying to remove a contact by pressing on the button Remove.
    It needs to connect to the database to remove existing Contact.

    Returns:
        redirect html file to update contacts page
    """
    # Connect to database
    contact_id = int(request.form['contact_id'])
    conn = db_connection()
    cur = conn.cursor()
    # Delete contact from database
    cur.execute("DELETE FROM contacts WHERE id=%s", (contact_id,))
    conn.commit()

    # Close database connection
    conn.close()
    return redirect(url_for('contacts'))

@app.route('/update_contact', methods=['POST'])
@Summary.login_is_required

#@login_is_required
def update_contact():
    """
    This function is called whenever the manager is trying to update an existing contact by pressing on the button Update.
    It needs to connect to the database to update the existing Contact.

    Returns:
        redirect html file to update contacts page
    """
    contact_id = int(request.form['contact_id'])
    name = request.form['name']
    category = request.form['category']
    on_campus_dialing = request.form['on_campus_dialing']
    off_campus_dialing = request.form['off_campus_dialing']
    conn = db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE contacts SET name = %s,  category = %s, OnCampusDialing = %s, OffCampusDialingl = %s WHERE id = %s", (name, category, on_campus_dialing, off_campus_dialing, contact_id))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('contacts'))




@app.route('/vendors')
@Summary.login_is_required

#@login_is_required
def vendors():
    """
    This function calls on vendors to be displayed where it access the database and displays the table vendors

    Returns:
        render html file to go to the vendors page
    """
    conn = db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM vendors ORDER BY Name")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('vendors.html', data=data)

@app.route('/add_vendor', methods=['POST'])
@Summary.login_is_required

#@login_is_required
def add_vendor():
    """
    This function is called whenever the manager is trying to add a new vendor by pressing on the button Add Vendor.
    It needs to connect to the database to insert new vendor.

    Returns:
        redirect html file to update vendors page
    """
    # Get the new contact's details from the form
    conn = db_connection()
    cur = conn.cursor()
    id = int(request.form['id'])
    name = request.form['name']
    categories = request.form['categories']
    ingredients = request.form['ingredients']
    cur.execute("INSERT INTO vendors (VendorsId, Name, Categories, Ingredients) VALUES (%s, %s, %s, %s)", (id, name, categories, ingredients))
    conn.commit()
    conn.close()
    return redirect(url_for('vendors'))

@app.route('/remove_vendor', methods=['POST'])
@Summary.login_is_required

#@login_is_required
def remove_vendor():
    """
    This function is called whenever the manager is trying to remove a vendor by pressing on the button Remove.
    It needs to connect to the database to remove vendor.

    Returns:
        redirect html file to update vendors page
    """
    # Connect to database
    vendor_id = int(request.form['vendor_id'])
    conn = db_connection()
    cur = conn.cursor()
    # Delete contact from database
    cur.execute("DELETE FROM vendors WHERE VendorsId=%s", (vendor_id,))
    conn.commit()

    # Close database connection
    conn.close()
    return redirect(url_for('vendors'))

@app.route('/update_vendor', methods=['POST'])
@Summary.login_is_required

#@login_is_required
def update_vendor():
    """
    This function is called whenever the manager is trying to update the information of an existing vendor by pressing on the button Update.
    It needs to connect to the database to update vendor.

    Returns:
        redirect html file to update vendors page
    """
    vendor_id = (request.form['vendor_id'])
    name = request.form['name']
    categories = request.form['categories']
    ingredients = request.form['ingredients']
    conn = db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE vendors SET Name = %s,  Categories = %s, Ingredients = %s WHERE VendorsId = %s", (name, categories, ingredients,vendor_id))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('vendors'))

@app.route('/x_z_reports')
@Summary.login_is_required

#@login_is_required
def x_z_reports():
    """
    This function calls on X and Z reports to be displayed where it access the database and displays the tables
    if the corresponding buttons have been pressed

    Returns:
        render html file to go to ztable
    """
    conn = db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM ztable")
    data = cur.fetchall()
    # check which button was pressed
    if request.args.get('report') == 'z_report':
        # delete data from the database
        time.sleep(1.1)
        cur.execute("DELETE FROM ztable")
        conn.commit()
        data = []
    cur.close()
    conn.close()

    return render_template('x_z_reports.html', data=data)


