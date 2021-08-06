import datetime as dt


class Record:
    def __init__(self,
                 amount: int,
                 comment: str,
                 date: str = dt.date.today().strftime('%d.%m.%Y')) -> None:
        self.amount = amount
        self.comment = comment
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

    USD_RATE = 70
    EURO_RATE = 85

    def get_today_cash_remained(self, currency):
        limit = self.limit
        today_stats = self.get_today_stats()
        my_dict = {'rub': (today_stats, limit, 'руб'),
                   'usd': (today_stats / self.USD_RATE,
                           limit / self.USD_RATE, 'USD'),
                   'eur': (today_stats / self.EURO_RATE,
                           limit / self.EURO_RATE, 'euro')}
        money, limit_money, rate = my_dict[currency]
        balance = abs(limit_money - money)
        if limit > today_stats:
            return(f'на сегодня осталось {balance: .2f}'
                   f'{rate}')
        elif limit == today_stats:
            return('Денег нет, держись!')
        elif today_stats > limit:
            return(f'денег нет, держись: твой долг - {balance: .2f}'
                   f'{rate}')


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        limit = self.limit
        today_stats = self.get_today_stats()
        if limit > today_stats:
            new_limit_cal = limit - today_stats
            return(f'можно съесть что то еще,'
                   f'не более {new_limit_cal} каллорий')
        elif today_stats >= limit:
            return('Хватит есть!')


cash_calculator = CashCalculator(1000)
cash_calculator.add_record(Record(amount=100, comment="beer",
                                  date="06.08.2021"))
cash_calculator.add_record(Record(amount=10, comment="beer",
                                  date="06.08.2021"))
cash_calculator.add_record(Record(amount=890, comment="tea",
                                  date="06.08.2021"))
print(cash_calculator.get_today_cash_remained('rub'))
calories_calculator = CaloriesCalculator(2000)
calories_calculator.add_record(Record(amount=1000, comment="pizza",
                                      date="06.08.2021"))
calories_calculator.add_record(Record(amount=1, comment="pizza",
                                      date="06.08.2021"))
calories_calculator.add_record(Record(amount=500, comment="pizza",
                                      date="06.08.2021"))
