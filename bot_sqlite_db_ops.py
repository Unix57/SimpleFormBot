# // BUILT-IN MODULES
import logging
import sqlite3
from sqlite3 import Error


# --- SQLite3 DATABASE METHODS ---
class SQLiteOps:
    @staticmethod
    def create_connection(conn_name_1: str):
        try:
            connection = sqlite3.connect(conn_name_1)
            logging.info(f">>>>")
            logging.info(f"--- CONNECTION TO DATABASE | {conn_name_1} | ESTABLISHED ---")

        except Error as e:
            connection = None
            logging.error(f"// FAILED --- | CREATE_CONNECTION | TO DATABASE | {conn_name_1} |  --- {e} ---", exc_info=True)

        return connection

    @staticmethod
    def execute_query_no_data(conn_name_1: str, query_1: str):
        connection = SQLiteOps.create_connection(conn_name_1)
        cursor = connection.cursor()
        try:
            cursor.execute(query_1)
            connection.commit()
            logging.info("--- | QUERY_NO_DATA | EXECUTED ---")

        except Error as e:
            logging.error(f"// FAILED --- | QUERY_NO_DATA | --- {e} ---", exc_info=True)

        finally:
            if connection:
                connection.close()
                logging.info(f"--- CONNECTION TO DATABASE | {conn_name_1} | CLOSED ---")
                logging.info(">>>>")

    @staticmethod
    def execute_query_with_data(conn_name_1: str, query_1: str, data_1: tuple):
        connection = SQLiteOps.create_connection(conn_name_1)
        cursor = connection.cursor()
        try:
            cursor.execute(query_1, data_1)
            connection.commit()
            logging.info("--- | QUERY_WITH_DATA | EXECUTED ---")

        except Error as e:
            logging.error(f"// FAILED --- | QUERY_WITH_DATA | --- {e} ---", exc_info=True)

        finally:
            if connection:
                connection.close()
                logging.info(f"--- CONNECTION TO DATABASE | {conn_name_1} | CLOSED ---")
                logging.info(">>>>")

    @staticmethod
    def execute_query_with_data_many(conn_name_1: str, query_1: str, data_1: tuple):
        connection = SQLiteOps.create_connection(conn_name_1)
        cursor = connection.cursor()
        try:
            cursor.executemany(query_1, data_1)
            connection.commit()
            logging.info("--- | QUERY_WITH_DATA_MANY | EXECUTED ---")

        except Error as e:
            logging.error(f"// FAILED --- | QUERY_WITH_DATA_MANY | --- {e} ---", exc_info=True)

        finally:
            if connection:
                connection.close()
                logging.info(f"--- CONNECTION TO DATABASE | {conn_name_1} | CLOSED ---")
                logging.info(">>>>")

    @staticmethod
    def execute_read_query_one(conn_name_1: str, query_1: str):
        connection = SQLiteOps.create_connection(conn_name_1)
        cursor = connection.cursor()
        try:
            cursor.execute(query_1)
            result = cursor.fetchone()
            logging.info("--- | READ_QUERY_ONE | EXECUTED ---")
            return result

        except Error as e:
            logging.error(f"// FAILED --- | READ_QUERY_ONE | --- {e} ---", exc_info=True)

        finally:
            if connection:
                connection.close()
                logging.info(f"--- CONNECTION TO DATABASE | {conn_name_1} | CLOSED ---")
                logging.info(">>>>")

    @staticmethod
    def execute_read_query_all(conn_name_1: str, query_1: str):
        connection = SQLiteOps.create_connection(conn_name_1)
        cursor = connection.cursor()
        try:
            cursor.execute(query_1)
            result = cursor.fetchall()
            logging.info("--- | READ_QUERY_ALL | EXECUTED ---")
            return result

        except Error as e:
            logging.error(f"// FAILED --- | READ_QUERY_ALL | --- {e} ---", exc_info=True)

        finally:
            if connection:
                connection.close()
                logging.info(f"--- CONNECTION TO DATABASE | {conn_name_1} | CLOSED ---")
                logging.info(">>>>")


