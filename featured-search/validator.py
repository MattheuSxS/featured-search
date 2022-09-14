import os
import logging
import argparse
from pandas import read_excel, DataFrame
from re import search
from datetime import time, date
from validates.file_test import is_valid_file


logging.basicConfig(
    format='%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s', level='INFO')


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


def check_mandatory(data:DataFrame, file_name:str, mandatory:dict) -> None:

    data_keys = data.keys()

    for key, value in mandatory.items():
        assert key in data_keys, f"{file_name}: Expected mandatory argument ['{key}'] in received args: {data_keys}."
        assert isinstance(data.get(key)[0], value), \
            f"{file_name}: Expected argument ['{key}'] is {value}."


def main(args) -> None:

    columns_ = columns_type()

    if args.check:
        configs_path = os.path.join(os.getcwd(), 'configs')

        files = os.listdir(configs_path)

        for filename in files:
            if search(".xlsx$", filename):

                logging.info(f"ready for validation file: {filename}")
                data = read_excel(os.path.join(configs_path, filename) , parse_dates=True, dtype=columns_)

                if is_valid(data, filename, columns_):
                    logging.info(f"sucessfull validation for: {filename}")

                    del data



def is_valid(data:DataFrame, file_name:str, mandatory:dict) -> bool:

    check_mandatory(data, file_name, mandatory)
    columns_type()
    is_valid_file(data)

    return True


if __name__ == '__main__':

    try:
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-c", "--check", help="execute validates for config files.", required=True, action="store_true"
        )

        args = parser.parse_args()

        main(args)

    except Exception as e:
        raise(f"Invalid .xlsx file! Error: {e}.")