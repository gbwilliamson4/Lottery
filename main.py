from datetime import date
from database import DB
import streamlit as st
from player import Player
from operator import attrgetter
import pandas as pd


# 0 is false, 1 is true

def main():
    # Setup page view
    st.set_page_config(layout="wide")
    st.title('Lottery! Woo!')
    player_list = []
    winning_nums = Player(0, 'winning_nums')

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        my_date = st.date_input('Date')
        todays_date = str(my_date)

    st.subheader('Players')

    # if show_all:
    #     all_data = db.select_all()
    #     for row in all_data:
    #         st.write(row[0])
    #         # Making a change

    col1, col2, col3, col4 = st.columns(4)
    players = db.get_players()
    for player in players:
        playerID = player[0]
        player_name = player[1]
        objPlayer = Player(playerID, player_name)
        player_list.append(objPlayer)

    for player in player_list:
        with col1:
            st.write(player.player_name)
            player.nonerisa = st.text_input('Non-Erisa', key=player.playerID)
        with col2:
            st.write(' _ ')
            player.erisa = st.text_input('Erisa', key=player.playerID)
        with col3:
            st.write(' _ ')
            player.cafeteria = st.text_input('Cafeteria', key=player.playerID)
        with col4:
            st.write(' _ ')
            player.operating = st.text_input('Operating', key=player.playerID)

    if st.button('Save Guesses'):
        db.store_guesses(player_list, todays_date)
        st.success('Guesses saved successfully.')

    st.header('Winning Numbers')
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        winning_nums.nonerisa = st.text_input('Non-Erisa')

    with col2:
        winning_nums.erisa = st.text_input('Erisa')

    with col3:
        winning_nums.cafeteria = st.text_input('Cafeteria')

    with col4:
        winning_nums.operating = st.text_input('Operating')

    if st.button('Calculate Winner'):
        calculate_winner(player_list, winning_nums, 1, todays_date)
        # db.store_winning_nums(winning_nums, todays_date)


def calculate_winner(player_list, winning_nums, gamemode, todays_date):
    if gamemode == 1:  # 1 is the normal gamemode. I'll do that one first then get the other ones going.
        # I'll have the gamemodes passed through from the database. That way they can move around in the tables but the functionality will remain
        col1, col2, col3, col4, col5 = st.columns(5)
        for player in player_list:
            # Do calculations here
            off_by_nonerisa = abs(int(player.nonerisa) - int(winning_nums.nonerisa))
            off_by_erisa = abs(int(player.erisa) - int(winning_nums.erisa))
            off_by_cafeteria = abs(int(player.cafeteria) - int(winning_nums.cafeteria))
            off_by_operating = abs(int(player.operating) - int(winning_nums.operating))
            total_off = off_by_nonerisa + off_by_erisa + off_by_cafeteria + off_by_operating
            player.total_off = total_off

            # Display on the app.
            with col1:
                st.write(player.player_name)
                st.text_input('Non-Erisa', value=off_by_nonerisa, disabled=True, key=player.playerID + 100)
            with col2:
                st.write(' _ ')
                st.text_input('Erisa', value=off_by_erisa, disabled=True, key=player.playerID + 100)
            with col3:
                st.write(' _ ')
                st.text_input('Cafeteria', value=off_by_cafeteria, disabled=True, key=player.playerID + 100)
            with col4:
                st.write(' _ ')
                st.text_input('Operating', value=off_by_operating, disabled=True, key=player.playerID + 100)
            with col5:
                st.write(' _ ')
                st.text_input('Total', value=total_off, disabled=True, key=player.playerID + 100)

        st.header("And the winner is...")
        winner = min(player_list, key=attrgetter('total_off'))
        st.header(winner.player_name)

    # Regardless of which gamemode, we need to log the winner in the database.
    db.log_winner(winner.playerID, gamemode, todays_date)


def figure_out_graphs():
    # Ok, we can save the date correctly.
    # Now, we need to get the date from the db and be able to treat it as a date
    df = db.date_testing3()
    df['ScanDate'] = pd.to_datetime(df['ScanDate'])
    st.bar_chart(df)
    st.line_chart(df)
    print(df)


def read_from_excel(): # This is used for getting dummy data into the db for testing
    df = pd.read_csv('''C:\\Users\\George\\Desktop\\Checkscan Dummy Data.csv''')
    # df.to_sql('checkscan', db.con, if_exists='append', index=False)
    db.inserting_dummy_data(df)


if __name__ == '__main__':
    db = DB()
    # db.create_table()
    # main()
    figure_out_graphs()
    # read_from_excel()
