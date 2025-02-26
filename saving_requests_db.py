import sqlite3


def create_tables():
    with sqlite3.connect('stat_keywords.db') as connection:
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stat_keywords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                keyword TEXT NOT NULL UNIQUE,
                count INTEGER DEFAULT 1
            )
        ''')

    with sqlite3.connect('stat_genre_year.db') as connection:
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stat_genre_year (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                genre TEXT NOT NULL,
                year INTEGER NOT NULL,
                count INTEGER DEFAULT 1,
                UNIQUE(genre, year)
            )
        ''')


def change_stat_keywords(keyword):
    try:
        with sqlite3.connect('stat_keywords.db') as connection:
            cursor = connection.cursor()
            cursor.execute(
                """SELECT count FROM stat_keywords WHERE keyword = ?""",
                (keyword,))
            result = cursor.fetchone()
            if result:
                new_count = result[0] + 1
                cursor.execute(
                    """UPDATE stat_keywords SET count = ? WHERE keyword = ?""",
                    (new_count, keyword))
            else:
                cursor.execute(
                    """INSERT INTO stat_keywords (keyword, count) VALUES (?, ?)""",
                    (keyword, 1))
            connection.commit()
    except sqlite3.Error as e:
        print(f"Ошибка при работе с базой данных: {e}")


def change_stat_genre_year(genre, year):
    try:
        with sqlite3.connect('stat_genre_year.db') as connection:
            cursor = connection.cursor()
            cursor.execute(
                """SELECT count FROM stat_genre_year WHERE genre = ? AND year = ?""",
                (genre, year))
            result = cursor.fetchone()
            if result:
                new_count = result[0] + 1
                cursor.execute(
                    """UPDATE stat_genre_year SET count = ? WHERE genre = ? AND year = ?""",
                    (new_count, genre, year))
            else:
                cursor.execute(
                    """INSERT INTO stat_genre_year (genre, year, count) VALUES (?, ?, ?)""",
                    (genre, year, 1))
            connection.commit()
    except sqlite3.Error as e:
        print(f"Ошибка при работе с базой данных: {e}")


def get_rank_keywords():
    with sqlite3.connect('stat_keywords.db') as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
                    SELECT keyword, count 
                    FROM stat_keywords
                    ORDER BY count desc limit 3
                """
        )
        record = cursor.fetchall()
    return record

def get_rank_genre_year():
    with sqlite3.connect('stat_genre_year.db') as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
                    SELECT genre, count, year 
                    FROM stat_genre_year
                    ORDER BY count desc limit 3
                """
        )
        record = cursor.fetchall()
    return record