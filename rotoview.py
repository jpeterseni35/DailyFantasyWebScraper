# This module alows the user to view the data scraped in the Roto Scraper Launcher application
from rotoscrape import create_connection
import sqlite3
import tkinter
from sqlite3 import Error
from tkinter import ttk
from PIL import ImageTk, Image


class RotoView:

    def view_rotowiredk(self):
        """Query all rows of rotowiredk table and insert into tk treeview"""
        conn = create_connection("dailyfantasyscraper.db")
        cur = conn.cursor()

        cur.execute("SELECT * FROM rotowiredk")
        result = cur.fetchall()
        conn.commit()
        conn.close()

        for item in result:
            print(item)
            tree.insert('', 'end', values=item)

    def view_all_pitchers(self):
        """Query all rows of rotowiredk table and insert into tk treeview"""
        conn = create_connection("dailyfantasyscraper.db")
        cur = conn.cursor()
        position = "P"
        cur.execute("SELECT * FROM rotowiredk where position = ?", position)
        result = cur.fetchall()
        conn.commit()
        conn.close()

        for item in result:
            print(item)
            tree.insert('', 'end', values=item)

    def view_all_batters(self):
        """Query all rows of rotowiredk table and insert into tk treeview"""
        conn = create_connection("dailyfantasyscraper.db")
        cur = conn.cursor()
        position = "P"
        cur.execute("SELECT * FROM rotowiredk where position != ?", position)
        result = cur.fetchall()
        conn.commit()
        conn.close()

        for item in result:
            print(item)
            tree.insert('', 'end', values=item)

    def view_batter_bysalary(self):
        """Query all rows with a salary less than what is entered"""
        conn = create_connection("dailyfantasyscraper.db")
        salary = "$" + sal.get()
        position = "P"
        batter_salary = (salary, position)
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM rotowiredk WHERE salary <= ? and position != ? ", batter_salary)
        result = cur.fetchall()
        conn.commit()
        conn.close()

        for item in result:
            print(item)
            tree.insert('', 'end', values=item)

    def view_record_byvalue(self):
        """Query all rows with a value greather than what is entered"""
        conn = create_connection("dailyfantasyscraper.db")
        value = val.get()
        player_value = (value)
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM rotowiredk WHERE value > ?", player_value)
        result = cur.fetchall()
        conn.commit()
        conn.close()

        for item in result:
            print(item)
            tree.insert('', 'end', values=item)

    def reset_view(self):

        if tkinter.messagebox.askyesno(
                title="Reset View", message="Do you wish to reset the view?"):
            tree.delete(*tree.get_children())


if __name__ == "__main__":
    rv = RotoView()
    # create database connection from rotoscrape
    conn = create_connection("dailyfantasyscraper.db")
    # GUI code
    main_window = tkinter.Tk()
    main_window.title("Roto Scraper Viewer")
    main_window.geometry("825x1050")
    bg = ImageTk.PhotoImage(Image.open(
        "RotoViewerBackground.jpg"), master=main_window)
    canvas = tkinter.Canvas(master=main_window)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(50, 50, image=bg, anchor="nw")

    frame1 = tkinter.Frame(master=main_window, width=10, height=10)
    frame1.pack()
    tree = ttk.Treeview(master=frame1, show="headings", columns=("Column 1", "Column 2", "Column 3", "Column 4", "Column 5", "Column 6", "Column 7", "Column 8",
                                                                 "Column 9", "Column 10", "Column 11", "Column 12", "Column 13", "Column 14", "Column 15"))
    sb = tkinter.Scrollbar(frame1, orient="horizontal")
    sb.pack(side="bottom", fill="both")
    tree.config(xscrollcommand=sb.set)
    sb.config(command=tree.xview)
    tree.heading('Column 1', text='ID', anchor="center")
    tree.heading('Column 2', text='Player', anchor="center")
    tree.heading('Column 3', text='Position', anchor="center")
    tree.heading('Column 4', text='Team', anchor="center")
    tree.heading('Column 5', text='Opponent', anchor="center")
    tree.heading('Column 6', text='Starter', anchor="center")
    tree.heading('Column 7', text='Salary', anchor="center")
    tree.heading('Column 8', text='Projected Fpts', anchor="center")
    tree.heading('Column 9', text='Value', anchor="center")
    tree.heading('Column 10', text='Middleline', anchor="center")
    tree.heading('Column 11', text='Over/Under', anchor="center")
    tree.heading('Column 12', text='Projected Team Runs', anchor="center")
    tree.heading('Column 13', text='Projected Roster Percent', anchor="center")
    tree.heading('Column 14', text='Weather', anchor="center")
    tree.heading('Column 15', text='Date Time', anchor="center")
    tree.column('Column 1', stretch=tkinter.YES, width=2, anchor="w")
    tree.column('Column 2', stretch=tkinter.YES, width=150, anchor="w")
    tree.column('Column 3', stretch=tkinter.YES, width=100, anchor="w")
    tree.column('Column 4', stretch=tkinter.YES, width=75, anchor="w")
    tree.column('Column 5', stretch=tkinter.YES, width=75, anchor="w")
    tree.column('Column 6', stretch=tkinter.YES, width=50, anchor="w")
    tree.column('Column 7', stretch=tkinter.YES, width=50, anchor="w")
    tree.column('Column 8', stretch=tkinter.YES, width=50, anchor="w")
    tree.column('Column 9', stretch=tkinter.YES, width=50, anchor="w")
    tree.column('Column 10', stretch=tkinter.YES, width=50, anchor="w")
    tree.column('Column 11', stretch=tkinter.YES, width=50, anchor="w")
    tree.column('Column 12', stretch=tkinter.YES, width=100, anchor="w")
    tree.column('Column 13', stretch=tkinter.YES, width=100, anchor="w")
    tree.column('Column 14', stretch=tkinter.YES, width=100, anchor="w")
    tree.column('Column 15', stretch=tkinter.YES, width=500, anchor="w")
    tree.pack(side="left")
    btn_view_players = tkinter.Button(
        master=main_window, text="View All Projections", activebackground='chartreuse2', command=rv.view_rotowiredk)
    btn_view_players.pack(anchor="n", side="left", padx=5, pady=15)
    btn_view_pitchers = tkinter.Button(
        master=main_window, text="View All Pitchers", activebackground='chartreuse2', command=rv.view_all_pitchers)
    btn_view_pitchers.pack(anchor="n", side="left", padx=5, pady=15)
    btn_view_batters = tkinter.Button(
        master=main_window, text="View All Batters", activebackground='chartreuse2', command=rv.view_all_batters)
    btn_view_batters.pack(anchor="n", side="left", padx=5, pady=15)
    label1 = tkinter.Label(text="Salary")
    sal = tkinter.Entry()
    label1.pack()
    sal.pack()
    btn_view_bysalary = tkinter.Button(
        master=main_window, text="View Batters Equal or Below Entered Salary", activebackground='chartreuse2', command=rv.view_batter_bysalary)
    btn_view_bysalary.pack(padx=5, pady=5)
    label2 = tkinter.Label(text="Value")
    val = tkinter.Entry()
    label2.pack()
    val.pack()
    btn_view_byvalue = tkinter.Button(
        master=main_window, text="View Players Above Entered Value", activebackground='chartreuse2', command=rv.view_record_byvalue)
    btn_view_byvalue.pack(padx=5, pady=5)
    btn_reset = tkinter.Button(
        master=main_window, text="Reset View", activebackground='chartreuse2', command=rv.reset_view)
    btn_reset.pack(padx=5, pady=15)

    main_window.mainloop()
