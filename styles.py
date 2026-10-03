import streamlit as st


def apply_global_styles():

    # =========================================================
    # CHECK LOGIN STATUS
    # =========================================================

    logged_in = st.session_state.get("logged_in", False)

    # =========================================================
    # GLOBAL STYLES
    # =========================================================

    st.markdown(
        f"""
        <style>

        /* =====================================================
           SIDEBAR
           Show ONLY after login
        ===================================================== */

        section[data-testid="stSidebar"] {{
            background: #d8c9b8 !important;
        }}

        section[data-testid="stSidebar"] > div {{
            background: #d8c9b8 !important;
        }}


        /* =====================================================
           SIDEBAR TEXT
        ===================================================== */

        section[data-testid="stSidebar"] * {{
            color: #3f342c !important;
        }}


        /* =====================================================
           SIDEBAR NAVIGATION
        ===================================================== */

        section[data-testid="stSidebar"]
        [data-testid="stSidebarNavLink"] {{

            border-radius: 9px !important;

            margin: 3px 8px !important;

            padding: 10px 12px !important;

            transition: 0.2s ease !important;

            font-size: 17px !important;

            font-weight: 500 !important;
        }}


        /* =====================================================
           SIDEBAR HOVER
        ===================================================== */

        section[data-testid="stSidebar"]
        [data-testid="stSidebarNavLink"]:hover {{

            background: #cbb8a4 !important;
        }}


        /* =====================================================
           SELECTED PAGE
        ===================================================== */

        section[data-testid="stSidebar"]
        [data-testid="stSidebarNavLink"][aria-current="page"] {{

            background: #b99d82 !important;

            color: #2f261f !important;

            font-weight: 700 !important;
        }}


        /* =====================================================
           SIDEBAR DIVIDER
        ===================================================== */

        section[data-testid="stSidebar"] hr {{

            border-color: rgba(63, 52, 44, 0.15) !important;
        }}


            /* =====================================================
           HIDE "APP" FROM SIDEBAR
           ===================================================== */

        section[data-testid="stSidebarNav"]
        [data-testid="stSidebarNavLink"][href="/"] {{
            display: none !important;
        }}

        /* =====================================================
           LOGIN / REGISTER
           HIDE SIDEBAR COMPLETELY
        ===================================================== */

        {"section[data-testid='stSidebar'] { display: none !important; }" if not logged_in else ""}

        {"[data-testid='collapsedControl'] { display: none !important; }" if not logged_in else ""}


        /* =====================================================
           MAIN APPLICATION
        ===================================================== */

        .stApp {{
            background: #f7f3ed;
        }}


        /* =====================================================
           HIDE STREAMLIT MENU
        ===================================================== */

        #MainMenu {{
            visibility: hidden;
        }}

        footer {{
            visibility: hidden;
        }}

        header {{
            height: 0 !important;
            background: transparent !important;
        }}

        [data-testid="stAppViewContainer"] {{
            padding-top: 0rem !important;
        }}
        [data-testid="stMainBlockContainer"] {{
        padding-top: 0rem !important;
        }}
        section[data-testid="stMain"] > div:first-child {{
            padding-top: 0 !important;
        }}

        </style>
        """,
        unsafe_allow_html=True,
    )