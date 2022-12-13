import sys
import master
from prettytable import PrettyTable

if __name__ == "__main__":
    print ("Welcome onboard Akshay Stores\n")
    metadata = master.login()

    if metadata == 0:
        sys.exit()

    if metadata[0] == "SWD":
        check = True
        cart_table = PrettyTable(["Item", "Code", "Quantity", "Original Price", "Price"])
        customer = master.Student(metadata[1], metadata[2], metadata[3])
        total = 0
        discount_availed = 0
        while check:
            print ("\n(1) To view the market")
            print ("(2) To add an item to your cart")
            print ("(3) To remove items from your cart")
            print ("(4) To view the items in your cart")
            print ("(5) To check out and complete your purchase")
            print ("(6) To search for an item in the market\n")
            print ("\n")
            option = int(input("Enter your choice: "))
            market = master.view_market(master.akshay)

            if option == 1:
                print (market)

            elif option == 2:
                cart_table = PrettyTable(["Item", "Code", "Quantity", "Original Price", "Price"])
                code = str(input("Enter the item code: ")).upper()
                in_market = master.check_item_code(code, master.akshay)
                if type(in_market) == list and in_market[0]:
                    qty = int(input("Enter the quantity: "))
                    customer.add_to_cart(in_market[1], qty)
                    print ("Item added succesfully!")
                else:
                    print ("Item not found!")
                total, discount_availed = master.view_cart(customer, cart_table)

            elif option == 3:
                cart_table = PrettyTable(["Item", "Code", "Quantity", "Original Price", "Price"])
                master.view_cart(customer, cart_table)
                code = str(input("Enter the item code: ")).upper()
                values = master.delete_from_cart(customer, code, total)
                if type(values) == bool:
                    print ("Item not found!")
                else:
                    print ("Item removed!")
                    customer = values[0]
                    total = values[1]

            elif option == 4:
                cart_table = PrettyTable(["Item", "Code", "Quantity", "Original Price", "Price"])
                only_view = True
                master.view_cart(customer, cart_table)
                only_view = False

            elif option == 5:
                cart_table = PrettyTable(["Item", "Code", "Quantity", "Original Price", "Price"])
                print ("AKSHAY SUPERMARKET")
                print (f"Student Name: {metadata[2]}")
                print (f"BITS ID: {metadata[1]}")
                print ("Payment method : SWD account")
                only_view = True
                total, discount_availed = master.view_cart(customer, cart_table)
                print ("Total price after GST (9%): ₹", total + 9/100*(total))
                print ("Total discount availed: ₹", discount_availed)
                print ("Thank you for your succesful purchase!\n")
                print ("\n")
                break

            elif option == 6:
                checker6 = True
                while checker6:
                    print ("(1) Search by name")
                    print ("(2) Search by code")
                    print ("(3) Exit")
                    choice = int (input("Enter your option: "))
                    if choice == 1:
                        name = str(input("Enter the keyword: "))
                        print (master.akshay.search_by_name(name))
                    elif choice == 2:
                        code = str(input("Enter the item code: "))
                        print (master.akshay.search_by_code(code))
                    elif choice == 3:
                        break
                    else:
                        print ("Invalid input. Try again \n")

    elif metadata[0] == "no_SWD":
        check = True
        customer = master.Non_SWD_Customer(metadata[1], metadata[2], master.isUPI)
        cart_table = PrettyTable(["Item", "Code", "Quantity", "Original Price", "Price"])
        total = 0
        discount_availed = 0
        while check:
            print ("\n(1) To view the market")
            print ("(2) To add an item to your cart")
            print ("(3) To remove items from your cart")
            print ("(4) To view the items in your cart")
            print ("(5) To check out and complete your purchase")
            print ("(6) To search for an item in the market\n")
            print ("\n")
            option = int(input("Enter your choice: "))
            market = master.view_market(master.akshay)

            if option == 1:
                print (market)

            elif option == 2:
                cart_table = PrettyTable(["Item", "Code", "Quantity", "Original Price", "Price"])
                code = str(input("Enter the item code: ")).upper()
                in_market = master.check_item_code(code, master.akshay)
                if type(in_market) == list and in_market[0]:
                    qty = int(input("Enter the quantity: "))
                    customer.add_to_cart(in_market[1], qty)
                    print ("Item added succesfully!")
                else:
                    print ("Item not found!")
                total, discount_availed = master.view_cart(customer, cart_table)

            elif option == 3:
                cart_table = PrettyTable(["Item", "Code", "Quantity", "Original Price", "Price"])
                master.view_cart(customer, cart_table)
                code = str(input("Enter the item code: ")).upper()
                values = master.delete_from_cart(customer, code, total)
                if type(values) == bool:
                    print ("Item not found!")
                else:
                    print ("Item removed!")
                    customer = values[0]
                    total = values[1]

            elif option == 4:
                cart_table = PrettyTable(["Item", "Code", "Quantity", "Original Price", "Price"])
                only_view = True
                master.view_cart(customer, cart_table)
                only_view = False

            elif option == 5:
                cart_table = PrettyTable(["Item", "Code", "Quantity", "Original Price", "Price"])
                print ("AKSHAY SUPERMARKET")
                print (f"Student Name: {metadata[2]}")
                print (f"BITS ID: {metadata[1]}")
                print ("Payment method : ", end="")
                if master.isUPI:
                    print ("UPI")
                else:
                    print ("CASH")
                only_view = True
                total, discount_availed = master.view_cart(customer, cart_table)
                print ("Total price after GST (9%): ₹", total + 9/100*(total))
                print ("Total discount availed: ₹", discount_availed)
                print ("Thank you for your succesful purchase!\n")
                print ("\n")
                break

            elif option == 6:
                pass
    elif metadata == "admin":
        print ("Here are the details of the market: ")
        print (master.view_market(master.akshay))
    else:
        print ("Error incurred")
