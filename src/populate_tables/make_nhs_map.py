import hashlib


def make_nhs_map(person_ids):
    rows = []
    for person_id in person_ids:
        hashed = hashlib.sha256(f"NHS-{person_id}-trial".encode("utf-8")).hexdigest()
        rows.append((person_id, hashed))
    return rows
