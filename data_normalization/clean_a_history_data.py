import os
import datetime
import time

def to_date(str):
    y, m, d = time.strptime(str, "%Y/%m/%d")[0:3]
    return datetime.date(y, m, d)


def normalize_single_file(input, output):
    input = open(input, 'r')
    output = open(output, 'w')

    input.readline()
    input.readline()
    output.write(','.join(["date", "open", "high", "low", "close", "trading_volume", "transaction_volume\n"]))
    line = input.readline()

    prev_date = to_date(line.split('\t')[0]) - datetime.timedelta(days=1)
    prev_price = line.split('\t')[1:]

    while line:
        line = line.split('\t')

        # meet last line
        if len(line) <= 2:
            break

        cur_date = to_date(line[0])
        line[0] = str(cur_date)

        temp_date = prev_date + datetime.timedelta(days=1)
        if temp_date != cur_date:
            while temp_date < cur_date:
                if temp_date.weekday() >= 5:
                    temp_date += datetime.timedelta(days=1)
                    continue
                temp_line = [str(temp_date)]
                temp_line.extend(prev_price)
                print("fake data ==>", temp_line)
                output.write(','.join(temp_line))
                temp_date += datetime.timedelta(days=1)
            output.write(','.join(line))
        else:
            output.write(','.join(line))
        prev_date = cur_date
        prev_price = line[1:]

        line = input.readline()

    input.close()
    output.close()


def normalize_all_file(dir):
    files = os.listdir(dir)
    cnt = 0
    for file in files:
        id = file.split('.')[0]
        outfile = "complete_data/" + str(id) + ".csv"
        infile = "A_history_data/" + file
        print(cnt, ": ", infile, "==> ", outfile)
        normalize_single_file(infile, outfile)
        cnt += 1


def get_ids(input):
    input = open(input, 'r')

    ids = []
    line = input.readline()
    while line:
        ids.append(line)
        line = input.readline()

    input.close()
    return ids

if __name__ == "__main__":
    # normalize_single_file("A_history_data/SH600000.txt", "test.csv")
    # normalize_all_file("A_history_data")
    print("hello")