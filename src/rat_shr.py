from pandas import DataFrame, concat
from numpy import array
from function import hours_to_minutes, rounding


def annual_results(row:DataFrame, data:DataFrame, rat_duration:float, total_connected_duration_:float, variable:str) -> dict:

    count_audience_annual_duration = 0
    count_duration = 0
    rat_x_duration = 0
    greatest_ascendant = 0
    greatest_descendant = 0
    tvrxdur = 0

    for index, row_ in data.loc[(data.get('Programas') == row.get('Programas'))].iterrows():
        count_audience_annual_duration += round(row_.get(rat_duration), 7)
        count_duration += round(hours_to_minutes(row_.get('Tdur')), 7)
        rat_x_duration += round(row_.get(rat_duration), 6)
        tvrxdur += row_.get(total_connected_duration_)
        if rounding(row_.get(variable)) >= greatest_ascendant:
            greatest_ascendant = rounding(row_.get(variable))

        if row_.get(variable) >= greatest_descendant:
            greatest_descendant = row_.get(variable)

    result = \
        dict(
            count_audience_annual_duration=count_audience_annual_duration,
            count_duration=count_duration,
            rat_x_duration=rat_x_duration,
            tvrxdur=tvrxdur,
            greatest_ascendant=greatest_ascendant,
            greatest_descendant=greatest_descendant
            )

    return result


def number_records(row:DataFrame, data:DataFrame, greatest_ascendant:float, variable:str) -> dict:

    list_day_week_date = []
    number_of_times = 0

    for index, row_ in data.loc[(data.get('Programas') == row.get('Programas'))].iterrows():
        if greatest_ascendant == rounding(row_.get(variable)):
            number_of_times += 1
            day_week_date = '{} {}'.format(row_.get('Diadasemana')[:3], row_.get('Data').strftime('%d-%m-%Y'))
            list_day_week_date.append(day_week_date)

    result = \
        dict(
            list_day_week_date=list_day_week_date,
            number_of_times=number_of_times
            )

    return result


def repeated_that_position(row:DataFrame, data:DataFrame, variable:str) -> dict:

    rank = None
    repetition = 0

    program_list = list(set(array(round(data.loc[(data.get('Programas') == row.get('Programas'))][variable]))))
    program_list.sort(reverse=True)
    for program_index in program_list:
        if program_index == round(row.get(variable)):
            rank = program_list.index(program_index)  # Rankeamento
            for program_index_ in array(round(data.loc[(data.get('Programas') == row.get('Programas'))][variable])):
                if program_index_ == program_index:
                    repetition += 1

    result = \
        dict(
            rank=rank,
            repetition=repetition
        )

    return result


def get_date(list_day_week_date:list, rank:int) -> str:

    if len(list_day_week_date) == 1:
        date = list_day_week_date[0]  # data do dia
    elif len(list_day_week_date) >= 1 and (rank + 1) != 1:
        date = list_day_week_date[-1]
    else:
        date = list_day_week_date[-2]  # ultima data

    return date


def calculate_duration(row:DataFrame, data:DataFrame, rat_duration:str, total_connected_duration_:str) -> dict:

    count_duration_audience = 0
    count_weekly_duration = 0
    audience_weekly_duration = 0
    total_connected_x_duration = 0

    for index, row in data.loc[
        (data.get('Programas') == row.get('Programas')) & (data.get('Diadasemana') == row.get('Diadasemana'))].iterrows():
        count_duration_audience += round(row.get(rat_duration), 7)
        count_weekly_duration += round(hours_to_minutes(row.get('Tdur')), 7)
        audience_weekly_duration += round(row.get(rat_duration), 6)
        total_connected_x_duration += round(row.get(total_connected_duration_), 6)

    result = \
        dict(
            count_duration_audience=count_duration_audience,
            count_weekly_duration=count_weekly_duration,
            audience_weekly_duration=audience_weekly_duration,
            total_connected_x_duration=total_connected_x_duration
        )

    return result


def repeat_rank_day(row:DataFrame, data:DataFrame, variable:str) -> dict:

    rank_day = 0
    repeat_day = 0

    program_list = list(set(array(
        round(data.loc[(data.get('Programas') == row.get('Programas')) &
                       (data.get('Diadasemana') == row.get('Diadasemana'))][variable]))))

    program_list.sort(reverse=True)
    for program_index in program_list:
        if program_index == round(row.get(variable)):
            rank_day = program_list.index(program_index)
            for program_index_ in array(
                round(data.loc[(data.get('Programas') == row.get('Programas')) &
                (data.get('Diadasemana') == row.get('Diadasemana'))][variable])):
                if program_index_ == program_index:
                    repeat_day += 1

    result = \
        dict(
            rank_day=rank_day,
            repeat_day=repeat_day
        )
    return result


def calculate_averages(count_audience_annual_duration:float, count_duration:float, rat_x_duration:float,
                       tvrxdur:float, count_duration_audience:float, count_weekly_duration:float,
                       audience_weekly_duration:float, total_connected_x_duration:float) -> dict:

    annual_average = round((round(count_audience_annual_duration, 6) / round(count_duration, 6)), 6)
    annual_average_ = (rat_x_duration / tvrxdur) * 100
    weekly_average = round((round(count_duration_audience, 6) / round(count_weekly_duration, 6)), 6)
    weekly_average_ = (audience_weekly_duration / total_connected_x_duration) * 100

    result = \
        dict(
            annual_average=annual_average,
            annual_average_=annual_average_,
            weekly_average=weekly_average,
            weekly_average_=weekly_average_
            )

    return result


