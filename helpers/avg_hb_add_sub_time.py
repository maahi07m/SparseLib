"""This script calculate addition and subtraction algorithms' average execution time on hb files"""
import sys

import xlsxwriter

sys.path.append('../')

file_names = [
    'olm1000.rua',
    'tub1000.rua',
    'sherman1.rua',
    'saylr3.rua',
    'orsirr_1.rua',
    'illc1033.rra',
    'well1033.rra',
    'bcsstk08.rsa',
    'bcsstm08.rsa',
    'sherman2.rua',
    'bcsstk09.rsa',
    'bcsstm09.rsa',
    'bcsstk10.rsa',
    'bcsstm10.rsa',
    'tols1090.rua',
    'sherman4.rua',
    'gre_1107.rua',
    '1138_bus.rsa',
    'fidap032.rua',
    'cavity05.rua',
    'cavity06.rua',
    'cavity07.rua',
    'cavity08.rua',
    'cavity09.rua',
    'bcsstk27.rsa',
    'bcsstm27.rsa',
    'pores_2.rua',
    'rdb1250l.rua',
    'mahindas.rua',
    'mhd1280a.cua',
    'mhd1280b.cua',
    'nnc1374.rua',
    'fidap023.rua',
    'bcsstk11.rsa',
    'bcsstk12.rsa',
    'bcsstm11.rsa',
    'bcsstm12.rsa',
    'qh1484.rua',
    'west1505.rua',
    'fidap004.rua',
    'fidap007.rua',
    'fidap006.rua',
    'utm1700b.rua',
    'utm1700a.rua',
    'fidap033.rua',
    'bcsstk14.rsa',
    'fidap003.rua',
    'illc1850.rra',
    'well1850.rra',
    'watt__2.rua',
    'watt__1.rua',
    'plat1919.rsa',
    'plsk1919.rza',
    'bcsstk26.rsa',
    'bcsstm26.rsa',
    'bwm2000.rua',
    'olm2000.rua',
    'tols2000.rua',
    'bcsstk13.rsa',
    'bcsstm13.rsa',
    'west2021.rua',
    'dw2048.rua',
    'rdb2048l.rua',
    'fidapm07.rua',
    'fidap026.rua',
    'fidap020.rua',
    'orsreg_1.rua',
    'fidap024.rua',
    'fidapm33.rua',
    'add20.rua',
    'fidap010.rua',
    'cry2500.rua',
    'orani678.rua',
    'fidapm03.rua',
    'qc2534.cua',
    'fidap013.rua',
    'cavity10.rua',
    'cavity11.rua',
    'cavity12.rua',
    'cavity13.rua',
    'cavity14.rua',
    'cavity15.rua',
    'fidap028.rua',
    'fidap029.rua',
    'zenios.rsa',
    'pde2961.rua',
    'fidapm10.rua',
    'utm3060.rua',
    'fidap036.rua',
    'fidap008.rua',
    'bcsstk23.rsa',
    'bcsstm23.rsa',
    'psmigr_1.rua',
    'psmigr_2.rua',
    'psmigr_3.rua',
    'mhd3200a.rua',
    'rdb3200l.rua',
    'fidap014.rua',
    'sherman5.rua',
    'fidap009.rua',
    'fidapm13.rua',
    'bcsstk24.rsa',
    'bcsstm24.rsa',
    'saylr4.rua',
    'fidap037.rua',
    'bcsstk21.rsa',
    'bcsstm21.rsa',
    'fidapm08.rua',
    'fidap031.rua',
    'lnsp3937.rua',
    'bcsstk15.rsa',
    'fidap012.rua',
    'tols4000.rua',
    'e20r0000.rua',
    'e20r0100.rua',
    'bcsstk28.rsa',
    'cavity16.rua',
    'cavity17.rua',
    'cavity18.rua',
    'cavity19.rua',
    'cavity20.rua',
    'cavity21.rua',
    'cavity22.rua',
    'cavity23.rua',
    'cavity24.rua',
    'cavity25.rua',
    'fidapm09.rua',
    'mhd4800a.rua',
    'gemat1.rra',
    'gemat11.rua',
    'gemat12.rua',
    'add32.rua',
    'olm500.rua',
    'sherman3.rua',
    'rw5151.rua',
    's3rmt3m3.dat',
    's3rmt3m1.dat',
    's3rmq4m1.dat',
    's2rmt3m1.dat',
    's2rmq4m1.dat',
    's1rmt3m1.dat',
    's1rmq4m1.dat',
    'fidap018.rua',
    'utm5940.rua',
    'fidap015.rua',
    'dw8192.rua',
    'fidapm37.rua',
    'fidapm15.rua',
    'e30r0000.rua',
    'e30r2000.rua',
    'bcsstk17.rsa',
    'bcsstk18.rsa',
    'fidap019.rua',
    'fidapm29.rua',
    'bcsstk25.rsa',
    'bcsstm25.rsa',
    'fidap011.rua',
    'e40r0000.rua',
    'e40r2000.rua',
    'memplus.rua',
    'fidap035.rua',
    'fidapm11.rua',
    'af23560.rua']


