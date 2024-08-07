import random
import getpass
import admin
from prettytable import PrettyTable

isUPI = False

class Item:
    def __init__(self, name, category, _cost_price, original_price, selling_price, is_discounted, item_code):
        self.name = name
        self.category = category
        self.cost_price = _cost_price
        self.original_price = original_price
        self.selling_price = selling_price
        self.is_discounted = is_discounted
        self.item_code = item_code

    def discount(self, discount_percentage):
        self.selling_price = self.original_price - self.original_price * (discount_percentage / 100)

    def profit(self):
        if not self.is_discounted:
            return 0
        else:
            return self.original_price - self.selling_price
    
    def __str__(self):
        return f"{self.name}, {self.category}, {self.cost_price}, {self.original_price}, {self.selling_price}, {self.is_discounted}, {self.item_code}"

    def return_list_notadmin(self):
        return [self.name, self.category, self.original_price, self.selling_price, self.item_code]

    def return_list(self):
        return [self.name, self.category, self.cost_price, self.original_price, self.selling_price, self.item_code, round(self.selling_price - self.cost_price, 2)]

class Market:
    def __init__(self, items={}):
        self.__available_items = items

    def add_item(self, item):
        if item.category in self.__available_items:
            self.__available_items[item.category].append(item)
        else:
            self.__available_items[item.category] = [item]

    def remove_item(self, item):
        self.__available_items.remove(item)

    def all_items(self):
        return (self.__available_items.values())

    def category_items(self):
        return self.__available_items

    def search_by_name(self, name):
        for list_item in self.__available_items.values():
            for item in list_item:
                if item.name == name:
                    return item
        return None

    def search_by_code(self, code):
        for list_item in self.__available_items.values():
            for item in list_item:
                if item.item_code == code:
                    return item
        return None

class General_customer:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.__cart = {}

    def add_to_cart(self, item, quantity):
        self.__cart[item] = quantity

    def view_cart(self):
        return self.__cart

    def remove_from_cart(self, item):
        self.__cart.pop(item)

    def total_profit(self):
        total = 0
        for item in self.__cart:
            total += item.profit()
        return total

class Student(General_customer):
    def __init__(self, id, name, room_number):
        super().__init__(id, name)
        self.room_number = room_number

class Non_SWD_Customer(General_customer):
    def __init__(self, id, name, isUPI):
        super().__init__(id, name)
        self.mode_of_payment = "UPI" if isUPI else "CASH"

def view_market(market_obj):
    table = PrettyTable(["Name", "Category", "Original Price", "Price", "Item Code"])
    for list_item in market_obj.all_items():
        for item in list_item:
            table.add_row(Item.return_list_notadmin(item))
    return table

def check_item_code(item_code, market_obj):
    for list_item in market_obj.all_items():
        for item in list_item:
            list = Item.return_list_notadmin(item)
            if item_code == list[4]:
                return [True, item]
            else:
                continue
    return False

def view_cart(customer, table, only_view=False):
    total = 0
    discount = 0
    keys = list((customer.view_cart()).keys())
    values = list((customer.view_cart()).values())
    for i in range (0, len(keys), 1):
        if not only_view:
            table.add_row([keys[i].name, keys[i].item_code, values[i], values[i]*keys[i].original_price, values[i]*keys[i].selling_price])
            total = total + values[i]*keys[i].selling_price
            discount = discount - values[i]*(keys[i].selling_price - keys[i].original_price)
    print (table)
    print ("Current total price is: ₹", total)
    return [total, discount]
        
def delete_from_cart(customer, item_code, cur_total):
    list = []
    item_list = []
    for item in customer.view_cart().keys():
        list.append(Item.return_list_notadmin(item))
        item_list.append(item)
    for j in range(0, len(list), 1):    
        if item_code.upper() == list[j][4]:
            qty = list(customer.view_cart().values())[j]
            customer.remove_from_cart(item_list[j])
            cur_total = cur_total - list[j][3]*qty
            return (customer, cur_total)
        else:
            continue
    return False

def admin_views(market_obj):
    table = PrettyTable(["Name", "Category", "Cost Price",  "Original Price", "Selling Price", "Item Code", "Profit per item"])
    for list_item in market_obj.all_items():
        for item in list_item:
            table.add_row(Item.return_list(item))
    return table

def search(option, param):
    if option == 1:
        pass
    else:
        pass
    
def login():
    global isUPI
    check_login = True
    while check_login:
        admin_check = int(input(("Would you like to login as a customer (1) or an administrator (2)?: ")))
        if admin_check == 1:
            id = str(input("Enter your BITS ID: "))
            name = str(input("Enter your name: "))
            check_SWD = True
            while check_SWD:
                SWD_check = str(input(f"Hello {name}, would you like to pay with your SWD account? (Y/N): "))
                if SWD_check.upper() == "Y":
                    room_number = str(input("Enter your room number: "))
                    return ["SWD", id, name, room_number]
                elif SWD_check.upper() == "N":
                    payment_check = True
                    while payment_check:
                        payment_method = int(input("Would you like to pay using UPI (1) or Cash (2)?: "))
                        if payment_method == 1:
                            isUPI = True
                            return ["no_SWD", id, name]
                        elif payment_method == 2:
                            isUPI = False
                            return ["no_SWD", id, name]
                        else:
                            print ("Invalid input. Try again.\n")
                            payment_check = True
                else:
                    print ("Invalid input. Try again.\n")
                    check_SWD = True
        elif admin_check == 2:
            username = str(input("Enter the administrator username: "))
            pwd = getpass.getpass("Enter the password (hidden for privacy): ")
            if username == admin.admin_username and pwd == admin.admin_password:
                return "admin"
            else:
                print ("Incorrect credentials entered")
                return 0
        else:
            print ("Invalid input. Try again.\n")
            admin_check = True

