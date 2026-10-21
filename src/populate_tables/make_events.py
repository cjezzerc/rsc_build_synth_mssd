import random
from datetime import date

try:
    from .random_date_between import random_date_between
except ImportError:
    from random_date_between import random_date_between


def make_events(person_ids, practice_ids):
    fake_snomed = [44054006, 386661006, 195967001, 162864005, 233604007]
    rows = []
    for person_id in person_ids:
        for _ in range(10):
            rows.append(
                (
                    person_id,
                    random.choice(practice_ids),
                    random_date_between(date(2020, 1, 1), date(2026, 7, 1)),
                    random.choice(fake_snomed),
                    None,
                    1,
                )
            )
    return rows
