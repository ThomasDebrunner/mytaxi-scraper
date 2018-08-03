from extract import parse_bill
import os
import sys
import matplotlib.pyplot as plt


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

    times = [meta['time'].hour for meta in metas]
    plt.hist(times, range(25))
    plt.xticks(range(24))
    plt.xlabel('Time of day')
    plt.ylabel('Frequency')
    plt.show()

    print(sum(meta['price'] for meta in metas))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Not enough arguments. Please specify path with the mytaxi receipts.')
    path = sys.argv[1]
    main(path)
