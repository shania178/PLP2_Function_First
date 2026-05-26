# OWNER: Person 4
# WHAT THIS FILE DOES:
#   - register_vendor()  (new vendor signs up)
#   - login_vendor()     (existing vendor logs in)
#   - browse_harvests()  (shows all available listings)
#   - search_harvests()  (search listings by crop type)

from database import connect_db, get_input, get_letters_only

# VENDOR: Register a new vendor

def register_vendor():
    print("\nREGISTER AS A VENDOR")

    name          = get_letters_only("your full name")
    business_name = get_input("your business/company name")
    location      = get_input("your location")
    contact       = get_input("your contact number")
    password      = get_input("a password")

    conn   = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO vendors (name, business_name, location, contact, password) VALUES (?, ?, ?, ?)",
        (name, business_name, location, contact, password)
    )   

    conn.commit()

    # Show the vendor their new ID immediately so they can write it down
    vendor_id = cursor.lastrowid

    conn.close()

    print("Vendor registered successfully!")
    print()
    print(f"Your Vendor ID is: {vendor_id}")
    print("IMPORTANT: Please write this down!")
    print("You will need this ID every time you log in.")
    print("We cannot recover it for you if you forget.\n")


# VENDOR: Login

def login_vendor():
    print("\nVENDOR LOGIN")

    while True:
        try:
            vendor_id = int(get_input("your Vendor ID"))
            break
        except ValueError:
            print("Vendor ID must be a number. Please try again.")

    password = get_input("your password")

    conn   = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM vendors WHERE vendor_id = ? AND password = ?",
        (vendor_id, password)
    )
    vendor = cursor.fetchone()
    conn.close()

    if vendor:
        print(f"\nWelcome back, {vendor[1]} ({vendor[2]})!\n")
        return vendor_id
    else:
        print("Wrong ID or password. Please try again.\n")
        return None


# VENDOR: Browse all available harvests

# NOTE: Farmer details are HIDDEN — only crop info is shown
# Listings are sorted: urgent ones first, then fewest days to spoilage
def browse_harvests():
    print("\nAVAILABLE HARVEST LISTINGS---")

    conn   = connect_db()
    cursor  = conn.cursor()

    cursor.execute("""
        SELECT listing_id, crop_type, quantity, harvest_date, days_to_spoilage, urgent
        FROM harvest_listings
        WHERE quantity > 0
        ORDER BY urgent DESC, days_to_spoilage ASC
    """)

    listings = cursor.fetchall()
    conn.close()

    if not listings:
        print("No harvests available right now. Check back later.\n")
        return False   # False = nothing was found, used by place_order to stop early

    print()
    print(f"{'ID':<5} {'Crop':<15} {'Qty (KG)':<10} {'Harvest Date':<15} {'Days Left':<10} {'Urgent?'}")
    

    for row in listings:
        urgent_label = "YES" if row[5] == 1 else "NO"
        print(f"{row[0]:<5} {row[1]:<15} {row[2]:<10} {row[3]:<15} {row[4]:<10} {urgent_label}")

    print()
    return True   # True = listings were found


# VENDOR: Search harvests by crop type

def search_harvests():
    print("\nSEARCH HARVEST BY CROP TYPES")
    crop_search = get_input("the crop type you are looking for: ").lower()

    conn   = connect_db()
    cursor = conn.cursor()

    # LOWER() makes the search case-insensitive
    # so "Tomato" and "tomato" and "TOMATO" all match
    cursor.execute("""
        SELECT listing_id, crop_type, quantity, harvest_date, days_to_spoilage, urgent
        FROM harvest_listings
        WHERE LOWER(crop_type) = ? AND quantity > 0
        ORDER BY urgent DESC, days_to_spoilage ASC
    """, (crop_search,))

    results = cursor.fetchall()
    conn.close()

    if not results:
        print(f"No listings found for '{crop_search}'.")
        print("Here is what is currently available:\n")
        browse_harvests()
        return

    print(f"\nFound {len(results)} listing(s) for '{crop_search}':\n")
    print(f"{'ID':<5} {'Crop':<15} {'Qty (KG)':<10} {'Days Left':<10} {'Urgent?'}")

    for row in results:
        urgent_label = "YES" if row[5] == 1 else "NO"
        print(f"{row[0]:<5} {row[1]:<15} {row[2]:<10} {row[4]:<10} {urgent_label}")
    print() 
