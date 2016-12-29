import datetime
import time
import csv

def to_date(str):
    y, m, d = time.strptime(str, "%Y-%m-%d")[0:3]
    return datetime.date(y, m, d)


def normalize_single_file(input, output):
    begin_date = datetime.date(2014, 11, 3)

    input = open(input, 'r')
    output = open(output, 'w')

    line = input.readline()
    output.write(line)
    line = input.readline()

    while line:
        cur_date = to_date(line.split(',')[0])
        if cur_date < begin_date:
            line = input.readline()
            continue
        output.write(line)
        line = input.readline()

    input.close()
    output.close()


def get_ids(input):
    input = open(input, 'r')

    ids = []
    line = input.readline()
    while line:
        ids.append(line)
        line = input.readline()

    input.close()
    return ids


def normalize_all_file(filter_id):
    files = get_ids(filter_id)
    cnt = 0
    for file in files:
        file = file[:len(file)-1]
        infile = "complete_data/" + file
        outfile = "part_data/" + file
        print(cnt, ": ", infile, "==> ", outfile)
        normalize_single_file(infile, outfile)
        cnt += 1


def write_single_return(input, output):
    input = open(input, 'r')
    output = open(output, 'w')

    # skip column name
    line = input.readline()
    line = input.readline()
    base_price = float(line.split(',')[4])
    output.write("Date,Return\n")

    while line:
        line = line.split(',')
        cur_price = float(line[4])
        # print(cur_price , "==>", base_price)
        output.write(line[0] + "," + str(cur_price - base_price) + "\n")
        base_price = cur_price
        line = input.readline()

    input.close()
    output.close()


def write_all_return(filter_id):
    cnt = 0
    files = get_ids(filter_id)
    for file in files:
        file = file[:len(file)-1]
        infile = "part_data/" + file
        outfile = "part_data_returns/" + file
        print(cnt, ":", infile, "===>", outfile)
        write_single_return(infile, outfile)
        cnt += 1


def get_date_seq(input):
    with open(input, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        column = [row["Date"] for row in reader]
    return column


def get_return_seq(input):
    with open(input, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        column = [row["Return"] for row in reader]
    return column


def write_together(filter_id, output):
    output = open(output, 'w')

    cnt = 0
    files = get_ids(filter_id)
    for file in files:
        file = file[:len(file)-1]
        infile = "part_data_returns/" + file
        if cnt == 0:
            output.write(','.join(get_date_seq(infile)))
            output.write('\n')
        output.write(','.join(get_return_seq(infile)))
        output.write('\n')
        print("process ", cnt)
        cnt += 1

    output.close()


def write_date_seq(output):
    output = open(output, 'w')
    output.write("Date\n")

    date_seq = get_date_seq("part_data_returns/SH600000.csv");
    for date in date_seq:
        output.write(date + '\n')

    output.close()

if __name__ == "__main__":
    # normalize_single_file("A_history_data/SH600000.txt", "test.csv")
    # normalize_all_file("filter_id")
    # print("hello")
    # write_single_return("part_data/SH600000.csv", "return_test")
    # write_all_return("filter_id")
    # write_together("filter_id", "together_data")
    write_date_seq("date.csv")