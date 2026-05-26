# This file contains the codes for when a vendor (buyer) places an order for a crop listed by a farmer, 
# views their orders, cancels an order, or updates a payment reference.

from datetime import datetime
from database import connect_db, get_input, get_positive_number
from vendors  import browse_harvests   # We will need to reuse browse_harvests to show listings

def place_order(vendor_id):
    print("\n___ Place an Order ___")

    # Show all available listings first so the vendor can see what to pick

    found = browse_harvests()
    if not found:
        return   # Stop if there are no listings at all

    # the codes below asks the vendor to insert the items details they want to order, 
    #saves the order in the transaction table, with an update to the harvest listing.
    while True:
        try:
            listing_id = int(get_input("the Listing ID you want to order"))
            break
        except ValueError:
            print(" Listing ID must be a number. Please try again.")

    # the helper function get_positive_number will ensure the quantity is a positive number and not empty.

    quantity_ordered = get_positive_number("quantity you want to buy (KG)")

    conn   = connect_db()
    cursor = conn.cursor()

    # checking if the listing exists and has enough quantity before proceeding with the order.
    cursor.execute(
        "SELECT crop_type, quantity FROM harvest_listings WHERE listing_id = ?",
        (listing_id,)
    )
    result = cursor.fetchone()

    if not result:
        print(" That listing ID does not exist. Please check and try again.\n")
        conn.close()
        return

    crop_name          = result[0]
    available_quantity = result[1]

    if quantity_ordered > available_quantity:
        print(f" Not enough stock. Only {available_quantity} KG available for {crop_name}.\n")
        conn.close()
        return
    
    # The vendor pays via bank transfer outside the app,
    # then enters their reference number here as proof

    print("\n___ Payment Instructions ___")
    print("Please make a bank transfer to:")
    print("  Bank Name   : AgriBridge Bank")
    print("  Account No  : 0123456789")
    print("  Account Name: AgriBridge Nigeria Ltd")
    print(f"  Amount      : Please contact admin for pricing of {quantity_ordered} KG of {crop_name}")
    print()

    payment_ref = input("Enter your bank transfer reference number (or type 'skip' to do later): ")

    order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # to determine the order status based on whether the vendor provided a payment reference or chose to skip it.

    if payment_ref.strip().lower() == "skip" or payment_ref.strip() == "":
        status      = "Pending Payment"
        payment_ref = "PENDING"   # This makes it clear in the database that they haven't provided a reference yet
    else:
        status = "Awaiting Admin Confirmation"

    # Save the order into the transactions table
    cursor.execute("""
        INSERT INTO transactions
            (vendor_id, listing_id, quantity_ordered, order_date, status, payment_reference)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (vendor_id, listing_id, quantity_ordered, order_date, status, payment_ref))

    # Reduce the available quantity in the listing
    # quantity - ordered amount = what is left

    new_quantity = available_quantity - quantity_ordered
    cursor.execute(
        "UPDATE harvest_listings SET quantity = ? WHERE listing_id = ?",
        (new_quantity, listing_id)
    )

    conn.commit()
    conn.close()

    print(f"\n Order placed for {quantity_ordered} KG of {crop_name}!")
    print(f"   Order Status: {status}")
    print("   AgriBridge will contact you once the admin confirms your payment.\n")
    
# this function view the vendors orders by fetching lerevant details from transactions
#  and harvest_listings tables using a JOIN, and displays them in a readable format.

def view_my_orders(vendor_id):
    print("\n___ My Orders ___")

    conn   = connect_db()
    cursor = conn.cursor()

    # JOIN connects two tables so we can show the crop name alongside the order
    # t = transactions table, h = harvest_listings table
    cursor.execute("""
        SELECT t.transaction_id, h.crop_type, t.quantity_ordered,
               t.order_date, t.status, t.payment_reference
        FROM transactions t
        JOIN harvest_listings h ON t.listing_id = h.listing_id
        WHERE t.vendor_id = ?
        ORDER BY t.order_date DESC
    """, (vendor_id,))

    orders = cursor.fetchall()
    conn.close()

    if not orders:
        print("❌ You have not placed any orders yet.\n")
        return

    print()
    for order in orders:
        print(f"  Order ID    : {order[0]}")
        print(f"  Crop        : {order[1]}")
        print(f"  Quantity    : {order[2]} KG")
        print(f"  Date        : {order[3]}")
        print(f"  Status      : {order[4]}")
        print(f"  Payment Ref : {order[5] if order[5] else 'Not provided yet'}")
        

# the codes below allow the vendor to cancel an order that is still pending payment or awaiting admin confirmation.
# Only orders that are "Pending Payment" or "Awaiting Admin Confirmation" can be cancelled.
# Once an admin confirms, it is too late to cancel.

def cancel_order(vendor_id):
    print("\n___ Cancel an Order ___")

    conn   = connect_db()
    cursor = conn.cursor()

    # Only fetch orders that are still cancellable (waiting Admin approval / pending payment)

    cursor.execute("""
        SELECT t.transaction_id, h.crop_type, t.quantity_ordered,
               t.status, t.listing_id
        FROM transactions t
        JOIN harvest_listings h ON t.listing_id = h.listing_id
        WHERE t.vendor_id = ?
        AND t.status IN ('Pending Payment', 'Awaiting Admin Confirmation')
        ORDER BY t.order_date DESC
    """, (vendor_id,))

    cancellable = cursor.fetchall()

    if not cancellable:
        print(" You have no orders that can be cancelled.")
        print("   Orders that are already confirmed cannot be cancelled.\n")
        conn.close()
        return

    print("\nOrders you can cancel:")
    
    for order in cancellable:
        print(f"  Order ID : {order[0]}")
        print(f"  Crop     : {order[1]}")
        print(f"  Quantity : {order[2]} KG")
        print(f"  Status   : {order[3]}")
        

    while True:
        try:
            transaction_id = int(get_input("the Order ID you want to cancel"))
            break
        except ValueError:
            print(" Order ID must be a number. Please try again.")

    # Verify the order belongs to this vendor and is still cancellable

    cursor.execute("""
        SELECT transaction_id, listing_id, quantity_ordered
        FROM transactions
        WHERE transaction_id = ?
        AND vendor_id = ?
        AND status IN ('Pending Payment', 'Awaiting Admin Confirmation')
    """, (transaction_id, vendor_id))

    order = cursor.fetchone()

    if not order:
        print(" That Order ID was not found or cannot be cancelled.\n")
        conn.close()
        return

    # Ask the vendor to confirm — prevents accidental cancellations

    print(f"\nAre you sure you want to cancel Order {order[0]}?")
    confirm = get_input("type YES to confirm, or anything else to go back").strip().upper()

    if confirm != "YES":
        print("Cancellation was not made. Your order is still active.\n")
        conn.close()
        return

    # Step 1: Mark the order as cancelled in the transactions table

    cursor.execute(
        "UPDATE transactions SET status = 'Cancelled' WHERE transaction_id = ?",
        (transaction_id,)
    )

    # Step 2: Give the quantity back to the listing
    # quantity + ? means: take current quantity and add the cancelled amount back

    cursor.execute(
        "UPDATE harvest_listings SET quantity = quantity + ? WHERE listing_id = ?",
        (order[2], order[1])
    )

    conn.commit()
    conn.close()

    print(" Your order has been cancelled.")
    print("   The stock has been returned to the listing.\n")

    # the code below allows the vendor to update their payment reference number 
    # for orders that are still pending payment or awaiting admin confirmation.

def fix_payment_reference(vendor_id):
    print("\n___ Update Payment Reference ___")

    conn   = connect_db()
    cursor = conn.cursor()

    # Only show orders where the reference can still be changed

    cursor.execute("""
        SELECT t.transaction_id, h.crop_type, t.quantity_ordered,
               t.payment_reference, t.status
        FROM transactions t
        JOIN harvest_listings h ON t.listing_id = h.listing_id
        WHERE t.vendor_id = ?
        AND t.status IN ('Pending Payment', 'Awaiting Admin Confirmation')
        ORDER BY t.order_date DESC
    """, (vendor_id,))

    orders = cursor.fetchall()

    if not orders:
        print(" You have no orders where the payment reference can be updated.\n")
        conn.close()
        return

    print("\nOrders you can update:")
   
    for order in orders:
        current_ref = order[3] if order[3] else "Not provided yet"
        print(f"  Order ID       : {order[0]}")
        print(f"  Crop           : {order[1]}")
        print(f"  Quantity       : {order[2]} KG")
        print(f"  Current Ref No : {current_ref}")
        print(f"  Status         : {order[4]}")
        

    while True:
        try:
            transaction_id = int(get_input("the Order ID you want to update"))
            break
        except ValueError:
            print(" Order ID must be a number. Please try again.")

    # Confirm it belongs to this vendor and is still editable(can be chnaged).

    cursor.execute("""
        SELECT transaction_id FROM transactions
        WHERE transaction_id = ?
        AND vendor_id = ?
        AND status IN ('Pending Payment', 'Awaiting Admin Confirmation')
    """, (transaction_id, vendor_id))

    found = cursor.fetchone()

    if not found:
        print(" That Order ID was not found or can no longer be updated.\n")
        conn.close()
        return

    new_ref = get_input("your new payment reference number")

    # Save the new reference and reset status so admin knows to check again

    cursor.execute("""
        UPDATE transactions
        SET payment_reference = ?, status = 'Awaiting Admin Confirmation'
        WHERE transaction_id = ?
    """, (new_ref, transaction_id))

    conn.commit()
    conn.close()

    print(" Payment reference updated successfully!")
    print("   Status set to: Awaiting Admin Confirmation\n")