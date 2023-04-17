from datetime import datetime
import pandas as pd

def date_to_string(date):
    return str(date)

def string_to_date(date_str):
    return pd.to_datetime(date_str).date()

def parse_tiingo_date(date_string):
    date_format = '%Y-%m-%dT%H:%M:%S.%fZ'

    # Convert the date string to a datetime object
    datetime_obj = datetime.strptime(date_string, date_format) \
        if '.' in date_string \
        else datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')

    return datetime_obj