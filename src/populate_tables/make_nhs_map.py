import hashlib


def make_nhs_map(person_ids):
    rows = []
    for person_id in person_ids:
        # hashed = hashlib.sha256(f"NHS-{person_id}-trial".encode("utf-8")).hexdigest()
        hashed = f"synthetic-data-{person_id}" # make sure it does not look real
        rows.append((person_id, hashed))
    return rows
