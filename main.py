import sqlite3
from datetime import date
from database import DB
import streamlit as st


def main():
    st.set_page_config(layout="wide")
    data = st.text_input('Name')
    # st.button('Submit')
    show_all = st.button('Show All')

    if st.button('Submit'):
        st.success('Successfully written and committed to DB.')
        db.insert(data)

    if show_all:
        all_data = db.select_all()
        for row in all_data:
            st.write(row[0])


if __name__ == '__main__':
    db = DB()
    # db.create_table()
    main()
