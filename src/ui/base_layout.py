import streamlit as st


def style_background_home():

    st.markdown("""
        <style>

            .stApp {
                background: #5865F2 !important;
            }

            .stApp div[data-testid="stColumn"] {
                background-color: #E0E3FF !important;
                padding: 2.5rem !important;
                border-radius: 5rem !important;
            }

        </style>
    """, unsafe_allow_html=True)


def style_background_dashboard():

    st.markdown("""
        <style>

            .stApp {
                background: #E0E3FF !important;
            }

        </style>
    """, unsafe_allow_html=True)


def style_base_layout():

    st.markdown("""
        <style>

            /* =================================
               FONTS
            ================================= */

            @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&display=swap');
            @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@100..900&display=swap');


            /* =================================
               HIDE STREAMLIT DEFAULT UI
            ================================= */

            #MainMenu,
            footer,
            header {
                visibility: hidden;
            }


            /* =================================
               MAIN CONTAINER
            ================================= */

            .block-container {
                padding-top: 1.5rem !important;
            }


            /* =================================
               HEADINGS
            ================================= */

            h1 {
                font-family: 'Climate Crisis', sans-serif !important;
                font-size: 3.5rem !important;
                line-height: 1.1 !important;
                margin-bottom: 0rem !important;
                color: black !important;
            }

            h2 {
                font-family: 'Climate Crisis', sans-serif !important;
                font-size: 2rem !important;
                line-height: 0.9 !important;
                margin-bottom: 0rem !important;
                color: black !important;
            }

            h3,
            h4,
            p {
                font-family: 'Outfit', sans-serif !important;
                color: black !important;
            }


            /* =================================
               STREAMLIT INPUT LABELS
            ================================= */

            div[data-testid="stWidgetLabel"] label,
            div[data-testid="stWidgetLabel"] p {
                color: black !important;
                font-family: 'Outfit', sans-serif !important;
            }


            /* =================================
               STREAMLIT DIALOG
            ================================= */

            div[data-testid="stDialog"] {
                background-color: #E0E3FF !important;
            }

            div[data-testid="stDialog"] [role="dialog"] {
                background-color: #E0E3FF !important;
                color: black !important;
            }

            div[data-testid="stDialog"] [role="dialog"] > div {
                background-color: #E0E3FF !important;
            }

            div[data-testid="stDialog"] h1,
            div[data-testid="stDialog"] h2,
            div[data-testid="stDialog"] h3,
            div[data-testid="stDialog"] h4,
            div[data-testid="stDialog"] p,
            div[data-testid="stDialog"] label {
                color: black !important;
            }


            /* =================================
               BUTTON TEXT
            ================================= */

            button,
            button *,
            [data-testid="stBaseButton-primary"],
            [data-testid="stBaseButton-primary"] *,
            [data-testid="stBaseButton-secondary"],
            [data-testid="stBaseButton-secondary"] *,
            [data-testid="stBaseButton-tertiary"],
            [data-testid="stBaseButton-tertiary"] * {
                color: white !important;
            }


            /* =================================
               PRIMARY BUTTON
            ================================= */

            button {
                border-radius: 1.5rem !important;
                background-color: #5865F2 !important;
                color: white !important;
                padding: 10px 20px !important;
                border: none !important;
                transition: transform 0.25s ease-in-out !important;
            }


            /* =================================
               SECONDARY BUTTON
            ================================= */

            button[kind="secondary"] {
                border-radius: 1.5rem !important;
                background-color: #EB459E !important;
                color: white !important;
                padding: 10px 20px !important;
                border: none !important;
                transition: transform 0.25s ease-in-out !important;
            }


            /* =================================
               TERTIARY BUTTON
            ================================= */

            button[kind="tertiary"] {
                border-radius: 1.5rem !important;
                background-color: black !important;
                color: white !important;
                padding: 10px 20px !important;
                border: none !important;
                transition: transform 0.25s ease-in-out !important;
            }


            /* =================================
               DIALOG CLOSE BUTTON
            ================================= */

            div[data-testid="stDialog"] button[aria-label="Close"] {
                background-color: #5865F2 !important;
                color: white !important;
            }

            div[data-testid="stDialog"] button[aria-label="Close"] * {
                color: white !important;
            }


            /* =================================
               TOAST NOTIFICATIONS
            ================================= */

            div[data-testid="stToast"],
            div[data-testid="stToast"] *,
            div[data-testid="stToast"] p,
            div[data-testid="stToast"] span {
                color: white !important;
            }


            /* =================================
               BUTTON HOVER
            ================================= */

            button:hover {
                transform: scale(1.05);
            }

        </style>
    """, unsafe_allow_html=True)