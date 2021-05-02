# A web scraper that pulls the probable pitchers and batters of the MLB games of the day. After receiving
# the probable players, it gathers daily projection data from public sources to find an aggregate value and
# stores them in a database. Finally, the program outputs the data, either displayed in the GUI or as a CSV
# file.

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import sqlite3
import tkinter
from sqlite3 import Error
from tkinter import ttk
from tkinter import messagebox
import datetime
import time


def main():
    """Main Program"""

    # initiate selinum driver
    driver = webdriver.Chrome()
    delay = 5  # seconds
    driver.get('https://www.rotowire.com/daily/mlb/optimizer.php?site=DraftKings')
    time.sleep(delay)  # wait for javascript to load

    def create_connection(db):
        """ Connect to a SQLite database
        :param db: filename of database
        :return connection if no error, otherwise None"""
        try:
            conn = sqlite3.connect(db)
            return conn
        except Error as err:
            print(err)
        return None

    def create_table(conn, sql_create_table):
        """ Creates table with given sql statement
        :param conn: Connection object
        :param sql_create_table: a SQL CREATE TABLE statement
        :return:
        """
        try:
            c = conn.cursor()
            c.execute(sql_create_table)
        except Error as e:
            print(e)

    def create_tables(database):

        sql_create_rotowiredk_table = """ CREATE TABLE IF NOT EXISTS rotowiredk (
                                            id integer PRIMARY KEY,
                                            player text NOT NULL,
                                            position text NOT NULL,
                                            team text NOT NULL,
                                            opponent text NOT NULL,
                                            starter text NOT NULL,
                                            salary text NOT NULL,
                                            projected_fpts real NOT NULL,
                                            value real NOT NULL,
                                            middleline text NOT NULL,
                                            overunder real NOT NULL,
                                            projected_team_runs real NOT NULL,
                                            projected_roster_percent real NOT NULL,
                                            weather text NOT NULL,
                                            date_time numeric NOT NULL

                                        ); """
        # Future Table
        # sql_create_rotowirefd_table = """CREATE TABLE IF NOT EXISTS rotowirefd (
        #                                 id integer PRIMARY KEY,
        #                                 major text NOT NULL,
        #                                 startdate text NOT NULL,
        #                                 FOREIGN KEY (id) REFERENCES person (id)
        #                             );"""

        # create a database connection

        conn = create_connection(database)
        if conn is not None:
            # create rotowiredk table
            create_table(conn, sql_create_rotowiredk_table)
            # # create rotowirefd table
            # create_table(conn, sql_create_rotowirefd_table)
        else:
            print("Unable to connect to " + str(database))

    def create_player_projections():
        """Create a new player for table
        :param conn:
        :param player:
        :return: player id
        """
        conn = create_connection("dailyfantasyscraper.db")

        sql = ''' INSERT INTO rotowiredk(player,position,team,opponent,starter,salary,projected_fpts,value,
                                                middleline,overunder,projected_team_runs,projected_roster_percent,weather,date_time)
                  VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''

        # Scrape data to put into lists
        player = get_cells_by_column(2)
        position = get_cells_by_column(3)
        team = get_cells_by_column(4)
        opponent = get_cells_by_column(5)
        starter = get_cells_by_column(6)
        salary = get_input(7)
        projected_fpts = get_input(8)
        value = get_cells_by_column(9)
        middleline = get_cells_by_column(10)
        overunder = get_cells_by_column(11)
        projected_team_runs = get_cells_by_column(12)
        projected_roster_percent = get_cells_by_column(13)
        weather = get_cells_by_column(14)
        date_time = datetime.datetime.now()

        # Establish list of lists
        index = 0
        dkplayer = [player[index], position[index], team[index], opponent[index], starter[index], salary[index], projected_fpts[index], value[index],
                    middleline[index], overunder[index], projected_team_runs[index], projected_roster_percent[index], weather[index], date_time]
        loading_message = "Inserting"
        # loop through lists of lists and insert row into database for each index value
        try:
            # use salary due to reliabile length and clean data. -1 to prevent index out of range
            for index in range((len(salary)-1)):
                dkplayer = [player[index], position[index], team[index], opponent[index], starter[index], salary[index], projected_fpts[index], value[index],
                            middleline[index], overunder[index], projected_team_runs[index], projected_roster_percent[index], weather[index], date_time]
                cur = conn.cursor()  # cursor object
                cur.execute(sql, dkplayer)
                conn.commit()
                print(f"{loading_message} {dkplayer} into database...")
                index = index + 1
            conn.close()
            messagebox.showinfo(
                'Results', 'Daily Projections added to database.')
        except Error as e:
            print(e)

    def get_cells_by_column(column_index):
        """Gets the cell data from Draft Kings Daily Projections and puts them in a list"""
        try:
            rotodk_body = []
            loading_message = "Scraping"
            for item in driver.find_elements_by_xpath(f'//div[@aria-colindex="{column_index}"]'):
                rotodk_body.append(item.text)
                # print loading message
                print(f"{loading_message} {item.text}...")
        except Error as e:
            print(e)
        return rotodk_body

    def get_input(column_index):
        """Gets the cell input type data from Draft Kings Daily Projections and puts them in a list"""
        try:
            rotodk_body = []
            loading_message = "Scraping"
            for item in driver.find_elements_by_xpath(f'//div[@aria-colindex="{column_index}"]/input[1]'):
                rotodk_body.append(item.get_attribute("value"))
                # print loading message
                print(f"{loading_message} {item.get_attribute('value')}...")
        except Error as e:
            print(e)
        return rotodk_body

    # call functions
    create_tables("dailyfantasyscraper.db")
    conn = create_connection("dailyfantasyscraper.db")
    # create_player_projections()

    #### Work in progress #######
    #### Want to spit results to GUI and have launcher to kick off selenium driver #####
    main_window = tkinter.Tk()
    title = main_window.title("Roto Scraper Launcher")
    main_window.geometry("300x150")
    btn_add_players = tkinter.Button(
        main_window, text="Add Player Projections to Database", command=create_player_projections)
    btn_add_players.pack()
    main_window.mainloop()
    driver.quit()


main()
