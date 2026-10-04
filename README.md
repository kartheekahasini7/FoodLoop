# FoodLoop

FoodLoop is a restaurant food waste management system built with Python,
Streamlit, and SQLite.

It helps restaurant staff manage inventory, monitor expiry dates, record
food waste, track donations, and view operational reports from one
application.
## 🚀 Live Demo

👉 [Open FoodLoop Web App](https://foodloop.streamlit.app/)

## Features

-   User registration and login
-   Role-based user information
-   Restaurant inventory management
-   Expiry monitoring
-   Waste recording and management
-   Automatic movement of expired inventory into waste records
-   Food donation tracking
-   Reports and summaries
-   SQLite database for local data storage
-   Professional restaurant-management interface

## Project Structure

``` text
FoodLoop/
├── app.py
├── auth.py
├── database.py
├── styles.py
├── requirements.txt
├── .gitignore
├── .streamlit/
│   └── config.toml
├── assets/
│   └── FoodLoop_logo.png
├── pages/
│   ├── dashboard.py
│   ├── inventory.py
│   ├── expiry.py
│   ├── waste.py
│   ├── donations.py
│   └── reports.py
└── data/
    └── restaurant.db
```

The local SQLite database is intentionally excluded from Git using
`.gitignore`.

## Technologies Used

-   Python
-   Streamlit
-   SQLite
-   HTML/CSS

## Running FoodLoop Locally

### 1. Clone the repository

``` bash
git clone https://github.com/kartheekahasini7/FoodLoop.git
cd FoodLoop
```

### 2. Create a virtual environment

Windows PowerShell:

``` bash
python -m venv venv
venv\Scripts\Activate.ps1
```

### 3. Install dependencies

``` bash
pip install -r requirements.txt
```

### 4. Run the application

``` bash
streamlit run app.py
```

## Database

FoodLoop uses SQLite for local data storage. The database is created
automatically at:

``` text
data/restaurant.db
```

The database file is excluded from version control so local restaurant
data is not uploaded to GitHub.

## Main Modules

### Dashboard

Provides an overview of current restaurant operations, including
inventory, expiry alerts, waste, donations, activity, and quick actions.

### Inventory

Allows staff to add, view, and remove inventory items while recording
quantities, units, and expiry dates.

### Expiry

Groups inventory by expiry status and allows expired items to be moved
into Waste Management.

### Waste

Records wasted food along with quantity, unit, reason, and date.

### Donations

Records donated food, quantities, recipients, dates, and notes.

### Reports

Provides summaries of inventory, waste, donations, and expired items
with reporting-period filters.

## License

This project currently does not include a specific open-source license.
