import datetime
import time
import data_normalization.date_util as date_util

begin = datetime.date(1990, 3, 1)
end = datetime.date(2000, 3, 31)
delta = datetime.timedelta(days=1)

def normalize_data(input, output, date_format, base_price):
    input = open(input, 'r')
    output = open(output, 'w')
    today = begin
    base_price = [2635.59, 2655.63, 2607.88, 2635.59]

    # skip column name
    line = input.readline()
    output.write(line)

    line = input.readline()
    while line:
        line = line.split(',')
        y, m, d = time.strptime(line[0], date_format)[0:3]
        line[0] = str(datetime.date(y, m, d))
        cur_date = datetime.date(y, m, d)

        if cur_date.weekday() >= 5:
            line = input.readline()
            continue

        if cur_date == today:
            output.write(",".join(line))
            base_price = line[1:]
        else:
            while today < cur_date:
                if today.weekday() > 4:
                    today += datetime.timedelta(days=1)
                    continue
                temp_line = [str(today)]
                temp_line.extend(base_price)
                output.write(",".join(temp_line))
                print("fake data ==> ", ",".join(temp_line))
                today += datetime.timedelta(days=1)
            output.write(",".join(line))

        line = input.readline()
        if today.weekday() == 4:
            today += datetime.timedelta(days=3)
        else:
            today += datetime.timedelta(days=1)

    input.close()
    output.close()


def write_returns(input, output, base_price):
    input = open(input, 'r')
    output = open(output, 'w')

    # skip column name
    line = input.readline()
    line = input.readline()
    output.write("Date,Return\n")

    while line:
        line = line.split(',')
        cur_price = float(line[4])
        print(cur_price , "==>", base_price)
        output.write(line[0] + "," + str(cur_price - base_price) + "\n")
        base_price = cur_price
        line = input.readline()

    input.close()
    output.close()


if __name__ == "__main__":
    # normalize_data("DJIA_history.csv", "djia.csv", "%m/%d/%Y", [])
    # normalize_data("NASDAQ_composite_history.csv", "nasdaq.csv", "%Y-%m-%d", [])
    # write_returns("djia.csv", "djia_return.csv", 2635.59)
    # write_returns("nasdaq.csv", "nasdaq_return.csv", 427.200012)
    print(date_util.is_holiday("2015-01-01"))