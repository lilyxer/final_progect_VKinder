import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
import psycopg2
from environs import Env
from models.Users import *

env = Env()
env.read_env()

def create_db():
        """
        Заходит под админом и пробует создать базу данных vkinder_db под нужды ORM
        для подключения к вашей базе данных в conn необходимо прописать ВАШИ логин
        и пароль 
        """
        psd = env('PASSWORD')
        conn = psycopg2.connect(database='postgres', user='postgres', password=psd)
        conn.set_session(autocommit=True)
        cur = conn.cursor()
        try:
            cur.execute("""CREATE DATABASE vkinder_db;""")
            print('[+] База данных vkinder_db создана')
        except Exception as e:
            print(e, end='')
            print(f'[-] База данных vkinder_db была создана ранее')
            conn.rollback()
        conn.close()

class VKengine:
    def __init__(self):
        self._engine = self.crete_engine_connection()
        Session = sessionmaker(bind=self._engine)
        self._session = Session()
        print('[+] Соединение с БД')

    def crete_engine_connection(self):
        DSN = f"{env('DRIVER')}://{env('LOGIN')}:{env('PASSWORD')}@{env('HOST')}:{env('PORT')}/{env('DATABASE')}"
        engine = sa.create_engine(DSN)
        return engine

    def create_tables(self): 
        """Создание, либо дроп отношений-классов
        engine - указатель на бд"""
        # Base.metadata.drop_all(engine)
        Base.metadata.create_all(bind=self._engine)

    def closed(self) -> None:
         self._session.close()
