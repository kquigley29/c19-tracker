import tabula
from csv import DictReader


def pdf_to_csv(input_file):
    table = tabula.read_pdf(input_file, pages='all')
    tabula.convert_into(input_file, input_file[:-4]+'.csv', pages='all')


def csv_to_dict(file):
    reader = DictReader(open(file))
    dict_list = []
    for line in reader:
        dict_list.append(line)
    return dict_list
