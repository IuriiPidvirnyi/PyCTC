# coding=utf-8
import os
import csv


def env_files(input_dir="input"):
    print("\nENV file(s) to be used in parsing:")
    count = 0
    env_files = []
    for _file in os.listdir(input_dir):
        if not _file.__contains__('input') and _file.endswith('.env'):
            env_files.append(_file)
            count += 1
            print "\t%i)." % count, _file
        else:
            continue
    return env_files


def env_parser(env_file, input_dir='input'):
    try:
        with open(os.path.join(input_dir, env_file), 'rb') as env_in:
            csv_data = env_in.readlines()
    except:
        print("Error while read ENV file %s", env_file)
    else:
        count_lines = 0
        count_else_lines = 0
        count_skipped_lines = 0
        count_values = 0
        values = []
        for line in csv_data:
            count_lines += 1
            if line.startswith("#") or line.startswith("["):
                count_skipped_lines += 1
                continue
            elif line.startswith("\""):
                values.append(line.split("\\"))
                count_values += 1
            else:
                count_else_lines += 1
        return values, count_values, count_lines, count_skipped_lines


def csv_out_data(env_file):
        name = [i[1:-1] for i in [e[0] for e in [el for el in env_parser(env_file)[0]]]]
        value = [i[1:-1] for i in [e[-1].strip() for e in [el for el in env_parser(env_file)[0]]]]
        csv_out_data = zip(name, value)
        return csv_out_data, name, value


def csv_writer(output_dir, csv_file_name, csv_file_fieldnames, env_file):
    with open(os.path.join(output_dir, csv_file_name), 'wb') as csv_out:
        csv_writer = csv.writer(csv_out)
        csv.DictWriter(csv_out, csv_file_fieldnames).writeheader()
        for row in csv_out_data(env_file)[0]:
            csv_writer.writerow(row)


def main():
    output_dir = 'output'
    csv_file_name = 'ENVIRONMENT_VARIABLES.csv'
    csv_file_fieldnames = ("Name", "Value")
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    for env_file in env_files():
        csv_writer(output_dir, csv_file_name, csv_file_fieldnames, env_file)


if __name__ in "__main__":
    main()
