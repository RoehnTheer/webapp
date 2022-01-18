import mariadb


class UseDatabase:
    def __init__(self, config: dict) -> None:
        #Передаём словарь с параметрами подключения
        self.configuration = config

    def __enter__(self) -> 'cursor':
        #Подключаемся к БД и создаём курсор
        self.conn = mariadb.connect(**self.configuration)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, exc_trace) -> None:
        #Приказываем БД быстро, решительно записать данные
        self.conn.commit()
        #Закрываем курсор и соединение с БД
        self.cursor.close()
        self.conn.close()