def init_database(conn_name_1):
    create_users_data_sql = (
        "CREATE TABLE IF NOT EXISTS user_data("
        "chat_id INTEGER PRIMARY KEY, "
        "user_state TEXT, "
        "name TEXT, "
        "age TEXT, "
        "gender TEXT, "
        "reg_flag INTEGER);")

    SQLiteOps.execute_query_no_data(conn_name_1, create_users_data_sql)


# |---| DATABASE TABLES/COLUMNS DICTS
db_tables_dict = {
    "user_data": "user_data"
}

user_data_cols_dict = {
    "chat_id": "chat_id",
    "user_state": "user_state",
    "name": "name",
    "age": "age",
    "gender": "gender",
    "reg_flag": "reg_flag"
}


# --- CRUD --- DATABASE TABLES ---
class UserDataCRUD:
    # --- CREATE ---
    @staticmethod
    def add_new_user(conn_name_1: str, chat_id_1: int):
        add_user_sql = "INSERT INTO user_data VALUES(?, ?, ?, ?, ?, ?);"
        add_user_data = (chat_id_1, "state_default", "", "", "", 0)
        SQLiteOps.execute_query_with_data(conn_name_1, add_user_sql, add_user_data)

    # --- READ ---
    @staticmethod
    def read_user_data(conn_name_1: str, chat_id_1: int):
        read_sql = (
            f"SELECT name, age, gender "
            f"FROM user_data "
            f"WHERE chat_id = {chat_id_1};")
        read_result = SQLiteOps.execute_read_query_one(conn_name_1, read_sql)

        return read_result

    # --- UPDATE ---
    @staticmethod
    def upd_user_col(conn_name_1: str, user_col_1: str, new_user_data_1, chat_id_1: int):
        update_user_sql = (
            f"UPDATE user_data "
            f"SET {user_col_1} = '{new_user_data_1}' " 
            f"WHERE chat_id = {chat_id_1};")
        SQLiteOps.execute_query_no_data(conn_name_1, update_user_sql)

    @staticmethod
    def upd_user_reg_flag(conn_name_1: str, new_value_1: int, chat_id_1: int):
        update_user_sql = (
            f"UPDATE user_data "
            f"SET reg_flag = {new_value_1} "
            f"WHERE chat_id = {chat_id_1};")
        SQLiteOps.execute_query_no_data(conn_name_1, update_user_sql)

    @staticmethod
    def upd_user_state(conn_name_1: str, new_value_1: str, chat_id_1: int):
        update_user_sql = (
            f"UPDATE user_data "
            f"SET user_state = '{new_value_1}' "
            f"WHERE chat_id = {chat_id_1};")
        SQLiteOps.execute_query_no_data(conn_name_1, update_user_sql)

    # --- DELETE ---
    @staticmethod
    def del_user(conn_name_1: str, chat_id_1: int):
        delete_user_sql = (
            f"DELETE FROM user_data "
            f"WHERE chat_id = {chat_id_1};")
        SQLiteOps.execute_query_no_data(conn_name_1, delete_user_sql)

    # --- OTHER --- FLAGS and STATES ---
    @staticmethod
    def check_user_reg_flag(conn_name_1: str, chat_id_1: int):
        read_sql = (
            f"SELECT reg_flag "
            f"FROM user_data "
            f"WHERE chat_id = {chat_id_1} AND reg_flag = 1;")
        reg_flag_tup = SQLiteOps.execute_read_query_one(conn_name_1, read_sql)

        return reg_flag_tup

    @staticmethod
    def check_user_cid(conn_name_1: str, chat_id_1: int):
        read_sql = (
            f"SELECT chat_id "
            f"FROM user_data "
            f"WHERE chat_id = {chat_id_1};")
        user_cid_tup = SQLiteOps.execute_read_query_one(conn_name_1, read_sql)

        return user_cid_tup

    @staticmethod
    def get_user_state(conn_name_1: str, chat_id_1: int):
        read_sql = (
            f"SELECT user_state "
            f"FROM user_data "
            f"WHERE chat_id = {chat_id_1};")
        user_state_tup = SQLiteOps.execute_read_query_one(conn_name_1, read_sql)

        return user_state_tup
