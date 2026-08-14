import streamlit as st


def subject_card(name, code, section, stats=None, footer_callback=None):

    html = f"""
    <div style="
        background: white;
        border-left: 8px solid #EB459E;
        padding: 25px;
        border-radius: 20px;
        border: 1px solid black;
        margin-bottom: 20px;
        color: #1e293b;
    ">

        <h3 style="
            margin: 0;
            color: #1e293b !important;
            font-size: 1.5rem;
        ">
            {name}
        </h3>

        <p style="
            color: #1e293b !important;
            margin: 10px 0;
        ">
            Code :

            <span style="
                background: #E0E3FF;
                color: #5865F2 !important;
                padding: 2px 8px;
                border-radius: 5px;
            ">
                {code}
            </span>

            |

            Section : {section}
        </p>
    """

    if stats:

        html += """
        <div style="
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        ">
        """

        for icon, label, value in stats:

            html += f"""
            <div style="
                background: #EB459E10;
                color: black !important;
                padding: 5px 12px;
                border-radius: 12px;
                font-size: 0.9rem;
            ">
                {icon}

                <b style="color: black !important;">
                    {value}
                </b>

                <span style="color: black !important;">
                    {label}
                </span>
            </div>
            """

        html += """
        </div>
        """

    html += """
    </div>
    """

    # Use Streamlit's HTML renderer
    st.html(html)

    if footer_callback:
        footer_callback()