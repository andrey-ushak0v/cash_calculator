import datetime as dt
from typing import Optional


class Record:
    def __init__(self,
                 amount: int,
                 comment: str,
                 date: Optional[str] = None) -> None:
        self.amount = amount
        self.comment = comment
        self.date: dt.date = dt.date.today()
        if date is not None:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()
       

class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):          # добавляет запись в список records
        self.records.append(record)

    def get_today_stats(self):    # считает сумму за день
        today_stats = 0
        today = dt.date.today()
        for i in self.records:
            if i.date == today:
                today_stats = today_stats + i.amount
        return today_stats

    def get_week_stats(self):     # считает за неделю
        today = dt.date.today()
        week_stats = 0
        first_day_from_seven = today - dt.timedelta(days=7)
        for i in self.records:
            if today >= i.date >= first_day_from_seven:
                week_stats = week_stats + i.amount
        return week_stats


class CashCalculator(Calculator):

    USD_RATE = 70.00
    EURO_RATE = 85.00

    def get_today_cash_remained(self, currency):
        limit = self.limit
        today_stats = self.get_today_stats()
        my_dict = {'rub': (today_stats, limit, 'руб'),
                   'usd': (today_stats / self.USD_RATE,
                           limit / self.USD_RATE, 'USD'),
                   'eur': (today_stats / self.EURO_RATE,
                           limit / self.EURO_RATE, 'Euro')}
        money, limit_money, rate = my_dict[currency]
        balance = abs(limit_money - money)
        if limit > today_stats:
            return(f'На сегодня осталось{balance: .2f}'
                   f' {rate}')
        elif limit == today_stats:
            return('Денег нет, держись')
        elif today_stats > limit:
            return(f'Денег нет, держись: твой долг -{balance: .2f}'
                   f' {rate}')


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        limit = self.limit
        today_stats = self.get_today_stats()
        if limit > today_stats:
            new_limit_cal = limit - today_stats
            return(f'Сегодня можно съесть что-нибудь ещё, но с общей'
                   f' калорийностью не более {new_limit_cal} кКал')
        elif today_stats >= limit:
            return('Хватит есть!')


cash_calculator = CashCalculator(1000)
cash_calculator.add_record(Record(amount=400, comment="beer",
                                  date="07.08.2021"))
cash_calculator.add_record(Record(amount=100, comment="beer",
                                  date="07.08.2021"))
cash_calculator.add_record(Record(amount=5, comment="tea",
                                  date="07.08.2021"))
print(cash_calculator.get_today_cash_remained('rub'))           
calories_calculator = CaloriesCalculator(2000)
calories_calculator.add_record(Record(amount=180, comment="pizza",
                                      date="07.08.2021"))
calories_calculator.add_record(Record(amount=1, comment="pizza",
                                      date="07.08.2021"))
calories_calculator.add_record(Record(amount=500, comment="pizza",
                                      date="07.08.2021"))
