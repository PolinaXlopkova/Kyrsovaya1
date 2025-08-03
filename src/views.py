import pandas as pd
from django.http import JsonResponse
from .utils import process_date, process_data
import logging

logger = logging.getLogger(__name__)

def parse_datetime(request):
    date_time_str = request.GET.get('date_time', None)

    if date_time_str:
        try:
            result = process_date(date_time_str)
            return JsonResponse(result)
        except Exception as e:
            logger.error(f"Error processing date: {e}")
            return JsonResponse({'error': 'Invalid date format'}, status=400)
    else:
        return JsonResponse({'error': 'No date provided'}, status=400)

def events_view(dataframe: pd.DataFrame):
    try:
        events_data = process_data(dataframe)
        return JsonResponse(events_data)
    except Exception as e:
        logging.error(f"Error processing events: {e}")
        return JsonResponse({"error": "Unable to process events"}), 500
