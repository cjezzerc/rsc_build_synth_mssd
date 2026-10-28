from datetime import date
import random




def make_people(n_persons=None):

    age_probability=[1.0]*65 + [1-x/35.0 for x in range (0,35)]
    age_choices=range(0,100)
    print(age_probability)
    ages=random.choices(population=age_choices, weights=age_probability, k=n_persons)

    people = []
    today = date.today()
    for i_person in range(0, n_persons):
        age=ages[i_person]
        year = today.year - age
        birthday = date(year, random.randint(1, 12), random.randint(1, 28))
        people.append(
            (
                i_person,
                birthday,
                random.choice(["M", "F"]),
                random.choice(["White", "Asian", "Black", "Mixed", "Other"]),
                None,
            )
        )
    return people
