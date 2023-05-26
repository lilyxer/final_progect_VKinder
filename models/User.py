class User:
    """Экземпляры класса содержат в себе идентефикатор
    """

    def __init__(self, id: int) -> None:
        self._id = id

    @property
    def id(self) -> int:
        """Устанавливаем настройки приватности, реализуем геттер
        Возвращает значение по запросу"""
        return self._id

    @id.setter
    def id(self, num: int) -> None:
        self._id = num