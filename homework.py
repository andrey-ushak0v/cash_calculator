import datetime as dt
from typing import Optional


DATE_FORMAT = '%d.%m.%Y'


class Record:
    def __init__(self,
                 amount: int,
                 comment: str,
                 date: Optional[str] = None) -> None:
        self.amount = amount
        self.comment = comment
        self.date: dt.date = dt.date.today()
        if date is not None:
            self.date = dt.datetime.strptime(date, DATE_FORMAT).date()


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today = dt.date.today()
        return sum(i.amount for i in self.records
                   if i.date == today)

    def get_week_stats(self):
        today = dt.date.today()
        first_day_from_seven = today - dt.timedelta(days=7)
        return sum(i.amount for i in self.records
                   if first_day_from_seven <= i.date <= today)

    def balance(self):
        return abs(self.limit - self.get_today_stats())


class CashCalculator(Calculator):

    USD_RATE = 60.00
    EURO_RATE = 70.00
    RUB_RATE = 1.00

    money: dict = {'rub': (RUB_RATE, 'руб'),
                   'usd': (USD_RATE, 'USD'),
                   'eur': (EURO_RATE, 'Euro')}

    def get_today_cash_remained(self, currency):
        today_stats = self.get_today_stats()
        if currency not in self.money:
            return 'неизвестная валюта'
        rate, rate_name = self.money[currency]
        balance = self.balance()
        if self.limit > today_stats:
            return(f'На сегодня осталось{balance / rate: .2f}'
                   f' {rate_name}')
        elif self.limit == today_stats:
            return'Денег нет, держись'
        return(f'Денег нет, держись: твой долг -{balance / rate: .2f}'
               f' {rate_name}')


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        today_stats = self.get_today_stats()
        if self.limit > today_stats:
            new_limit = self.balance()
            return('Сегодня можно съесть что-нибудь ещё, но с общей'
                   f' калорийностью не более {new_limit} кКал')
        return'Хватит есть!'
