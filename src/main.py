from PySimpleGUI import PySimpleGUI as Sg
from back_end import rat_shr_result as result
from back_end import excel_result as excel
from back_end import read_file
from pandas import read_excel
import tkinter as tk
from tkinter import filedialog
import logging
import re
import os


logging.basicConfig(
    format='%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s', level='INFO')


def number_days() -> Sg:
    Sg.theme('Reddit')

    layout = [
        [Sg.Text('Quantidade de dias? '), Sg.Combo(values=list(
            range(1, 11)), key='nday', default_value=1, size=(3, 1))],
        [Sg.Button('Enviar'), Sg.Button('Sair')],
    ]
    return Sg.Window('Macro Luna \\(o.O)/', layout=layout, finalize=True, size=(275, 70))


def path() -> str:
    result = filedialog.askdirectory(parent=root, initialdir="/", title ='select output folder')

    return result


def main(day:int) -> None:

    try:
        input_path = path()
        output_path = path()
    except:
        raise Exception (f'Invalid directory!')

    configs_path = os.path.join(os.getcwd(), input_path)
    files = os.listdir(configs_path)

    for filename in files:
        if re.search(".xlsx$", filename):
            logging.info(f"ready for validation file: {filename}")

            path_name = os.path.join(configs_path, filename)
            data = read_excel(path_name, parse_dates=True)
            data_ = read_file(data)

            rat_result = result(day, 'rat', data_)
            shr_result = result(day, 'shr', data_)
            excel(data_, rat_result, shr_result, output_path)

            logging.info(f"report generated successfully for: {filename}")

            del data, data_


root = tk.Tk()
root.withdraw()


if __name__ == "__main__":
    # Criar as janelas inicias
    number_days = number_days()

    # Criar um loop de leitura de eventos
    while True:
        window, event, values = Sg.read_all_windows()
        # Quando janela for fechada
        if window == number_days and (event == Sg.WINDOW_CLOSED or event == 'Sair'):
            break

        if window == number_days and event == 'Enviar':
            number_days.hide()
            day = int(values['nday'])
            main(day)
            option = Sg.popup('Todos os arquivos foram gerados com sucesso!')
            break