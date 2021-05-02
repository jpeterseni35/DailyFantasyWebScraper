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
import datetime


def main():
    """Main Program"""

    driver = webdriver.Chrome()
    delay = 5  # seconds
    driver.get('https://www.rotowire.com/daily/mlb/optimizer.php?site=DraftKings')

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

        dkplayer = (player, position, team, opponent, starter, salary, projected_fpts, value,
                    middleline, overunder, projected_team_runs, projected_roster_percent, weather, date_time)
        try:
            cur = conn.cursor()  # cursor object
            cur.execute(sql, dkplayer)
            conn.commit()
            conn.close()
        except Error as e:
            print(e)

    def get_headers():
        """Gets the Draft Kings Daily Projections headers and puts them in a list"""
        try:
            element = WebDriverWait(driver, delay).until(
                EC.presence_of_element_located(
                    (By.ID, "webix_ss_header"))
            )
        # Time out garunteed so exception used to get elements
        except:
            rotodk_header = []
            for item in driver.find_elements_by_xpath('//div[@role="columnheader"]'):
                rotodk_header.append(item.text)
        return rotodk_header

    def get_cells_by_column(column_index):
        """Gets the cell data from Draft Kings Daily Projections and puts them in a list"""
        try:
            element = WebDriverWait(driver, delay).until(
                EC.presence_of_element_located(
                    (By.ID, "webix_ss_body"))
            )
        except:
            rotodk_body = []
            for item in driver.find_elements_by_xpath(f'//div[@aria-colindex="{column_index}"]'):
                rotodk_body.append(item.text)
        return rotodk_body

    # def get_column_index(rotodk_header):

    def get_input(column_index):
        """Gets the cell input type data from Draft Kings Daily Projections and puts them in a list"""
        try:
            element = WebDriverWait(driver, delay).until(
                EC.presence_of_element_located(
                    (By.ID, "webix_ss_body")))
        except:
            rotodk_body = []
            for item in driver.find_elements_by_xpath(f'//div[@aria-colindex="{column_index}"]/input[1]'):
                rotodk_body.append(item.get_attribute("value"))
        return rotodk_body

    # construct columns

    create_tables("dailyfantasyscraper.db")
    conn = create_connection("dailyfantasyscraper.db")
    create_player_projections()

    # player = get_cells_by_column(2)
    # position = get_cells_by_column(3)
    # team = get_cells_by_column(4)
    # opponent = get_cells_by_column(5)
    # starter = get_cells_by_column(6)
    # salary = get_input(7)
    # projected_fpts = get_input(8)
    # value = get_cells_by_column(9)
    # middleline = get_cells_by_column(10)
    # overunder = get_cells_by_column(11)
    # projected_team_runs = get_cells_by_column(12)
    # projected_roster_percent = get_cells_by_column(13)
    # weather = get_cells_by_column(14)
    # date_time = datetime.datetime.now()

    # print(f"{get_headers()}")
    # print(f"{players_col}")
    # print(f"{pos_col}")
    # print(f"{team_col}")
    # print(f"{opp_col}")
    # print(f"{start_col}")
    # print(f"{sal_col}")
    # print(f"{fpts_col}")
    # print(f"{val_col}")
    # print(f"{ml_col}")
    # print(f"{ou_col}")
    # print(f"{teamruns_col}")
    # print(f"{roster_percent_col}")
    # print(f"{weather_col}")
    driver.quit()


if __name__ == '__main__':
    main()
