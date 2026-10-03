import streamlit as st
from datetime import date, datetime

from styles import apply_global_styles

from database import (
    get_inventory_items,
    get_waste_records,
    get_donation_records,
)


apply_global_styles()


def show_dashboard(user):

    # =========================================================
    # USER INFORMATION
    # =========================================================

    if not user:
        user = {}

    name = (
        user.get("full_name")
        or user.get("name")
        or user.get("username")
        or "User"
    )

    role = user.get("role") or "Restaurant Staff"


    # =========================================================
    # LOAD LIVE DATA
    # =========================================================

    inventory_items = get_inventory_items()
    waste_records = get_waste_records()
    donation_records = get_donation_records()

    today = date.today()


    # =========================================================
    # INVENTORY COUNT
    # =========================================================

    inventory_count = len(inventory_items)


    # =========================================================
    # EXPIRY CALCULATIONS
    # =========================================================

    expiring_soon_count = 0
    expired_count = 0

    for item in inventory_items:

        try:
            expiry_value = item["expiry_date"]

            if isinstance(expiry_value, date):
                expiry_date = expiry_value
            else:
                expiry_date = datetime.strptime(
                    str(expiry_value),
                    "%Y-%m-%d",
                ).date()

            days_left = (expiry_date - today).days

            if days_left < 0:
                expired_count += 1

            elif days_left <= 3:
                expiring_soon_count += 1

        except (ValueError, TypeError):
            continue


    # =========================================================
    # TODAY'S WASTE
    # =========================================================

    todays_waste = []

    for record in waste_records:

        if str(record["waste_date"]) == today.isoformat():
            todays_waste.append(record)

    todays_waste_quantity = sum(
        float(record["quantity"])
        for record in todays_waste
    )


    # =========================================================
    # TODAY'S DONATIONS
    # =========================================================

    todays_donations = []

    for record in donation_records:

        if str(record["donation_date"]) == today.isoformat():
            todays_donations.append(record)

    todays_donation_count = len(todays_donations)


    # =========================================================
    # PAGE DESIGN
    # =========================================================

    st.markdown(
        """
<style>

.stApp {
    background: #f3eee7;
}

.block-container {
    max-width: 1250px;
    padding-top: 0rem;
    padding-bottom: 2rem;
}

/* ---------------- HEADER ---------------- */

.dashboard-title {
    color: #292522;
    font-size: 36px;
    font-weight: 750;
    margin-bottom: 4px;
}

.dashboard-subtitle {
    color: #766d66;
    font-size: 15px;
    margin-bottom: 12px;
}

.role-badge {
    display: inline-block;
    background: #f5ddd4;
    color: #b84e35;
    padding: 7px 15px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
}

/* ---------------- SECTION TITLES ---------------- */

.section-title {
    color: #292522;
    font-size: 21px;
    font-weight: 700;
    margin-top: 30px;
    margin-bottom: 14px;
}

/* ---------------- SUMMARY CARDS ---------------- */

.summary-card {
    border-radius: 18px;
    padding: 21px;
    min-height: 155px;
    border: 1px solid rgba(50, 40, 35, 0.08);
    box-shadow: 0 7px 18px rgba(50, 40, 35, 0.08);
}

.inventory-card {
    background: #e8f1f8;
}

.expiry-card {
    background: #fff0e8;
}

.waste-card {
    background: #e8f3ec;
}

.donation-card {
    background: #fff5d9;
}

.card-icon {
    font-size: 27px;
    margin-bottom: 12px;
}

.card-label {
    color: #625a54;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.6px;
    text-transform: uppercase;
}

.card-number {
    color: #292522;
    font-size: 31px;
    font-weight: 750;
    margin-top: 8px;
}

.card-description {
    color: #766d66;
    font-size: 12px;
    margin-top: 4px;
}

/* ---------------- ATTENTION ---------------- */

.attention-expiry {
    background: #fff1e9;
    border-left: 5px solid #e2744f;
    border-radius: 12px;
    padding: 17px 20px;
    margin-bottom: 12px;
}

.attention-good {
    background: #edf6ef;
    border-left: 5px solid #6ba47a;
    border-radius: 12px;
    padding: 17px 20px;
    margin-bottom: 12px;
}

/* ---------------- ACTIVITY ---------------- */

.activity-card {
    background: #ffffff;
    border-radius: 16px;
    padding: 18px 20px;
    border: 1px solid #e3d9cf;
    box-shadow: 0 6px 16px rgba(50, 40, 35, 0.06);
    min-height: 105px;
}

.activity-title {
    color: #292522;
    font-size: 14px;
    font-weight: 700;
}

.activity-text {
    color: #817872;
    font-size: 12px;
    margin-top: 7px;
}

/* ---------------- QUICK ACTION CARDS ---------------- */

.action-card {
    border-radius: 17px;
    padding: 21px;
    min-height: 165px;
    border: 1px solid rgba(50, 40, 35, 0.08);
    box-shadow: 0 7px 18px rgba(50, 40, 35, 0.08);
}

.action-inventory {
    background: #eaf3fa;
}

.action-waste {
    background: #eaf5ee;
}

.action-expiry {
    background: #fff1e8;
}

.action-icon {
    font-size: 29px;
    margin-bottom: 10px;
}

.action-title {
    color: #292522;
    font-size: 16px;
    font-weight: 700;
}

.action-text {
    color: #756c65;
    font-size: 12px;
    margin-top: 6px;
}

/* ---------------- BUTTONS ---------------- */

.stButton > button {
    border-radius: 10px;
    min-height: 40px;
    background: #ffffff;
    color: #3f3935;
    border: 1px solid #d9cec3;
    font-weight: 600;
}

.stButton > button:hover {
    border-color: #d65f3f;
    color: #d65f3f;
}

</style>
""",
        unsafe_allow_html=True,
    )


    # =========================================================
    # HEADER
    # =========================================================

    st.markdown(
        f"""
<div class="dashboard-title">hey hiii— {name} 👋</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        """
<div class="dashboard-subtitle">
Here's what is happening in your restaurant today.
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
<span class="role-badge">{role}</span>
""",
        unsafe_allow_html=True,
    )


    # =========================================================
    # TODAY'S OPERATIONS
    # =========================================================

    st.markdown(
        '<div class="section-title">Today\'s Operations</div>',
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)


    with col1:
        st.markdown(
            f"""
<div class="summary-card inventory-card">
<div class="card-icon">📦</div>
<div class="card-label">Inventory</div>
<div class="card-number">{inventory_count}</div>
<div class="card-description">items in stock</div>
</div>
""",
            unsafe_allow_html=True,
        )


    with col2:
        st.markdown(
            f"""
<div class="summary-card expiry-card">
<div class="card-icon">⏰</div>
<div class="card-label">Expiring Soon</div>
<div class="card-number">{expiring_soon_count}</div>
<div class="card-description">items need attention</div>
</div>
""",
            unsafe_allow_html=True,
        )


    with col3:
        st.markdown(
            f"""
<div class="summary-card waste-card">
<div class="card-icon">♻️</div>
<div class="card-label">Today's Waste</div>
<div class="card-number">{todays_waste_quantity:g} kg</div>
<div class="card-description">food waste recorded</div>
</div>
""",
            unsafe_allow_html=True,
        )


    with col4:
        st.markdown(
            f"""
<div class="summary-card donation-card">
<div class="card-icon">🤝</div>
<div class="card-label">Donations</div>
<div class="card-number">{todays_donation_count}</div>
<div class="card-description">donations today</div>
</div>
""",
            unsafe_allow_html=True,
        )


    # =========================================================
    # NEEDS ATTENTION
    # =========================================================

    st.markdown(
        '<div class="section-title">Needs Attention</div>',
        unsafe_allow_html=True,
    )


    if expired_count > 0:

        expiry_message = (
            f"{expired_count} item"
            f"{'s' if expired_count != 1 else ''} "
            "have expired and need attention."
        )

        attention_class = "attention-expiry"
        attention_icon = "⚠️"

    elif expiring_soon_count > 0:

        expiry_message = (
            f"{expiring_soon_count} item"
            f"{'s' if expiring_soon_count != 1 else ''} "
            "are approaching expiry."
        )

        attention_class = "attention-expiry"
        attention_icon = "⏰"

    else:

        expiry_message = (
            "No ingredients are currently approaching expiry."
        )

        attention_class = "attention-good"
        attention_icon = "✓"


    st.markdown(
        f"""
<div class="{attention_class}">
<div class="activity-title">
{attention_icon} Expiry Check
</div>
<div class="activity-text">
{expiry_message}
</div>
</div>
""",
        unsafe_allow_html=True,
    )


    if st.button(
        "Check expiry",
        key="dashboard_check_expiry",
    ):
        st.switch_page("pages/expiry.py")


    # =========================================================
    # TODAY'S ACTIVITY
    # =========================================================

    st.markdown(
        '<div class="section-title">Today\'s Activity</div>',
        unsafe_allow_html=True,
    )

    activity1, activity2, activity3 = st.columns(3)


    with activity1:

        if inventory_count > 0:
            inventory_activity = (
                f"{inventory_count} item"
                f"{'s' if inventory_count != 1 else ''} "
                "currently in stock."
            )
        else:
            inventory_activity = (
                "No inventory items currently in stock."
            )

        st.markdown(
            f"""
<div class="activity-card">
<div class="activity-title">📦 Inventory</div>
<div class="activity-text">
{inventory_activity}
</div>
</div>
""",
            unsafe_allow_html=True,
        )


    with activity2:

        if todays_waste:

            waste_activity = (
                f"{todays_waste_quantity:g} kg "
                "of food waste recorded today."
            )

        else:

            waste_activity = "No waste records today."

        st.markdown(
            f"""
<div class="activity-card">
<div class="activity-title">♻️ Food Waste</div>
<div class="activity-text">
{waste_activity}
</div>
</div>
""",
            unsafe_allow_html=True,
        )


    with activity3:

        if todays_donations:

            donation_activity = (
                f"{todays_donation_count} donation"
                f"{'s' if todays_donation_count != 1 else ''} "
                "recorded today."
            )

        else:

            donation_activity = "No donations recorded today."

        st.markdown(
            f"""
<div class="activity-card">
<div class="activity-title">🤝 Donations</div>
<div class="activity-text">
{donation_activity}
</div>
</div>
""",
            unsafe_allow_html=True,
        )


    # =========================================================
    # QUICK ACTIONS
    # =========================================================

    st.markdown(
        '<div class="section-title">Quick Actions</div>',
        unsafe_allow_html=True,
    )

    action1, action2, action3 = st.columns(3)


    # ---------------------------------------------------------
    # INVENTORY
    # ---------------------------------------------------------

    with action1:

        st.markdown(
            """
<div class="action-card action-inventory">
<div class="action-icon">📦</div>
<div class="action-title">Add Inventory</div>
<div class="action-text">
Record ingredients and stock received by the restaurant.
</div>
</div>
""",
            unsafe_allow_html=True,
        )

        if st.button(
            "Open Inventory",
            key="open_inventory",
            use_container_width=True,
        ):
            st.switch_page("pages/inventory.py")


    # ---------------------------------------------------------
    # WASTE
    # ---------------------------------------------------------

    with action2:

        st.markdown(
            """
<div class="action-card action-waste">
<div class="action-icon">♻️</div>
<div class="action-title">Record Food Waste</div>
<div class="action-text">
Record ingredients or prepared food that was wasted.
</div>
</div>
""",
            unsafe_allow_html=True,
        )

        if st.button(
            "Open Food Waste",
            key="open_waste",
            use_container_width=True,
        ):
            st.switch_page("pages/waste.py")


    # ---------------------------------------------------------
    # EXPIRY
    # ---------------------------------------------------------

    with action3:

        st.markdown(
            """
<div class="action-card action-expiry">
<div class="action-icon">⏰</div>
<div class="action-title">Check Expiry</div>
<div class="action-text">
Review ingredients that need to be used soon.
</div>
</div>
""",
            unsafe_allow_html=True,
        )

        if st.button(
            "Open Expiry",
            key="open_expiry",
            use_container_width=True,
        ):
            st.switch_page("pages/expiry.py")