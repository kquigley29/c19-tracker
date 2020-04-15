import tabula
from csv import DictReader


def pdf_to_csv(file):
    csv_file_name = file[:-4] + '.csv'
    table = tabula.read_pdf(file, pages='all')
    tabula.convert_into(file, csv_file_name, pages='all')
    return csv_file_name


def new_line_correction(file):
    with open(file, 'r') as read_file:
        file_text = read_file.read()
    file_text = file_text.replace("\n", "")
    with open(file, 'w') as write_file:
        write_file.write(file_text)


def csv_to_list(file):
    with open(file, 'r') as read_file:
        csv_text = read_file.read()
    csv_entries = csv_text.split(",")
    for entry in csv_entries:
        if entry == "":
            csv_entries.remove(entry)
    return csv_entries


def csv_to_dict(file):
    reader = DictReader(open(file))
    dict_list = []
    for line in reader:
        dict_list.append(line)
    return dict_list
