"""This script calculate multiplication algorithms' average execution time using numpy"""
import sys

import xlsxwriter

sys.path.append('../')


def create_dicts():
    time_dict = {
        'inner_product_numpy': {
            '0.005': {
                '1000': 0, '2000': 0, '3000': 0, '4000': 0, '5000': 0, '6000': 0,
                '7000': 0, '8000': 0
            },
            '0.01': {
                '1000': 0, '2000': 0, '3000': 0, '4000': 0, '5000': 0, '6000': 0,
                '7000': 0, '8000': 0
            },
            '0.02': {
                '1000': 0, '2000': 0, '3000': 0, '4000': 0, '5000': 0, '6000': 0,
                '7000': 0, '8000': 0
            }
        },
        'outer_product_numpy': {
            '0.005': {
                '1000': 0, '2000': 0, '3000': 0, '4000': 0, '5000': 0, '6000': 0,
                '7000': 0, '8000': 0
            },
            '0.01': {
                '1000': 0, '2000': 0, '3000': 0, '4000': 0, '5000': 0, '6000': 0,
                '7000': 0, '8000': 0
            },
            '0.02': {
                '1000': 0, '2000': 0, '3000': 0, '4000': 0, '5000': 0, '6000': 0,
                '7000': 0, '8000': 0
            }
        },
        'matrix-vector_numpy': {
            '0.005': {
                '1000': 0, '2000': 0, '3000': 0, '4000': 0, '5000': 0, '6000': 0,
                '7000': 0, '8000': 0
            },
            '0.01': {
                '1000': 0, '2000': 0, '3000': 0, '4000': 0, '5000': 0, '6000': 0,
                '7000': 0, '8000': 0
            },
            '0.02': {
                '1000': 0, '2000': 0, '3000': 0, '4000': 0, '5000': 0, '6000': 0,
                '7000': 0, '8000': 0
            }
        },
        'vector-matrix_numpy': {
            '0.005': {
                '1000': 0, '2000': 0, '3000': 0, '4000': 0, '5000': 0, '6000': 0,
                '7000': 0, '8000': 0
            },
            '0.01': {
                '1000': 0, '2000': 0, '3000': 0, '4000': 0, '5000': 0, '6000': 0,
                '7000': 0, '8000': 0
            },
            '0.02': {
                '1000': 0, '2000': 0, '3000': 0, '4000': 0, '5000': 0, '6000': 0,
                '7000': 0, '8000': 0
            }
        },
        'matrix-matrix_numpy': {
            '0.005': {
                '1000': {'1000': 0, '2000': 0}, '2000': {'2000': 0, '4000': 0}, '3000': {'3000': 0, '6000': 0},
                '4000': {'4000': 0, '8000': 0}, '5000': {'5000': 0, '10000': 0}, '6000': {'6000': 0, '12000': 0},
                '7000': {'7000': 0, '14000': 0}, '8000': {'8000': 0, '16000': 0}
            },
            '0.01': {
                '1000': {'1000': 0, '2000': 0}, '2000': {'2000': 0, '4000': 0}, '3000': {'3000': 0, '6000': 0},
                '4000': {'4000': 0, '8000': 0}, '5000': {'5000': 0, '10000': 0}, '6000': {'6000': 0, '12000': 0},
                '7000': {'7000': 0, '14000': 0}, '8000': {'8000': 0, '16000': 0}
            },
            '0.02': {
                '1000': {'1000': 0, '2000': 0}, '2000': {'2000': 0, '4000': 0}, '3000': {'3000': 0, '6000': 0},
                '4000': {'4000': 0, '8000': 0}, '5000': {'5000': 0, '10000': 0}, '6000': {'6000': 0, '12000': 0},
                '7000': {'7000': 0, '14000': 0}, '8000': {'8000': 0, '16000': 0}
            }
        },
    }
    return time_dict


def read_exec_times():
    """
    Read execution times from a txt file and store them to a list
    ----------------------
    :return: a list with the execution times
    """
    times = []
    with open('../execution_results/multiplication_numpy_time.txt', 'r') as f:
        for lines in f:
            times.append(lines.split())
    return times


