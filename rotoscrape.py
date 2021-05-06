# A web scraper that pulls the probable pitchers and batters of the MLB games of the day. After receiving
# the probable players, it gathers daily projection data from public sources to find an aggregate value and
# stores them in a database. Finally, the program outputs the data, either displayed in the GUI or as a CSV
# file.

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import sqlite3
import tkinter
from sqlite3 import Error
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
import datetime
import time


class RotoScrape:

    """RotoScrape main class"""

    def initiate_driver(self):
        """initiate selenium driver"""
        global driver
        driver = None
        if not driver:
            driver = webdriver.Chrome()
            delay = 5  # seconds
            driver.get(
                'https://www.rotowire.com/daily/mlb/optimizer.php?site=DraftKings')
            time.sleep(delay)  # wait for javascript to load

            # Eventually will update script to automatically scroll so we don't need to, to perform a large scrape
            # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def close_driver(self):
        """Close selenium driver"""
        global driver
        if driver:
            driver.close()
            driver = None

    def create_connection(self, db):
        """ Connect to a SQLite database
        :param db: filename of database
        :return connection if no error, otherwise None"""
        try:
            conn = sqlite3.connect(db)
            return conn
        except Error as err:
            print(err)
        return None

    def create_table(self, conn, sql_create_table):
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

    def create_tables(self, database):
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
        conn = rs.create_connection(database)
        if conn is not None:
            # create rotowiredk table
            rs.create_table(conn, sql_create_rotowiredk_table)
            # # create rotowirefd table
            # create_table(conn, sql_create_rotowirefd_table)
        else:
            print("Unable to connect to " + str(database))

    def create_player_projections(self):
        """Create a new player for table
        :param conn:
        :param player:
        :return: player id
        """
        conn = rs.create_connection("dailyfantasyscraper.db")
        sql = ''' INSERT INTO rotowiredk(player,position,team,opponent,starter,salary,projected_fpts,value,
                                                middleline,overunder,projected_team_runs,projected_roster_percent,weather,date_time)
                  VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''
        try:
            # Scrape data to put into lists
            player = rs.get_cells_by_column(2)
            position = rs.get_cells_by_column(3)
            team = rs.get_cells_by_column(4)
            opponent = rs.get_cells_by_column(5)
            starter = rs.get_cells_by_column(6)
            salary = rs.get_input(7)
            projected_fpts = rs.get_input(8)
            value = rs.get_cells_by_column(9)
            middleline = rs.get_cells_by_column(10)
            overunder = rs.get_cells_by_column(11)
            projected_team_runs = rs.get_cells_by_column(12)
            projected_roster_percent = rs.get_cells_by_column(13)
            weather = rs.get_cells_by_column(14)
            date_time = datetime.datetime.now()
            # Establish list of lists
            index = 0
            dkplayer = [player[index], position[index], team[index], opponent[index], starter[index], salary[index], projected_fpts[index], value[index],
                        middleline[index], overunder[index], projected_team_runs[index], projected_roster_percent[index], weather[index], date_time]
            # loop through lists of lists and insert row into database for each index value
            # use salary due to reliabile length and clean data. -1 to prevent index out of range
            for index in range((len(salary)-1)):
                dkplayer = [player[index], position[index], team[index], opponent[index], starter[index], salary[index], projected_fpts[index], value[index],
                            middleline[index], overunder[index], projected_team_runs[index], projected_roster_percent[index], weather[index], date_time]
                cur = conn.cursor()  # cursor object
                cur.execute(sql, dkplayer)
                conn.commit()
                rs.write(f"Inserting {dkplayer[0]} into database...")
                main_window.update()
                index = index + 1
            conn.close()
            messagebox.showinfo(
                'Results', 'Daily Projections added to database.')
            rs.write(f"")
        except Error:
            rs.write(f"No players found!")

    def get_cells_by_column(self, column_index):
        """Gets the cell data from Draft Kings Daily Projections and puts them in a list"""
        try:
            rotodk_body = []
            for item in driver.find_elements_by_xpath(f'//div[@aria-colindex="{column_index}"]'):
                rotodk_body.append(item.text)
                # print loading message
                rs.write(f"Scraping {item.text}...")
                main_window.update()
        except:
            rs.write(f"No players found!")
            main_window.update()
        return rotodk_body

    def get_input(self, column_index):
        """Gets the cell input type data from Draft Kings Daily Projections and puts them in a list"""
        try:
            rotodk_body = []
            for item in driver.find_elements_by_xpath(f'//div[@aria-colindex="{column_index}"]/input[1]'):
                rotodk_body.append(item.get_attribute("value"))
                # print loading message
                rs.write(f"Scraping {item.get_attribute('value')}...")
                main_window.update()
        except Error:
            rs.write(f"No players found!")
            main_window.update()
        return rotodk_body

    def write(self, loading_message):
        """This function rs.writes to a label displayed on the GUI"""
        label.config(state=tkinter.NORMAL)
        label.config(text=loading_message)
        label.config(state=tkinter.DISABLED)


if __name__ == "__main__":
    rs = RotoScrape()
    rs.create_tables("dailyfantasyscraper.db")
    # GUI Code
    main_window = tkinter.Tk()
    main_window.title("Roto Scraper Launcher")
    main_window.attributes('-alpha', 0.95)
    main_window.geometry("729x550")
    bg = ImageTk.PhotoImage(Image.open(
        "RotoScraperBackground.jpg"), master=main_window)
    canvas = tkinter.Canvas(master=main_window)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(1, 1, image=bg, anchor="nw")
    frame1 = tkinter.Frame(master=main_window, width=10, height=10)
    frame2 = tkinter.Frame(master=main_window, width=5, height=5)
    frame1.pack()
    btn_initiate_driver = tkinter.Button(
        master=frame1, text="Launch Web Scraper", activebackground='chartreuse2', command=rs.initiate_driver)
    btn_initiate_driver.pack(side=tkinter.LEFT, padx=5, pady=5)
    btn_close_driver = tkinter.Button(
        master=frame1, text="Close Web Scraper", activebackground='firebrick2', command=rs.close_driver)
    btn_close_driver.pack(side=tkinter.RIGHT, padx=5, pady=5)
    frame2.pack()
    btn_add_players = tkinter.Button(
        master=frame2, text="Add Player Projections to Database", activebackground='chartreuse2', command=rs.create_player_projections)
    btn_add_players.pack(padx=5, pady=5)
    label = tkinter.Label(master=frame2, height=1)
    label.pack()
    main_window.mainloop()
