# Import everything we need from the other files in the same folder

from database import create_tables
from farmers  import register_farmer, login_farmer, list_harvest
from vendors  import register_vendor, login_vendor, browse_harvests, search_harvests
from orders   import place_order, view_my_orders, cancel_order, fix_payment_reference
from admin    import admin_confirm_payment, rate_platform, view_trust_score

# the codes below are the main menu and sub-menus that call the functions imported above. 
# The main() function is where the program starts when you run main.py.
# This appears after a farmer logs in successfully

def farmer_menu(farmer_id):
    while True:
        print("\n^^^^ FARMER MENU ^^^^")
        print("1. List a new harvest")
        print("2. Go back to main menu")
        choice = input("Choose (1-2): ")

        if choice == "1":
            list_harvest(farmer_id)
        elif choice == "2":
            break
        else:
            print(" Invalid option.\n")


# the codes are for the Vendor Menu.
# This appears after a vendor logs in successfully

def vendor_menu(vendor_id):
    while True:
        print("\n^^^^ VENDOR MENU ^^^^")
        print("1. Browse all harvests")
        print("2. Search for a specific crop")
        print("3. Place an order")
        print("4. View my orders")
        print("5. Cancel an order")
        print("6. Fix a wrong payment reference")
        print("7. Rate the platform")
        print("8. Go back to main menu")
        choice = input("Choose (1-8): ")

        if choice == "1":
            browse_harvests()
        elif choice == "2":
            search_harvests()
        elif choice == "3":
            place_order(vendor_id)
        elif choice == "4":
            view_my_orders(vendor_id)
        elif choice == "5":
            cancel_order(vendor_id)
        elif choice == "6":
            fix_payment_reference(vendor_id)
        elif choice == "7":
            rate_platform(vendor_id)
        elif choice == "8":
            break
        else:
            print(" Invalid option.\n")

# the codes are for the Admin Menu.

def admin_menu():
    while True:
        print("\n^^^^ ADMIN MENU ^^^^")
        print("1. Confirm a payment")
        print("2. View trust score")
        print("3. Go back to main menu")
        choice = input("Choose (1-3): ")

        if choice == "1":
            admin_confirm_payment()
        elif choice == "2":
            view_trust_score()
        elif choice == "3":
            break
        else:
            print(" Invalid option.\n")



# main() function the heart of the program starts from here.

def main():
    # Create all tables when the program first runs
    create_tables()

    # Welcome message
    print("   Welcome to AGRI-BRIDGE ")
    print("   Connecting Farmers to Buyers in Nigeria")
    print("   Reducing Post-Harvest Waste, One Order at a Time")
    

    while True:
        print("\n^^^^ WHO ARE YOU? ^^^^")
        print("1. I am a Farmer")
        print("2. I am a Vendor (Buyer)")
        print("3. Admin")
        print("4. Exit")
        user_type = input("Choose (1-4): ")

        #  Farmer flow
        if user_type == "1":
            print("\n1. Register (new farmer)")
            print("2. Login (existing farmer)")
            farmer_choice = input("Choose (1-2): ")

            if farmer_choice == "1":
                register_farmer()
            elif farmer_choice == "2":
                farmer_id = login_farmer()
                if farmer_id:   # Only go to menu if login was successful
                    farmer_menu(farmer_id)
            else:
                print(" Invalid option.\n")

        # Vendor flow
        elif user_type == "2":
            print("\n1. Register (new vendor)")
            print("2. Login (existing vendor)")
            vendor_choice = input("Choose (1-2): ")

            if vendor_choice == "1":
                register_vendor()
            elif vendor_choice == "2":
                vendor_id = login_vendor()
                if vendor_id:   # Only go to menu if login was successful
                    vendor_menu(vendor_id)
            else:
                print(" Invalid option.\n")

        # Admin flow
        elif user_type == "3":
            admin_menu()

        # Exit option
        elif user_type == "4":
            print("\n Thank you for using AgriBridge. Goodbye!")
            break

        else:
            print(" Invalid option. Please choose 1, 2, 3, or 4.\n")


# Only run main() if this file is run directly
# If another file imports main.py, this line prevents it from auto-starting
if __name__ == "__main__":
    main()