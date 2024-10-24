'''QA автоматизация. Спринт 3. ООП (инкапсуляция).'''


class OnlineSalesRegisterCollector:
    '''Онлайн-касса.'''
    __DISCOUNT = 0.9
    __ITEMS_FOR_DISCOUNT = 10
    VAT_10 = {'value': 10, 'quotient': 0.1}
    VAT_20 = {'value': 20, 'quotient': 0.2}
    AVAILABILITY_ERROR = 'Позиция отсутствует в товарном справочнике'
    CHARACTERS_ERROR = ('Нельзя добавить товар, если в его названии нет '
                        'символов или их больше 40')
    NOT_IN_CHEQUE_ERROR = 'Позиция отсутствует в чеке'

    def __init__(self):
        self.__name_items = []
        self.__number_items = 0
        self.__item_price = {
            'чипсы': 50, 'кола': 100, 'печенье': 45, 'молоко': 55, 'кефир': 70
        }
        self.__tax_rate = {
            'чипсы': 20, 'кола': 20, 'печенье': 20, 'молоко': 10, 'кефир': 10
        }

    @property
    def name_items(self):
        '''Получить перечень товаров в чеке.'''
        return self.__name_items

    @property
    def number_items(self):
        '''Получить количество товаров в чеке.'''
        return self.__number_items

    def add_item_to_cheque(self, name):
        '''Добавить товар в чек.'''
        if 0 < len(name) < 41:
            if name not in self.__item_price:
                raise NameError(self.AVAILABILITY_ERROR)
            self.__name_items.append(name)
            self.__number_items += 1
        else:
            raise ValueError(self.CHARACTERS_ERROR)

    def delete_item_from_cheque(self, name):
        '''Убрать товары из чека.'''
        if name not in self.__name_items:
            raise NameError(self.NOT_IN_CHEQUE_ERROR)
        self.__name_items.remove(name)
        self.__number_items -= 1

    def __apply_discount(self, amount):
        '''Применить скидку при необходимости.'''
        if len(self.__name_items) > self.__ITEMS_FOR_DISCOUNT:
            amount *= self.__DISCOUNT
        return amount

    def cheque_amount(self):
        '''Посчитать общую сумму покупок.'''
        total = [
            self.__item_price[item] for item in self.__name_items
        ]
        return self.__apply_discount(sum(total))

    def __tax_calculation(self, vat):
        '''Рассчитать НДС товаров для требуемой налоговой ставки.'''
        x_percent_tax = filter(
            lambda item: self.__tax_rate[item] == vat['value'],
            self.__name_items
        )
        total = [
            self.__item_price[item] for item in x_percent_tax
        ]
        return self.__apply_discount(sum(total)) * vat['quotient']

    def twenty_percent_tax_calculation(self):
        '''Рассчитать НДС товаров с налоговой ставкой 20%.'''
        return self.__tax_calculation(self.VAT_20)

    def ten_percent_tax_calculation(self):
        '''Рассчитать НДС товаров с налоговой ставкой 10%.'''
        return self.__tax_calculation(self.VAT_10)

    def total_tax(self):
        '''Посчитать общую сумму НДС по чеку.'''
        return (self.ten_percent_tax_calculation() +
                self.twenty_percent_tax_calculation())

    @staticmethod
    def get_telephone_number(telephone_number):
        '''Вернуть номер телефона покупателя в полном формате.'''
        if not isinstance(telephone_number, int):
            raise ValueError('Необходимо ввести цифры')
        if len(str(telephone_number)) != 10:
            raise ValueError('Необходимо ввести 10 цифр после "+7"')
        return f'+7{telephone_number}'

    @staticmethod
    def get_date_and_time():
        '''Вернуть дату и время покупки.'''
        from datetime import datetime
        now = datetime.now()
        date = now.date().strftime('%d.%m.%Y')
        time = now.time().strftime('%H:%M').rjust(17, ' ')
        return f'Дата покупки: {date}\nВремя: {time}'


if __name__ == '__main__':
    register = OnlineSalesRegisterCollector()
    register.add_item_to_cheque('чипсы')
    register.add_item_to_cheque('кола')
    register.add_item_to_cheque('кефир')
    assert register.number_items == 3
    assert register.name_items == ['чипсы', 'кола', 'кефир']
    assert register.cheque_amount() == 220
    assert register.twenty_percent_tax_calculation() == 30
    assert register.ten_percent_tax_calculation() == 7
    assert register.total_tax() == 37
    for _ in range(8):
        register.add_item_to_cheque('молоко')
    assert register.number_items == 11
    assert register.twenty_percent_tax_calculation() == 27
    assert register.ten_percent_tax_calculation() == 45.900000000000006
    assert register.total_tax() == 72.9
    assert register.cheque_amount() == 594
    assert (OnlineSalesRegisterCollector.get_telephone_number(9258076451) ==
            '+79258076451')
    print(register.get_date_and_time())
