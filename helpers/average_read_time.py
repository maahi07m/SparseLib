"""This script reads the execution times which takes to read a matrix mxn parallel or sequentially and calculate the
    average time for each density and dimension"""
import sys
sys.path.append('../')


def create_dicts():
    time_dict = {
        'sequential': {
            '0.005': {
                '5000': 0, '7000': 0, '9000': 0, '11000': 0, '13000': 0, '15000': 0,
                '17000': 0, '19000': 0, '21000': 0, '23000': 0
            },
            '0.01': {
                '5000': 0, '7000': 0, '9000': 0, '11000': 0, '13000': 0, '15000': 0,
                '17000': 0, '19000': 0, '21000': 0, '23000': 0
            },
            '0.015': {
                '5000': 0, '7000': 0, '9000': 0, '11000': 0, '13000': 0, '15000': 0,
                '17000': 0, '19000': 0, '21000': 0, '23000': 0
            },
            '0.02':  {
                '5000': 0, '7000': 0, '9000': 0, '11000': 0, '13000': 0, '15000': 0,
                '17000': 0, '19000': 0, '21000': 0, '23000': 0
            }
        },
        'parallel': {
            '0.005': {
                '5000': 0, '7000': 0, '9000': 0, '11000': 0, '13000': 0, '15000': 0,
                '17000': 0, '19000': 0, '21000': 0, '23000': 0
            },
            '0.01': {
                '5000': 0, '7000': 0, '9000': 0, '11000': 0, '13000': 0, '15000': 0,
                '17000': 0, '19000': 0, '21000': 0, '23000': 0
            },
            '0.015': {
                '5000': 0, '7000': 0, '9000': 0, '11000': 0, '13000': 0, '15000': 0,
                '17000': 0, '19000': 0, '21000': 0, '23000': 0
            },
            '0.02':  {
                '5000': 0, '7000': 0, '9000': 0, '11000': 0, '13000': 0, '15000': 0,
                '17000': 0, '19000': 0, '21000': 0, '23000': 0
            }
        }
    }

    return time_dict


def read_exec_times():
    """
    Read execution times from a txt file and create a list
    ----------------------
    :return: a list with the execution times
    """
    times = []
    with open('read_time.txt', 'r') as f:
        for lines in f:
            times.append(lines.split())

    return times


def calculate_avg(exec_time, dict_times, type):
    """
    :param exec_time: list
    :param dict_times: dictionary
    :param type: -
    ----------------------
    Calculate the average time and call the function write_times to store them in a txt file
    ----------------------
    :return: -
    """
    for time in exec_time:
        dict_times[time[0]][time[2]][time[1]] = dict_times[time[0]][time[2]][time[1]] + float(time[3])

    print(dict_times)

    for index in dict_times:
        for inner_index in dict_times[index]:
            for inner_inner_index in dict_times[index][inner_index]:
                dict_times[index][inner_index][inner_inner_index] /= 3
    print(dict_times)
    write_times(dict_times, type)


def write_times(t_dict, type):
    """
    :param t_dict: dictionary
    :param type: -
    ----------------------

    ----------------------
    :return: -
    """
    file_name = 'read_times_final.txt'

    with open(file_name, 'w') as f:
        for key, inner_dict in t_dict.items():
            for key_inner, value in inner_dict.items():
                f.write("%s\t%s\t%s\n" % (key, key_inner, value))


if __name__ == "__main__":
    exec_time_dicts = create_dicts()
    exec_times_file = read_exec_times()
    calculate_avg(exec_times_file, exec_time_dicts, type)
