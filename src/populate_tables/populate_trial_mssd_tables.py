import random
import sys
import tomllib

import pyodbc

from make_events import make_events
from make_immunisations import make_immunisations
from make_nhs_map import make_nhs_map
from make_people import make_people
from make_practices import make_practices
from make_prescriptions import make_prescriptions
from make_registrations import make_registrations


config = tomllib.load(open(sys.argv[1], "rb"))

random.seed(42)

# Format for connection string (unecrytped dev connection):
# 'DRIVER={ODBC Driver 18 for SQL Server};SERVER=???.???.???.???,???;DATABASE=???;UID=???;PWD=???;Encrypt=no;TrustServerCertificate=yes'
connection = pyodbc.connect(config["connection_string"])

cursor = connection.cursor()
cursor.fast_executemany=True

try:
    # Clear existing data in child-to-parent order for reruns.
    cursor.execute("DELETE FROM dbo.ImmunisationByName")
    cursor.execute("DELETE FROM dbo.Prescription")
    cursor.execute("DELETE FROM dbo.Event")
    cursor.execute("DELETE FROM dbo.PersonRegistration")
    cursor.execute("DELETE FROM dbo.NHSNumberMap")
    cursor.execute("DELETE FROM dbo.Practice")
    cursor.execute("DELETE FROM dbo.Person")

    practices = make_practices(n_practices=config["n_practices"])
    people = make_people(n_persons=config["n_persons"])

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
        make_events(person_ids, practice_ids, config=config),
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

    print(f'n_persons: {config["n_persons"]}')
    print(f'n_practices: {config["n_practices"]}')
    print(f'n_events_per_person: {config["n_events_per_person"]}')

except Exception:
    connection.rollback()
    raise
finally:
    cursor.close()
    connection.close()
