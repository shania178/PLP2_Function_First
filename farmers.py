# This file is for the farmer section
# The file functions to :
# register_farmer() where new farmer signs up
# login_farmer() where existing farmer logs in
# list_farmer() where farmer posts a crop listing

from database import connect_db, get_contact_number, get_date, get_input, get_positive_number, get_letters_only

# Register a new farmer

def register_farmer():
    print("\n Register as Farmer")
    
    name = get_letters_only(" your full name")
    location = get_input(" your location (state/city)")
    contact = get_contact_number(" your contact number. \nN.B. It should be a nigerian number without a country code included.:")
    password = get_input(" a password (at least 8 characters long)")
    
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO farmers (name, location, contact, password) VALUES (?, ?, ?, ?)",
        (name, location, contact, password)
    )
    
    conn.commit()
    
    # An id is auto-created and the cursor.lastrowid reads it back
    # The auoto-created id is then shown to the farmer
    
    farmer_id = cursor.lastrowid
    conn.close()
    
    print("Your registration is successful")
    print()
    print(f" Your farmer ID is: {farmer_id}")
    print(" IMPORTANT: Please write this down!!!")
    print(" You will need your ID everytime you log in")
    print(" We cannot recover it for you if you forget or loose it. \n")
    
    
    # Login a farmer
    
def login_farmer():
    print("\n Farmer Login")
        
    while True:
        try:
            farmer_id = int(get_input("Enter your Farmer ID"))
            break
        except ValueError:
            print("Farmer ID must be a number, please try again.")
                
    password = get_input("Enter your password")
    
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT * FROM farmers WHERE farmer_id = ? AND password = ?",
        (farmer_id, password)
    )
    farmer = cursor.fetchone()
    conn.close()
    
    if farmer:
        print(f"\n Welcome back, {farmer[1]}!\n")
        return farmer_id
    else:
        print("Wrong ID or password, please try again.\n")
        return None
    
    # List a crop
    
def list_harvest(farmer_id):
    print("\n List Your Crop")
        
    crop_type = get_letters_only("Enter crop type (e.g. tomatoes, onions)")
    quantity = get_positive_number("Enter quantity available in KG")
    harvest_date = get_date("Enter harvest date (YYYY-MM-DD)")
    days_to_spoilage = get_positive_number("estimated days before it spoils", whole_number=True)
    urgent = 1 if days_to_spoilage <= 7 else 0
        
    conn = connect_db()
    cursor = conn.cursor()
        
    cursor.execute("""
        INSERT INTO harvest_listings
            (farmer_id, crop_type, quantity, harvest_date, days_to_spoilage, urgent)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (farmer_id, crop_type, quantity, harvest_date, days_to_spoilage, urgent))

    conn.commit()
    conn.close()
    
    if urgent:
        print("Your listing has been marked as urgent because it spoils in 7 days or less.")
        print("It will appear at the top of the listings so vendors see it first")
        print("Crop listed successfully!\n")
        
        