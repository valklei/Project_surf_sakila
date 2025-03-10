# Project_surf_sakila


Этот проект представляет собой графическое приложение для поиска фильмов 
в базе данных sakila. 
Он использует `tkinter ` для интерфейса, MySQL для хранения данных о фильмах и 
SQLite для сохранения поисковых запросов.

## Функциональность
- Поиск фильмов по названию.
- Фильтрация фильмов по жанру и году выпуска.
- Отображение популярных запросов.
- Подключение к MySQL и SQLite.

## Требования
Для работы проекта требуется установка следующих зависимостей:
```bash
python -m venv venv
venv\Scripts\activate
```

```bash
pip install -r requirements.txt
```

Файл `requirements.txt` включает (в том числе):
 
- `pymysql` — для работы с MySQL.
- `cryptography`  — для выполнения хэширования паролей.
- `python-dotenv` — загружает переменные окружения из .env.

## Настройка
### 1. Конфигурация базы данных
Перед запуском создайте файл `.env` в корневой директории проекта и укажите параметры подключения:

HOST=your-mysql-host
USER=your-mysql-user
PASSWORD=your-mysql-password
DATABASE=sakila
 
```

### 2. Запуск приложения
Запустите `main.py`:

```bash
python main.py
```

## Структура проекта
```
1.main: 
Центральный модуль, который инициализирует приложение. 
Он создает экземпляры QueryHandler и FilmSearchApp, а также запускает 
главный цикл обработки событий tkinter.

2.db_config: 
Управляет конфигурацией подключения к базе данных, загружая параметры 
из переменных окружения.

3.db_connection: 
Содержит класс DBConnector, который управляет подключением к базе данных. 
Он использует конфигурацию из db_config для установления соединения и 
предоставляет методы для работы с курсором и соединением.

4.query_manager: 
Содержит класс QueryHandler, который наследуется от DBConnector и 
управляет выполнением запросов к базе данных, таких как поиск фильмов 
по ключевым словам, категориям и годам.

5.user_interface: 
Содержит класс FilmSearchApp, который создает графический интерфейс 
приложения с использованием tkinter. Включает вкладки для поиска фильмов 
и отображения статистики. Взаимодействует с query_manager для выполнения 
поисковых запросов и отображения результатов.

6.saving_requests_db: Управляет обновлением и хранением статистики поисковых 
запросов, таких как подсчет использования ключевых слов и комбинаций 
жанров и годов.

Взаимодействие модулей:
main.py инициализирует приложение, используя конфигурацию из db_config.py для 
установления соединения с базой данных через db_connection.py и 
query_manager.py.
user_interface.py взаимодействует с query_manager.py для выполнения поисковых запросов 
и отображения результатов.
saving_requests_db.py обновляет статистику поиска на основе действий 
пользователя и предоставляет данные для отображения на вкладке статистики.
 
 
## Дополнительная информация
- База данных Sakila должна быть предварительно загружена в MySQL.
- SQLite используется для хранения истории запросов и популярных поисков.

## Автор
### Valerii Kleinberg

Проект разработан в образовательных целях.

