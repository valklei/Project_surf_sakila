from db_connection import DBConnector

class QueryHandler(DBConnector):
    def __init__(self, dbconfig):
        super().__init__(dbconfig)

    def get_all_category(self):
        cursor = self.get_cursor()
        cursor.execute("SELECT name FROM category")
        return cursor.fetchall()

    def get_all_year(self):
        cursor = self.get_cursor()
        cursor.execute("SELECT DISTINCT release_year FROM film")
        return cursor.fetchall()

    def get_films_by_keyword(self, keyword: str):
        cursor = self.get_cursor()
        query = """
        SELECT title, release_year, description
        FROM film
        WHERE title LIKE %s OR description LIKE %s
        LIMIT 10
        """
        cursor.execute(query, ('%' + keyword + '%', '%' + keyword + '%'))
        return cursor.fetchall()

    def get_film_by_category_and_year(self, category=None, year=None):
        cursor = self.get_cursor()

        query = """
            SELECT f.title, f.release_year, f.description
            FROM film AS f
            JOIN film_category AS f_c ON f.film_id = f_c.film_id
            JOIN category AS c ON f_c.category_id = c.category_id
        """

        conditions = []
        params = []

        if category:
            conditions.append("c.name = %s")
            params.append(category)
        if year:
            conditions.append("f.release_year = %s")
            params.append(year)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " LIMIT 10"

        cursor.execute(query, params)
        return cursor.fetchall()

    def close(self):
        self.get_cursor().close()
        self.get_connection().close()

