from datetime import date
import random


def make_people():
    people = []
    target_ages = [1, 7, 25, 52, 79]
    today = date.today()
    for idx, age in enumerate(target_ages, start=1):
        year = today.year - age
        birthday = date(year, random.randint(1, 12), random.randint(1, 28))
        people.append(
            (
                idx,
                birthday,
                random.choice(["M", "F"]),
                random.choice(["White", "Asian", "Black", "Mixed", "Other"]),
                None,
            )
        )
    return people
