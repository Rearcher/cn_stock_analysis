import csv
from utils.date_util import get_date_ruler


def read_data(data_dir, file, begin_date, end_date):
    filename, returns = ''.join([data_dir, file]), []
    date_ruler = list(map(str, get_date_ruler('2015-01-06', '2015-11-02')))
    begin_index, end_index = date_ruler.index(begin_date), date_ruler.index(end_date)

    with open(filename, 'r') as f:
        returns = f.readlines()
        returns = list(map(float, returns))

    return returns[begin_index:end_index+1]


def read_raw_data(data_dir, file, begin_date, end_date, columns):
    filename, returns = ''.join([data_dir, file]), []

    with open(filename, 'r') as f:
        csv_reader = csv.DictReader(f)
        date = [row['date'] for row in csv_reader]
        begin_index, end_index = date.index(begin_date), date.index(end_date)

        for column in columns:
            f.seek(0)
            csv_reader = csv.DictReader(f)
            returns.append([float(row[column]) for row in csv_reader][begin_index:end_index+1])

    return date[begin_index:end_index+1], returns


def get_valid_stock():
    with open('../resources/national_team_investment.csv') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        valid_stock = [row['股票代码'] for row in csv_reader]
    return valid_stock


def main():
    data_dir = '/Users/rahul/tmp/correlations/'
    data = read_data(data_dir=data_dir, file='cor_000001_000002', begin_date='2015-01-06', end_date='2015-11-02')
    print(len(data), data)

    data_dir = '/Users/rahul/tmp/data/aligned_data/'
    (date, data) = read_raw_data(data_dir=data_dir, file='000001.txt', begin_date='2015-01-06', end_date='2015-11-02',
                                 columns=['close', 'trading_volume', 'transaction_volume'])
    print(len(date), date)
    for x in data:
        print(len(x), list(map(float, x)))

if __name__ == '__main__':
    main()
