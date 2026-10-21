from datetime import date
import random


def make_practices():
    practices = []
    latest_extract = date(2026, 7, 1)
    regions = ["North East", "North West", "Midlands", "London", "South West"]
    for i in range(10):
        practice_id = f"P{i + 1:05d}"
        practices.append(
            (
                practice_id,
                random.choice(["Software-A", "Software-B"]),
                random.choice(["A", "B"]),
                latest_extract,
                f"Practice {i + 1}",
                random.choice(regions),
                f"ICB{i % 5 + 1:02d}",
                f"ICB Name {i % 5 + 1}",
                f"E010{1000 + i:05d}"[:9],
                random.randint(1, 5),
                random.choice(["Urban", "Rural"]),
            )
        )
    return practices
