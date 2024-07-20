from catboost import CatBoostRegressor
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error
from joblib import dump
from config import config
from clearml import Task
import pandas as pd


# Разделение на тест и трейн
def splitter(data_reg):
    # Разделение данных на признаки (X) и целевую переменную (y)
    X = data_reg.drop('days_in_shelter', axis=1)
    y = data_reg['days_in_shelter']

    # Разделение данных на обучающий и тестовый наборы
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=config["random_state"])

    return X_train, X_test, y_train, y_test


def learn(X_train, y_train):
    model_regress = CatBoostRegressor(iterations=config["catboost_regressor"]["iterations"],
                                      learning_rate=config["catboost_regressor"]["learning_rate"],
                                      depth=config["catboost_regressor"]["depth"],
                                      loss_function=config["catboost_regressor"]["loss_function"],
                                      cat_features=config["catboost_regressor"]["cat_features"])
    model_regress.fit(X_train, y_train)
    return model_regress


# Оцениваем метрики получившейся модели
def get_result(predictions, y_test):

    # Оценка MAE
    mae = mean_absolute_error(y_test, predictions)

    # Оценка MSE
    mse = mean_squared_error(y_test, predictions)

    # Расчет MAPE
    mape = np.mean(np.abs((y_test - predictions) / y_test)) * 100

    test_results = {'MAE': mae,
                    'MSE': mse,
                    'MAPE': mape}

    # CLEARML
    task = Task.init(project_name='MFDP', task_name='catboost_regressor')
    task.connect(config["catboost_regressor"])
    logger = task.get_logger()
    logger.report_single_value(name='MAE', value=mae)
    logger.report_single_value(name='MSE', value=mse)
    logger.report_single_value(name='MAPE', value=mape)
    task.close()
    return test_results


def learn_model_regressor() -> None:
    # Загрузка данных
    data_reg = pd.read_csv('/app/data/data_reg.csv')

    # Разделение данных на обучающий и тестовый наборы
    X_train, X_test, y_train, y_test = splitter(data_reg)

    # Создание и обучение модели CatBoost с категориальными признаками
    model_regress = learn(X_train, y_train)

    # Прогнозирование на тестовом наборе данных
    predictions = model_regress.predict(X_test)

    # Оцениваем метрики получившейся модели
    test_results = get_result(predictions, y_test)

    # Сравниваем результаты с действующией моделью
    try:
        old_mae = pd.read_csv('/app/data/model_regressor_result.csv')
        if old_mae['MAE'][0] > test_results['MAE']:
            result = pd.DataFrame([test_results], index=['Metrics'])
            result.to_csv('/app/data/model_regressor_result.csv')
            dump(model_regress, '/app/ml_models/model_regressor')
    except FileNotFoundError:
        result = pd.DataFrame([test_results], index=['Metrics'])
        result.to_csv('/app/data/model_regressor_result.csv')
        dump(model_regress, '/app/ml_models/model_regressor')








