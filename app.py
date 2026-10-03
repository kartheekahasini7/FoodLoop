import streamlit as st
from pathlib import Path
import base64
from styles import apply_global_styles
from database import initialize_database
from auth import login_user, register_user

from pages import dashboard
def dashboard_page():
    dashboard.show_dashboard(
        st.session_state.user
    )

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="FoodLoop",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="locked",
)

apply_global_styles()

# ============================================================
# INITIALIZE DATABASE
# ============================================================

initialize_database()


# ============================================================
# SESSION STATE
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

if "show_register" not in st.session_state:
    st.session_state.show_register = False


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
LOGO_PATH = BASE_DIR / "assets" / "FoodLoop_logo.png"

# Also support the lowercase filename if that is what exists.
if not LOGO_PATH.exists():
    LOGO_PATH = BASE_DIR / "assets" / "foodloop_logo.png"


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
<style>

.stApp {
    background: #f7f3ed;
}

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    background: transparent;
}


/* ============================================================
   LEFT FEATURE CARD
   ============================================================ */

.feature-card {
    background: #fffaf4;
    border: 1px solid #eadfd2;
    border-radius: 28px;
    padding: 42px;
    min-height: 540px;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    justify-content: center;
    box-shadow: 0 12px 35px rgba(60, 45, 30, 0.07);
}


/* ============================================================
   LOGO
   ============================================================ */

.logo-wrapper {
    text-align: center;
    margin-bottom: 25px;
}

.foodloop-logo {
    width: 210px;
    max-width: 80%;
    height: auto;
    display: inline-block;
}


/* ============================================================
   FEATURE TEXT
   ============================================================ */

.feature-heading {
    text-align: center;
    font-size: 25px;
    font-weight: 700;
    color: #272421;
    margin-bottom: 24px;
}

.feature-description {
    color: #625b54;
    font-size: 16px;
    line-height: 1.75;
    margin-top: 10px;
    margin-bottom: 10px;
}

.feature-list {
    margin-top: 24px;
    color: #514b45;
    font-size: 15px;
    line-height: 2.5;
}

.feature-list div {
    position: relative;
    padding-left: 15px;
}

.feature-list div::before {
    content: "•";
    position: absolute;
    left: 0;
    color: #dd6545;
    font-weight: bold;
}


/* ============================================================
   RIGHT AUTH AREA
   ============================================================ */

.auth-card {
    padding: 45px 40px;
}

.brand-title {
    font-size: 42px;
    font-weight: 700;
    color: #292522;
    margin-bottom: 8px;
    line-height: 1.15;
}

.brand-subtitle {
    color: #746c64;
    font-size: 16px;
    margin-bottom: 30px;
    line-height: 1.6;
}


/* ============================================================
   INPUTS
   ============================================================ */

div[data-baseweb="input"] {
    border-radius: 10px;
}

div[data-baseweb="input"] > div {
    background-color: #eef1f5;
    border-radius: 10px;
    border: 1px solid transparent;
}

div[data-baseweb="input"] > div:focus-within {
    border: 1px solid #dd6545;
    box-shadow: 0 0 0 1px #dd6545;
}

input {
    color: #292522 !important;
}


/* ============================================================
   SELECTBOX
   ============================================================ */

div[data-baseweb="select"] > div {
    background-color: #eef1f5;
    border-radius: 10px;
    border: 1px solid transparent;
}

div[data-baseweb="select"] > div:focus-within {
    border: 1px solid #dd6545;
    box-shadow: 0 0 0 1px #dd6545;
}


/* ============================================================
   BUTTONS
   ============================================================ */

/* ============================================================
   BUTTONS
   ============================================================ */

.stButton > button {
    width: 100%;
    min-height: 48px;
    border-radius: 11px;
    font-size: 15px;
    font-weight: 600;
    transition: all 0.2s ease;
}


/* ------------------------------------------------------------
   PRIMARY BUTTON - SIGN IN
   ------------------------------------------------------------ */

.stButton > button[kind="primary"] {
    background: #dd6545 !important;
    color: white !important;
    border: 1px solid #dd6545 !important;
}

