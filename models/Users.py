import sqlalchemy as sa
from sqlalchemy.orm import relationship, DeclarativeBase


class Base(DeclarativeBase): 
    pass

class User(Base):
    """Создаёт класс-отношение для пользователя бота
    id - уникальный id аккауанта во ВКонтакте
    first_name - имя пользователя, обязательно
    last_name - фамилия пользователя, не обязательно
    """
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True)
    first_name = sa.Column(sa.String(length=30), nullable=False)
    last_name = sa.Column(sa.String(length=50))

    def __str__(self) -> str:
        return f'Пользователь: {self.first_name} {self.last_name}'
    
class Partner(Base):
    """Создаёт класс-отношение для анкет, которые пользоватеь просмотрел
    id - уникальный id аккауанта во ВКонтакте
    first_name - имя пользователя из анкеты, обязательно
    last_name - фамилия пользователя из анкеты, не обязательно
    city_id - город проживания,
    age - возраст
    sex - 1=женский, 2=мужской
    like - True если анкета заинтересовала, по умолчанию False
    """
    __tablename__ = 'partners'
    
    id = sa.Column(sa.Integer, primary_key=True)
    first_name = sa.Column(sa.String(length=30), nullable=False)
    last_name = sa.Column(sa.String(length=50))
    city_id = sa.Column(sa.Integer, nullable=False)
    age = sa.Column(sa.Integer, nullable=False)
    sex = sa.Column(sa.Integer, nullable=False)
    sex_check = sa.CheckConstraint('sex > 0 and sex <= 2')
    like = sa.Column(sa.Boolean(), default=False)
    id_user = sa.Column(sa.Integer, sa.ForeignKey('users.id'), 
                        nullable=False)
    
    user = relationship(User, backref='partners') 

    def __str__(self) -> str:
        return (f'Данные из анкеты: {self.first_name} {self.last_name}\n'
                f'Возраст {self.age}, заинтересованность {self.like}')
    
class Photo(Base):
    """Создаёт класс-отношение для ссылок на фото партнеров
    url - ссылка на фотографию из аккаунта, записываются 3 самых популярных
    """
    __tablename__ = 'photos'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    url = sa.Column(sa.String(100), unique=True, nullable=False)
    id_user = sa.Column(sa.Integer, sa.ForeignKey('partners.id'), 
                        nullable=False)
    
    partner = relationship(Partner, backref='photos')
