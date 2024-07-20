# MFDP

Сервис по предсказанию длительности пребыания животного в приюте и передачи его в семью.

# Описание продукта

**Продукт** - веб-сайт для оценки ожидаемого срока пребывания животных в приюте. Это инструмент, который помогает работникам приюта оптимизировать процессы устройства животных, повышая их шансы на быструю адаптацию и счастливую жизнь в новом доме.

**Целевыми пользователями** продукта являются сотрудники приютов для животных, чья задача - обеспечить эффективное размещение подопечных и увеличить количество найденных семей для животных.

**Ценность продукта** заключается в предоставлении данных о сроке пребывания каждого животного в приюте, что помогает сотрудникам приюта эффективнее распределять ресурсы:
- уделять особое внимание животным, склонным к долгому нахождению в приюте, что позволит поддержать их здоровье и повысит их шансы найти семью в долгосрочной перспективе;
- для животных с коротким сроком пребывания в первую очередь проводить мероприятия, способствующие передаче в семью (фотосессии, офлайн мероприятия). Таким образом будут освобождаться места для новых животных, что повысит проходимость приюта и позволит помочь большему количеству животных.
Это позволяет сократить время пребывания животных в приюте, улучшает их благополучие и способствует росту числа животных, нашедших семью. Также это может помочь оптимизировать расходование средств приюта, что даст возможность помочь большему количеству животных.

**Взаимодействие пользователя** с продуктом осуществляется через интерфейс портала. Для ввода входных параметров о животных доступны поля с поиском и выбором значений из списков.

# План проекта

- Сбора и анализ данных. Обработка данных, выделение признаков для обучения модели. 
- Проведение экспериментов, выбор оптимальных для задачи модели и метрик качества. 
- Настройка регулярного обновления данных и дообучения модели на них.
- Создание сервиса для работы с моделью.
- Оценка результатов проекта, формирование презентации.

# Сбор и анализ данных. Обработка данных, выделение признаков для обучения модели
- На данном этапе были выполнены следующие работы:
- Обеспечена загрузка исходных данных через API сервиса;
- Проведен разведывательный анализ исходных данных;
- Сформирован итоговый датасет для обучения модели;
- Обработаны исходные признаки и выделены новые.

# Эксперименты, выбор оптимальных для задачи модели и метрик качества
- На данном этапе были выполнены следующие работы:
- Обучены базовые модели для формирования базлайна решения;
- В качестве метрик качества были рассмотрены MAE, MAPE, MSE;
- Целевой метрикой оценки выбрана MAE, т.к. является легко интерпретируемой для бизнеса;
- Обработаны результаты предсказаний базовой модели;
- Улучшен пайплайн предобработки данных;
- Проведены эксперименты по обучению разных моделей с подбором гиперпараметров;
- Обучена модель CatboostRegressor, подобраны гиперпараметры;
- Итоговая метрика MAE была улучшена с 31 до 12 дней.

# Настройка регулярного обновления данных и дообучения модели на них.
- На данном этапе была настроена работа Airflow со следующими процессами:
- Загрузка данных с источника;
- Обработка данных для обучения модели;
- Обучение модели с подобранными гиперпараметрами (логирование результатов в CLEARML);
- Сравнение результатов обучения с предыдущей моделью;
- В случае уменьшения значения MAE модели происходит сохранение новой модели в качестве рабочей.
Т.к. данные на источнике обновляются ежедневно, настроен ежедневный запуск задачи.

# Создание сервиса для работы с моделью
- На данном этапе были выполнены следующие работы:
- Реализован интерфейс приложения на Streamlit;
- Обеспечено хранение данных за счет СУБД;
- Реализован REST интерфейс для взаимодействия с сервисом;
- Реализован пользовательский интерфейс для сервиса на Streamlit;
- Сервис упакован в Docker контейнер;
- Обеспечена возможность масштабирования количества воркеров с моделью.
- Оценка результатов проекта, формирование презентации
- На данном этапе были сформированы презентация о результатах работ и текущий документ, содержащий информацию о проекте и его этапах.

