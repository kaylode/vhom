from datetime import timedelta

def nearest_date(items, pivot):
    """
    Get nearest date
    """
    return min(items, key=lambda x: abs(x - pivot))

def hourly_it(start, finish, step=1):
    """
    Iterate through hours
    """
    while finish > start:
        start = start + timedelta(hours=step)
        yield start

def daily_it(start, finish, step=1):
    """
    Iterate through days
    """
    while finish > start:
        start = start + timedelta(days=step)
        yield start