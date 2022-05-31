import holidays
from datetime import timedelta, date
from fast_bitrix24 import Bitrix
from datetime import datetime
import os

# данные для создания задачи в битрикс
webhook = os.environ.get('WEBHOOK')   # вебхук хранится в переменных окружения
bitrix = Bitrix(webhook)
method = 'tasks.task.add'
params = {'fields': {'ID': '1', 'TITLE': 'задача', 'DESCRIPTION': 'Текст', 'RESPONSIBLE_ID': '1'}}

# тут хранятся данные о годе, количестве дней до праздника и список, в который будут помещены даты за 3 дня до праздника
BEFORE_HOLIDAYS_DELTA_DAYS = 3
CURRENT_YEAR = 2022
date_list = []

# указываем, что работаем с российскими праздниками
ru_holidays = holidays.country_holidays("RU")

before_holidays_delta = timedelta(days=BEFORE_HOLIDAYS_DELTA_DAYS)

# получаем даты праздников
holidays_base = holidays.RU(years=CURRENT_YEAR).items()
holiday_start_date_base = dict()

upper_date = date(year=CURRENT_YEAR + 1, month=1, day=1)

for holiday_date, holiday_name in holidays_base:
    current_holiday_start_date = holiday_start_date_base.get(holiday_name, upper_date)
    if holiday_date < current_holiday_start_date:
        holiday_start_date_base[holiday_name] = holiday_date

# получаем дату до праздников и заносим ее в список
for holiday_name, holiday_date_start in holiday_start_date_base.items():
    date_before_holiday = holiday_date_start - before_holidays_delta
    date_list.append(date_before_holiday)

# сравниваем текущую дату с датами из списка
for i in date_list:
    if datetime.now().date() == i:
        r = bitrix.call(method, params)
