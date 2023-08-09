#import psycopg2
import app
from flask import session,abort
from collections import defaultdict
import ast

class Summary:
    def __init__(self,cartItem):
        """
        Creates a Summary object with the following properties:
        - ordernumber: a unique order number
        - cartItem: a dictionary representing the items in the cart
        - total: the total cost of all items in the cart
        - tax: the tax on the total cost of all items in the cart
        - subtotal: the total cost of all items in the cart plus tax
        - Cart_num: the total number of items in the cart
        
        Args:
            cartItem (dict): a dictionary representing the items in the cart, with item names as keys and a list of selected extras as values
        """
        self.ordernumber = app.get_ordernumber()
        self.cartItem = cartItem
        self.total = self.get_total()
        self.tax = self.get_tax()
        self.subtotal = self.total +self.tax
        self.Cart_num = self.get_cartnum()
    
    def get_total(self): #returns total from Summary class
        total = 0.0
        for key in self.cartItem:
            for value in self.cartItem[key]:
                total += self.getPrice(key, value)
        print(total)
        return round(total, 2)
    
    def get_tax(self): #returns tax from Summary class
        return round(self.total* 0.03, 2)

    def get_cartnum(self): #returns cart num from Summary class
        num =0
        for key in self.cartItem:
            for value in self.cartItem[key]:
                num += 1
        print(num)
        return num
    
    def getPrice(self,key,value): 
        """
            Calculates the price of an item based on its key and value.

            :param key: The name of the item.
            :type key: str
            :param value: The list of values selected for the item.
            :type value: list
            :return: The total price of the item.
            :rtype: float
        """
        price = 0.0
        print(self.cartItem)
        #indivial price
        conn = app.db_connection()
        cur = conn.cursor()
        cur.execute("SELECT price FROM items WHERE item = %s", (key,))
        resultSet = cur.fetchall()
        if resultSet:
            price = resultSet[0][0]
        else:
            print("Product not found.")
        #print(price)
        #indivial
        
        isCombo = "combo" in key.lower()  
        if isCombo:
            key = key.replace("combo", "").strip()  
        for item in value:
            if item =="None":
                break
            elif isCombo:
                query = "SELECT price FROM combos WHERE item = %s"
                cur.execute(query, (item,))
            else: 
                query = "SELECT price FROM extras WHERE ExtraCategory = %s AND item = %s"
                cur.execute(query, (key, item))
            resultSet = cur.fetchall()
            for row in resultSet:
                price += row[0]
        cur.close()
        conn.close()
        
        return round(price, 2)
    
    def get_cartItem(self): #returns cartItems dictfrom Summary class
        return self.cartItem
      
    def close(self):
        """
        Clears the cart and updates the ingredients based on the cart items. Also adds the current cart to order history 
        and z-table.

        """
        ingredients = []
        for key in self.cartItem:
            isCombo = "combo" in key.lower()
            if isCombo:
                key = key.replace("combo", "").strip()
            ingredent_of_item = app.get_ingredients_from_item(key)
            ingredients.extend(ingredent_of_item)
            

        for ing in ingredients:
            print(ing)
            app.remove_ingredient(ing)

        for key in self.cartItem:
            for value in self.cartItem[key]:
                key_val = key
                if value == 'None':
                    break
                for item in value:
                    print(item)
                    value = app.get_add_value(key_val,item)
                if value == 1:  # add pickel
                    print(item)
                    app.remove_ingredient(item)
                elif value == 0:  # no pickel
                    print(item)
                    app.add_ingredient(item)
        if self.Cart_num != 0:
            print("adding to cart")
            app.add_to_history(self)
            app.add_to_ztable(self)

        self.cartItem.clear()
        self.subtotal = 0.0
        self.tax = 0.0
        self.Cart_num = 0
        return


def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function(*args, **kwargs) # Pass any arguments to decorated function
    wrapper.__name__ = function.__name__
    return wrapper
