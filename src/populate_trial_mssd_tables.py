from datetime import date, datetime, timedelta
import hashlib
import random
import sys

import pyodbc

def random_date_between(start_date, end_date):
    delta_days = (end_date - start_date).days
    return start_date + timedelta(days=random.randint(0, max(0, delta_days)))


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


def make_nhs_map(person_ids):
    rows = []
    for person_id in person_ids:
        hashed = hashlib.sha256(f"NHS-{person_id}-trial".encode("utf-8")).hexdigest()
        rows.append((person_id, hashed))
    return rows


def make_registrations(person_ids, practice_ids):
    rows = []
    for rank, person_id in enumerate(person_ids, start=1):
        registration_date = date(2018 + rank, random.randint(1, 12), random.randint(1, 28))
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


def make_prescriptions(person_ids):
    fake_dmd = [33146011000001109, 37436011000001101, 32194911000001108, 31847511000001100]
    rows = []
    for person_id in person_ids:
        for _ in range(10):
            rows.append(
                (
                    person_id,
                    random_date_between(date(2020, 1, 1), date(2026, 7, 1)),
                    random.choice(fake_dmd),
                    None,
                    round(random.uniform(1, 56), 2),
                    random.choice(["tablet", "capsule", "ml"]),
                    "As directed",
                    1,
                )
            )
    return rows


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


def main():
    random.seed(42)

    # Format for connection string (unecrytped dev connection):
    # 'DRIVER={ODBC Driver 18 for SQL Server};SERVER=???.???.???.???,???;DATABASE=???;UID=???;PWD=???;Encrypt=no;TrustServerCertificate=yes'
    connection_string=sys.argv[1]
    connection=pyodbc.connect(connection_string)

    cursor = connection.cursor()

    try:
        # Clear existing data in child-to-parent order for reruns.
        cursor.execute("DELETE FROM dbo.ImmunisationByName")
        cursor.execute("DELETE FROM dbo.Prescription")
        cursor.execute("DELETE FROM dbo.Event")
        cursor.execute("DELETE FROM dbo.PersonRegistration")
        cursor.execute("DELETE FROM dbo.NHSNumberMap")
        cursor.execute("DELETE FROM dbo.Practice")
        cursor.execute("DELETE FROM dbo.Person")

        practices = make_practices()
        people = make_people()

        cursor.executemany(
            """
            INSERT INTO dbo.Practice
            (PracticeID, ClinicalSystem, DataSource, LatestExtractDate, PracticeName, NHSRegion,
             ICBCode, ICBName, LSOA2021, PracticeIMDQuintile, PracticeUrbanRural)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            practices,
        )

        cursor.executemany(
            """
            INSERT INTO dbo.Person
            (PersonID, Birthday, Sex, Ethnicity19Pt, DateOfDeath)
            VALUES (?, ?, ?, ?, ?)
            """,
            people,
        )

        person_ids = [p[0] for p in people]
        practice_ids = [p[0] for p in practices]

        cursor.executemany(
            """
            INSERT INTO dbo.NHSNumberMap (PersonID, HashedNHSNumber)
            VALUES (?, ?)
            """,
            make_nhs_map(person_ids),
        )

        cursor.executemany(
            """
            INSERT INTO dbo.PersonRegistration
            (PersonID, PracticeID, RegistrationDate, DeRegistrationDateNoNulls, PatientType,
             LSOA2021, NHSRegion, IMDQuintile, UrbanRuralCode, Rank)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            make_registrations(person_ids, practice_ids),
        )

        cursor.executemany(
            """
            INSERT INTO dbo.Event
            (PersonID, PracticeID, EventDate, SnomedConceptID, Term, RegFlag)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            make_events(person_ids, practice_ids),
        )

        cursor.executemany(
            """
            INSERT INTO dbo.Prescription
            (PersonID, IssueDate, DMDCode, Term, Quantity, Units, Directions, RegFlag)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            make_prescriptions(person_ids),
        )

        cursor.executemany(
            """
            INSERT INTO dbo.ImmunisationByName
            (PersonID, PracticeID, VaccinationDate, SnomedConceptID, Compound, Term, Source,
             VaccineName, Manufacturer, BatchNo, RegFlag, RecNo, Label)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            make_immunisations(person_ids, practice_ids),
        )

        connection.commit()

        print("Inserted 10 practices, 5 people, 50 events, 50 prescriptions, 15 immunisations.")
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    main()