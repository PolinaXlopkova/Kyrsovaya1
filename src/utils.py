import json
from datetime import datetime
import pandas as pd
import logging

def process_date(date_time_str):
    # Преобразование строки в объект datetime
    dt = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')

    # Пример использования pandas для обработки данных
    df = pd.DataFrame({'datetime': [dt]})
    result = df.to_dict(orient='records')

    return json.dumps(result)

def process_data(dataframe: pd.DataFrame):
    events = []
    for index, row in dataframe.iterrows():
        event = {
            "id": row['id'],
            "name": row['name'],
            "date": row['date'].strftime("%Y-%m-%d"),
            "location": row['location']
        }
        events.append(event)
    return events