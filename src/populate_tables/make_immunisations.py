import random
from datetime import date

try:
    from .random_date_between import random_date_between
except ImportError:
    from random_date_between import random_date_between


def make_immunisations(person_ids, practice_ids):
    vaccine_rows = [
        (840539006, "COVID-19 vaccine", "mRNA"),
        (871717007, "Influenza vaccine", "Inactivated"),
        (1119349007, "Pneumococcal vaccine", "Conjugate"),
    ]
    rows = []
    rec_no = 1
    for person_id in person_ids:
        for _ in range(3):
            snomed, vaccine_name, compound = random.choice(vaccine_rows)
            rows.append(
                (
                    person_id,
                    random.choice(practice_ids),
                    random_date_between(date(2020, 1, 1), date(2026, 7, 1)),
                    snomed,
                    compound,
                    None,
                    "GP",
                    vaccine_name,
                    random.choice(["Acme Pharma", "NorthBio", "HealthCorp"]),
                    f"B{random.randint(100000, 999999)}",
                    1,
                    rec_no,
                    "Routine",
                )
            )
            rec_no += 1
    return rows
