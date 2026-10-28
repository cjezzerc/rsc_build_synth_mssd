import random
from datetime import date
from code_weighting import generate_weighted_concept_occurrences
# from populate_tables.populate_trial_mssd_tables import config

try:
    from .random_date_between import random_date_between
except ImportError:
    from random_date_between import random_date_between


def make_events(person_ids, practice_ids, config_file=None):

    gwco=generate_weighted_concept_occurrences(config_file=config_file, n_occurrences=10*len(person_ids))

    events_per_person=10
    rows = []
    for i_person, person_id in enumerate(person_ids):
        for i_event in range(events_per_person):
            concept_id, term, count=gwco[i_person*events_per_person + i_event]
            rows.append(
                (
                    person_id,
                    random.choice(practice_ids),
                    random_date_between(date(2020, 1, 1), date(2026, 7, 1)),
                    concept_id,
                    term,
                    1,
                )
            )
    return rows
