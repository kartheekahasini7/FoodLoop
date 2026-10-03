import streamlit as st
from datetime import date


from database import (
    get_inventory_items,
    mark_inventory_item_as_waste,
)


# ============================================================
# LOGIN CHECK
# ============================================================

if not st.session_state.get("logged_in", False):
    st.warning("Please log in to access Expiry.")
    st.stop()


# ============================================================
# PAGE STYLING
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       HEADER
    ======================================================== */

    .expiry-header {
        margin-bottom: 28px;
    }

    .expiry-title {
        font-size: 34px;
        font-weight: 750;
        color: #292522;
        margin-bottom: 6px;
    }

    .expiry-subtitle {
        font-size: 15px;
        color: #756c65;
    }


    /* ========================================================
       SUMMARY CARDS
    ======================================================== */

    .summary-card {
        border-radius: 16px;
        padding: 18px;
        min-height: 105px;
        box-sizing: border-box;
    }

    .summary-card.expired {
        background: #fde8e7;
        border: 1px solid #f3c9c6;
    }

    .summary-card.expiring {
        background: #fff0dc;
        border: 1px solid #f2d5ad;
    }

    .summary-card.use-soon {
        background: #fff7d6;
        border: 1px solid #eee0a7;
    }

    .summary-card.fresh {
        background: #e5f4eb;
        border: 1px solid #c8e5d4;
    }

    .summary-label {
        color: #756c65;
        font-size: 12px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .summary-number {
        color: #292522;
        font-size: 28px;
        font-weight: 750;
        margin-top: 6px;
    }


    /* ========================================================
       ITEM CARDS
    ======================================================== */

    .item-card {
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 14px;
        box-sizing: border-box;
        box-shadow: 0 6px 16px rgba(50, 40, 35, 0.06);
    }

    .item-card.expired {
        background: #fff5f4;
        border: 1px solid #f3c9c6;
    }

    .item-card.expiring {
        background: #fff8ed;
        border: 1px solid #f2d5ad;
    }

    .item-card.use-soon {
        background: #fffdf0;
        border: 1px solid #eee0a7;
    }

    .item-card.fresh {
        background: #f2faf5;
        border: 1px solid #c8e5d4;
    }


    /* ========================================================
       ITEM TEXT
    ======================================================== */

    .item-name {
        color: #292522;
        font-size: 18px;
        font-weight: 700;
    }

    .item-details {
        color: #756c65;
        font-size: 14px;
        margin-top: 6px;
    }


    /* ========================================================
       STATUS BADGES
    ======================================================== */

    .status-expired {
        display: inline-block;
        color: #b42318;
        background: #fde8e7;
        padding: 6px 10px;
        border-radius: 8px;
        font-size: 12px;
        font-weight: 700;
        margin-top: 14px;
    }

    .status-expiring {
        display: inline-block;
        color: #b54708;
        background: #fff0dc;
        padding: 6px 10px;
        border-radius: 8px;
        font-size: 12px;
        font-weight: 700;
        margin-top: 14px;
    }

    .status-use {
        display: inline-block;
        color: #8a6500;
        background: #fff7d6;
        padding: 6px 10px;
        border-radius: 8px;
        font-size: 12px;
        font-weight: 700;
        margin-top: 14px;
    }

    .status-fresh {
        display: inline-block;
        color: #28704b;
        background: #e5f4eb;
        padding: 6px 10px;
        border-radius: 8px;
        font-size: 12px;
        font-weight: 700;
        margin-top: 14px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="expiry-header">'
    '<div class="expiry-title">Expiry Monitoring</div>'
    '<div class="expiry-subtitle">'
    'Keep track of ingredients that need attention before they expire.'
    '</div>'
    '</div>',
    unsafe_allow_html=True,
)


# ============================================================
# GET INVENTORY
# ============================================================

inventory_items = [
    dict(item)
    for item in get_inventory_items()
]


# ============================================================
# CALCULATE EXPIRY STATUS
# ============================================================

expiry_items = []

for item in inventory_items:

    expiry_value = item.get("expiry_date")

    if not expiry_value:
        continue

    try:
        expiry_date = date.fromisoformat(expiry_value)

    except (ValueError, TypeError):
        continue

    days_left = (expiry_date - date.today()).days


    # --------------------------------------------------------
    # EXPIRED
    # --------------------------------------------------------

    if days_left < 0:

        status = "Expired"
        status_class = "status-expired"
        status_text = (
            f"Expired {abs(days_left)} day(s) ago"
        )


    # --------------------------------------------------------
    # EXPIRING SOON
    # --------------------------------------------------------

    elif days_left <= 3:

        status = "Expiring Soon"
        status_class = "status-expiring"
        status_text = f"{days_left} day(s) left"


    # --------------------------------------------------------
    # USE SOON
    # --------------------------------------------------------

    elif days_left <= 7:

        status = "Use Soon"
        status_class = "status-use"
        status_text = f"{days_left} day(s) left"


    # --------------------------------------------------------
    # FRESH
    # --------------------------------------------------------

    else:

        status = "Fresh"
        status_class = "status-fresh"
        status_text = f"{days_left} day(s) left"


    expiry_items.append(
        {
            "item": item,
            "expiry_date": expiry_date,
            "days_left": days_left,
            "status": status,
            "status_class": status_class,
            "status_text": status_text,
        }
    )


# ============================================================
# SUMMARY COUNTS
# ============================================================

expired_count = sum(
    1
    for item in expiry_items
    if item["status"] == "Expired"
)

expiring_count = sum(
    1
    for item in expiry_items
    if item["status"] == "Expiring Soon"
)

use_soon_count = sum(
    1
    for item in expiry_items
    if item["status"] == "Use Soon"
)

fresh_count = sum(
    1
    for item in expiry_items
    if item["status"] == "Fresh"
)


# ============================================================
# SUMMARY CARDS
# ============================================================

col1, col2, col3, col4 = st.columns(4)


# ------------------------------------------------------------
# EXPIRED
# ------------------------------------------------------------

with col1:

    st.markdown(
        f'<div class="summary-card expired">'
        f'<div class="summary-label">Expired</div>'
        f'<div class="summary-number">{expired_count}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


# ------------------------------------------------------------
# EXPIRING SOON
# ------------------------------------------------------------

with col2:

    st.markdown(
        f'<div class="summary-card expiring">'
        f'<div class="summary-label">Expiring Soon</div>'
        f'<div class="summary-number">{expiring_count}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


# ------------------------------------------------------------
# USE SOON
# ------------------------------------------------------------

with col3:

    st.markdown(
        f'<div class="summary-card use-soon">'
        f'<div class="summary-label">Use Soon</div>'
        f'<div class="summary-number">{use_soon_count}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


# ------------------------------------------------------------
# FRESH
# ------------------------------------------------------------

with col4:

    st.markdown(
        f'<div class="summary-card fresh">'
        f'<div class="summary-label">Fresh</div>'
        f'<div class="summary-number">{fresh_count}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


st.write("")


# ============================================================
# FILTER
# ============================================================

filter_option = st.selectbox(
    "Show",
    [
        "All Items",
        "Expired",
        "Expiring Soon",
        "Use Soon",
        "Fresh",
    ],
)


# ============================================================
# FILTER ITEMS
# ============================================================

if filter_option == "All Items":

    visible_items = expiry_items.copy()

else:

    visible_items = [
        item
        for item in expiry_items
        if item["status"] == filter_option
    ]


# ============================================================
# SORT BY EXPIRY DATE
# ============================================================

visible_items.sort(
    key=lambda item: item["expiry_date"]
)


# ============================================================
# DISPLAY ITEMS
# ============================================================

if not visible_items:

    st.info(
        "No inventory items match this expiry filter."
    )

else:

    for expiry_item in visible_items:

        item = expiry_item["item"]

        item_name = item.get(
            "item_name",
            "Unnamed item",
        )

        quantity = item.get(
            "quantity",
            0,
        )

        unit = item.get(
            "unit",
            "",
        )

        expiry_date = expiry_item["expiry_date"]

        status_class = expiry_item["status_class"]

        status_text = expiry_item["status_text"]


        # ----------------------------------------------------
        # DETERMINE ITEM CARD COLOR
        # ----------------------------------------------------

        card_class = {
            "status-expired": "expired",
            "status-expiring": "expiring",
            "status-use": "use-soon",
            "status-fresh": "fresh",
        }.get(
            status_class,
            "fresh",
        )


        # ----------------------------------------------------
        # ITEM CARD
        # ----------------------------------------------------

        col1, col2 = st.columns([5, 1])

        with col1:

            st.markdown(
                f'<div class="item-card {card_class}">'
                f'<div class="item-name">{item_name}</div>'
                f'<div class="item-details">'
                f'Quantity: {quantity:g} {unit}'
                f' &nbsp;&nbsp;•&nbsp;&nbsp; '
                f'Expiry: {expiry_date.strftime("%d %b %Y")}'
                f'</div>'
                f'<div class="{status_class}">'
                f'{status_text}'
                f'</div>'
                f'</div>',
                unsafe_allow_html=True,
            )

        with col2:

            if expiry_item["status"] == "Expired":

                st.markdown(
                    "<div style='height: 18px;'></div>",
                    unsafe_allow_html=True,
                )

                if st.button(
                    "Mark as Waste",
                    key=f"mark_waste_{item['id']}",
                ):

                    success = mark_inventory_item_as_waste(
                        item_id=item["id"],
                        reason="Expired",
                        waste_date=date.today().isoformat(),
                    )

                    if success:
                        st.success(
                            f"{item_name} moved to Waste."
                        )
                        st.rerun()