def annual_result(row:DataFrame, variable:str, annual_average:float) -> str:
    pts = rounding(row.get(variable)) - rounding(annual_average)
    if pts > 0:
        pts_ = (pts / int(rounding(annual_average))) * 100
        result = '{} pts (+{})%'.format(pts, rounding(pts_))
    else:
        result = ' '

    return result


def result_day_week(row:DataFrame, variable:str, weekly_average:float) -> str:
    pts = rounding(row.get(variable)) - rounding(weekly_average)
    if pts > 0:
        pts_ = (pts / int(rounding(weekly_average))) * 100
        result = '{} pts (+{})%'.format(pts, rounding(pts_))
    else:
        result = ' '

    return result


def absolute_record(row:DataFrame, variable:str, greatest_descendant:float) -> str:
    if row.get(variable) >= greatest_descendant and rounding(row.get(variable)) > 0:
        result = 'Sim'
    else:
        result = ' '

    return result


def base_rat_shr(basis_analysis:DataFrame, data:DataFrame, option:str, columns_list:list):

    empty_dataframe = DataFrame(None, columns=columns_list)

    if option == 'rat':
        rat_duration = 'AudxTDur'
        total_connected_duration_ = 'TvrxDur'
        variable = 'RAT'

    elif option == 'shr':
        rat_duration = 'AudxTDur_Shr'
        total_connected_duration_ = 'TvrxDur_Shr'
        variable = 'SHR'

    for index, row in basis_analysis.iterrows():

        # =============================== Quantidade de Exibições. ===============================#
        display_quantity = 0
        display_quantity += int(len(data.get(data.get('Programas') == row.get('Programas'))))

        # =============================== Média do ano e Recorde do Ano. ===============================#
        annual_results_ = annual_results(row, data, rat_duration, total_connected_duration_, variable)

        count_audience_annual_duration = annual_results_.get('count_audience_annual_duration')
        count_duration = annual_results_.get('count_duration')
        rat_x_duration= annual_results_.get('rat_x_duration')
        tvrxdur = annual_results_.get('tvrxdur')
        greatest_ascendant = annual_results_.get('greatest_ascendant')
        greatest_descendant = annual_results_.get('greatest_descendant')

        # =============================== Quantidade de vezes que repetiu aquele recorde. ===============================#
        number_records_ = number_records(row, data, greatest_ascendant, variable)

        list_day_week_date = number_records_.get('list_day_week_date')
        number_of_times = number_records_.get('number_of_times')

        # =============================== Quantidade de vezes que repetiu aquele posição. ===============================#
        repeated_that_position_ = repeated_that_position(row, data, variable)

        rank = repeated_that_position_.get('rank')
        repetition = repeated_that_position_.get('repetition')

        # =============================== Data da Coluna Q do Excel ( Data ). ===============================#
        date = get_date(list_day_week_date, rank)

        # =============================== Dia da Semana ===============================
        calculate_duration_ = calculate_duration(row, data, rat_duration, total_connected_duration_)

        count_duration_audience = calculate_duration_.get('count_duration_audience')
        count_weekly_duration = calculate_duration_.get('count_weekly_duration')
        audience_weekly_duration = calculate_duration_.get('audience_weekly_duration')
        total_connected_x_duration = calculate_duration_.get('total_connected_x_duration')

        repeat_rank_day_ = repeat_rank_day(row, data, variable)

        rank_day = repeat_rank_day_.get('rank_day')
        repeat_day = repeat_rank_day_.get('repeat_day')

        calculate_averages_ = calculate_averages(count_audience_annual_duration, count_duration, rat_x_duration, tvrxdur,
                       count_duration_audience, count_weekly_duration, audience_weekly_duration,total_connected_x_duration)

        annual_average = calculate_averages_.get('annual_average')
        annual_average_ = calculate_averages_.get('annual_average_')
        weekly_average = calculate_averages_.get('weekly_average')
        weekly_average_ = calculate_averages_.get('weekly_average_')

        # ================== Anual ==========================
        res = annual_result(row, variable, annual_average)

        # ================== Dia da Semana ==========================
        res_ = result_day_week(row, variable, weekly_average)

        # ================== Recorde Absoluto ========================== #
        absolute_record_ = absolute_record(row, variable, greatest_descendant)

        # ================================= Result =================================
        empty_space = ' '
        analysis_result = \
            DataFrame(
                [
                    [
                        row.get('Praca'),
                        row.get('Programas'),
                        '{} {}'.format(row.get('Diadasemana')[:3], row.get('Data').strftime('%d-%m-%Y')),
                        row.get('Tdur'),
                        row.get('Ini'),
                        row.get('Fim'),
                        row.get('RAT'),
                        row.get('SHR'),
                        empty_space,
                        int(rank + 1),
                        '{}x'.format(repetition),
                        display_quantity,
                        '{} pts ({}%)'.format(rounding(annual_average), rounding(annual_average_)),
                        res,
                        '{} pts'.format(greatest_ascendant),
                        '{}x'.format(number_of_times),
                        date,
                        empty_space,
                        int(rank_day + 1),
                        '{}x'.format(repeat_day),
                        '{} pts ({}%)'.format(rounding(weekly_average), rounding(weekly_average_)),
                        res_,
                        empty_space,
                        absolute_record_
                    ]
                ],
            columns=columns_list
        )

        empty_dataframe = concat([empty_dataframe, analysis_result])

    return empty_dataframe
