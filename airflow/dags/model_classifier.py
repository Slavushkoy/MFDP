from catboost import CatBoostClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, classification_report
from joblib import dump
from config import config
from clearml import Task
import pandas as pd


# Разделение на тест и трейн
def splitter(data_class, target_class):
    # Разделение данных на признаки (X) и целевую переменную (y)
    X = data_class.drop(['adopt_in_year', 'adopt_in_quarter', 'adopt_in_month'], axis=1)
    y = data_class[target_class]

    # Разделение данных на обучающий и тестовый наборы
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=config["random_state"])

    # Балансировка классов
    # Объединение обучающих данных
    train_data = pd.concat([X_train, y_train], axis=1)

    # Подсчет количества значений в целевой переменной
    counts = train_data[target_class].value_counts()

    # Находим класс с меньшим количеством значений
    minority_class = counts.idxmin()
    majority_class = 1 - minority_class  # Определяем преобладающий класс

    # Определяем количество строк для удаления из преобладающего класса
    num_to_remove = counts.loc[majority_class] - counts.loc[minority_class]

    # Удаляем лишние строки из преобладающего класса
    train_data_balanced = train_data.drop(
        train_data[train_data[target_class] == majority_class].sample(n=num_to_remove,
                                                                      random_state=config["random_state"]).index)

    # Разделяем данные на обновленные признаки и целевую переменную
    X_train = train_data_balanced.drop(target_class, axis=1)
    y_train = train_data_balanced[target_class]
    return X_train, X_test, y_train, y_test


# Создание и обучение модели CatBoost с категориальными признаками
def learn(X_train, X_test, y_train, y_test):
    model = CatBoostClassifier(iterations=config["catboost_classifier"]["iterations"],
                                          learning_rate=config["catboost_classifier"]["learning_rate"],
                                          depth=config["catboost_classifier"]["depth"],
                                          eval_metric=config["catboost_classifier"]["eval_metric"],
                                          cat_features=config["catboost_classifier"]["cat_features"])
    model.fit(X_train, y_train, eval_set=(X_test, y_test), verbose=False)
    return model


# Оценка и логирование результатов
def get_result(y_pred, y_test, target_class):
    report = classification_report(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)

    test_results = {'F1': f1}

    # CLEARML
    task = Task.init(project_name='MFDP', task_name='catboost_classifier' + target_class)
    task.connect(config["catboost_classifier"])
    logger = task.get_logger()
    logger.report_text("Classification Report:", report)
    logger.report_single_value(name='F1', value=f1)
    task.close()

    return test_results


def learn_model_classifier(target_classes: list) -> None:
    for target_class in target_classes:
        # Загрузка данных
        data_class = pd.read_csv('/app/data/data_class.csv')

        # Разделение на тест и трейн
        X_train, X_test, y_train, y_test = splitter(data_class, target_class)

        # Создание и обучение модели CatBoost с категориальными признаками
        model = learn(X_train, X_test, y_train, y_test)

        # Предсказание на тестовом наборе данных
        y_pred = model.predict(X_test)

        # Оценка и логирование результатов
        test_results = get_result(y_pred, y_test, target_class)

        # Сравниваем результаты с действующией моделью
        try:
            old_f1 = pd.read_csv('/app/data/model_classifier_' + target_class + '_result.csv')
            if old_f1['F1'][0] > test_results['F1']:
                result = pd.DataFrame([test_results], index=['Metrics'])
                result.to_csv('/app/data/model_classifier_' + target_class + '_result.csv')
                dump(model, '/app/ml_models/model_classifier' + target_class)
                return 'load_data_to_db'
            else:
                return 'task_to_skip'
        except FileNotFoundError:
            result = pd.DataFrame([test_results], index=['Metrics'])
            result.to_csv('/app/data/model_classifier_' + target_class + '_result.csv')
            dump(model, '/app/ml_models/model_classifier_' + target_class)

