import mariadb


class ConnectionError(Exception):
    pass

class CredentialsError(Exception):
    pass

class SQLError(Exception):
    pass

class UseDatabase:
    def __init__(self, config: dict) -> None:
        #Передаём словарь с параметрами подключения
        self.configuration = config

    def __enter__(self) -> 'cursor':
        #Подключаемся к БД и создаём курсор
        try:
            self.conn = mariadb.connect(**self.configuration)
            self.cursor = self.conn.cursor()
            return self.cursor
        except mariadb.InterfaceError as err:
            raise ConnectionError(err)
        except mariadb.ProgrammingError as err:
            raise CredentialsError(err)


    def __exit__(self, exc_type, exc_value, exc_trace) -> None:
        #Приказываем БД быстро, решительно записать данные
        self.conn.commit()
        #Закрываем курсор и соединение с БД
        self.cursor.close()
        self.conn.close()
        if exc_type is mariadb.ProgrammingError:
            raise SQLError(exc_value)
        elif exc_type:
            exc_type(exc_value)
