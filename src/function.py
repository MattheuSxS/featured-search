# Funções extras para cálculos.
from decimal import Decimal, ROUND_HALF_UP
from datetime import time, date

def columns_type() -> dict:

    mandatory = \
        dict(
            Praca=str,
            Programas=str,
            Nivel= str,
            Data=date,
            Diadasemana=str,
            Tdur=time,
            Ini=time,
            Fim=time,
            RAT=float,
            SHR=float
            )

    return mandatory


def hours_to_minutes(hour:str) -> float:  # Pega o campo hora e transforma em segundos.
    assert isinstance(hour, str), \
        f"Expected argument ['hour'] is {str}."
    minutes = sum(int(number) * 60**index for index, number in enumerate(hour.split(":")[::-1]))
    return minutes/1440


def rounding(number:float) -> int:  # Faz uma arredondamento preciso exp: 0.5 ou 0.50 = 1 | 0.49 = 0
    assert isinstance(number, float), \
        f"Expected argument ['number'] is {float}."
    result = int(Decimal(number).quantize(0, ROUND_HALF_UP))
    return result


def columns_list() -> list:
    columns = list(['Praça', 'Programas', 'Data_D-1', 'Tdur', 'Ini', 'Fim', 'RAT', 'SHR', '|',
                    'Posição', 'Repetição', 'Qtd_Exibicoes', 'MédiaDoAno', '+pts_%', 'RecordeAno',
                    'Qtd_Vezes', 'Data', '||', 'PosiçãoDiaSemana', 'RepetiçãoDiaSemana',
                    'MediaDiaSemana', 'DS_pts_%', '|||', 'RecordAbsoluto'])
    return columns
