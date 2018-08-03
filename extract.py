from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from datetime import date, time
from io import StringIO
import re


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


def parse_text(text):
    # Split by newline
    splits = text.split('\n')

    # filter empty lines
    splits = [split for split in splits if split.strip() != '']
    # for split in splits:
    #     print('"' + split + '"')

    from_r = re.compile('^von: (.*)$')
    to_r = re.compile('^nach: (.*)$')
    date_r = re.compile('^(\d\d).(\d\d).(\d\d) (\d\d):(\d\d)$')
    price_r = re.compile('^(\d+),(\d+) €$')

    meta_data = {}
    for i, split in enumerate(splits):

        # id
        if 'mytaxi ID' in split and len(splits) > i+1:
            meta_data['id'] = splits[i+1]

        # from
        if from_r.match(split):
            m = from_r.search(split)
            meta_data['from'] = m.group(1)

        # to
        if to_r.match(split):
            m = to_r.search(split)
            meta_data['to'] = m.group(1)

        # date/time
        if date_r.match(split):
            m = date_r.search(split)
            meta_data['date'] = date(2000 + int(m.group(3)), int(m.group(2)), int(m.group(1)))
            meta_data['time'] = time(int(m.group(4)), int(m.group(5)))

        # price
        if price_r.match(split):
            m = price_r.search(split)
            price = float(m.group(1)) + float(m.group(2))/100
            if 'prices' in meta_data:
                meta_data['prices'].append(price)
            else:
                meta_data['prices'] = [price]

    if 'prices' in meta_data:
        meta_data['price'] = max(meta_data['prices'])

    return meta_data


def parse_bill(filename):
    text = convert_pdf_to_txt(filename)
    return parse_text(text)
