# Здесь расположим генератор для генераторов

from random import randint


class GeneratorRelay:

    """
    Генератор положения реле
    Номер реле - генерируется рандомно от 1 до 5
    Положение реле передается в state. По умолчанию - положение True

    Пока работает только генерация одного элемента
    """
    __state = None
    relay = None

    def __init__(self, state: bool = True):
        self.relay = None
        self.__state = state

        # Теперь получаем нужный нам показатель реле
        self.relay = self.__generate_relay_one_element()

    # Генератор только одного элемента реле
    def __generate_relay_one_element(self):
        """Генератор только одного элемента реле"""

        relay = []

        relay_element = \
            {
                "id": randint(1, 5),
                "state": self.__state
            }
        relay.append(relay_element)
        return relay
