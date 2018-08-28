from extract import parse_bill
import os
import sys
import matplotlib.pyplot as plt
import requests
import pickle
from gmplot import gmplot

hour_colors = {
    0: '#2E3291',
    1: '#0353A4',
    2: '#0072BA',
    3: '#038FD5',
    4: '#01ACEF',
    5: '#00ABC5',
    6: '#00A89E',
    7: '#00A674',
    8: '#03A652',
    9: '#3AB54A',
    10: '#8DC53E',
    11: '#CADB2A',
    12: '#FEF106',
    13: '#FFC211',
    14: '#F7941C',
    15: '#F36522',
    16: '#ED1B25',
    17: '#ED1841',
    18: '#ED145B',
    19: '#EC0874',
    20: '#ED008C',
    21: '#BC1A8C',
    22: '#92278F',
    23: '#662E91'
}


def get_metas(path):
    metas = []
    for file in os.listdir(path):
        if not file.endswith('.pdf'):
            continue

        meta = parse_bill(path + file)
        metas.append(meta)
    return metas


def get_lat_lng_from_google(address):
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {
        'sensor': 'false',
        'address': address,
        'key': os.getenv('GMAPS_API_KEY')
    }
    r = requests.get(url, params=params)
    results = r.json()['results']
    location = results[0]['geometry']['location']
    return location['lat'], location['lng']


def add_coordinates(metas):
    for i, meta in enumerate(metas):
        if 'from' in meta:
            meta['from_coords'] = get_lat_lng_from_google(meta['from'])
        else:
            print('from missing in')
            print(meta)
        if 'to' in meta:
            meta['to_coords'] = get_lat_lng_from_google(meta['to'])
        else:
            print('to missing in')
            print(meta)
        print('adding meta to %d of %d' % (i+1, len(metas)))
    return metas


def plot_time_frequency(metas):
    times = [meta['time'].hour for meta in metas]
    plt.hist(times, range(25))
    plt.xticks(range(24))
    plt.xlabel('Time of day')
    plt.ylabel('Frequency')
    plt.show()



def main(path):
    if os.path.exists('metas.pkl'):
        with open('metas.pkl', 'rb') as file:
            metas = pickle.load(file)
    else:
        metas = get_metas(path)
        metas = add_coordinates(metas)
        with open('metas.pkl', 'wb') as file:
            pickle.dump(metas, file)

    all_lats = []
    all_lngs = []

    route_map = gmplot.GoogleMapPlotter(52.5200, 13.4050, 13)
    for meta in metas:
        if 'from_coords' not in meta or 'to_coords' not in meta:
            continue
        from_lat, from_lng = meta['from_coords']
        to_lat, to_lng = meta['to_coords']
        hour = meta['time'].hour
        route_map.plot([from_lat, to_lat], [from_lng, to_lng], color=hour_colors[hour], edge_width=2.0)

        all_lats.append(from_lat)
        all_lats.append(to_lat)
        all_lngs.append(from_lng)
        all_lngs.append(to_lng)
    route_map.heatmap(all_lats, all_lngs, threshold=1, radius=50, opacity=0.9)
    route_map.draw('route_map.html')


    print(sum(meta['price'] for meta in metas))



if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Not enough arguments. Please specify path with the mytaxi receipts.')
    path = sys.argv[1]
    main(path)


