# Вы можете свободно менять параметры модели
config = {
    "random_state": 42,
    "catboost_regressor": {
        "iterations": 1500,
        "learning_rate": 0.1,
        "depth": 8,
        "loss_function": 'MAE',
        "cat_features": ['intake_type', 'sex_upon_intake', 'intake_condition', 'first_breed',
                                                    'second_breed', 'first_color', 'second_color', 'animal_type']
    },
    "catboost_classifier": {
        "iterations": 500,
        "learning_rate": 0.1,
        "depth": 6,
        "eval_metric": 'F1',
        "cat_features": ['intake_type', 'sex_upon_intake', 'intake_condition', 'first_breed',
                                                    'second_breed', 'first_color', 'second_color', 'animal_type']
    }
}