def calculate_avg(exec_time, dict_times):
    """
    :param exec_time: list
    :param dict_times: dictionary
    ----------------------
    Calculate the average time for each format type, density and dimension
    ----------------------
    :return: a dictionary with the average times
    """
    for time in exec_time:
        if time[0] == 'matrix-matrix_numpy':
            dict_times[time[0]][time[4]][time[1]][time[3]] += float(time[5])
        elif time[0] == 'outer_product_numpy':
            dict_times[time[0]][time[4]][time[2]] += float(time[5])
        else:
            dict_times[time[0]][time[4]][time[1]] += float(time[5])

    for operation_type_index in dict_times:
        if operation_type_index == 'matrix-matrix_numpy':
            for density_size in dict_times[operation_type_index]:
                for size_index in dict_times[operation_type_index][density_size]:
                    for results_size_index in dict_times[operation_type_index][density_size][size_index]:
                        dict_times[operation_type_index][density_size][size_index][results_size_index] /= 10
        elif operation_type_index == 'vector-matrix_numpy' or operation_type_index == 'matrix-vector_numpy':
            for density_size in dict_times[operation_type_index]:
                for size_index in dict_times[operation_type_index][density_size]:
                    dict_times[operation_type_index][density_size][size_index] /= 10
        else:
            for density_size in dict_times[operation_type_index]:
                for size_index in dict_times[operation_type_index][density_size]:
                    dict_times[operation_type_index][density_size][size_index] /= 10

    return dict_times


def create_tables(execution_time_dict):
    """
    :param execution_time_dict: dictionary
    ----------------------
    Create a xlsx file with tables to present the average times
    ----------------------
    :return: -
    """
    workbook = xlsxwriter.Workbook('../execution_results/multiplication_numpy_times_table.xlsx')
    worksheet = workbook.add_worksheet()
    caption = 'Tables with numpy\' s multiplication execution time'
    # Set the columns widths.
    worksheet.set_column('B:F', 14)
    _format = workbook.add_format()
    # Write the caption.
    worksheet.write('B1', caption)

    row_index = 3
    densities = ['0.005', '0.01', '0.02']

    general_columns_values = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000]

    time_values = []
    for density in densities:
        # transform our data to the needed format
        for key, inner_dict in execution_time_dict.items():
            if key == 'matrix-matrix_numpy':
                continue
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

        row_to_show = 'B' + str(row_index) + ':J' + str((row_index + 8))
        row_index += 8
        # Add a table to the worksheet.
        worksheet.add_table(row_to_show, options)
        time_values = []

    # write table for nxn matrix-matrix multiplication

    time_values_table_1, time_values_table_2 = [], []
    for density, inner_dict in exec_time_dicts['matrix-matrix_numpy'].items():
        temp_list1 = [density]
        temp_list2 = [density]
        for size_index, inner_inner_dict in inner_dict.items():
            size_values = [*inner_inner_dict]
            temp_list1.append(inner_inner_dict[size_values[0]])
            temp_list2.append(inner_inner_dict[size_values[1]])
        time_values_table_1.append(temp_list1)
        time_values_table_2.append(temp_list2)

    table_1_columns, table_2_columns = [{'header': 'matrix-matrix_numpy'}], [{'header': 'matrix-matrix_numpy_2n'}]
    for value in general_columns_values:
        table_1_columns.append(
            {'header': str(value), 'format': _format}
        )
        table_2_columns.append(
            {'header': str(value), 'format': _format}
        )
    table_1_options = {'data': time_values_table_1, 'columns': table_1_columns}
    row_to_show = 'B' + str(row_index) + ':J' + str((row_index + 5))
    row_index += 8
    worksheet.add_table(row_to_show, table_1_options)

    table_2_options = {'data': time_values_table_2, 'columns': table_2_columns}
    row_to_show = 'B' + str(row_index) + ':J' + str((row_index + 8))
    worksheet.add_table(row_to_show, table_2_options)

    workbook.close()


if __name__ == "__main__":
    exec_time_dicts = create_dicts()
    exec_times_file = read_exec_times()
    exec_time_dicts = calculate_avg(exec_times_file, exec_time_dicts)
    create_tables(exec_time_dicts)
