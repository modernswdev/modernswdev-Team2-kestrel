import streamlit as st

pages = {
    "Pet Management": [
        st.Page("page1.py", title="🐾 Create Profile", icon="📝"),
    ],
    "Engine Analytics": [
        st.Page("page2.py", title="📊 Check Compatibility", icon="⚡"),
    ]
}

pg = st.navigation(pages)
pg.run()
