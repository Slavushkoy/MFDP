import pandas as pd
import re


def convert_to_days(interval):
    match = re.search(r'\d+', interval)
    if match:
        num = int(match.group())
        if 'years' in interval:
            return num * 365
        elif 'months' in interval:
            return num * 30
        elif 'weeks' in interval:
            return num * 7
        elif 'days' in interval:
            return num
    return 0


def transform_data():
    input_data = pd.read_csv('/app/data/input_data.csv')
    outcome_data = pd.read_csv('/app/data/outcome_data.csv')

    # Заменям имя на признак наличия имения у животного
    input_data['name'] = input_data['name'].isnull().astype(int)

    # Удаляем пропуски и некорректно введенные значения
    input_data.dropna(subset=['sex_upon_intake'], inplace=True)
    input_data.dropna(subset=['age_upon_intake'], inplace=True)
    input_data = input_data[~input_data['age_upon_intake'].str.contains('-')]

    # Преобразование значений в дни в исходном датасете
    input_data['age_upon_intake'] = input_data['age_upon_intake'].apply(convert_to_days)

    # Преобразования столбца color
    input_data['mixed_color'] = input_data['color'].apply(lambda x: 1 if isinstance(x, str) and '/' in x else 0)

    input_data['first_color'] = input_data['color'].str.split('/').str[0]
    input_data['second_color'] = input_data['color'].str.split('/').apply(lambda x: x[1] if len(x) > 1 else 'NOT')
    input_data = input_data.drop('color', axis=1)

    # Преобразования столбца breed
    input_data['mixed_breed'] = input_data['breed'].apply(lambda x: 1 if ('Mix' in x) or ('/' in x) else 0)
    input_data['breed'] = input_data['breed'].str.replace(' Mix', '')
    input_data['first_breed'] = input_data['breed'].str.split('/').str[0]
    input_data['second_breed'] = input_data['breed'].str.split('/').apply(lambda x: x[1] if len(x) > 1 else 'NOT')
    input_data = input_data.drop('breed', axis=1)
    input_data.drop('datetime2', axis=1, inplace=True)
    input_data.drop('found_location', axis=1, inplace=True)

    # Объединяем входные и выходные данные
    df = pd.merge(input_data[(input_data['intake_type'] != 'Euthanasia Request') & (
                (input_data['animal_type'] == 'Dog') | (input_data['animal_type'] == 'Cat') | (
                    input_data['animal_type'] == 'Bird'))], outcome_data[['animal_id', 'datetime', 'outcome_type']], on='animal_id',
                   how='inner')

    # Вычисляем длительность пребывания животного в приюте
    df['datetime_y'] = pd.to_datetime(df['datetime_y'])
    df['datetime_x'] = pd.to_datetime(df['datetime_x'])
    df['days_in_shelter'] = (df['datetime_y'] - df['datetime_x']).dt.days

    # Удаляем дату убытия/прибытия и айди животного
    df.drop('datetime_y', axis=1, inplace=True)
    df.drop('animal_id', axis=1, inplace=True)
    df.drop('datetime_x', axis=1, inplace=True)

    # Удаление строк с отрицательными значениями в столбце "days_in_shelter"
    df = df[df['days_in_shelter'] > 0]

    # Очищаем данные от выбросов
    df_cleaned = pd.DataFrame()

    # Группировка данных по типу животного
    grouped_data = df.groupby('animal_type')

    # Удаление выбросов для каждой категории животного отдельно
    for animal_type, data in grouped_data:
        Q1 = data['days_in_shelter'].quantile(0.25)
        Q3 = data['days_in_shelter'].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        data_cleaned = data[(data['days_in_shelter'] >= lower_bound) & (data['days_in_shelter'] <= upper_bound)]
        df_cleaned = pd.concat([df_cleaned, data_cleaned])

    df = df_cleaned.copy()
    df.drop(columns=['outcome_type'], inplace=False).to_csv('/app/data/' + 'data_reg.csv', index=False)

    df = df[df.outcome_type == 'Adoption']

    # Формируем таргеты для задачи классификации, признак передачи в семью в течении месяца/квартала/года
    df['adopt_in_month'] = ((df['days_in_shelter'] <= 30)).astype(int)
    df['adopt_in_quarter'] = ((df['days_in_shelter'] <= 90)).astype(int)
    df['adopt_in_year'] = ((df['days_in_shelter'] <= 365)).astype(int)

    df = df.drop(['days_in_shelter','outcome_type'], axis=1)
    df.to_csv('/app/data/' + 'data_class.csv', index=False)



