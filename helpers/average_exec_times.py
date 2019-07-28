"""This script calculate compress algorithms' average execution time """
import sys
import xlsxwriter
sys.path.append('../')


def create_dicts():
    time_dict = {
        'CSR': {
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
        'CSC': {
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
        'COO': {
            '0.005': {
                '5000': 0, '7000': 0, '9000': 0, '11000': 0, '13000': 0, '15000': 0,
                '17000': 0, '19000': 0, '21000': 0, '23000': 0}
            ,
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
        'Diagonal': {
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
    with open('execution_time.txt', 'r') as f:
        for lines in f:
            times.append(lines.split())

    return times


def calculate_avg(exec_time, dict_times, type):
    """
    :param exec_time: list
    :param dict_times: dictionary
    :param type: -
    ----------------------
    Calculate the average time for each format type, density and dimension
    ----------------------
    :return: a dictionary with the average times
    """
    for time in exec_time:
        dict_times[time[0]][time[2]][time[1]] = dict_times[time[0]][time[2]][time[1]] + float(time[3])

    # print(dict_times)

    for index in dict_times:
        for inner_index in dict_times[index]:
            for inner_inner_index in dict_times[index][inner_index]:
                dict_times[index][inner_index][inner_inner_index] /= 10
    print(dict_times)
    write_times(dict_times, type)

    return dict_times


def write_times(t_dict, type):
    """
    :param t_dict: dictionary
    :param type: -
    ----------------------
    Write average times in a txt file
    ----------------------
    :return: -
    """
    file_name = 'exec_times_final.txt'

    with open(file_name, 'w') as f:
        for key, inner_dict in t_dict.items():
            for key_inner, value in inner_dict.items():
                f.write("%s\t%s\t%s\n" % (key, key_inner, value))


def create_tables(exec_time_dicts):
    """
    :param exec_time_dicts: dictionary
    ----------------------
    Create a xlsx file with tables to present the average times
    ----------------------
    :return: -
    """
    workbook = xlsxwriter.Workbook('seq_execution_times_table.xlsx')
    worksheet = workbook.add_worksheet()
    caption = 'Sequential execution time'
    # Set the columns widths.
    worksheet.set_column('B:F', 12)
    _format = workbook.add_format()
    # Write the caption.
    worksheet.write('B1', caption)

    row_index = 3
    densities = ['0.005', '0.01', '0.015', '0.02']

    general_columns_values = [5000, 7000, 9000, 11000, 13000, 15000, 17000, 19000, 21000, 23000]
    time_values = []
    for density in densities:
        # transform our data to the needed format
        for key, inner_dict in exec_time_dicts.items():
            temp_list = [key]
            for key_inner, value in inner_dict[density].items():
                temp_list.append(value)
            time_values.append(temp_list)

        table_columns = [{'header': str(density)}]
        for value in general_columns_values:
            table_columns.append(
                {'header': str(value), 'format': _format}
            )

        # Options to use in the table.
        options = {'data': time_values,
                   'columns': table_columns}

        row_to_show = 'B' + str(row_index) + ':L' + str((row_index+4))
        row_index += 8
        # Add a table to the worksheet.
        worksheet.add_table(row_to_show, options)
        time_values = []

    workbook.close()


if __name__ == "__main__":
    exec_time_dicts = create_dicts()
    exec_times_file = read_exec_times()
    exec_time_dicts = calculate_avg(exec_times_file, exec_time_dicts, type)
    create_tables(exec_time_dicts)
