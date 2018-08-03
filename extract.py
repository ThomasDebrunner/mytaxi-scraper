from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO


def convert_pdf_to_txt(path):
    resource_manager = PDFResourceManager()
    return_string = StringIO()
    codec = 'utf-8'
    la_params = LAParams()
    device = TextConverter(resource_manager, return_string, codec=codec, laparams=la_params)
    interpreter = PDFPageInterpreter(resource_manager, device)

    with open(path, 'rb') as file:
        for page in PDFPage.get_pages(file, caching=True, check_extractable=True):
            interpreter.process_page(page)

    text = return_string.getvalue()

    device.close()
    return_string.close()
    return text


def main():
    text = convert_pdf_to_txt('taxi-bill.pdf')
    print(text)


if __name__ == '__main__':
    main()
