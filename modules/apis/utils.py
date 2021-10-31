from datetime import timedelta

def nearest_date(items, pivot):
    return min(items, key=lambda x: abs(x - pivot))

def hourly_it(start, finish, step=1):
    while finish > start:
        start = start + timedelta(hours=step)
        yield start

def daily_it(start, finish, step=1):
    while finish > start:
        start = start + timedelta(days=step)
        yield start