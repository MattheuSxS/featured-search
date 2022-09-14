import xlsxwriter
from pandas import DataFrame


def first_page(workbook, result:DataFrame, sheet:str, column_cell_format, line_cell_format) -> None:

        worksheet = workbook.add_worksheet(sheet)

        # Defini o tamanho da coluna.
        worksheet.set_column('A:A', 5)  # A
        worksheet.set_column_pixels(1, 1, 200)  # B
        worksheet.set_column_pixels(2, 2, 100)  # C
        worksheet.set_column_pixels(3, 3, 60)  # D
        worksheet.set_column_pixels(4, 4, 57)  # E
        worksheet.set_column_pixels(5, 5, 57)  # F
        worksheet.set_column_pixels(6, 6, 40)  # G
        worksheet.set_column_pixels(7, 7, 40)  # H
        worksheet.set_column_pixels(8, 8, 15)  # I
        worksheet.set_column_pixels(9, 9, 55)  # J
        worksheet.set_column_pixels(10, 10, 70)  # K
        worksheet.set_column_pixels(11, 11, 98)  # L
        worksheet.set_column_pixels(12, 12, 90)  # M
        worksheet.set_column_pixels(13, 13, 85)  # N
        worksheet.set_column_pixels(14, 14, 85)  # O
        worksheet.set_column_pixels(15, 15, 75)  # P
        worksheet.set_column_pixels(16, 16, 104)  # Q
        worksheet.set_column_pixels(17, 17, 15)  # R
        worksheet.set_column_pixels(18, 18, 125)  # S
        worksheet.set_column_pixels(19, 19, 140)  # T
        worksheet.set_column_pixels(20, 20, 120)  # U
        worksheet.set_column_pixels(21, 21, 80)  # V
        worksheet.set_column_pixels(22, 22, 15)  # W
        worksheet.set_column_pixels(23, 23, 108)  # X

        # Add a format. Light red fill with dark red text.
        first_format = workbook.add_format(
            dict(
                bg_color= '#b7dee8',
                font_color= '#000000'
                )
            )

        second_format = workbook.add_format(
            dict(
                bg_color= '#f2f2f2',
                font_color= '#000000'
                )
            )

        third_format = workbook.add_format(
            dict(
                bg_color= '#d9d9d9',
                font_color= '#000000'
                )
            )

        # Some sample data to run the conditional formatting against.
        data = result.values.tolist()

        for index in range(len(result.columns)):
            worksheet.write(0, index, result.columns[index], column_cell_format)

        for row, row_data in enumerate(data):
            worksheet.write_row(row + 1, 0, row_data, line_cell_format)

        cell_number = len(result) + 1
        # Função de core na Cell.
        worksheet.conditional_format(f'K1:Q{cell_number}', dict(type= 'cell', criteria= '!=',
                                                                value= '999', format= second_format))

        worksheet.conditional_format(f'T1:V{cell_number}', dict(type= 'cell', criteria= '!=',
                                                                value= '999', format= third_format))

        worksheet.conditional_format(f'X1:X{cell_number}', dict(type= 'cell', criteria= '!=',
                                                                value= '999', format= third_format))

        worksheet.conditional_format(f'J1:J{cell_number}', dict(type= 'cell', criteria= '==',
                                                                value= 1, format= first_format))

        worksheet.conditional_format(f'J1:J{cell_number}', dict(type= 'cell', criteria= '!=',
                                                                value= 1, format= second_format))

        worksheet.conditional_format(f'S1:S{cell_number}', dict(type= 'cell', criteria= '==',
                                                                value= 1, format= first_format))

        worksheet.conditional_format(f'S1:S{cell_number}', dict(type= 'cell', criteria= '!=',
                                                                value= 1, format= third_format))

        # Escrita em acima da marca.
        caption = 'Macro Luna | Marca & Comunicação | Pesquisa & Conhecimento'
        worksheet.write(f'A{cell_number + 3}', caption)

        # Imagem Marca
        linkimage = './icones/logo_macro.png'

        worksheet.insert_image(f'A{cell_number + 4}', linkimage)

        # Congela o cabeçalho e as 10 primeiras linhas.
        worksheet.freeze_panes(1, 8)

        # Tira a linha de grade
        worksheet.hide_gridlines(2)


def second_page(workbook, result:DataFrame, sheet:str, column_cell_format, line_cell_format) -> None:
    worksheet = workbook.add_worksheet(sheet)

    # Transforma o DataFrame em uma lista.
    data = result[['Praca', 'Programas', 'Nivel', 'Data', 'Diadasemana',
               'Tdur', 'Ini', 'Fim', 'RAT', 'SHR']].values.tolist()

    # Escreve no arquivo excel. (Coluna)
    for index in range(0, len(result.columns) - 7):
        worksheet.write(0, index, result.columns[index], column_cell_format)

    # Escreve no arquivo excel. (Linhas)
    for row, row_data in enumerate(data):
        worksheet.write_row(row + 1, 0, row_data, line_cell_format)

    # Configura o tamanho de cada coluna.
    worksheet.set_column('A:A', 5)  # A
    worksheet.set_column_pixels(1, 1, 255)  # B
    worksheet.set_column_pixels(2, 2, 40)  # C
    worksheet.set_column_pixels(3, 3, 75)  # D
    worksheet.set_column_pixels(4, 4, 95)  # E
    worksheet.set_column_pixels(5, 5, 60)  # F
    worksheet.set_column_pixels(6, 6, 60)  # G
    worksheet.set_column_pixels(7, 7, 60)  # H
    worksheet.set_column_pixels(8, 8, 70)  # I
    worksheet.set_column_pixels(9, 9, 70)  # J

    # Tira a linha de grade
    worksheet.hide_gridlines(2)


def whiter_excel(file_name:str, rat_result:DataFrame, shr_result:DataFrame, data:DataFrame) -> None:

    workbook = xlsxwriter.Workbook(file_name)

    # Centraliza os dados da coluna ( Coluna )
    column_cell_format = workbook.add_format(dict(bold= True, font_color= 'black', border= 1))
    column_cell_format.set_align('center')
    column_cell_format.set_align('vcenter')

    # Centraliza os dados da coluna ( linha )
    line_cell_format = workbook.add_format()
    line_cell_format.set_align('center')
    line_cell_format.set_align('vcenter')

    # Cria o arquivo excel com o sheet já nomeada.
    first_page(workbook, rat_result, 'Aud', column_cell_format, line_cell_format)
    first_page(workbook, shr_result, 'Shr', column_cell_format, line_cell_format)
    second_page(workbook, data, 'Dados', column_cell_format, line_cell_format)

    # close the excel
    workbook.close()