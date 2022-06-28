from abc import ABC, abstractmethod

# ШАГ 1
# создали класс (на базе абстрактного родительского импортируемого модуля) с абстрактными методами
class Storage(ABC):
    @abstractmethod
    def __init__(self, items, capasity):  # товары и емкость
        self._items = items  # словарь название:количество
        self._capasity = capasity

    @abstractmethod
    def add(self, title, count):  # увеличивает запас items
        pass

    @abstractmethod
    def remove(self, title, count):  # уменьшает запас items
        pass

    @property
    @abstractmethod
    def get_free_space(self):  # вернуть количество свободных мест
        pass

    @property
    @abstractmethod
    def items(self):  # возвращает сожержание склада в словаре {товар: количество}
        pass

    @property
    @abstractmethod
    def get_unique_items_count(self):  # возвращает количество уникальных товаров.
        pass

# ШАГ 2
# создаем вполне конкретные классы на базе абстрактного
class Store(Storage):
    def __init__(self):
        self._items = {}  # задали атрибут класса - пустой словарь, где будут храниться товары
        self._capacity = 100  # задали максимальную емкость количества товаров

    def add(self, title, count):
        # 'Добавление товара на склад'
        if title in self._items:
            self._items[title] += count  # если товар есть на складе (ключ в словаре), то увеличиваем его количество (значение от ключа)
        else:
            self._items[title] = count  # если товара нет, то создаем его
        self._capacity -= count  # в любом случае, уменьшаем емкость склада

    def remove(self, title, count):
        # 'Удаление товара со склада'
        res = self._items[title] - count  # уменьшили количество конкретного товара
        if res > 0:  # если товар все-таки еще остался на складе
            self._capacity += count  # емкость склада увеличивается
            self._items[title] = res  # перезаписали количество товара на новое значение
        else:  # если товар целиком забрали со склада. Считаем, что не могут попросить забрать со склада больше чем есть
            del self._items[title]
        self._capacity += count

    @property
    def get_free_space(self):
        return self._capacity

    @property  # позволяет вызывать внутреннее защищенное поле как функцию, но не в виде функции .items() а в виде поля .items
    def items(self):
        return self._items

    @items.setter
    def items(self, new_items):
        self._items = new_items
        self._capacity -= sum(self._items.values())

    @property
    def get_unique_items_count(self):
        return len(self._items.keys())


# ШАГ 3
# создаем вполне конкретный класс на базе существующего
class Shop(Store):
    def __init__(self):
        super().__init__()  # явно указываем определение полей родительского класса (self._items, self._capacity )
        self._capacity = 20  # переопределяем конкретное поле


# ШАГ 4
# создаем новый класс
class Request:  # создаем новый класс - обработчик запросов от пользователя. Т.е. это блок информации запросов
    def __init__(self, info):  # info - ввод пользователя, в объект инициализируется в разобранном виде (ТЕКСТОВКА ИЗВЕСТНА), ниже
        self.info = self._split_info(info)  # команда от пользователя --- сплитуем в список элементов и переопределяем их на поля-значения
        self.from_ = self.info[4]
        self.to = self.info[6]
        self.amount = int(self.info[1])
        self.product = self.info[2]

    @staticmethod
    def _split_info(info):  # обычная статическая функция по разбиению строки в список подстрок
        return info.split(" ")

    def __repr__(self): # форма представления, если захотим распечатать объект класса
        return f"Доставить {self.amount} {self.product} из {self.from_} в {self.to}"


# ШАГ 5  ОСНОВНАЯ БИЗНЕС-ЛОГИКА ПРОГРАМММЫ
def main():
    while (True):  # создаем бесконечный цикл получения запросов пользователя и их исполнения
        user_input = input("Введите запрос: ")
        # user_input = "Доставить 3 печеньки из склад в магазин"  # имитируем ввод от пользователя
        print("Доставить 3 печеньки из склад в магазин")

        if user_input == 'stop':  # отбойник
            break

        request = Request(user_input)  # создаем объект-запроса




        if request.from_ == request.to:
            print("Пункт назначения == Пункт отправки")
            continue  # вылетаем на новый круг while

        if request.from_ == 'склад':
            if request.product in store.items:
                print(f'Нужный товар есть в пункте \"{request.from_}\"')
            else:
                print(f"На складе {request.from_} нет такого товара")
                continue

            if store.items[request.product] >= request.amount:
                print(f"Нужное количество есть в пункте \"{request.from_}\"")
            else:
                print(f"В пункте {request.from_} не хватает {request.amount - store.items[request.product]}")
                continue

            if shop.get_free_space >= request.amount:
                print(f'В пункте \"{request.to}\" достаточно места')
            else:
                print(f"В пункте {request.to} не хватает {request.amount - shop.get_free_space} места")
                continue

            if request.to == 'магазин' and shop.get_unique_items_count == 5 and request.product not in shop.items:
                print("В магазине достаточно уникальных значений")
                continue

            store.remove(request.product, request.amount)
            print(f'Курьер забрал {request.amount} {request.product} из пункта {request.from_}')
            print(f'Курьер везет {request.amount} {request.product} из пункта {request.from_} в пункт {request.to}')
            shop.add(request.product, request.amount)
            print(f'Курьер доставил {request.amount} {request.product} в пункта {request.to}')

        else:
            if request.product in shop.items:
                print(f'Нужный товар есть в пункте \"{request.from_}\"')
            else:
                print(f"На складе {request.from_} нет такого товара")
                continue

            if store.items[request.product] >= request.amount:
                print(f"Нужное количество есть в пункте \"{request.from_}\"")
            else:
                print(f"В пункте {request.from_} не хватает {request.amount - shop.items[request.product]}")
                continue

            if shop.get_free_space >= request.amount:
                print(f'В пункте \"{request.to}\" достаточно места')
            else:
                print(f"В пункте {request.to} не хватает {request.amount - store.get_free_space} места")
                continue

            store.remove(request.product, request.amount)
            print(f'Курьер забрал {request.amount} {request.product} из пункта {request.from_}')
            print(f'Курьер везет {request.amount} {request.product} из пункта {request.from_} в пункт {request.to}')
            shop.add(request.product, request.amount)
            print(f'Курьер доставил {request.amount} {request.product} в пункта {request.to}')


        print("=" * 30)
        print(f'На складе:')
        for title, count in store.items.items():
            print(f"{title}: {count}")
        print(f"Свободного места {store.get_free_space}")

        print("=" * 30)
        print(f'В магазине:')
        for title, count in shop.items.items():
            print(f"{title}: {count}")
        print(f"Свободного места {shop.get_free_space}")
        print("=" * 30)


if __name__ == '__main__':
    # при запуске программы на RUN создаем объекты склада и магазина
    store = Store()
    shop = Shop()

    # заранее создаем загрузку склада
    store_items = {
        'чипсы': 10,
        'сок': 20,
        'кофе': 7,
        'печеньки': 38
    }

    # загружаем склад
    store.items = store_items

    # вызываем главную функцию программы
    main()
