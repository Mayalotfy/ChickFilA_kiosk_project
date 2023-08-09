from flask import Flask, render_template,request, redirect, url_for,session
from Summary import Summary 
import psycopg2
from collections import defaultdict
import ast
from app import app

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
    newOrder = Summary(cart_items)
    #Cartend
    return newOrder

@app.route('/kiosk')
def Start_Order():
    """
    This function retrieves the current cart using Summary class

    Returns:
        str: The renders to kiosk.html template with a Summary object representing the cart's contents
    """
    #Cartinfo
    newOrder = get_newOrder()
    #cart end
    return render_template('kiosk/kiosk.html',newOrder=newOrder )


@app.route('/categories')
def categories():
    """
    This function retrieves the current cart using Summary class

    Returns:
        str: The renders categories.html template with the categories and a Summary object representing the cart's contents
    """
    #Cartinfo
    newOrder = get_newOrder()
    #cart end
    conn = db_connection()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT category FROM items;")
    data = cur.fetchall()
    cur.close()
    # cur2 = conn.cursor()
    # cur2.execute(f"SELECT category, image FROM categoryImg;")
    # image = cur2.fetchall()
    # cur2.close()
    conn.close()
    #navbar contain
    # newOrder = Summary()
    return render_template('kiosk/categories.html', data=data, newOrder=newOrder )



@app.route("/kiosk/categories/<cat>")
def menu(cat):
    """
    This function retrieves the current cart using Summary class

    Args:
        cat (str): The category of menu items to retrieve from database

    Returns:
        str: The renders menu.html template with the menu items, categories, and a Summary object representing the cart's contents
    """
    #Cartinfo
    newOrder = get_newOrder()
    #cart end

    conn = db_connection()
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT category FROM items;")
    cats = cur.fetchall()
    cur.execute(f"SELECT item, price, images FROM items WHERE category='{cat}';")
    data = cur.fetchall()
    cur.close()
    conn.close()
    # navbar contain
    # newOrder = Summary()
    return render_template(
        "kiosk/menu.html", data=data, newOrder=newOrder, cats=cats, cur=cat
    )

@app.route("/kiosk/customization/<m>")
def customization(m):
    """
        This function retrieves the current cart using Summary class

    Args:
        m (str): The value of the <m> parameter in the URL.

    Returns:
        str: The renders customization.html template with the customizations of each item clicked, categories, and a Summary object representing the cart's contents
    """
    #Cartinfo
    newOrder = get_newOrder()
    #cart end

    print(request.args.get("cat", "Entrees"))
    conn = db_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT item, price, add, images FROM extras WHERE extracategory='{m}';")
    extra = cur.fetchall()
    cur.close()

    price = conn.cursor()
    price.execute(f"SELECT price FROM items WHERE item='{m}';")
    prices = price.fetchall()
    price.close()

    images = conn.cursor()
    images.execute(f"SELECT images FROM items WHERE item='{m}';")
    image = images.fetchall()
    images.close()

    cur2 = conn.cursor()
    if m.split()[-1] == "Salad":
        cur2.execute(f"SELECT item, price, images FROM items WHERE category='Dressings';")
    else:
        cur2.execute(f"SELECT item, price, images FROM items WHERE category='Sauces';")
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
    if menu == 'Grilled Chicken Cool Wrap':
        combo_extras.execute(f"SELECT item, price, image FROM combos WHERE category='ExtraWrap';")
    else:
        combo_extras.execute(f"SELECT item, price, image FROM combos WHERE category='ExtraSandwich';")
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
            "kiosk/customization.html",
            image=image,
            prices=prices,
            name=m,
            extra=extra,
            sauce=sauce,
            newOrder=newOrder,
            cur=cur,
        )
    elif (m.split()[-1] == "Combo"):
        if 'Nuggets' in (m.split()):
            return render_template(
                "kiosk/customizationN.html",
                image=image,
                prices=prices,
                name=m,
                newOrder=newOrder,
                combo_drinks=c_drinks,
                combo_sauces=c_sauces,
                combo_sides=c_sides,
                combo_extras=[],
                cur=cur,
            )
        else:
            return render_template(
                "kiosk/customizationN.html",
                image=image,
                prices=prices,
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
            "kiosk/customization.html",
            image=image,
            prices=prices,
            name=m,
            extra=extra,
            newOrder=newOrder,
            cur=cur,
        )


@app.route("/kiosk/sendToCart", methods=["POST", "GET"])
def sendToCart():
    """
    This function receives the POST request from customization.html and updates the cart using the Summary class.

    Returns:
        str: If the request is a POST, the function redirects to the /kiosk/checkout URL. If the request is a GET, the function renders the sendToCart.html template with the Summary object representing the cart's contents.
    
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


@app.route('/kiosk/receipt')
def receipt():
    """
    This function generates the receipt for the order placed using the cart data stored in the session.

    Returns:
        str: The renders receipt.html template with the order details and the total amount.
        Redirects to menu if the cart is empty.
    """
    print("hi")
    #Cartinfo
    newOrder = get_newOrder()
    #cart end
    return render_template('kiosk/receipt.html',newOrder=newOrder )


@app.route('/kiosk/payment')
def payment():
    """
    This function handles the payment process of the user's order.

    Returns:
        str: it renders the receipt.html template with the user's order information. 
    """
    #Cartinfo
    newOrder = get_newOrder()
    #cart end
    return render_template('kiosk/payment.html', newOrder=newOrder)


@app.route('/kiosk/confirmation')
def confirmation():
    """
    This function displays a confirmation page with ordernumber for the customer purchase.

    Returns:
        str: The rendered confirmation.html template
    """
    #Cartinfo
    newOrder = get_newOrder()
    #cart end
    lat = 30.61213892669398
    lng = -96.3414524265124
    
    newOrder.close()
    session.clear()
    return render_template('kiosk/confirmation.html',newOrder=newOrder, code_lat=lat, code_lng=lng)


@app.route('/remove_from_cart', methods=['POST']) 
def remove_from_cart(): 
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

    return render_template('kiosk/receipt.html',newOrder=newOrder )