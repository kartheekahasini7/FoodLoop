import streamlit as st
from datetime import date

from database import (
    add_waste_record,
    get_waste_records,
    delete_waste_record,
)


# ---------------------------------------------------------
# LOGIN CHECK
# ---------------------------------------------------------

if not st.session_state.get("logged_in", False):
    st.warning("Please log in to access Waste.")
    st.stop()


user = st.session_state.get("user", {})
user_id = user.get("id")


# ---------------------------------------------------------
# PAGE STYLING
# ---------------------------------------------------------

st.markdown(
    """
    <style>

    .waste-page {
        max-width: 1100px;
        margin: 0 auto;
    }

    .waste-header {
        margin-bottom: 25px;
    }

    .waste-title {
        font-size: 34px;
        font-weight: 700;
        color: #3f342c;
        margin-bottom: 5px;
    }

    .waste-subtitle {
        font-size: 16px;
        color: #75685f;
    }

    .section-title {
        font-size: 22px;
        font-weight: 700;
        color: #3f342c;
        margin-bottom: 18px;
    }

    .waste-record-card {
        background: #ffffff;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 14px;
        border: 1px solid #eee5dc;
        box-shadow: 0 5px 14px rgba(50, 40, 35, 0.05);
    }

    .waste-item-name {
        font-size: 19px;
        font-weight: 700;
        color: #3f342c;
        margin-bottom: 7px;
    }

    .waste-details {
        font-size: 15px;
        color: #75685f;
        margin-bottom: 8px;
    }

    .waste-reason {
        display: inline-block;
        background: #fff0e8;
        color: #9a4f38;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.markdown(
    """
    <div class="waste-page">
        <div class="waste-header">
            <div class="waste-title">Waste Management</div>
            <div class="waste-subtitle">
                Record and track food waste in your restaurant.
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# RECORD WASTE
# ---------------------------------------------------------

st.markdown(
    '<div class="section-title">Record Food Waste</div>',
    unsafe_allow_html=True,
)


col1, col2 = st.columns(2)


with col1:

    item_name = st.text_input(
        "Food item",
        placeholder="e.g. Tomatoes",
    )

    quantity = st.number_input(
        "Quantity wasted",
        min_value=0.0,
        step=0.1,
    )

    unit = st.selectbox(
        "Unit",
        [
            "kg",
            "g",
            "litres",
            "ml",
            "pieces",
            "packets",
        ],
    )


with col2:

    reason = st.selectbox(
        "Reason for waste",
        [
            "Expired",
            "Spoiled",
            "Overproduction",
            "Preparation Waste",
            "Customer Leftovers",
            "Damaged",
            "Other",
        ],
    )

    waste_date = st.date_input(
        "Waste date",
        value=date.today(),
    )


st.markdown(
    "<div style='height: 8px;'></div>",
    unsafe_allow_html=True,
)


record_button = st.button(
    "Record Waste",
    type="primary",
    use_container_width=True,
)


# ---------------------------------------------------------
# SAVE WASTE RECORD
# ---------------------------------------------------------

if record_button:

    if not item_name.strip():

        st.error("Please enter a food item.")

    elif quantity <= 0:

        st.error("Please enter a quantity greater than 0.")

    else:

        add_waste_record(
            item_name=item_name.strip(),
            quantity=quantity,
            unit=unit,
            reason=reason,
            waste_date=waste_date.isoformat(),
            created_by=user_id,
        )

        st.success("Waste record added successfully.")

        st.rerun()


# ---------------------------------------------------------
# RECORDED WASTE
# ---------------------------------------------------------

st.markdown(
    '<div class="section-title">Recorded Waste</div>',
    unsafe_allow_html=True,
)


waste_records = get_waste_records()


if not waste_records:

    st.info("No waste records have been recorded yet.")

else:

    for record in waste_records:

        item_name = record["item_name"]
        quantity = record["quantity"]
        unit = record["unit"]
        reason = record["reason"]
        waste_date = record["waste_date"]
        waste_id = record["id"]

        col1, col2 = st.columns([5, 1])

        with col1:

            st.markdown(
                f"""<div class="waste-record-card">
<div class="waste-item-name">{item_name}</div>
<div class="waste-details">
Quantity: {quantity:g} {unit}
&nbsp;&nbsp;•&nbsp;&nbsp;
Date: {waste_date}
</div>
<div class="waste-reason">{reason}</div>
</div>""",
                unsafe_allow_html=True,
            )

        with col2:

            st.markdown(
                "<div style='height: 18px;'></div>",
                unsafe_allow_html=True,
            )

            if st.button(
                "Delete",
                key=f"delete_waste_{waste_id}",
            ):

                delete_waste_record(waste_id)

                st.success("Waste record deleted.")

                st.rerun()