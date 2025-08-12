import json
import logging
import re
from datetime import datetime
from datetime import timedelta

# Настройка логгирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_cashback_categories(year, month, transactions):
    try:
        # Преобразование входных данных в дату
        target_date = datetime(year, month, 1)

        # Список для хранения категорий с повышенным кешбэком
        cashback_categories = {}

        # Обработка транзакций
        for transaction in transactions:
            transaction_date = datetime.strptime(transaction['date'], '%Y-%m-%d')
            if transaction_date.year == year and transaction_date.month == month:
                category = transaction['category']
                amount = transaction['amount']

                # Суммируем кешбэк по категориям
                if category in cashback_categories:
                    cashback_categories[category] += amount
                else:
                    cashback_categories[category] = amount

        # Формирование JSON-ответа
        response = {
            "year": year,
            "month": month,
            "cashback_categories": cashback_categories
        }

        logging.info("Кешбэк категории успешно обработаны")
        return json.dumps(response)

    except Exception as e:
        logging.error(f"Ошибка в обработке кешбэка: {e}")
        return json.dumps({"error": "Произошла ошибка при обработке запроса"})

def invest_piggy_bank(month: str, transactions: list, round_limit: int) -> str:
    try:
        # Преобразование месяца в формат datetime
        month_date = datetime.strptime(month, '%Y-%m')
        month_start = month_date.replace(day=1)
        month_end = month_date.replace(day=28) + timedelta(
            days=4)  # берем 4 дня для гарантии перехода на следующий месяц
        month_end = month_end - timedelta(days=month_end.day)  # последний день текущего месяца

        total_investment = 0

        for transaction in transactions:
            transaction_date = datetime.strptime(transaction['date'], '%Y-%m-%d')
            if month_start <= transaction_date <= month_end:
                total_investment += transaction['amount']

        # Округление по лимиту
        rounded_investment = round(total_investment / round_limit) * round_limit

        # Формирование JSON-ответа
        response = {
            'month': month,
            'total_investment': rounded_investment
        }

        return json.dumps(response)

    except Exception as e:
        logging.error(f"Ошибка в расчете: {e}")
        return json.dumps({'error': 'Invalid input or processing error'})

def simple_search(query, transactions):
    logger.info("Запрос на поиск: %s", query)

    # Приведение запроса к нижнему регистру для нечувствительного поиска
    query_lower = query.lower()

    # Фильтрация транзакций по запросу
    results = [
        transaction for transaction in transactions
        if query_lower in transaction.get('description', '').lower()
    ]

    # Формирование JSON-ответа
    response = {
        'query': query,
        'results': results,
        'count': len(results)
    }

    logger.info("Найдено %d результатов для запроса: %s", len(results), query)

    # Возврат ответа в формате JSON
    return json.dumps(response)

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def search_by_phone(transactions, phone_number):
    """
    Функция для поиска транзакций по телефонному номеру.

    :param transactions: Список транзакций в формате словарей
    :param phone_number: Номер телефона для поиска
    :return: JSON-ответ с найденными транзакциями
    """
    try:
        pattern = re.compile(re.escape(phone_number))
        results = [transaction for transaction in transactions if pattern.search(transaction.get('phone', ''))]

        response = {
            'status': 'success',
            'data': results
        }

        logger.info("Поиск завершен, найдено %d транзакций", len(results))
        return json.dumps(response)

    except Exception as e:
        logger.error("Ошибка при поиске: %s", e)
        return json.dumps({'status': 'error', 'message': str(e)})


# Настройка логирования
logging.basicConfig(level=logging.INFO)


def search_transfers(transactions):
    """
    Функция для поиска переводов физическим лицам.

    :param transactions: список словарей с транзакциями
    :return: JSON-ответ с результатами поиска
    """
    logging.info("Начало поиска переводов")

    results = []

    for transaction in transactions:
        # Проверка на корректность данных
        if 'name' in transaction and 'amount' in transaction:
            name = transaction['name']
            amount = transaction['amount']

            # Использование регулярного выражения для проверки имени
            if re.match(r'^[A-Za-z\s]+$', name):
                results.append({
                    'name': name,
                    'amount': amount,
                })
                logging.info(f"Добавлена транзакция: {name}, сумма: {amount}")
            else:
                logging.warning(f"Некорректное имя: {name}")
        else:
            logging.warning("Недостаточно данных в транзакции")

    # Формирование JSON-ответа
    json_response = json.dumps(results)
    logging.info("Поиск завершен")

    return json_response