import sqlite3
from datetime import datetime

# We are going to connect to a SQLite database called 'agribridge.db'. If it doesn't exist, it will be created.
#Every other file that needs to interact with the database will import this function to establish a connection.

def connect_db():
    return sqlite3.connect('agribridge.db')

#I am going to create all tables
#This runs only once when the application is first started. It checks if the tables already exist before creating them to avoid errors.
def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    #Creating the "FARMERS" table.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS farmers(
            farmer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            location TEXT NOT NULL,
            contact TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)
    #Creating the "Vendors (BUYERS)" table.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vendors(
            vendor_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            business_name TEXT NOT NULL,
            location TEXT NOT NULL,
            contact TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)
    #Creating harvest_listings table. It will contain the harvested crop information provided by the farmers.
    #Urgent =1 means the crop spoils in 5 days or less.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS harvest_listings(
            listing_id INTEGER PRIMARY KEY AUTOINCREMENT,
            farmer_id INTEGER NOT NULL,
            crop_type TEXT NOT NULL,
            quantity REAL NOT NULL,
            harvest_date TEXT NOT NULL,
            days_to_spoilage INTEGER NOT NULL,
            urgent INTEGER DEFAULT 0,
            FOREIGN KEY (farmer_id) REFERENCES farmers(farmer_id)
        )
    """)
    #Creating the "TRANSACTIONS" table. It will store the transactions placed by the vendors (buyers) for the crops listed by the farmers.
    #payment_reference = bank transfer reference number the vendor provides after making the payment.
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions(
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            vendor_id INTEGER NOT NULL,       
            listing_id INTEGER NOT NULL,
            quantity_ordered REAL NOT NULL,
            order_date TEXT NOT NULL,
            status TEXT DEFAULT 'Pending payment',
            payment_reference TEXT,
            FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id)
            FOREIGN KEY (listing_id) REFERENCES harvest_listings(listing_id)
        )
    """)
    #Creating the "FEEDBACK" table. It will store the feedback provided by the vendors (buyers).
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback(
            feedback_id INTEGER PRIMARY KEY AUTOINCREMENT,
            vendor_id INTEGER NOT NULL,
            rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
            comment TEXT,
            feedback_date TEXT NOT NULL,
            FOREIGN KEY (vendor_id) REFERENCES vendors(vendor_id)
        )
    """)
    conn.commit()
    conn.close()

    #Error handlers functions.
    #1st function, will not allow empty inputs for the required fields.
def get_input(label):
    while True:
        value = input(f"Enter {label}: ")
        if value.strip() == "":
            print("This field cannot be empty. Please enter a value.")
        else:
            return value
#2nd function, will validate the contact number to ensure it is in the correct format (e.g., 10 digits).
def get_positive_number(label, whole_number=False):
    while True:
        try:
            if whole_number:
                value = int(input(f"Enter {label}: "))
            else:
                value = float(input(f"Enter {label}: "))
 
            if value <= 0:
                print(f"{label} must be greater than zero. Please try again.")
            else:
                return value
 
        except ValueError:
            print(f"{label} is not a valid number. Please type digits only.")
#3rd function, will accept the letters and spaces. For e.g: names and crop types. No numbers or symbols allowed.
def get_letters_only(label):
    while True:
        value = input(f"Enter {label}: ").strip()
        if value.replace(" ", "").isalpha() and len(value) > 0:
            return value
        else:
            print(f"\n{label} must contain only letters. No numbers or symbols allowed. Please try again.")
#4th function, will validate the contact number to ensure it is in the correct format (e.g., 11 digits).
def get_contact_number(label):
    while True:
        value = input(f"Enter {label}: ").strip()
 
        # .isdigit() returns True only if every character is a digit (0-9)
        if value.isdigit() and len(value) >= 11:
            return value
        elif not value.isdigit():
            print(f"\n{label} should only contain digits. Do not include symbols or letters.")
        else:
            # This runs if they typed digits but less than 11 of them
            print(f"\n {label} seems too short. Please enter a valid number Nigerian number without a country code.")
# The date must follow the format YYYY-MM-DD exactly
# For example: 2025-06-15 is valid, "tomorrow" or "15/06/25" are not
def get_date(label):
    while True:
        value = input(f"Enter {label} (YYYY-MM-DD): ").strip()
 
        # We try to read the date using the exact format we expect
        # If it does not match, datetime raises a ValueError and we reject it
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return value   # Format is correct — send it back
        except ValueError:
            print(f"\n Invalid date format. Please use YYYY-MM-DD (example: 2025-06-15).")

