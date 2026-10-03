import streamlit as st
from datetime import date

from database import (
    add_donation_record,
    get_donation_records,
    delete_donation_record,
)


# ---------------------------------------------------------
# LOGIN CHECK
# ---------------------------------------------------------

if not st.session_state.get("logged_in", False):
    st.warning("Please log in to access Donations.")
    st.stop()


user = st.session_state.get("user", {})
user_id = user.get("id")


# ---------------------------------------------------------
# PAGE STYLING
# ---------------------------------------------------------

st.markdown(
    """
    <style>

    /* -----------------------------------------------------
       HEADER
    ----------------------------------------------------- */

    .donation-header {
        margin-bottom: 28px;
    }

    .donation-title {
        color: #292522;
        font-size: 34px;
        font-weight: 750;
        margin-bottom: 6px;
    }

    .donation-subtitle {
        color: #756c65;
        font-size: 15px;
    }


    /* -----------------------------------------------------
       DONATION FORM HEADER
    ----------------------------------------------------- */

    .donation-form-header {
        background: #eef3f7;
        border: 1px solid #d8e2e9;
        border-radius: 16px;
        padding: 18px 20px;
        margin-bottom: 18px;
    }

    .form-icon {
        font-size: 25px;
        margin-bottom: 5px;
    }

    .form-title {
        color: #304452;
        font-size: 20px;
        font-weight: 700;
    }

    .form-subtitle {
        color: #687983;
        font-size: 13px;
        margin-top: 4px;
    }


    /* -----------------------------------------------------
       DONATION BUTTON
    ----------------------------------------------------- */

    .stButton button[kind="primary"] {
    background: #4f7182 !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    min-height: 52px !important;
    font-size: 15px !important;
    font-weight: 700 !important;
}

.stButton button[kind="primary"]:hover {
    background: #3f5f6f !important;
    color: white !important;
}


    /* -----------------------------------------------------
       RECORDS SECTION
    ----------------------------------------------------- */

    .records-header {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-top: 34px;
        margin-bottom: 16px;
    }

    .records-title {
        color: #292522;
        font-size: 22px;
        font-weight: 700;
    }


    /* -----------------------------------------------------
       DONATION HANDOFF CARD
    ----------------------------------------------------- */

    .donation-card {
        background: #fffdf8;
        border: 1px solid #eadfca;
        border-left: 5px solid #c89b4a;
        border-radius: 15px;
        padding: 19px 20px;
        margin-bottom: 14px;
        box-shadow: 0 5px 14px rgba(50, 40, 35, 0.05);
    }

    .donation-item-name {
        color: #292522;
        font-size: 19px;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .donation-quantity {
        color: #5f574f;
        font-size: 15px;
        margin-bottom: 12px;
    }

    .recipient-label {
        color: #8a7654;
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 3px;
    }

    .recipient-name {
        color: #344d5b;
        font-size: 15px;
        font-weight: 700;
        margin-bottom: 9px;
    }

    .donation-date {
        color: #81776e;
        font-size: 13px;
    }

    .donation-notes {
        background: #f4f6f7;
        border-radius: 9px;
        padding: 9px 11px;
        margin-top: 12px;
        color: #6c7478;
        font-size: 13px;
    }


    /* -----------------------------------------------------
       DELETE BUTTON
    ----------------------------------------------------- */

    .delete-space {
        height: 18px;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.markdown(
    """<div class="donation-header">
<div class="donation-title">Donations</div>
<div class="donation-subtitle">
Manage food donations and keep a record of where surplus food goes.
</div>
</div>""",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# FORM HEADER
# ---------------------------------------------------------

st.markdown(
    """<div class="donation-form-header">
<div class="form-icon">🤝</div>
<div class="form-title">New Donation</div>
<div class="form-subtitle">
Record food that is being given to a recipient.
</div>
</div>""",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# DONATION FORM
# ---------------------------------------------------------

col1, col2 = st.columns(2)


with col1:

    item_name = st.text_input(
        "Food item",
        placeholder="e.g. Rice",
    )

    quantity = st.number_input(
        "Quantity donated",
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

    recipient = st.selectbox(
        "Recipient",
        [
            "Local Food Bank",
            "Community Kitchen",
            "Charity Organization",
            "Shelter",
            "School",
            "Relief Organization",
            "Other",
        ],
    )

    donation_date = st.date_input(
        "Donation date",
        value=date.today(),
    )

    notes = st.text_area(
        "Notes",
        placeholder="Optional notes about this donation",
        height=100,
    )


# ---------------------------------------------------------
# RECORD BUTTON
# ---------------------------------------------------------

col_left, col_button, col_right = st.columns([1, 2, 1])

with col_button:

    record_button = st.button(
        "🤝  Record Donation",
        key="record_donation",
        type="primary",
        use_container_width=True,
    )


# ---------------------------------------------------------
# SAVE DONATION
# ---------------------------------------------------------

if record_button:

    if not item_name.strip():

        st.error("Please enter a food item.")

    elif quantity <= 0:

        st.error("Please enter a quantity greater than 0.")

    else:

        add_donation_record(
            item_name=item_name.strip(),
            quantity=quantity,
            unit=unit,
            recipient=recipient,
            donation_date=donation_date.isoformat(),
            notes=notes.strip() or None,
            created_by=user_id,
        )

        st.success("Donation recorded successfully.")

        st.rerun()


# ---------------------------------------------------------
# RECORDED DONATIONS
# ---------------------------------------------------------

st.markdown(
    """<div class="records-header">
<div class="records-title">Donation History</div>
</div>""",
    unsafe_allow_html=True,
)


donation_records = get_donation_records()


if not donation_records:

    st.info("No donations have been recorded yet.")

else:

    for record in donation_records:

        item_name = record["item_name"]
        quantity = record["quantity"]
        unit = record["unit"]
        recipient = record["recipient"]
        donation_date = record["donation_date"]
        notes = record["notes"]
        donation_id = record["id"]

        col1, col2 = st.columns([5, 1])


        with col1:

            notes_html = ""

            if notes:

                notes_html = (
                    f'<div class="donation-notes">'
                    f'📝 {notes}'
                    f'</div>'
                )

            st.markdown(
                f"""<div class="donation-card">
<div class="donation-item-name">{item_name}</div>
<div class="donation-quantity">
{quantity:g} {unit} donated
</div>
<div class="recipient-label">
Recipient
</div>
<div class="recipient-name">
🤝 {recipient}
</div>
<div class="donation-date">
Donation date: {donation_date}
</div>
{notes_html}
</div>""",
                unsafe_allow_html=True,
            )


        with col2:

            st.markdown(
                '<div class="delete-space"></div>',
                unsafe_allow_html=True,
            )

            if st.button(
                "Delete",
                key=f"delete_donation_{donation_id}",
            ):

                delete_donation_record(donation_id)

                st.success("Donation deleted.")

                st.rerun()