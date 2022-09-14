# from time import strptime
from pandas import DataFrame
from datetime import datetime

def _validate(typeof, value, valid: list, argument: str) -> None:
    assert isinstance(value, typeof), \
        f"Expected argument ['{argument}'] is {typeof}."
    assert value in valid, f"Invalid {argument}: [{value}]. Valid arguments: {valid}."


def check_day_list(data:DataFrame) -> None:
    valid = ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo']
    day_list = set(data.get('Diadasemana'))
    for resource in day_list:
        _validate(str, resource, valid, 'Diadasemana')


def check_date(data:DataFrame) -> None:
    data_format = "%Y-%m-%d"
    date_list = list(set(data.get('Data')))

    for date in date_list:
        assert(bool(datetime.strptime(str(date.strftime('%Y-%m-%d')), data_format))), \
            f'Date does not match format: {"%Y-%m-%d"}'


def is_valid_file(data:DataFrame) -> bool:
    check_day_list(data)
    check_date(data)

    return True