.stButton > button[kind="primary"]:hover {
    background: #c95537 !important;
    color: white !important;
    border-color: #c95537 !important;
    transform: translateY(-1px);
}


/* ------------------------------------------------------------
   SECONDARY BUTTONS
   ------------------------------------------------------------ */

.stButton > button[kind="secondary"] {
    background: #fffaf4 !important;
    color: #4d4742 !important;
    border: 1px solid #ded5cb !important;
}

.stButton > button[kind="secondary"]:hover {
    background: #C65D4B !important;
    color: white !important;
    border-color: #C65D4B !important;
    transform: translateY(-1px);
}



/* ============================================================
   FOOTER
   ============================================================ */

.auth-footer {
    text-align: center;
    color: #a08f80;
    font-size: 13px;
    margin-top: 38px;
}


/* ============================================================
   MOBILE
   ============================================================ */

@media (max-width: 900px) {

    .feature-card {
        min-height: auto;
        padding: 32px;
        margin-bottom: 20px;
    }

    .auth-card {
        padding: 30px 10px;
    }

    .brand-title {
        font-size: 34px;
    }

    .feature-heading {
        font-size: 22px;
    }
}
/* -----------------------------
   BUTTON STYLING
----------------------------- */

/* Sign in button */
.sign-in-btn {
    background-color: #C65D4B;
    color: white;
    border: 1px solid #C65D4B;
}




</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# LOGIN / REGISTER SCREEN
# ============================================================

if not st.session_state.logged_in:

    left, right = st.columns([1.05, 1], gap="large")

    # ========================================================
    # LEFT SIDE
    # ========================================================

    with left:

        logo_html = ""

        if LOGO_PATH.exists():

            with open(LOGO_PATH, "rb") as logo_file:
                logo_base64 = base64.b64encode(
                    logo_file.read()
                ).decode()

            logo_html = f"""
<div class="logo-wrapper">
<img
src="data:image/png;base64,{logo_base64}"
class="foodloop-logo"
>
</div>
"""

        feature_html = f"""
<div class="feature-card">

{logo_html}

<div class="feature-heading">
Smarter operations. Less waste.
</div>

<div class="feature-description">
A simple workspace for restaurants to manage
inventory, food waste, expiry, and surplus food.
</div>

<div class="feature-list">
<div>Inventory management</div>
<div>Food waste tracking</div>
<div>Expiry monitoring</div>
<div>Surplus food management</div>
</div>

</div>
"""

        st.markdown(
            feature_html,
            unsafe_allow_html=True,
        )

    # ========================================================
    # RIGHT SIDE
    # ========================================================

    with right:

        st.markdown(
            '<div class="auth-card">',
            unsafe_allow_html=True,
        )

        # ====================================================
        # LOGIN
        # ====================================================

        if not st.session_state.show_register:

            st.markdown(
                """
<div class="brand-title">
Welcome back
</div>
""",
                unsafe_allow_html=True,
            )

            st.markdown(
                """
<div class="brand-subtitle">
Sign in to your restaurant workspace.
</div>
""",
                unsafe_allow_html=True,
            )

            email = st.text_input(
                "Email address",
                placeholder="you@restaurant.com",
                key="login_email",
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password",
                key="login_password",
            )

            st.write("")

            if st.button(
                "Sign in",
                use_container_width=True,
                key="sign_in_button",
                type="primary",
            ):

                email_clean = email.strip()

                if not email_clean or not password:

                    st.error(
                        "Please enter your email and password."
                    )

                else:

                    success, user = login_user(
                        email_clean,
                        password,
                    )

                    if success:

                        st.session_state.logged_in = True
                        st.session_state.user = user

                        st.rerun()

                    else:

                        st.error(
                            "Invalid email or password."
                        )

            st.write("")

            if st.button(
                "Create a new account",
                use_container_width=True,
                key="open_register_button",
                type="secondary",
            ):

                st.session_state.show_register = True
                st.rerun()

           

            st.markdown(
                """
<div class="auth-footer">
FoodLoop · Track. Reduce. Reuse.
</div>
""",
                unsafe_allow_html=True,
            )

        # ====================================================
        # REGISTER
        # ====================================================

        else:

            st.markdown(
                """
<div class="brand-title">
Create account
</div>
""",
                unsafe_allow_html=True,
            )

            st.markdown(
                """
<div class="brand-subtitle">
Create your FoodLoop restaurant account.
</div>
""",
                unsafe_allow_html=True,
            )

            full_name = st.text_input(
                "Full name",
                placeholder="Your full name",
                key="register_full_name",
            )

            email = st.text_input(
                "Email address",
                placeholder="you@restaurant.com",
                key="register_email",
            )

            role = st.selectbox(
                "Your role",
                [
                    "Owner",
                    "Manager",
                    "Kitchen Staff",
                    "Inventory Staff",
                    "Restaurant Staff",
                    "Other",
                ],
                key="register_role",
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Create a password",
                key="register_password",
            )

            confirm_password = st.text_input(
                "Confirm password",
                type="password",
                placeholder="Repeat your password",
                key="register_confirm_password",
            )

            st.write("")

            if st.button(
                "Create account",
                use_container_width=True,
                key="create_account_button",
            ):

                full_name_clean = full_name.strip()
                email_clean = email.strip()

                if (
                    not full_name_clean
                    or not email_clean
                    or not password
                    or not confirm_password
                ):

                    st.error(
                        "Please fill in all required fields."
                    )

                elif "@" not in email_clean:

                    st.error(
                        "Please enter a valid email address."
                    )

                elif password != confirm_password:

                    st.error(
                        "Passwords do not match."
                    )

                elif len(password) < 6:

                    st.error(
                        "Password must contain at least 6 characters."
                    )

                else:

                    success, message = register_user(
                        full_name_clean,
                        email_clean,
                        password,
                        role,
                    )

                    if success:

                        st.success(message)

                        st.session_state.show_register = False

                        for key in [
                            "register_full_name",
                            "register_email",
                            "register_password",
                            "register_confirm_password",
                        ]:
                            st.session_state.pop(key, None)

                        st.rerun()

                    else:

                        st.error(message)

            st.write("")

            st.markdown(
                '<div class="secondary-button">',
                unsafe_allow_html=True,
            )

            if st.button(
                "Already have an account? Sign in",
                use_container_width=True,
                key="back_to_login_button",
                type="secondary",
            ):

                st.session_state.show_register = False
                st.rerun()


            st.markdown(
                "</div>",
                unsafe_allow_html=True,
            )

            st.markdown(
                """
<div class="auth-footer">
FoodLoop · Track. Reduce. Reuse.
</div>
""",
                unsafe_allow_html=True,
            )

        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )
    def dashboard_page():
        dashboard.show_dashboard(
            st.session_state.user
        )
    
