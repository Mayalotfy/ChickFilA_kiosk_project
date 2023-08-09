from flask import Flask, render_template, redirect, url_for, request, session
from datetime import datetime
import psycopg2
import Summary 
from collections import defaultdict
from flask import session,abort
import ast
from app import app


def db_connection():
    conn = psycopg2.connect(
        host="csce-315-db.engr.tamu.edu",
        database="csce315331_iota",
        user="csce315331_iota_master",
        password="IOTA"
    )
    return conn
app.secret_key = "my_secret_key"



def get_newOrder():
    """
    This function retrieves the current cart from the user's session and returns
    a Summary object representing the cart's contents.

    Returns:
        Summary: A Summary object representing the cart's contents
    """
    #Cartinfo
    if 'cart' not in session:
        cart_items = defaultdict(list)
        session['cart'] = cart_items
        print("creating new")
    else:
        cart_items = session['cart']
        print("getting old session")
    print("In cart:")
    print(cart_items)
    newOrder = Summary.Summary(cart_items)
    #Cartend
    return newOrder
# Define a function to get the current timestamp



def get_timestamp():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Define a route for the server's dashboard page
@app.route('/server')
@Summary.login_is_required
def server():
    timestamp = get_timestamp()
    return render_template('server.html', timestamp=timestamp)


@app.route('/serverMenu')
@Summary.login_is_required
def serverMenu():
    return render_template('serverMenu.html')

@app.route('/serverCategories/<cat>')
@Summary.login_is_required
def serverMenuCat(cat):
    #cart end
    """
    This function retrieves the current cart using Summary class

    Args:
        cat (str): The category of menu items to retrieve from database

    Returns:
        str: The renders serverMenuCat.html template with the menu items, categories, and a Summary object representing the cart's contents
    """
    newOrder = get_newOrder()
    conn = db_connection()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT category FROM items;")
    cats = cur.fetchall()
    cur.execute(f"SELECT item, price, images FROM items WHERE category='{cat}';")
    data = cur.fetchall()
    cur.close()
    # navbar contain
    # newOrder = Summary()
    conn.close()
    # navbar contain
    # newOrder = Summary()
    return render_template(
        "serverMenuCat.html", data=data, newOrder=newOrder, cats=cats, cur=cat
    )


    


@app.route("/serverCustomization/<m>")
@Summary.login_is_required
def serverCustomization(m):
    """
        This function retrieves the current cart using Summary class

    Args:
        m (str): The value of the <m> parameter in the URL.

    Returns:
        str: The renders serverCustomization.html template with the customizations of each item clicked, categories, and a Summary object representing the cart's contents
    """
    #Cartinfo
    newOrder = get_newOrder()
    print(request.args.get("cat", "Entrees"))
    conn = db_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT item, price, add FROM extras WHERE extracategory='{m}';")
    extra = cur.fetchall()
    cur.close()

    images = conn.cursor()
    images.execute(f"SELECT images FROM items WHERE item='{m}';")
    image = images.fetchall()
    images.close()

    cur2 = conn.cursor()
    if m.split()[-1] == "Salad":
        cur2.execute(f"SELECT item, price FROM items WHERE category='Dressings';")
    else:
        cur2.execute(f"SELECT item, price FROM items WHERE category='Sauces';")
    sauce = cur2.fetchall()
    cur2.close()

    combo_drinks = conn.cursor()
    combo_drinks.execute(f"SELECT item, price, image FROM combos WHERE category='Drinks';")
    c_drinks = combo_drinks.fetchall()
    combo_drinks.close()
    combo_sauces = conn.cursor()
    combo_sauces.execute(f"SELECT item, price, image FROM combos WHERE category='Sauces';")
    c_sauces = combo_sauces.fetchall()
    combo_sauces.close()
    combo_sides = conn.cursor()
    combo_sides.execute(f"SELECT item, price, image FROM combos WHERE category='Sides';")
    c_sides = combo_sides.fetchall()
    combo_sides.close()
    menu = ' '.join(m.split()[:-1])
    combo_extras = conn.cursor()
    combo_extras.execute(f"SELECT item, price, add FROM extras WHERE extracategory='{menu}';")
    c_extras = combo_extras.fetchall()
    combo_extras.close()
    conn.close()

    # newOrder.cartItem['Brownie'].append([])
    cur = request.args.get("cat", "Entrees")
    if (
        m.split()[-1] == "Salad"
        or m.split()[-1] == "Sandwich"
        or m.split()[-1] == "Nuggets"
        or m.split()[-1] == "Wrap"
    ):
        return render_template(
            "serverCustomization.html",
            image=image,
            name=m,
            extra=extra,
            sauce=sauce,
            newOrder=newOrder,
            cur=cur,
        )
    elif (m.split()[-1] == "Combo"):
        return render_template(
            "serverCustomization.html",
            image=image,
            name=m,
            newOrder=newOrder,
            combo_drinks=c_drinks,
            combo_sauces=c_sauces,
            combo_sides=c_sides,
            combo_extras=c_extras,
            cur=cur,
        )
    else:
        return render_template(
            "serverCustomization.html",
            image=image,
            name=m,
            extra=extra,
            newOrder=newOrder,
            cur=cur,
        ) 
    
    
