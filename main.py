import db_config
from user_interface import FilmSearchApp
from query_manager import QueryHandler
import tkinter as tk

def main():
    root = tk.Tk()
    query_handler = QueryHandler(db_config.get_dbconfig())
    app = FilmSearchApp(root, query_handler)
    root.mainloop()

if __name__ == "__main__":
    main()