# ============================================================
# LOGGED-IN AREA
# =============================================================

else:

    # Sidebar logout
    with st.sidebar:

        st.markdown(
            "<div style='height: 10px;'></div>",
            unsafe_allow_html=True,
        )

        if st.button(
            "🚪  Sign out",
            key="sidebar_logout",
            type="secondary",
            use_container_width=True,
        ):

            st.session_state.logged_in = False
            st.session_state.user = None
            st.session_state.show_register = False

            st.rerun()


    # Dashboard
    
    if LOGO_PATH.exists():
         with open(LOGO_PATH, "rb") as logo_file:
            logo_base64 = base64.b64encode(
                logo_file.read()
            ).decode()

    st.markdown(
        f"""
        <style>

        section[data-testid="stSidebar"]::before {{
            content: "";
            display: block;
            width: 100%;
            height: 160px;
            background-image: url("data:image/png;base64,{logo_base64}");
            background-repeat: no-repeat;
            background-position: center center;
            background-size: 180px auto;
            margin-bottom: -35px;
        }}

        </style>
        """,
        unsafe_allow_html=True,
    )



    pg = st.navigation(
    [   
        st.Page(dashboard_page, title="Dashboard"),
        st.Page("pages/inventory.py", title="Inventory"),
        st.Page("pages/expiry.py", title="Expiry"),
        st.Page("pages/waste.py", title="Waste"),
        st.Page("pages/donations.py", title="Donations"),
        st.Page("pages/reports.py", title="Reports"),
    ],
    position="sidebar",
    )


    pg.run()
   