def create_dicts():
    inner_dict = {}
    for file_name in file_names:
        inner_dict[file_name] = 0

    time_dict = {
        'addition_csr': inner_dict.copy(),
        'subtraction_csr': inner_dict.copy(),
        'addition_csc': inner_dict.copy(),
        'subtraction_csc': inner_dict.copy(),
        'No_supported_format!': [],
        'Wrong_file_format': []
    }
    return time_dict


def read_exec_times():
    """
    Read execution times from a txt file and create a list
    ----------------------
    :return: a list with the execution times
    """
    times = []
    with open('../execution_results/add_sub_hb_time.txt', 'r') as f:
        for lines in f:
            times.append(lines.split())
    return times


def calculate_avg(exec_time, dict_times):
    """
    :param exec_time: list
    :param dict_times: dictionary
    ----------------------
    Calculate the average line for each format type, density and dimension
    ----------------------
    :return: a dictionary with the average times
    """
    for line in exec_time:
        if line[0] == 'Wrong_file_format':
            dict_times['Wrong_file_format'].append(line[1])
        elif line[0] == 'No_supported_format!':
            dict_times['No_supported_format!'].append(line[1])
        else:
            dict_times[line[0]][line[1]] += float(line[2])

    for file_name in file_names:
        if file_name in dict_times['Wrong_file_format'] or file_name in dict_times['No_supported_format!']:
            continue
        else:
            dict_times['addition_csr'][file_name] /= 10
            dict_times['subtraction_csr'][file_name] /= 10
            dict_times['addition_csc'][file_name] /= 10
            dict_times['subtraction_csc'][file_name] /= 10

    return dict_times


def create_tables(execution_time_dict):
    """
    :param execution_time_dict: dictionary
    ----------------------
    Create a xlsx file with tables to present the average times
    ----------------------
    :return: -
    """
    workbook = xlsxwriter.Workbook('../execution_results/add_sub_hb_times_table.xlsx')
    worksheet = workbook.add_worksheet()
    caption = 'HB\'s addition and subtraction execution time'
    # Set the columns widths.
    worksheet.set_column('B:F', 15)
    _format = workbook.add_format()
    # Write the caption.
    worksheet.write('B1', caption)

    row_index = 3

    time_values_table = []
    for file_name in file_names:
        if file_name in execution_time_dict['Wrong_file_format'] or file_name in execution_time_dict[
            'No_supported_format!']:
            continue
        temp_list = [file_name]
        for operation_key in execution_time_dict:
            if operation_key == 'No_supported_format!' or operation_key == 'Wrong_file_format':
                continue
            temp_list.append(float(execution_time_dict[operation_key][file_name]))
        time_values_table.append(temp_list)

    table_1_columns = [{'header': 'HB execution time'}]
    for operation_key in execution_time_dict:
        table_1_columns.append(
            {'header': str(operation_key), 'format': _format}
        )

    table_1_options = {'data': time_values_table, 'columns': table_1_columns}
    row_to_show = 'B' + str(row_index) + ':F' + str((row_index + 166))
    row_index += 8
    worksheet.add_table(row_to_show, table_1_options)

    workbook.close()


if __name__ == '__main__':
    execution_time_dict = create_dicts()
    exec_times_file = read_exec_times()
    execution_time_dict = calculate_avg(exec_times_file, execution_time_dict)
    create_tables(execution_time_dict)
