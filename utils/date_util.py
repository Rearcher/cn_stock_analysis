import time
import datetime


holiday = ['2015-01-01', '2015-01-02', '2015-01-03', '2015-02-18', '2015-02-19', '2015-02-20', '2015-02-21',
           '2015-02-22', '2015-02-23', '2015-02-24', '2015-04-06', '2015-05-01', '2015-06-22', '2015-09-03',
           '2015-09-04', '2015-10-01', '2015-10-02', '2015-10-05', '2015-10-06', '2015-10-07']


def to_date(date_str, date_format='%Y-%m-%d'):
    y, m, d = time.strptime(date_str, date_format)[0:3]
    return datetime.date(y, m, d)


def is_holiday(date_str):
    return date_str in holiday


def get_date_ruler(begin_date, end_date):
    """
    get date ruler from begin_date to end_date, begin_date and end_date must be valid
    :param begin_date: begin of date ruler
    :param end_date: end of date ruler
    :return: date ruler from begin_date to end_date
    """
    date_input = open('date_ruler', 'r')
    d_format = '%Y-%m-%d'
    begin_date = to_date(begin_date, d_format)
    end_date = to_date(end_date, d_format)

    all_date = date_input.read().split('\n')
    all_date = all_date[:len(all_date) - 1]
    all_date = map(lambda d: to_date(d, d_format), all_date)

    result = []
    for date in all_date:
        if date < begin_date:
            continue
        if date > end_date:
            break
        result.append(date)

    date_input.close()
    return result


def main():
    print(to_date('2010/09/10', '%Y/%m/%d'))


if __name__ == '__main__':
    main()