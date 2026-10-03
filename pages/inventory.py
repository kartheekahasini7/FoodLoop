import streamlit as st
from datetime import date
from styles import apply_global_styles

apply_global_styles()
from database import (
    add_inventory_item,
    get_inventory_items,
    delete_inventory_item,
)


# =========================================================
# LOGIN CHECK
# =========================================================

if not st.session_state.get("logged_in", False):
    st.warning("Please log in to access Inventory.")
    st.stop()

user = st.session_state.get("user", {})
user_id = user.get("id")


# =========================================================
# PAGE STYLE
# =========================================================

st.markdown(
    """
    <style>

    /* =====================================================
       PAGE
    ===================================================== */

    .stApp {
        background: #eee5da;
    }

    .block-container {
        max-width: 1100px;
        padding-top: 2.5rem;
        padding-bottom: 3rem;
    }


    /* =====================================================
       HEADER
    ===================================================== */

    .inventory-title {
        font-size: 36px;
        font-weight: 750;
        color: #302923;
        margin-bottom: 5px;
        letter-spacing: -0.7px;
    }

    .inventory-subtitle {
        color: #786d63;
        font-size: 15px;
        margin-bottom: 32px;
    }


    /* =====================================================
       SECTION TITLES
    ===================================================== */

    .section-title {
        color: #302923;
        font-size: 21px;
        font-weight: 700;
        margin-top: 28px;
        margin-bottom: 15px;
    }


    /* =====================================================
       INPUTS
    ===================================================== */

    div[data-baseweb="input"] > div {
        background: #faf7f3 !important;
        border: 1px solid #d5c8bc !important;
        border-radius: 9px !important;
    }

    div[data-baseweb="input"] > div:focus-within {
        border-color: #b46a4d !important;
        box-shadow: 0 0 0 1px #b46a4d !important;
    }

    div[data-baseweb="select"] > div {
        background: #faf7f3 !important;
        border: 1px solid #d5c8bc !important;
        border-radius: 9px !important;
    }

    div[data-baseweb="select"] > div:focus-within {
        border-color: #b46a4d !important;
        box-shadow: 0 0 0 1px #b46a4d !important;
    }

    .stTextInput label,
    .stNumberInput label,
    .stSelectbox label,
    .stDateInput label {
        color: #655b53 !important;
        font-size: 12px !important;
        font-weight: 600 !important;
    }


    /* =====================================================
       NORMAL BUTTONS
    ===================================================== */

    .stButton > button {
        border-radius: 10px !important;
        min-height: 42px !important;
        font-weight: 650 !important;
        transition: 0.2s ease !important;
    }


    /* =====================================================
       ADD BUTTON
    ===================================================== */

    .stButton > button[kind="primary"] {
        background: #a85d43 !important;
        border: 1px solid #a85d43 !important;
        color: #ffffff !important;
    }

    .stButton > button[kind="primary"]:hover {
        background: #914d38 !important;
        border-color: #914d38 !important;
        color: #ffffff !important;
    }


    /* =====================================================
       FORM SUBMIT BUTTON
    ===================================================== */

    .stFormSubmitButton > button {
        background: #a85d43 !important;
        border: 1px solid #a85d43 !important;
        color: #ffffff !important;

        border-radius: 10px !important;

        min-height: 42px !important;

        font-weight: 650 !important;

        box-shadow:
            0 4px 10px
            rgba(168, 93, 67, 0.18) !important;

        transition: 0.2s ease !important;
    }

    .stFormSubmitButton > button:hover {
        background: #914d38 !important;
        border-color: #914d38 !important;
        color: #ffffff !important;

        transform: translateY(-1px);
    }


    /* =====================================================
       INVENTORY CARD
    ===================================================== */

    [class*="st-key-inventory-card-"] {
        border-radius: 18px !important;

        padding: 20px 18px 20px 23px !important;

        margin-bottom: 13px !important;

        border: 1px solid !important;

        box-shadow:
            0 6px 17px
            rgba(60, 45, 35, 0.08) !important;
    }


    /* =====================================================
       CARD COLORS
    ===================================================== */

    .st-key-inventory-card-0 {
        background: #e7d0b5 !important;
        border-color: #d1b696 !important;
    }

    .st-key-inventory-card-1 {
        background: #d5e4da !important;
        border-color: #b8cdbf !important;
    }

    .st-key-inventory-card-2 {
        background: #eadcbd !important;
        border-color: #d4bf98 !important;
    }

    .st-key-inventory-card-3 {
        background: #d6e2e6 !important;
        border-color: #b8cbd1 !important;
    }

    .st-key-inventory-card-4 {
        background: #e7d0b5 !important;
        border-color: #d1b696 !important;
    }

    .st-key-inventory-card-5 {
        background: #d5e4da !important;
        border-color: #b8cdbf !important;
    }

    .st-key-inventory-card-6 {
        background: #eadcbd !important;
        border-color: #d4bf98 !important;
    }

    .st-key-inventory-card-7 {
        background: #d6e2e6 !important;
        border-color: #b8cbd1 !important;
    }


    /* =====================================================
       CARD TEXT
    ===================================================== */

    .card-name {
        color: #302923;
        font-size: 18px;
        font-weight: 750;
        margin-bottom: 5px;
    }

    .card-subtitle {
        color: #766a60;
        font-size: 12px;
    }

    .card-label {
        color: #776b62;
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 1px;
        text-transform: uppercase;
        margin-bottom: 4px;
    }

    .card-value {
        color: #302923;
        font-size: 17px;
        font-weight: 700;
    }


    /* =====================================================
       DELETE BUTTON
    ===================================================== */

    [class*="st-key-inventory-card-"] button {
        background: rgba(255, 255, 255, 0.58) !important;

        color: #75695f !important;

        border: 1px solid
            rgba(90, 70, 55, 0.18) !important;

        border-radius: 9px !important;

        min-height: 38px !important;

        width: 42px !important;

        padding: 0 !important;

        box-shadow: none !important;

        font-size: 14px !important;

        transition: 0.2s ease !important;
    }

    [class*="st-key-inventory-card-"] button:hover {
        background: #efd5cf !important;

        color: #984d40 !important;

        border-color: #d4aaa1 !important;
    }


    /* =====================================================
       STATUS BADGES
    ===================================================== */

    .fresh {
        display: inline-block;

        background: #d4e8d9;

        color: #356344;

        padding: 5px 10px;

        border-radius: 20px;

        font-size: 10px;

        font-weight: 700;

        margin-top: 7px;
    }

    .soon {
        display: inline-block;

        background: #f1dfbb;

        color: #8c642c;

        padding: 5px 10px;

        border-radius: 20px;

        font-size: 10px;

        font-weight: 700;

        margin-top: 7px;
    }

    .expired {
        display: inline-block;

        background: #efd2cb;

        color: #984d40;

        padding: 5px 10px;

        border-radius: 20px;

        font-size: 10px;

        font-weight: 700;

        margin-top: 7px;
    }


    /* =====================================================
       FORM BORDER
    ===================================================== */

    [data-testid="stForm"] {
        border: 1px solid #d7c7b7 !important;

        border-radius: 17px !important;

        background: rgba(245, 235, 224, 0.45) !important;

        padding: 20px 16px 16px 16px !important;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
    <div class="inventory-title">
        📦 Inventory
    </div>

    <div class="inventory-subtitle">
        Keep track of the ingredients currently in your restaurant.
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# ADD INGREDIENT
# =========================================================

st.markdown(
    '<div class="section-title">Add Ingredient</div>',
    unsafe_allow_html=True,
)


# =========================================================
# FORM
# clear_on_submit=True clears the fields after submission
# =========================================================

with st.form(
    "add_inventory_form",
    clear_on_submit=True
):

    col1, col2, col3 = st.columns(
        [2.5, 1.2, 1.2]
    )


    # -----------------------------------------------------
    # INGREDIENT
    # -----------------------------------------------------

    with col1:

        item_name = st.text_input(
            "Ingredient",
            placeholder="e.g. Chicken Breast",
        )


    # -----------------------------------------------------
    # QUANTITY
    # -----------------------------------------------------

    with col2:

        quantity = st.number_input(
            "Quantity",
            min_value=0.0,
            step=0.5,
            format="%.2f",
        )


    # -----------------------------------------------------
    # UNIT
    # -----------------------------------------------------

    with col3:

        unit = st.selectbox(
            "Unit",
            [
                "kg",
                "g",
                "L",
                "ml",
                "pieces",
                "packets",
                "boxes",
            ],
        )


    # -----------------------------------------------------
    # EXPIRY
    # -----------------------------------------------------

    expiry_date = st.date_input(
        "Expiry date",
        value=date.today(),
    )


    # -----------------------------------------------------
    # ADD BUTTON
    # -----------------------------------------------------

    add_button = st.form_submit_button(
        "➕ Add to Inventory",
        use_container_width=True,
    )


# =========================================================
# SAVE INVENTORY ITEM
# =========================================================

if add_button:

    if not item_name.strip():

        st.error(
            "Please enter an ingredient name."
        )

    elif quantity <= 0:

        st.error(
            "Quantity must be greater than 0."
        )

    else:

        add_inventory_item(
            item_name=item_name.strip(),

            category="Other",

            quantity=quantity,

            unit=unit,

            purchase_date=date.today().isoformat(),

            expiry_date=expiry_date.isoformat(),

            storage_location="Kitchen",

            created_by=user_id,
        )

        st.success(
            f"{item_name.strip()} added to inventory."
        )

        st.rerun()


# =========================================================
# CURRENT INVENTORY
# =========================================================

st.markdown(
    '<div class="section-title">Current Inventory</div>',
    unsafe_allow_html=True,
)


items = get_inventory_items()

today = date.today()


# =========================================================
# EMPTY INVENTORY
# =========================================================

if not items:

    st.info(
        "📦 No inventory items yet. "
        "Add your first ingredient above."
    )


# =========================================================
# DISPLAY INVENTORY
# =========================================================

else:

    for index, item in enumerate(items):

        # =================================================
        # EXPIRY DATE
        # =================================================

        expiry = None

        if item["expiry_date"]:

            try:

                expiry = date.fromisoformat(
                    item["expiry_date"]
                )

            except ValueError:

                expiry = None


        # =================================================
        # EXPIRY STATUS
        # =================================================

        if expiry:

            days_left = (
                expiry - today
            ).days


            if days_left < 0:

                status_text = "Expired"

                status_class = "expired"


            elif days_left <= 3:

                status_text = "Expiring Soon"

                status_class = "expired"


            elif days_left <= 7:

                status_text = "Use Soon"

                status_class = "soon"


            else:

                status_text = "Fresh"

                status_class = "fresh"


        else:

            status_text = "No expiry date"

            status_class = "soon"


        # =================================================
        # INVENTORY CARD
        # =================================================

        with st.container(
            key=f"inventory-card-{index}"
        ):

            col1, col2, col3, col4 = st.columns(
                [2.6, 1.2, 1.5, 0.55]
            )


            # ---------------------------------------------
            # INGREDIENT
            # ---------------------------------------------

            with col1:

                st.markdown(
                    f"""
                    <div class="card-name">
                        📦 {item["item_name"]}
                    </div>

                    <div class="card-subtitle">
                        Restaurant inventory
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


            # ---------------------------------------------
            # QUANTITY
            # ---------------------------------------------

            with col2:

                st.markdown(
                    f"""
                    <div class="card-label">
                        Quantity
                    </div>

                    <div class="card-value">
                        {item["quantity"]:g} {item["unit"]}
                    </div>
                    """,
                    unsafe_allow_html=True,
                )


            # ---------------------------------------------
            # EXPIRY
            # ---------------------------------------------

            with col3:

                expiry_text = (
                    expiry.strftime("%d %b %Y")
                    if expiry
                    else "Not set"
                )

                st.markdown(
                    f"""
                    <div class="card-label">
                        Expiry
                    </div>

                    <div class="card-value">
                        {expiry_text}
                    </div>

                    <span class="{status_class}">
                        {status_text}
                    </span>
                    """,
                    unsafe_allow_html=True,
                )


            # ---------------------------------------------
            # DELETE
            # ---------------------------------------------

            with col4:

                delete_button = st.button(
                    "🗑",
                    key=f"delete_{item['id']}",
                    help=f"Delete {item['item_name']}",
                )


                if delete_button:

                    delete_inventory_item(
                        item["id"]
                    )

                    st.rerun()