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


def dict_to_html(input_dict):
    table_head = '<tr>'
    for key in input_dict[0].keys():
        table_head += '<th>' + str(key) + '</th>'
    table_head += '</tr>'

    table_data = ''               
    for row_dict in input_dict:
        table_data += '<tr>'
        for key in row_dict.keys():
            table_data += "<td>"  + str(row_dict[key]) + "</td>"
        table_data += '</tr>'

    return "<table border=1>" + table_head + table_data + "</table>"