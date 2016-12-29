import time
import datetime


holiday = ['2015-01-01', '2015-01-02', '2015-01-03', '2015-02-18', '2015-02-19', '2015-02-20', '2015-02-21',
           '2015-02-22', '2015-02-23', '2015-02-24', '2015-04-06', '2015-05-01', '2015-06-22', '2015-09-03',
           '2015-09-04', '2015-10-01', '2015-10-02', '2015-10-05', '2015-10-06', '2015-10-07']


def to_date(date_str):
    y, m, d = time.strptime(date_str, "%Y-%m-%d")[0:3]
    return datetime.date(y, m, d)


def is_holiday(date_str):
    return date_str in holiday


print(is_holiday('2015-01-04'))
