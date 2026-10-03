import hashlib
from database import get_connection


# ============================================================
# PASSWORD HASHING
# ============================================================

def hash_password(password):
    return hashlib.sha256(
        password.encode()
    ).hexdigest()


# ============================================================
# REGISTER USER
# ============================================================

def register_user(full_name, email, password, role):

    connection = get_connection()
    cursor = connection.cursor()

    password_hash = hash_password(password)

    try:

        cursor.execute("""
            INSERT INTO users (
                full_name,
                email,
                password_hash,
                role
            )
            VALUES (?, ?, ?, ?)
        """, (
            full_name,
            email,
            password_hash,
            role
        ))

        connection.commit()

        return True, "Account created successfully."

    except Exception as error:

        if "UNIQUE constraint failed" in str(error):
            return False, "An account with this email already exists."

        return False, "Registration failed."

    finally:

        connection.close()


# ============================================================
# LOGIN USER
# ============================================================

def login_user(email, password):

    connection = get_connection()
    cursor = connection.cursor()

    password_hash = hash_password(password)

    cursor.execute("""
        SELECT
            id,
            full_name,
            email,
            role
        FROM users
        WHERE email = ?
        AND password_hash = ?
    """, (
        email,
        password_hash
    ))

    user = cursor.fetchone()

    connection.close()

    if user:
        return True, dict(user)

    return False, None