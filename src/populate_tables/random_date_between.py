import random
from datetime import timedelta


def random_date_between(start_date, end_date):
    delta_days = (end_date - start_date).days
    return start_date + timedelta(days=random.randint(0, max(0, delta_days)))