def view_products(market_obj):
    table = PrettyTable(["Name", "Category", "Original Price", "Price", "Item Code"])
    for list_item in market_obj.all_items():
        for item in list_item:
            table.add_row(Item.return_list_notadmin(item))
    return table

def item_code(item_code, market_obj):
    for list_item in market_obj.all_items():
        for item in list_item:
            list = Item.return_list_notadmin(item)
            if item_code == list[4]:
                return [True, item]
            else:
                continue
    return False

def view_cart(customer, table, only_view=False):
    total = 0
    discount = 0
    keys = list((customer.view_cart()).keys())
    values = list((customer.view_cart()).values())
    for x in range (0, len(keys), 1):
        if not only_view:
            table.add_row([keys[x].name, keys[x].item_code, values[x], values[x]*keys[x].original_price, values[x]*keys[x].selling_price])
            total = total + values[x]*keys[x].selling_price
            discount = discount - values[x]*(keys[x].selling_price - keys[x].original_price)
    print (table)
    print ("Current total price is: ", total)
    return [total, discount]

def remove_from_cart(customer, item_code, cur_total):
    list = []
    item_list = []
    for item in customer.view_cart().keys():
        list.append(Item.return_list_notadmin(item))
        item_list.append(item)
    for z in range(0, len(list), 1):    
        if item_code.upper() == list[z][4]:
            qty = list(customer.view_cart().values())[z]
            customer.remove_from_cart(item_list[z])
            cur_total = cur_total - list[z][3]*qty
            return (customer, cur_total)
        else:
            continue
    return False

def admin_views(is_admin, market_obj):
    table = PrettyTable(["Name", "Category", "Cost Price",  "Original Price", "Selling Price", "Item Code", "Profit per item"])
    for list_item in market_obj.all_items():
        for item in list_item:
            table.add_row(Item.return_list(item))
    return table

discount = 0
cur_item = None
akshay = Market()
i1f = Item("Uncle Chips", "Food", 15, 20, 20, True, "F1")
i2f = Item("Kissan Tomato Ketchup", "Food", 100, 105, 105, True, "F2")
i3f = Item("Jim Jam Treat", "Food", 30, 35, 35, True, "F3")
i4f = Item("Jeera Cookies", "Food", 75, 80, 80, True, "F4")
i5f = Item("Dairy Milk Silk", "Food", 150, 160, 160, True, "F5")
food = [i1f, i2f, i3f, i4f, i5f]
for v in range(0, len(food), 1):
    cur_item = food[v]
    discount = random.randrange(0, 10)
    cur_item.discount(discount)
    akshay.add_item(cur_item)

i1c = Item("USPA - Polo T Shirt", "Clothes", 450, 500, 500, True, "C1")
i2c = Item("Van Heusen Sweatshirt", "Clothes", 1000, 1200, 1200, True, "C2")
i3c = Item("Angora Wool Gloves", "Clothes", 350, 400, 400, True, "C3")
i4c = Item("Jockey - Pack of 3 Men's brief", "Clothes", 700, 750, 750, True, "C4")
i5c = Item("Levis - Track pant", "Clothes", 1200, 1300, 1300, True, "C5")
clothes = [i1c, i2c, i3c, i4c, i5c]
for z in range(0, len(clothes), 1):
    cur_item = clothes[z]
    discount = random.randrange(0, 15)
    cur_item.discount(discount)
    akshay.add_item(cur_item)

i1m = Item("Nebulizer", "Medicines", 250, 270, 270, True, "M1")
i2m = Item("Sanitizer", "Medicines", 70, 75, 75, True, "M2")
i3m = Item("Dettol", "Medicines", 100, 100, 100, True, "M3")
i4m = Item("Band-Aid", "Medicines", 15, 15, 15, True, "M4")
i5m = Item("Paracetamol", "Medicines", 80, 90, 90, True, "M5")
stationery = [i1m, i2m, i3m, i4m, i5m]
for y in range(0, len(stationery), 1):
    cur_item = stationery[y]
    discount = random.randrange(0, 1)
    cur_item.discount(discount)
    akshay.add_item(cur_item)

i1t = Item("Surf Excel - Liquid detergent", "Toiletries", 60, 65, 65, True, "T1")
i2t = Item("Pears Gel Bar", "Toiletries", 45, 48, 48, True, "T2")
i3t = Item("Oral B - Toothpaste", "Toiletries", 70, 80, 80, True, "T3")
i4t = Item("Colgate - Toothbrush", "Toiletries", 20, 20, 20, True, "T4")
i5t = Item("Pril - Dishwashing liquid", "Toiletries", 55, 55, 55, True, "T5")
toiletries = [i1t, i2t, i3t, i4t, i5t]
for x in range(0, len(toiletries), 1):
    cur_item = toiletries[x]
    discount = random.randrange(0, 2)
    cur_item.discount(discount)
    akshay.add_item(cur_item)

i1e = Item("Wipro - 9W LED bulb", "Electronics", 80, 100, 100, True, "E1")
i2e = Item("Philips - Table lamp", "Electronics", 400, 450, 450, True, "E2")
i3e = Item("Prestige - Electric Kettle", "Electronics", 1200, 1500, 1500, True, "E3")
i4e = Item("Orient Electric - Electric Heater", "Electronics", 1500, 1600, 1600, True, "E4")
i5e = Item("Electric Steamer", "Electronics", 200, 250, 250, True, "E5")
electronics = [i1e, i2e, i3e, i4e, i5e]
for w in range(0, len(electronics), 1):
    cur_item = electronics[w]
    discount = random.randrange(0, 25)
    cur_item.discount(discount)
    akshay.add_item(cur_item)
