import PySimpleGUI as Sg
from pandas import DataFrame, unique
from datetime import datetime, timedelta, time
from rat_shr import base_rat_shr
from function import columns_list
from excel import whiter_excel
import re


hour_formart = '%H:%M:%S'
regex = re.compile('^([01]?[0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]$')


def rat_x_duration(tdur:str, rat_shr:float) -> float:
    assert re.search(regex, tdur), \
        f"time data {tdur} does not match format {hour_formart}."
    assert isinstance(rat_shr, float), \
        f"Expected argument {rat_shr} is {float}."
    secunds = sum(int(number) * 60**index for index, number in enumerate(tdur.split(":")[::-1]))
    return round(secunds * rat_shr, 6) / 1440


def time_conversion(timestamp:str) -> str:
    assert re.search(regex, timestamp), \
        f"time data {timestamp} does not match format {hour_formart}."
    assert isinstance(timestamp, str), \
        f"Expected argument ['timestamp'] is {str}."
    result = time(hour=int(timestamp[:2:]), minute=int(timestamp[3:5:])).isoformat(timespec='minutes')
    return result


def read_file(data:DataFrame) -> DataFrame:
    assert isinstance(data, DataFrame), \
        f"Expected argument ['data'] is {DataFrame}."

    data['Tdur'] = [time_conversion(str(data.get('Tdur')[index])) for index in range(len(data.get('Tdur')))]

    data['Ini'] = [str(data.get('Ini')[index])[11::] if len(str(data.get('Ini')[index])) == 19
                    else str(data.get('Ini')[index]) for index in range(len(data.get('Ini')))]
    data['Fim'] = [str(data.get('Fim')[index])[11::] if len(str(data.get('Fim')[index])) == 19
                    else str(data.get('Fim')[index]) for index in range(len(data.get('Fim')))]

    # Cria a coluna ano
    data['Ano'] = data.get('Data').dt.year
    # Usa a função rat_x_duration para calcular Tdur vs RAT
    data['AudxTDur'] = [rat_x_duration(data.get('Tdur')[index], data.get('RAT')[index]) for index in range(len(data.get('RAT')))]
    # Usa a função rat_x_duration para calcular Tdur vs SHR
    data['AudxTDur_Shr'] = [rat_x_duration(data.get('Tdur')[index], data.get('SHR')[index]) for index in range(len(data.get('SHR')))]
    # Cálcula ( RAT / SHR ) * 100, Para gerar o %TVR, o resultado sai com 6 casas decimais
    data['%TVR'] = round((data.get('RAT') / data.get('SHR')) * 100, 6)
    # Cálcula ( SHR / RAT ) * 100, Para gerar o %TVR, o resultado sai com 6 casas decimais
    data['%TVR_Shr'] = round((data.get('SHR') / data.get('RAT')) * 100, 6)
    # Usa a função rat_x_duration para calcular Tdur vs RAT
    data['TvrxDur'] = [rat_x_duration(data.get('Tdur')[index], data.get('%TVR')[index]) for index in range(len(data.get('RAT')))]
    # Usa a função rat_x_duration para calcular Tdur vs SHR
    data['TvrxDur_Shr'] = [rat_x_duration(data.get('Tdur')[index], data.get('%TVR_Shr')[index]) for index in range(len(data.get('SHR')))]

    return data


def base_analysis(data:DataFrame, day:int) -> DataFrame:
    before_april = '{}-04-01'.format(datetime.today().year)
    after_april = '{}-01-01'.format(datetime.today().year)

    if datetime.today().strftime('%Y-%m-%d') < before_april:
        one_year = '{}-01-01'.format(datetime.today().year - 2)
        filter_data = data.loc[data.get('Data') >= one_year]

    else:
        filter_data = data.loc[data.get('Data') >= after_april]

    number_days = (datetime.today() - timedelta(days=day)).strftime('%Y-%m-%d')
    base_analysis = filter_data.loc[filter_data.get('Data') >= number_days]

    return base_analysis


def auxiliary_function(result:DataFrame, data:DataFrame, opction:str, columns:list) -> DataFrame:
    analyzed_data = DataFrame(columns=columns)

    data_list = list(unique(result.get('Data')))
    data_list.sort()

    if opction == 'rat':
        for line in data_list:
            result_rat_shr = base_rat_shr(result.get(result.get('Data') == line), data.get(data.get('Data') <= line), 'rat', columns)
            analyzed_data = analyzed_data.append(result_rat_shr, ignore_index=True)

    elif opction == 'shr':
        for line in data_list:
            result_rat_shr = base_rat_shr(result.get(result.get('Data') == line), data.get(data.get('Data') <= line), 'shr', columns)
            analyzed_data = analyzed_data.append(result_rat_shr, ignore_index=True)

    return analyzed_data


def file_path(square:str, output_path:str) -> str:
    date = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    file_name = 'CGCOM_{}_{}.xlsx'.format(date, square)
    return '{}/{}'.format(output_path, file_name)


def rat_shr_result(day:int, option:str, data:DataFrame,) -> DataFrame:
    assert isinstance(day, int), \
        f"Expected argument ['day'] is {int}."
    assert isinstance(option, str), \
        f"Expected argument ['option'] is {str}."
    base_assists = base_analysis(data, day)
    result = auxiliary_function(base_assists, data, option, columns_list())
    return result


def excel_result(data:DataFrame, rat_result:DataFrame, shr_result:DataFrame, output_path:str) -> None:
    square = data.get('Praca').iloc[-1]
    file_name = file_path(square, output_path)
    whiter_excel(file_name, rat_result, shr_result, data)
