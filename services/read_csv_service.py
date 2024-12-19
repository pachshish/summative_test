from datetime import datetime


def safe_date(year, month, day):
    try:
        if not (1 <= month <= 12):
            month = 1
        if not (1 <= day <= 31):
            day = 1
        return datetime(year, month, day).date()
    except ValueError:
        return datetime(year, 1, 1).date()

def safe_int(value, default=1):
    if value is not int:
        return default
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


def safe_float(value, default=0.0):
    if value is not float:
        return default
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

def safe_year(value, default=1970):
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

def safe_lat_end_lan(value, default=0.0):
    try:
        return float(value)
    except (ValueError, TypeError):
        return default

def process_terrorists(value):
    if value == '-99':
        return None
    try:
        return int(value)
    except (ValueError, TypeError):
        return 1
