import tkinter as tk
from tkinter import ttk
from tkinter import messagebox # импортируем модуль интерфейса

from saving_requests_db import (
    change_stat_keywords,
    change_stat_genre_year,
    get_rank_keywords,
    get_rank_genre_year,
    create_tables
) # импортируем функции по созданию, записи и обновлению  таблиц запросов,
# а также получения информации из таблиц


create_tables()

class FilmSearchApp(tk.Frame):
    """
    Класс для создания графического интерфейса поиска фильмов.
    """
    def __init__(self, parent, query_handler):
        super().__init__(parent)
        self.parent = parent
        self.query_handler = query_handler
        self.parent.title("Поиск фильмов")

        # Создаём Notebook (вкладки)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Вкладка поиска по ключевым словам
        self.keyword_search_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.keyword_search_frame, text="Поиск по ключевым словам")
        self.create_keyword_search_tab()

        # Вкладка поиска по категории и году
        self.category_year_search_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.category_year_search_frame, text="Поиск по категории/году")
        self.create_category_year_search_tab()

        # Вкладка статистики
        self.stats_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.stats_frame, text="Статистика поиска")
        self.create_stats_tab()

        self.pack(fill=tk.BOTH, expand=True)

    def create_keyword_search_tab(self):
        """
        Создание элементов управления для поиска по ключевым словам.
        """
        # Заголовок
        ttk.Label(
            self.keyword_search_frame,
            text="Введите ключевое слово для поиска (по названию или описанию):"
        ).pack(pady=5)

        # Поле ввода
        self.keyword_entry = ttk.Entry(self.keyword_search_frame, width=50)
        self.keyword_entry.pack(pady=5)

        # Кнопка "Поиск"
        ttk.Button(
            self.keyword_search_frame,
            text="Найти фильмы",
            command=self.search_by_keyword
        ).pack(pady=5)

        # Поле для отображения результатов
        self.keyword_results = tk.Text(self.keyword_search_frame, height=30, width=100, wrap="word")
        self.keyword_results.pack(padx=5, pady=5)

    def search_by_keyword(self):
        """
        Обработчик нажатия кнопки "Найти фильмы" во вкладке поиска по ключевым словам.
        """
        keyword = self.keyword_entry.get().strip()
        self.keyword_results.delete("1.0", tk.END)  # Очистка текстового поля

        if not keyword:
            messagebox.showwarning("Предупреждение", "Введите ключевое слово для поиска.")
            return

        # Добавляем или обновляем статистику по ключевым словам
        change_stat_keywords(keyword)

        # Выполняем запрос
        films = self.query_handler.get_films_by_keyword(keyword)
        if films:
            for film in films:
                title, year, description = film
                self.keyword_results.insert(tk.END, f"Название: {title}\nГод: {year}\nОписание: {description}\n\n")
        else:
            self.keyword_results.insert(tk.END, "Ничего не найдено.")

    def create_category_year_search_tab(self):
        """
        Создаём элементы управления для поиска по категории/году.
        """
        # Получим полный список категорий и годов из БД, чтобы заполнить выпадающие списки.
        categories = self.query_handler.get_all_category()
        years = self.query_handler.get_all_year()

        # Преобразуем список [(cat1,), (cat2,)...] в простой список [cat1, cat2, ...]
        self.category_list = [cat[0] for cat in categories]
        self.year_list = [year[0] for year in years if year[0] is not None]

        # Сортируем список годов
        self.year_list.sort()

        # Добавляем в начало «Все жанры» и «Все годы»
        self.category_list.insert(0, "Все жанры")
        self.year_list.insert(0, "Все годы")

        frame_top = ttk.Frame(self.category_year_search_frame)
        frame_top.pack(pady=5)

        # Метка и выпадающий список (Combobox) для категорий
        ttk.Label(frame_top, text="Категория:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        self.category_combo = ttk.Combobox(frame_top, values=self.category_list, state="readonly")
        self.category_combo.current(0)  # По умолчанию выбрана "Все жанры"
        self.category_combo.grid(row=0, column=1, padx=5, pady=5)

        # Метка и выпадающий список для годов
        ttk.Label(frame_top, text="Год выпуска:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.E)
        self.year_combo = ttk.Combobox(frame_top, values=self.year_list, state="readonly")
        self.year_combo.current(0)  # По умолчанию выбрано "Все годы"
        self.year_combo.grid(row=0, column=3, padx=5, pady=5)

        # Кнопка "Поиск"
        ttk.Button(
            frame_top,
            text="Найти фильмы",
            command=self.search_by_category_year
        ).grid(row=0, column=4, padx=5, pady=5)

        # Поле для вывода результатов
        self.cat_year_results = tk.Text(self.category_year_search_frame, height=30, width=100, wrap="word")
        self.cat_year_results.pack(pady=10)

    def search_by_category_year(self):
        """
        Поиск фильмов по выбранным категории и/или году.
        """
        category = self.category_combo.get()
        year = self.year_combo.get()

        # Очищаем текстовое поле
        self.cat_year_results.delete("1.0", tk.END)

        # Если «Все жанры» – будем передавать None, чтобы не фильтровать по категории
        if category == "Все жанры":
            category = None

        # Если «Все годы» – тоже передаём None, чтобы не фильтровать по году
        if year == "Все годы":
            year_int = None
        else:
            # Пробуем преобразовать год к int
            try:
                year_int = int(year)
            except ValueError:
                # Если не получилось – предупреждаем, но продолжаем
                messagebox.showwarning("Предупреждение", "Год должен быть числом.")
                return

        # Если ни жанр, ни год не выбраны – предупредим
        if not category and not year_int:
            messagebox.showwarning("Предупреждение", "Выберите хотя бы категорию или год, либо оба.")
            return

        # Если выбрана и категория, и год (не в режиме «Все»), сохраним в статистику
        if category and year_int:
            change_stat_genre_year(category, year_int)

        # Выполняем запрос к БД
        films = self.query_handler.get_film_by_category_and_year(category, year_int)
        if films:
            for film in films:
                title, film_year, description = film
                self.cat_year_results.insert(
                    tk.END, f"Название: {title}\nГод: {film_year}\nОписание: {description}\n\n"
                )
        else:
            self.cat_year_results.insert(tk.END, "Ничего не найдено.")

    def create_stats_tab(self):
        """
        Вкладка для вывода топ-результатов по поисковым словам и жанрам/годам.
        """
        ttk.Label(self.stats_frame, text="Топ-3 поисковых ключевых слова:", font=("Arial", 12, "bold")).pack(pady=5)
        self.keywords_stats_text = tk.Text(self.stats_frame, height=15, width=100, wrap="word")
        self.keywords_stats_text.pack()

        ttk.Label(self.stats_frame, text="Топ-3 (жанр/год):", font=("Arial", 12, "bold")).pack(pady=5)
        self.genre_year_stats_text = tk.Text(self.stats_frame, height=15, width=100, wrap="word")
        self.genre_year_stats_text.pack()

        # Кнопка обновления статистики
        ttk.Button(
            self.stats_frame,
            text="Обновить статистику",
            command=self.show_stats
        ).pack(pady=10)

    def show_stats(self):
        """
        Обновляет вкладку со статистикой.
        """
        self.keywords_stats_text.delete("1.0", tk.END)
        self.genre_year_stats_text.delete("1.0", tk.END)

        # Топ-3 ключевых слов
        top_keywords = get_rank_keywords()  # [(keyword, count), (...), ...]
        if top_keywords:
            for kw, cnt in top_keywords:
                self.keywords_stats_text.insert(tk.END, f"{kw}: {cnt} раз(а)\n")
        else:
            self.keywords_stats_text.insert(tk.END, "Статистика по ключевым словам пуста.\n")

        # Топ-3 жанров/годов
        top_genre_year = get_rank_genre_year()  # [(genre, count, year), ...]
        if top_genre_year:
            for genre, cnt, yr in top_genre_year:
                self.genre_year_stats_text.insert(tk.END, f"Жанр: {genre}, Год: {yr}, Кол-во поисков: {cnt}\n")
        else:
            self.genre_year_stats_text.insert(tk.END, "Статистика по жанрам/годам пуста.\n")
