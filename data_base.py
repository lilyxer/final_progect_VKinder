import sqlalchemy as sq
from sqlalchemy.orm import DeclarativeBase, sessionmaker
import psycopg2
from environs import Env


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
            print(f'[-] База данных vkinder_db была создана ранее')
            conn.rollback()
        conn.close()

class Base(DeclarativeBase): 
    pass

class User(Base):
    """Создаёт класс-отношение для пользователя бота
    :profile_id: уникальный id аккауанта во ВКонтакте
    :anket_id: уникальный id анкет поиска
    :like: по умолчанию False, необходим для изьраных анкет"""
    __tablename__ = 'users'

    profile_id = sq.Column(sq.Integer, primary_key=True)
    anket_id = sq.Column(sq.Integer, primary_key=True)
    like = sq.Column(sq.Boolean(), default=False)
    

class VKengine:
    def __init__(self):
        self._engine = self._create_engine_connection()
        Session = sessionmaker(bind=self._engine)
        self._session = Session()
        self._create_tables()

    def _create_engine_connection(self):
        """Создаёт движок сессии"""
        DSN = f"{env('DRIVER')}://{env('LOGIN')}:{env('PASSWORD')}@{env('HOST')}:{env('PORT')}/{env('DATABASE')}"
        engine = sq.create_engine(DSN)
        return engine

    def _create_tables(self): 
        """Создание, либо дроп отношений-классов
        :engine: указатель на бд"""
        # Base.metadata.drop_all(bind=self._engine)
        Base.metadata.create_all(bind=self._engine)

    def add_user(self, profile_id: int, anket_id: int, like: bool=False) -> None:
        """ Добавляет в БД просмотренные анкеты
        :profile_id: уникальный id аккауанта во ВКонтакте
        :anket_id: уникальный id анкет поиска
        :like: флаг для избранных"""
        self._session.add(User(profile_id=profile_id, anket_id=anket_id, like=like))
        self._session.commit()

    def update_user(self, profile_id: int, anket_id: int, like: bool=True) -> None:
        """ Добавляет в БД просмотренные анкеты
        :profile_id: уникальный id аккауанта во ВКонтакте
        :anket_id: уникальный id анкет поиска
        :like: флаг для избранных"""
        self._session.query(User).filter(User.profile_id==profile_id, 
                                         User.anket_id == anket_id).update(
                                            {User.like: like,}
                                         )
        self._session.commit()

    def request_id(self, profile_id: int,  anket_id: int) -> bool:
        """Ищет в БД просмотренную анкету
        :profile_id: уникальный id аккауанта во ВКонтакте
        :anket_id: уникальный id анкет поиска
        :return: True если совпадение есть иначе False"""
        return bool(self._session.query(User).filter(User.profile_id==profile_id, 
                                                User.anket_id == anket_id).all())
    
    def request_favorite(self, profile_id: int) -> list:
        """Ищет в БД просмотренную анкету, котру добавили в ибранное
        :profile_id: уникальный id аккауанта во ВКонтакте
        :return: список из anket_id которые отмечены like=True"""
        return self._session.query(User.anket_id).filter(User.profile_id==profile_id, 
                                                         User.like==True).all()


if __name__ == '__main__':
    create_db()
    eng = VKengine()
    print(eng.request_favorite(profile_id=2674056))