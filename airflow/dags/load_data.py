import pandas as pd
import requests
import io


# Загрузка данных с источника
def load_from_api(url: str, name: str):
    limit = 1000
    offset = 0
    all_data = []

    while True:
        params = {'$limit': limit, '$offset': offset}
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = pd.read_csv(io.StringIO(response.text))
            all_data.append(data)

            if len(data) < limit:
                break
            else:
                offset += limit
        else:
            print('Ошибка при получении данных')
            break
    input_data = pd.concat(all_data, ignore_index=True)
    input_data.to_csv('/app/data/' + name, index=False)


def load_data():
    load_from_api('https://data.austintexas.gov/resource/wter-evkm.csv', 'input_data.csv')
    load_from_api('https://data.austintexas.gov/resource/9t4d-g238.csv', 'outcome_data.csv')


