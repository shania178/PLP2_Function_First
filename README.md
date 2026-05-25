# AgriBridge

## Overview

AgriBridge is a Python-based console application designed to connect farmers directly with vendors (buyers) to reduce post-harvest waste and improve agricultural trade efficiency.

The platform allows:

* Farmers to register and list available harvests
* Vendors to browse and order crops
* Admins to confirm payments and manage trust operations
* Buyers and farmers to interact through a simple database-driven system

The system uses SQLite for data storage and follows a modular programming structure where each file handles a specific part of the application.

---

## Features

### Farmer Features

* Farmer registration and login
* Add harvest listings
* Mark urgent crops automatically when spoilage is near

### Vendor Features

* Vendor registration and login
* Browse all available harvests
* Search crops by type
* Place crop orders
* Cancel pending orders
* Update payment references
* View order history

### Admin Features

* Confirm vendor payments
* Monitor platform trust score

### System Features

* SQLite database integration
* Input validation and error handling
* Modular file organization
* Automatic stock updates after orders
* Crop urgency prioritization

---

## Technologies Used

* Python 3
* SQLite3
* VS Code 
* Git & GitHub

---

## Project Structure

```bash
AgriBridge/
│
├── database.py      # Database connection, table creation, validation helpers
├── farmers.py       # Farmer registration, login, and crop listings
├── vendors.py       # Vendor registration, login, browsing, searching
├── orders.py        # Order placement, cancellation, and payment updates
├── admin.py         # Admin operations
├── main.py          # Main application entry point
├── agribridge.db    # SQLite database file (auto-created)
└── README.md        # Project documentation
```

---

## Database Tables

The application automatically creates the following tables:

* `farmers`
* `vendors`
* `harvest_listings`
* `transactions`
* `feedback`

These tables store all platform data including users, harvests, orders, payments, and ratings.

---

## Installation

### Clone the repository

```bash
git clone https://github.com/shania178/PLP2_Function_First.git
```

### Navigate into the project folder

```bash
cd PLP2_Function_First
```

---

## How to Run the Program

Run the application using:

```bash
python main.py
```

When the program starts, the SQLite database and required tables will automatically be created if they do not already exist.

---

## Example Workflow

### Farmer Flow

1. Register as a farmer
2. Login using Farmer ID and password
3. List available harvests
4. Urgent crops are prioritized automatically

### Vendor Flow

1. Register as a vendor
2. Browse or search harvest listings
3. Place an order
4. Provide payment reference
5. Track order status

### Admin Flow

1. Confirm payments
2. Monitor trust score

---

