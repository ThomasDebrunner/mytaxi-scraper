import sys
from extract import parse_bill
import os
import json

from datetime import date, time


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (time, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


def get_metas(path):
    metas = []
    for file in os.listdir(path):
        if not file.endswith('.pdf'):
            continue

        meta = parse_bill(path + file)
        metas.append(meta)
    return metas


def main(path):
    metas = get_metas(path)
    with open('metadata.json', 'w') as file:
        json.dump(metas, file, default=json_serial, indent=4)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Not enough arguments. Please specify path with the mytaxi receipts.')
    path = sys.argv[1]
    main(path)
