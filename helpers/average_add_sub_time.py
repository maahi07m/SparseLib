"""This script calculate addition and subtraction algorithms' average execution time """
import sys
import xlsxwriter
sys.path.append('../')

def create_dicts():
    time_dict = {
        'addition_csr': {
            '0.005': {
                '1000': 0, '2000': 0, '3000': 0, '4000': 0, '5000': 0, '6000': 0,
                '7000': 0, '8000': 0, '9000': 0, '10000': 0, '11000': 0, '12000': 0,
                '13000': 0, '14000': 0, '15000': 0
            },
            '0.01': {
                '1000': 0, '2000': 0, '3000': 0, '4000': 0, '5000': 0, '6000': 0,
                '7000': 0, '8000': 0, '9000': 0, '10000': 0, '11000': 0, '12000': 0,
                '13000': 0, '14000': 0, '15000': 0
            },
            '0.02':  {
                '1000': 0, '2000': 0, '3000': 0, '4000': 0, '5000': 0, '6000': 0,
                '7000': 0, '8000': 0, '9000': 0, '10000': 0, '11000': 0, '12000': 0,
                '13000': 0, '14000': 0, '15000': 0
            }
        },
        'subtration_csr': {
            '0.005': {
                '1000': 0, '2000': 0, '3000': 0, '4000': 0, '5000': 0, '6000': 0,
                '7000': 0, '8000': 0, '9000': 0, '10000': 0, '11000': 0, '12000': 0,
                '13000': 0, '14000': 0, '15000': 0
            },
            '0.01': {
                '1000': 0, '2000': 0, '3000': 0, '4000': 0, '5000': 0, '6000': 0,
                '7000': 0, '8000': 0, '9000': 0, '10000': 0, '11000': 0, '12000': 0,
                '13000': 0, '14000': 0, '15000': 0
            },
            '0.02':  {
                '1000': 0, '2000': 0, '3000': 0, '4000': 0, '5000': 0, '6000': 0,
                '7000': 0, '8000': 0, '9000': 0, '10000': 0, '11000': 0, '12000': 0,
                '13000': 0, '14000': 0, '15000': 0
            }
        },
        'addition_csc': {
            '0.005': {
                '1000': 0, '2000': 0, '3000': 0, '4000': 0, '5000': 0, '6000': 0,
                '7000': 0, '8000': 0, '9000': 0, '10000': 0, '11000': 0, '12000': 0,
                '13000': 0, '14000': 0, '15000': 0
            },
            '0.01': {
                '1000': 0, '2000': 0, '3000': 0, '4000': 0, '5000': 0, '6000': 0,
                '7000': 0, '8000': 0, '9000': 0, '10000': 0, '11000': 0, '12000': 0,
                '13000': 0, '14000': 0, '15000': 0
            },
            '0.02': {
                '1000': 0, '2000': 0, '3000': 0, '4000': 0, '5000': 0, '6000': 0,
                '7000': 0, '8000': 0, '9000': 0, '10000': 0, '11000': 0, '12000': 0,
                '13000': 0, '14000': 0, '15000': 0
            }
        },
        'subtration_csc': {
            '0.005': {
                '1000': 0, '2000': 0, '3000': 0, '4000': 0, '5000': 0, '6000': 0,
                '7000': 0, '8000': 0, '9000': 0, '10000': 0, '11000': 0, '12000': 0,
                '13000': 0, '14000': 0, '15000': 0
            },
            '0.01': {
                '1000': 0, '2000': 0, '3000': 0, '4000': 0, '5000': 0, '6000': 0,
                '7000': 0, '8000': 0, '9000': 0, '10000': 0, '11000': 0, '12000': 0,
                '13000': 0, '14000': 0, '15000': 0
            },
            '0.02': {
                '1000': 0, '2000': 0, '3000': 0, '4000': 0, '5000': 0, '6000': 0,
                '7000': 0, '8000': 0, '9000': 0, '10000': 0, '11000': 0, '12000': 0,
                '13000': 0, '14000': 0, '15000': 0
            }
        },
    }
    return time_dict


def read_exec_times():
    times = []
    with open('../execution_results/add_sub_time.txt', 'r') as f:
        for lines in f:
            times.append(lines.split())
    return times


def calculate_avg(exec_time, dict_times, type):
    for time in exec_time:
        dict_times[time[0]][time[3]][time[1]] = dict_times[time[0]][time[3]][time[1]] + float(time[4])

    # print(dict_times)

    for index in dict_times:
        for inner_index in dict_times[index]:
            for inner_inner_index in dict_times[index][inner_index]:
                dict_times[index][inner_index][inner_inner_index] /= 10
    print(dict_times)
    write_times(dict_times, type)
    return dict_times


def write_times(t_dict, type):
    file_name = '../execution_results/add_sub_times_final.txt'

    with open(file_name, 'w') as f:
        for key, inner_dict in t_dict.items():
            for key_inner, value in inner_dict.items():
                f.write("%s\t%s\t%s\n" % (key, key_inner, value))


def create_tables(exec_time_dicts):
    workbook = xlsxwriter.Workbook('../execution_results/add_sub_exec_times_table.xlsx')
    worksheet = workbook.add_worksheet()
    caption = 'Addition and Subtraction time'
    # Set the columns widths.
    worksheet.set_column('B:F', 12)
    _format = workbook.add_format()
    # Write the caption.
    worksheet.write('B1', caption)

    row_index = 3
    densities = ['0.005', '0.01', '0.02']

    general_columns_values = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000,
                              9000, 10000, 11000, 12000, 13000, 14000, 15000]
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

