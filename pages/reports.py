import streamlit as st
from datetime import date, datetime, timedelta

from database import (
    get_inventory_items,
    get_waste_records,
    get_donation_records,
)


# --------------------------------------------------
# LOGIN CHECK
# --------------------------------------------------

if not st.session_state.get("logged_in", False):
    st.warning("Please log in to access Reports.")
    st.stop()


# --------------------------------------------------
# PAGE STYLING
# --------------------------------------------------

st.markdown(
    """
<style>

.reports-header {
    margin-bottom: 28px;
}

.reports-title {
    color: #292522;
    font-size: 34px;
    font-weight: 750;
    margin-bottom: 6px;
}

.reports-subtitle {
    color: #756c65;
    font-size: 15px;
}

.filter-card {
    background: #ffffff;
    border: 1px solid #e7dfd7;
    border-radius: 16px;
    padding: 18px 20px;
    margin-bottom: 28px;
    box-shadow: 0 5px 14px rgba(50, 40, 35, 0.04);
}

.filter-title {
    color: #292522;
    font-size: 16px;
    font-weight: 700;
    margin-bottom: 12px;
}

.summary-card {
    border-radius: 16px;
    padding: 20px;
    min-height: 125px;
    box-sizing: border-box;
    margin-bottom: 10px;
}

.summary-card.inventory {
    background: #e8f1f8;
    border: 1px solid #d0e0ec;
}

.summary-card.waste {
    background: #fdeceb;
    border: 1px solid #f0ceca;
}

.summary-card.donations {
    background: #fff5dc;
    border: 1px solid #eedeb5;
}

.summary-card.expiry {
    background: #fff0e8;
    border: 1px solid #f0d2c3;
}

.summary-label {
    color: #6f665f;
    font-size: 13px;
    font-weight: 600;
    margin-bottom: 8px;
}

.summary-value {
    color: #292522;
    font-size: 30px;
    font-weight: 750;
}

.section-title {
    color: #292522;
    font-size: 22px;
    font-weight: 700;
    margin-top: 24px;
    margin-bottom: 16px;
}

.report-card {
    background: #ffffff;
    border: 1px solid #e7dfd7;
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 14px;
    box-shadow: 0 5px 14px rgba(50, 40, 35, 0.05);
}

.report-card-title {
    color: #292522;
    font-size: 17px;
    font-weight: 700;
    margin-bottom: 14px;
}

.empty-report {
    color: #81776e;
    font-size: 14px;
}

.report-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.report-value-waste {
    font-size: 24px;
    font-weight: 750;
    color: #a94f3a;
}

.report-value-donation {
    font-size: 24px;
    font-weight: 750;
    color: #9a7331;
}

.report-value-inventory {
    font-size: 24px;
    font-weight: 750;
    color: #46677a;
}

</style>
""",
    unsafe_allow_html=True,
)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    """
<div class="reports-header">
<div class="reports-title">Reports</div>
<div class="reports-subtitle">
Review inventory, waste, expiry, and donation activity across your restaurant.
</div>
</div>
""",
    unsafe_allow_html=True,
)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

inventory_items = get_inventory_items()
all_waste_records = get_waste_records()
all_donation_records = get_donation_records()


# --------------------------------------------------
# REPORT PERIOD FILTER
# --------------------------------------------------

st.markdown(
    """
<div class="filter-card">
<div class="filter-title">Report Period</div>
</div>
""",
    unsafe_allow_html=True,
)

period = st.selectbox(
    "Report period",
    [
        "All Time",
        "Last 7 Days",
        "Last 30 Days",
        "This Month",
        "Custom Range",
    ],
    label_visibility="collapsed",
)


today = date.today()

start_date = None
end_date = today


if period == "Last 7 Days":
    start_date = today - timedelta(days=6)

elif period == "Last 30 Days":
    start_date = today - timedelta(days=29)

elif period == "This Month":
    start_date = today.replace(day=1)

elif period == "Custom Range":

    custom_col1, custom_col2 = st.columns(2)

    with custom_col1:
        start_date = st.date_input(
            "Start date",
            value=today.replace(day=1),
        )

    with custom_col2:
        end_date = st.date_input(
            "End date",
            value=today,
        )


# --------------------------------------------------
# FILTER WASTE RECORDS
# --------------------------------------------------

waste_records = []

for record in all_waste_records:

    try:
        record_date = datetime.strptime(
            str(record["waste_date"]),
            "%Y-%m-%d",
        ).date()
    except (ValueError, TypeError):
        continue

    if start_date is None:
        waste_records.append(record)

    elif start_date <= record_date <= end_date:
        waste_records.append(record)


# --------------------------------------------------
# FILTER DONATION RECORDS
# --------------------------------------------------

donation_records = []

for record in all_donation_records:

    try:
        record_date = datetime.strptime(
            str(record["donation_date"]),
            "%Y-%m-%d",
        ).date()
    except (ValueError, TypeError):
        continue

    if start_date is None:
        donation_records.append(record)

    elif start_date <= record_date <= end_date:
        donation_records.append(record)


