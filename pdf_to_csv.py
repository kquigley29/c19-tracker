import tabula

def pdf_to_csv(file_name):

    file = file_name

    table = tabula.read_pdf(file, pages='all')

    tabula.convert_into(file, file_name[:-4]+'.csv', pages='all')


if __name__ == "__main__":
    file_to_convert = input("File name: ")
    pdf_to_csv(file_to_convert)
