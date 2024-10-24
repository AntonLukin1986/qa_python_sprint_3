"""Калькулятор для подсчёта калорий и наличности.
ЯПрактикум, 2 спринт. Ревью."""
import datetime as dt


class Calculator:
    """Родительский класс Калькулятор с общим функционалом."""
    SEVEN_DAYS = dt.timedelta(days=7)

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, new_record):
        self.records.append(new_record)

    def get_today_stats(self):
        today = dt.date.today()
        return sum(record.amount for record in self.records
                   if record.date == today)

    def get_week_stats(self):
        today = dt.date.today()
        last_week = today - self.SEVEN_DAYS
        return sum(record.amount for record in self.records
                   if last_week < record.date <= today)


class Record:
    """Отдельный класс для записей в Калькулятор."""
    DATE_FORMAT = '%d.%m.%Y'

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        self.date = date
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, self.DATE_FORMAT).date()


class CaloriesCalculator(Calculator):
    """Калькулятор для подсчёта калорий."""
    NOTHING_TO_WARRY = ('Сегодня можно съесть что-нибудь ещё, '
                        'но с общей калорийностью не более {} кКал')
    WARNING = 'Хватит есть!'

    def get_calories_remained(self):
        calories_today = self.get_today_stats()
        if calories_today < self.limit:
            rest_calories = self.limit - calories_today
            return self.NOTHING_TO_WARRY.format(rest_calories)
        return self.WARNING


class CashCalculator(Calculator):
    """Калькулятор для подсчёта денег."""
    EURO_RATE = 70.0
    USD_RATE = 60.0
    RUB_RATE = 1.0
    CURRENCIES = {
        'rub': ('руб', RUB_RATE),
        'usd': ('USD', USD_RATE),
        'eur': ('Euro', EURO_RATE)
    }
    REST_MONEY = 'На сегодня осталось {balance} {currency}'
    DEBT = 'Денег нет, держись: твой долг - {balance} {currency}'
    NO_MONEY = 'Денег нет, держись'
    UNKNOWN_CURRENCY = 'Неизвестная валюта: {currency}'

    def get_today_cash_remained(self, currency):
        try:
            name, rate = self.CURRENCIES[currency]
        except KeyError:
            raise ValueError(self.UNKNOWN_CURRENCY.format(currency=currency))
        money_spent = self.get_today_stats()
        if money_spent == self.limit:
            return self.NO_MONEY
        money_balance = round((self.limit - money_spent) / rate, 2)
        if money_spent < self.limit:
            return self.REST_MONEY.format(currency=name, balance=money_balance)
        return self.DEBT.format(currency=name, balance=abs(money_balance))


# ========== Тестирование ==========

test = CaloriesCalculator(100)
test = CashCalculator(100)
test.add_record(Record(amount=20, comment='rec 1'))
test.add_record(Record(amount=30, comment='rec 2'))
test.add_record(Record(amount=40, comment='rec 3', date='01.10.2021'))


print('Сегодня:', test.get_today_stats())
print('За неделю:', test.get_week_stats())
print(test.get_calories_remained())
print(test.get_today_cash_remained('rub'))
