import random
from datetime import date

try:
    from .random_date_between import random_date_between
except ImportError:
    from random_date_between import random_date_between


def make_prescriptions(person_ids):
    fake_dmd = [33146011000001109, 37436011000001101, 32194911000001108, 31847511000001100]
    rows = []
    for person_id in person_ids:
        for _ in range(10):
            rows.append(
                (
                    person_id,
                    random_date_between(date(2020, 1, 1), date(2026, 7, 1)),
                    random.choice(fake_dmd),
                    None,
                    round(random.uniform(1, 56), 2),
                    random.choice(["tablet", "capsule", "ml"]),
                    "As directed",
                    1,
                )
            )
    return rows
