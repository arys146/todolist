from datetime import time, date, datetime, timedelta


def get_logical_date(offset: time, date: datetime):
    return (date - timedelta(hours=offset.hour, minutes=offset.minute)).date()
