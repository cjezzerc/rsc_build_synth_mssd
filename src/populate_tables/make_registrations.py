from datetime import date, datetime
import random


def make_registrations(person_ids, practice_ids):
    rows = []
    for rank, person_id in enumerate(person_ids, start=1):
        
        registration_date = date(random.randint(2015,2025), random.randint(1, 12), random.randint(1, 28))
        dereg = datetime(2099, 12, 31, 0, 0, 0)
        rows.append(
            (
                person_id,
                random.choice(practice_ids),
                registration_date,
                dereg,
                "Regular",
                f"E010{2000 + person_id:05d}"[:9],
                random.choice(["North East", "North West", "Midlands", "London", "South West"]),
                str(random.randint(1, 5)),
                random.choice(["U1", "R1"]),
                rank,
            )
        )
    return rows
