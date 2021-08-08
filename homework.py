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


class CashCalculator(Calculator):

    USD_RATE = 70.00
    EURO_RATE = 85.00

    def get_today_cash_remained(self, currency):
        limit = self.limit
        today_stats = self.get_today_stats()
        currency_dict = {'rub': (today_stats, limit, 'руб'),
                         'usd': (today_stats / self.USD_RATE,
                                 limit / self.USD_RATE, 'USD'),
                         'eur': (today_stats / self.EURO_RATE,
                                 limit / self.EURO_RATE, 'Euro')}
        if currency not in currency_dict:
            return('неизвестная валюта')
        money, limit_money, rate = currency_dict[currency]
        balance = abs(limit_money - money)
        if limit > today_stats:
            return(f'На сегодня осталось{balance: .2f}'
                   f' {rate}')
        elif limit == today_stats:
            return('Денег нет, держись')
        return(f'Денег нет, держись: твой долг -{balance: .2f}'
               f' {rate}')


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        limit = self.limit
        today_stats = self.get_today_stats()
        if limit > today_stats:
            new_limit_cal = limit - today_stats
            return('Сегодня можно съесть что-нибудь ещё, но с общей'
                   f' калорийностью не более {new_limit_cal} кКал')
        return('Хватит есть!')
