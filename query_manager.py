
from db_connection import DBConnector

class QueryHandler(DBConnector):
    def __init__(self, dbconfig):
        super().__init__(dbconfig)

    def get_all_category(self):
        cursor = self.get_cursor()
        cursor.execute("SELECT name from category")
        record = cursor.fetchall()
        return record

    def get_all_year(self):
        cursor = self.get_cursor()
        cursor.execute("SELECT distinct release_year from film")
        record = cursor.fetchall()
        return record

    def get_films_by_keyword(self, keyword: str):
        cursor = self.get_cursor()
        cursor.execute("""
        SELECT title, release_year, description 
        from film
        where title like %s
        or description like %s
        limit 10
        """,
        (f"%{keyword}%", f"%{keyword}%"))
        record = cursor.fetchall()
        return record

    def get_film_by_category_and_year(self, category=None, year=None):
        cursor = self.get_cursor()

        query = """
            SELECT f.title, f.release_year, f.description
            FROM film AS f
            JOIN film_category AS f_c ON f.film_id = f_c.film_id
            JOIN category AS c ON f_c.category_id = c.category_id
        """

        params = []

        if category and year:
            query += " WHERE c.name = %s AND f.release_year = %s"
            params = [category, year]
        elif category:
            query += " WHERE c.name = %s"
            params = [category]
        elif year:
            query += " WHERE f.release_year = %s"
            params = [year]

        query += " LIMIT 10"

        cursor.execute(query, params)
        return cursor.fetchall()

    def close(self):
        self.get_cursor().close()
        self.get_connection().close()
