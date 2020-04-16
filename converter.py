import tabula
from csv import DictReader


def pdf_to_csv(file):
    csv_file_name = file[:-4] + '.csv'
    table = tabula.read_pdf(file, pages='all')
    tabula.convert_into(file, csv_file_name, pages='all')
    return csv_file_name


def csv_to_dict(file):
    reader = DictReader(open(file))
    dict_list = []
    for line in reader:
        dict_list.append(line)
    return dict_list


possible_comma_strings = [','*10, ','*9, ','*8, ','*7, ','*6, ','*5, ','*4, ','*3, ','*2, ',']
