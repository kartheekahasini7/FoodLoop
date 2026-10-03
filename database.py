import sqlite3
from pathlib import Path


# =========================================================
# DATABASE LOCATION
# =========================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "restaurant.db"


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_connection():
    DATA_DIR.mkdir(exist_ok=True)

    connection = sqlite3.connect(DB_PATH)

    # Allows us to access columns by name
    connection.row_factory = sqlite3.Row

    # Enable foreign key support
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


# =========================================================
# INITIALIZE DATABASE
# =========================================================

def initialize_database():

    connection = get_connection()
    cursor = connection.cursor()

    # -----------------------------------------------------
    # USERS TABLE
    # -----------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'Manager',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # -----------------------------------------------------
    # INVENTORY TABLE
    # -----------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            item_name TEXT NOT NULL,

            category TEXT NOT NULL,

            quantity REAL NOT NULL DEFAULT 0,

            unit TEXT NOT NULL,

            purchase_date TEXT,

            expiry_date TEXT,

            storage_location TEXT,

            created_by INTEGER,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (created_by)
                REFERENCES users(id)
                ON DELETE SET NULL
        )
    """)
        # -----------------------------------------------------
    # WASTE TABLE
    # -----------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS waste (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            item_name TEXT NOT NULL,

            quantity REAL NOT NULL DEFAULT 0,

            unit TEXT NOT NULL,

            reason TEXT NOT NULL,

            waste_date TEXT NOT NULL,

            created_by INTEGER,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (created_by)
                REFERENCES users(id)
                ON DELETE SET NULL
        )
    """)
   

    # -----------------------------------------------------
    # DONATIONS TABLE
    # -----------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS donations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            item_name TEXT NOT NULL,

            quantity REAL NOT NULL DEFAULT 0,

            unit TEXT NOT NULL,

            recipient TEXT NOT NULL,

            donation_date TEXT NOT NULL,

            notes TEXT,

            created_by INTEGER,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (created_by)
                REFERENCES users(id)
                ON DELETE SET NULL
        )
    """)


    connection.commit()
    connection.close()
    

# =========================================================
# INVENTORY - ADD ITEM
# =========================================================

def add_inventory_item(
    item_name,
    category,
    quantity,
    unit,
    purchase_date=None,
    expiry_date=None,
    storage_location=None,
    created_by=None
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO inventory (
            item_name,
            category,
            quantity,
            unit,
            purchase_date,
            expiry_date,
            storage_location,
            created_by
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        item_name,
        category,
        quantity,
        unit,
        purchase_date,
        expiry_date,
        storage_location,
        created_by
    ))

    connection.commit()

    item_id = cursor.lastrowid

    connection.close()

    return item_id


# =========================================================
# INVENTORY - GET ALL ITEMS
# =========================================================

def get_inventory_items():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            inventory.id,
            inventory.item_name,
            inventory.category,
            inventory.quantity,
            inventory.unit,
            inventory.purchase_date,
            inventory.expiry_date,
            inventory.storage_location,
            inventory.created_by,
            inventory.created_at,
            users.full_name AS created_by_name

        FROM inventory

        LEFT JOIN users
            ON inventory.created_by = users.id

        ORDER BY inventory.created_at DESC
    """)

    items = cursor.fetchall()

    connection.close()

    return items


# =========================================================
# INVENTORY - GET ONE ITEM
# =========================================================

def get_inventory_item(item_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            inventory.id,
            inventory.item_name,
            inventory.category,
            inventory.quantity,
            inventory.unit,
            inventory.purchase_date,
            inventory.expiry_date,
            inventory.storage_location,
            inventory.created_by,
            inventory.created_at,
            users.full_name AS created_by_name

        FROM inventory

        LEFT JOIN users
            ON inventory.created_by = users.id

        WHERE inventory.id = ?
    """, (item_id,))

    item = cursor.fetchone()

    connection.close()

    return item


# =========================================================
# INVENTORY - UPDATE ITEM
# =========================================================

def update_inventory_item(
    item_id,
    item_name,
    category,
    quantity,
    unit,
    purchase_date=None,
    expiry_date=None,
    storage_location=None
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE inventory

        SET
            item_name = ?,
            category = ?,
            quantity = ?,
            unit = ?,
            purchase_date = ?,
            expiry_date = ?,
            storage_location = ?

        WHERE id = ?
    """, (
        item_name,
        category,
        quantity,
        unit,
        purchase_date,
        expiry_date,
        storage_location,
        item_id
    ))

    connection.commit()

    connection.close()