# --------------------------------------------------
# SUMMARY CALCULATIONS
# --------------------------------------------------

inventory_count = len(inventory_items)

total_waste_quantity = sum(
    float(record["quantity"])
    for record in waste_records
)

total_donation_quantity = sum(
    float(record["quantity"])
    for record in donation_records
)


# --------------------------------------------------
# EXPIRED ITEM COUNT
# --------------------------------------------------

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

        if expiry_date < today:
            expired_count += 1

    except (ValueError, TypeError):
        continue


# --------------------------------------------------
# SUMMARY CARDS
# --------------------------------------------------

col1, col2, col3, col4 = st.columns(4)


with col1:
    st.markdown(
        f"""
<div class="summary-card inventory">
<div class="summary-label">Inventory Items</div>
<div class="summary-value">{inventory_count}</div>
</div>
""",
        unsafe_allow_html=True,
    )


with col2:
    st.markdown(
        f"""
<div class="summary-card waste">
<div class="summary-label">Total Waste</div>
<div class="summary-value">{total_waste_quantity:g}</div>
</div>
""",
        unsafe_allow_html=True,
    )


with col3:
    st.markdown(
        f"""
<div class="summary-card donations">
<div class="summary-label">Donated Quantity</div>
<div class="summary-value">{total_donation_quantity:g}</div>
</div>
""",
        unsafe_allow_html=True,
    )


with col4:
    st.markdown(
        f"""
<div class="summary-card expiry">
<div class="summary-label">Expired Items</div>
<div class="summary-value">{expired_count}</div>
</div>
""",
        unsafe_allow_html=True,
    )


# --------------------------------------------------
# WASTE OVERVIEW
# --------------------------------------------------

st.markdown(
    '<div class="section-title">Waste Overview</div>',
    unsafe_allow_html=True,
)


if not waste_records:

    st.markdown(
        """
<div class="report-card">
<div class="report-card-title">Waste Summary</div>
<div class="empty-report">
No waste records found for this period.
</div>
</div>
""",
        unsafe_allow_html=True,
    )

else:

    waste_by_reason = {}

    for record in waste_records:

        reason = record["reason"]
        quantity = float(record["quantity"])

        waste_by_reason[reason] = (
            waste_by_reason.get(reason, 0)
            + quantity
        )

    for reason, quantity in sorted(
        waste_by_reason.items(),
        key=lambda x: x[1],
        reverse=True,
    ):

        st.markdown(
            f"""
<div class="report-card">
<div class="report-row">

<div>
<div class="report-card-title" style="margin-bottom: 4px;">
{reason}
</div>

<div class="empty-report">
Waste recorded
</div>
</div>

<div class="report-value-waste">
{quantity:g}
</div>

</div>
</div>
""",
            unsafe_allow_html=True,
        )


# --------------------------------------------------
# DONATION OVERVIEW
# --------------------------------------------------

st.markdown(
    '<div class="section-title">Donation Overview</div>',
    unsafe_allow_html=True,
)


if not donation_records:

    st.markdown(
        """
<div class="report-card">
<div class="report-card-title">Donation Summary</div>

<div class="empty-report">
No donation records found for this period.
</div>

</div>
""",
        unsafe_allow_html=True,
    )

else:

    donations_by_recipient = {}

    for record in donation_records:

        recipient = record["recipient"]
        quantity = float(record["quantity"])

        donations_by_recipient[recipient] = (
            donations_by_recipient.get(recipient, 0)
            + quantity
        )

    for recipient, quantity in sorted(
        donations_by_recipient.items(),
        key=lambda x: x[1],
        reverse=True,
    ):

        st.markdown(
            f"""
<div class="report-card">
<div class="report-row">

<div>
<div class="report-card-title" style="margin-bottom: 4px;">
🤝 {recipient}
</div>

<div class="empty-report">
Food donated
</div>
</div>

<div class="report-value-donation">
{quantity:g}
</div>

</div>
</div>
""",
            unsafe_allow_html=True,
        )


# --------------------------------------------------
# CURRENT INVENTORY
# --------------------------------------------------

st.markdown(
    '<div class="section-title">Current Inventory</div>',
    unsafe_allow_html=True,
)


if not inventory_items:

    st.markdown(
        """
<div class="report-card">
<div class="empty-report">
No inventory items are currently available.
</div>
</div>
""",
        unsafe_allow_html=True,
    )

else:

    inventory_summary = {}

    for item in inventory_items:

        unit = item["unit"]
        quantity = float(item["quantity"])

        inventory_summary[unit] = (
            inventory_summary.get(unit, 0)
            + quantity
        )

    for unit, quantity in sorted(
        inventory_summary.items(),
        key=lambda x: x[1],
        reverse=True,
    ):

        st.markdown(
            f"""
<div class="report-card">
<div class="report-row">

<div>
<div class="report-card-title" style="margin-bottom: 4px;">
Inventory
</div>

<div class="empty-report">
Current quantity in {unit}
</div>
</div>

<div class="report-value-inventory">
{quantity:g} {unit}
</div>

</div>
</div>
""",
            unsafe_allow_html=True,
        )