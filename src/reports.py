import pandas as pd
import json
import logging
from datetime import datetime, timedelta

# Настройка логирования
logging.basicConfig(level=logging.INFO)


def expenses_by_category(df: pd.DataFrame, category: str, date: str) -> str:
    try:
        # Преобразуем строку даты в объект datetime
        date = datetime.strptime(date, '%Y-%m-%d')

        # Определяем начальную и конечную даты трехмесячного периода
        start_date = date - timedelta(days=90)
        end_date = date

        # Фильтруем данные по категории и дате
        filtered_df = df[(df['category'] == category) &
                         (df['date'] >= start_date) &
                         (df['date'] <= end_date)]

        # Группируем по дате и суммируем расходы
        result = filtered_df.groupby(filtered_df['date'].dt.date)['amount'].sum().reset_index()

        # Преобразуем результат в JSON
        json_result = result.to_json(orient='records')

        logging.info("Отчет по категории '%s' успешно создан.", category)
        return json_result

    except Exception as e:
        logging.error("Ошибка при создании отчета: %s", e)
        return json.dumps({"error": str(e)})


# Настройка логирования
logging.basicConfig(level=logging.INFO)


def report_expenses_by_weekday(dataframe, date=None):
    """
    Функция отчета «Траты по дням недели».

    :param dataframe: DataFrame с данными о тратах
    :param date: Дата для анализа (по умолчанию - текущая дата)
    :return: JSON-ответ с тратами по дням недели
    """
    if date is None:
        date = datetime.now()

    # Преобразуем дату в формат, нужный для фильтрации
    start_date = date.replace(hour=0, minute=0, second=0, microsecond=0)
    end_date = start_date + pd.Timedelta(days=7)

    # Фильтруем данные по дате
    filtered_data = dataframe[(dataframe['date'] >= start_date) & (dataframe['date'] < end_date)]

    # Группируем данные по дням недели и суммируем траты
    expenses_by_weekday = filtered_data.groupby(filtered_data['date'].dt.day_name()).sum()['amount']

    # Преобразуем результат в JSON
    result = expenses_by_weekday.to_json()

    # Логируем информацию
    logging.info(f'Отчет по тратам за неделю: {result}')

    return json.loads(result)

    # Настройка логирования


logging.basicConfig(level=logging.INFO)


def report_expenses(df, category, reference_date):
    try:
        # Преобразуем строку даты в объект datetime
        reference_date = datetime.strptime(reference_date, '%Y-%m-%d')

        # Определяем начало и конец трехмесячного периода
        start_date = reference_date - timedelta(days=90)
        end_date = reference_date

        # Фильтруем данные по категории и дате
        filtered_df = df[(df['category'] == category) &
                         (df['date'] >= start_date) &
                         (df['date'] <= end_date)]

        # Группируем данные по рабочим и выходным дням
        filtered_df['is_weekend'] = filtered_df['date'].dt.weekday >= 5
        expenses_summary = filtered_df.groupby('is_weekend')['amount'].sum().to_dict()

        # Формируем JSON-ответ
        response = {
            'category': category,
            'expenses': expenses_summary,
            'reference_date': reference_date.strftime('%Y-%m-%d')
        }

        logging.info('Отчет успешно сгенерирован')
        return json.dumps(response)

    except Exception as e:
        logging.error(f'Ошибка при генерации отчета: {e}')
        return json.dumps({'error': str(e)})