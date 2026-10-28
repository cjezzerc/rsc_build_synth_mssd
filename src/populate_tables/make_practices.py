from datetime import date
import random


def make_practices(n_practices=None):
    practices = []
    latest_extract = date(2026, 7, 1)
    regions = ["North East", "North West", "Midlands", "London", "South West"]
    for i_practice in range(n_practices):
        practice_id = f"P{i_practice + 1:05d}"
        i_region=random.randint(0,4)
        i_icb=(i_region+1)*10 + random.randint(0,9)
        practices.append(
            (
                practice_id,
                random.choice(["Software-A", "Software-B"]),
                random.choice(["A", "B"]),
                latest_extract,
                f"Practice {i_practice + 1}",
                regions[i_region],
                f"ICB{i_icb:02d}",
                f"ICB Name {i_icb}",
                f"E010{1001 + i_practice:05d}"[:9],
                random.randint(1, 5),
                random.choice(["Urban", "Rural"]),
            )
        )
    return practices