# =========================================================
# INVENTORY - DELETE ITEM
# =========================================================

def delete_inventory_item(item_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM inventory
        WHERE id = ?
    """, (item_id,))

    connection.commit()

    connection.close()


# =========================================================
# INVENTORY - COUNT ITEMS
# =========================================================

def get_inventory_count():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM inventory
    """)

    count = cursor.fetchone()[0]

    connection.close()

    return count


# =========================================================
# INVENTORY - TOTAL QUANTITY
# =========================================================

def get_total_inventory_quantity():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COALESCE(SUM(quantity), 0)
        FROM inventory
    """)

    total = cursor.fetchone()[0]

    connection.close()

    return total
# ---------------------------------------------------------
# WASTE FUNCTIONS
# ---------------------------------------------------------

def add_waste_record(
    item_name,
    quantity,
    unit,
    reason,
    waste_date,
    created_by=None,
):
    connection = get_connection()

    connection.execute(
        """
        INSERT INTO waste (
            item_name,
            quantity,
            unit,
            reason,
            waste_date,
            created_by
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            item_name,
            quantity,
            unit,
            reason,
            waste_date,
            created_by,
        ),
    )

    connection.commit()
    connection.close()


def get_waste_records():
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT
            id,
            item_name,
            quantity,
            unit,
            reason,
            waste_date,
            created_by,
            created_at
        FROM waste
        ORDER BY waste_date DESC, id DESC
        """
    ).fetchall()

    connection.close()

    return rows


def delete_waste_record(waste_id):
    connection = get_connection()

    connection.execute(
        """
        DELETE FROM waste
        WHERE id = ?
        """,
        (waste_id,),
    )

    connection.commit()
    connection.close()
# ---------------------------------------------------------
# MOVE INVENTORY ITEM TO WASTE
# ---------------------------------------------------------

def mark_inventory_item_as_waste(
    item_id,
    reason,
    waste_date,
):
    connection = get_connection()

    try:

        item = connection.execute(
            """
            SELECT
                item_name,
                quantity,
                unit,
                created_by
            FROM inventory
            WHERE id = ?
            """,
            (item_id,),
        ).fetchone()

        if item is None:
            return False

        connection.execute(
            """
            INSERT INTO waste (
                item_name,
                quantity,
                unit,
                reason,
                waste_date,
                created_by
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                item["item_name"],
                item["quantity"],
                item["unit"],
                reason,
                waste_date,
                item["created_by"],
            ),
        )

        connection.execute(
            """
            DELETE FROM inventory
            WHERE id = ?
            """,
            (item_id,),
        )

        connection.commit()

        return True

    except Exception:
        connection.rollback()
        raise

    finally:
        connection.close()
    # ---------------------------------------------------------
# DONATION FUNCTIONS
# ---------------------------------------------------------

def add_donation_record(
    item_name,
    quantity,
    unit,
    recipient,
    donation_date,
    notes=None,
    created_by=None,
):
    connection = get_connection()

    connection.execute(
        """
        INSERT INTO donations (
            item_name,
            quantity,
            unit,
            recipient,
            donation_date,
            notes,
            created_by
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            item_name,
            quantity,
            unit,
            recipient,
            donation_date,
            notes,
            created_by,
        ),
    )

    connection.commit()
    connection.close()


def get_donation_records():
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT
            id,
            item_name,
            quantity,
            unit,
            recipient,
            donation_date,
            notes,
            created_by,
            created_at
        FROM donations
        ORDER BY donation_date DESC, id DESC
        """
    ).fetchall()

    connection.close()

    return rows


def delete_donation_record(donation_id):
    connection = get_connection()

    connection.execute(
        """
        DELETE FROM donations
        WHERE id = ?
        """,
        (donation_id,),
    )

    connection.commit()
    connection.close()