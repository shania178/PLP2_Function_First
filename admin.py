from datetime import datetime
from database import connect_db, get_input, get_positive_number

def admin_confirm_payment():
    print("\n ADMIN: Confirm a Payment")
    print("(This section is for AgriBridge admin use only)")

    conn = connect_db()
    cursor = conn.cursor()

#Fetch all orders that are waiting for admin confirmation (status = 'Pending payment')
#JOIN is our case is used to join the "transactions" table with the "vendors" and "harvest_listings" tables to get more information about the orders that are pending payment confirmation.

    cursor.execute("""
    SELECT t.transaction_id, v.name, v.business_name, h.crop_type, t.quantity_ordered, t.payment_reference, t.status
    FROM transactions t
    JOIN vendors v ON t.vendor_id = v.vendor_id
    JOIN harvest_listings h ON t.listing_id = h.listing_id
    WHERE t.status = 'Awaiting Admin Confirmation'
""")
    pending = cursor.fetchall()
    if not pending:
       print("No Payments are waiting confirmation right now.")
       conn.close()
       return

    print("\nOrders awaiting Confirmation... :\n")
    for order in pending:
        print(f"Transaction ID: {order[0]}")
        print(f"Vendor Name: {order[1]} ({order[2]})")
        print(f"Crop Ordered: {order[3]}") 
        print(f"Quantity: {order[4]} KG")
        print(f"Payment Reference: {order[5]}")
        print(f"Status: {order[6]}\n")

    while True:
        try:
            transaction_id = int(get_input("the Transaction ID to confirm"))
            break
        except ValueError:
            print(" Transaction ID must be a number. Please try again.")
 
    # Update the status to show the order is now confirmed and moving forward
    #Check if the transaction ID actually exists in the pending list before trying to confirm it
    cursor.execute("""
        SELECT transaction_id FROM transactions
        WHERE transaction_id = ?
        AND status = 'Awaiting Admin Confirmation'
    """, (transaction_id,))
 
    valid = cursor.fetchone()
 
    if not valid:
        print("\nThat Transaction ID was not found in the pending list.")
        print("  \nPlease choose an ID from the list shown above.\n")
        conn.close()
        return
 
    # Update the status to show the order is now confirmed and moving forward
    cursor.execute(
        "UPDATE transactions SET status = ? WHERE transaction_id = ?",
        ("Confirmed - Processing", transaction_id)
    )
 
    conn.commit()
    conn.close()
 
    print(" \n Done: Payment confirmed! Order is now active and being processed.\n")
 
# VENDOR: Submit a rating for the platform

def rate_platform(vendor_id):
    print("\nRate Our Service\n")
    print("Please rate your experience from 1 to 5:")
    print("  1 = Very Poor  |  3 = Average  |  5 = Excellent")
 
    # Keep asking until they type a valid number between 1 and 5
    while True:
        try:
            rating = int(get_positive_number("Your rating (1-5): ", min_value=1, max_value=5))
            if 1 <= rating <= 5:
                break
            else:
                print("Please enter a number between 1 and 5.")
        except ValueError:
            print("That is not a valid number. Please type a digit.")
 
    comment = input("Any comments? (Press Enter to skip): ")
    feedback_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
 
    conn = connect_db()
    cursor = conn.cursor()
 
    cursor.execute("""
        INSERT INTO feedback (vendor_id, rating, comment, feedback_date)
        VALUES (?, ?, ?, ?)
    """, (vendor_id, rating, comment if comment.strip() else None, feedback_date))
 
    conn.commit()
    conn.close()
 
    print("Thank you for your feedback! It helps us improve.\n")

# VIEW: Platform trust score
# AVG(rating) calculates the average of all ratings in the feedback table
def view_trust_score():
    conn = connect_db()
    cursor = conn.cursor()
 
    cursor.execute("SELECT AVG(rating), COUNT(rating) FROM feedback")
    result = cursor.fetchone()
    conn.close()
 
    avg = result[0]   # The average rating
    count = result[1]   # How many ratings have been submitted
 
    if avg is None:
        print("No ratings submitted yet.\n")
    else:
        trust_score = round(avg, 2)
        print(f"\nPlatform Trust Score : {trust_score} / 5")
        print(f"Based on {count} review(s)\n")