# def sendServerCustom(newOrder, m, lst):
#     newOrder.cartItem[m].append(lst)


@app.route('/serverReceipt')
@Summary.login_is_required
def serverReceipt():
    #navbar contain
    """
    This function generates the receipt for the order placed using the cart data stored in the session.

    Returns:
        str: The renders serverReceipt.html template with the order details and the total amount.
        Redirects to serverMenuCat if the cart is empty.
    """
    newOrder = get_newOrder()
    return render_template('serverReciept.html',newOrder=newOrder )

@app.route('/serverPayment')
@Summary.login_is_required
def serverPayment():
    """
    This function handles the payment process of the server's order.

    Returns:
        str: it renders the serverPayment.html template with the user's order information. 
    """
    newOrder = get_newOrder()
    return render_template('serverPayment.html', newOrder=newOrder)

@app.route('/serverConfirmation')
@Summary.login_is_required
def serverConfirmation():
    """
    This function displays a confirmation page with ordernumber for the server's order for the customer.

    Returns:
        str: The rendered serverConfirmation.html template
    """
    newOrder = get_newOrder()
    lat = 30.61213892669398
    lng = -96.3414524265124
    newOrder.close()
    session.pop("cart")
    return render_template('serverConfirmation.html',newOrder=newOrder, code_lat=lat, code_lng=lng)

@app.route('/removeFromServerCart', methods=['POST']) 
@Summary.login_is_required
def removeFromServerCart(): 
    """
    This function handles the removal of an item from the cart

    Returns:
        str: A JSON response indicating the success or failure of the operation
    """
    value = eval(request.form.get('value'))
    key = request.form.get('key') 
    #Cartinfo
    cart_items = session.get('cart', defaultdict(list))
    
    if key in cart_items:
        cart_items[key].remove(value)
        session['cart'] = cart_items
        print("Removed from cart")
    else:
        print("key not found")
    
    newOrder = get_newOrder()
    #Cartend

    return render_template('serverMenuCat.html',newOrder=newOrder )

@app.route("/sendToServerCart", methods=["POST", "GET"])
@Summary.login_is_required
def sendToServerCart():
    """
    This function receives the POST request from serverCustomization.html and updates the cart using the Summary class.

    Returns:
        str: If the request is a POST, the function redirects to the /serverCheckout URL. If the request is a GET, the function renders the sendToServerCart.html template with the Summary object representing the cart's contents.
    
    """
    data = request.get_json()
    # data is the dictionary from javascript
    print(data)
    m = data["name"]
    data.pop("name")
    lst = []
    for key, val in data.items():
        for i in range(val):
            lst.append(key)
    if len(lst) == 0:
        lst.append("None")
    # newOrder = Summary()

    #Cartinfo
    cart_items = defaultdict(list)
    cart_items = session.get('cart', defaultdict(list))
    print(type(cart_items))
    
    if m in cart_items:
        cart_items[m].append(lst)
    else:
        cart_items[m] = [lst]
    session['cart'] = cart_items
    cart_items = session.get('cart', defaultdict(list))
    print("Added to cart")
    print(cart_items)
    #Cartend

    #newOrder.add_to_cartItem(m, lst)
    return {}

@app.route('/serverOrders')
@Summary.login_is_required
def serverOrders():
        """
        This function retrieves the order history from the database

        Returns:
            str: The function renders serverOrders.html template with the order history items from the database
        """
        conn = db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM orderhistory")
        data = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('serverOrders.html', data=data)

@app.route('/serverContacts')
@Summary.login_is_required
def serverContacts():
        """
        This function retrieves the contacts from the database

        Returns:
            str: The function renders serverContacts.html template with the items from the database
        """
    
        conn = db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM contacts ORDER BY id")
        data = cur.fetchall()
        cur.close()
        conn.close()
        return render_template('serverContacts.html', data=data)
    
@app.route('/addServerContact', methods=['POST'])
@Summary.login_is_required
def addServerContact():
    """
        This function adds itemws to the contacts table in the database

        Returns:
            str: The function redirects to ServerContacts.html template
    """
    conn = db_connection()
    cur = conn.cursor()
    id = int(request.form['id'])
    name = request.form['name']
    category = request.form['category']
    onCampusDialing = request.form['onCampusDialing']
    offCampusDialing = request.form['offCampusDialing']
    cur.execute("INSERT INTO contacts (id, name, category, OnCampusDialing, OffCampusDialingl) VALUES (%s, %s, %s, %s, %s)", (id, name, category, onCampusDialing, offCampusDialing))
    conn.commit()
    conn.close()
    return redirect(url_for('serverContacts'))

@app.route('/removeServerContact', methods=['POST'])
@Summary.login_is_required
def removeServerContact():
    """
        This function removes itemws to the contacts table in the database

        Returns:
            str: The function redirects to ServerContacts.html template
    """
    contact_id = int(request.form['contact_id'])
    conn = db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM contacts WHERE id=%s", (contact_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('serverContacts'))


@app.route('/updateServerContact', methods=['POST'])
@Summary.login_is_required
def updateServerContact():
    """
        This function updates itemws to the contacts table in the database

        Returns:
            str: The function redirects to ServerContacts.html template
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
    return redirect(url_for('serverContacts'))


