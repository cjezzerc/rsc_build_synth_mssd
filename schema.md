# Trial MSSD Schema Diagram

```mermaid
erDiagram
    PERSON {
        int PersonID PK
        date Birthday
        varchar Sex
        varchar Ethnicity19Pt
        date DateOfDeath
    }

    PRACTICE {
        varchar PracticeID PK
        varchar ClinicalSystem
        varchar DataSource
        date LatestExtractDate
        varchar PracticeName
        varchar NHSRegion
        varchar ICBCode
        varchar ICBName
        varchar LSOA2021
        int PracticeIMDQuintile
        varchar PracticeUrbanRural
    }

    NHSNUMBERMAP {
        int PersonID
        varchar HashedNHSNumber
    }

    PERSONREGISTRATION {
        int PersonID
        varchar PracticeID
        date RegistrationDate
        datetime DeRegistrationDateNoNulls
        varchar PatientType
        varchar LSOA2021
        varchar NHSRegion
        varchar IMDQuintile
        varchar UrbanRuralCode
        int Rank
    }

    EVENT {
        int PersonID
        varchar PracticeID
        date EventDate
        bigint SnomedConceptID
        nvarchar Term
        int RegFlag
    }

    PRESCRIPTION {
        int PersonID
        date IssueDate
        bigint DMDCode
        varchar Term
        decimal Quantity
        varchar Units
        varchar Directions
        int RegFlag
    }

    IMMUNISATIONBYNAME {
        int PersonID
        varchar PracticeID
        date VaccinationDate
        bigint SnomedConceptID
        varchar Compound
        varchar Term
        varchar Source
        varchar VaccineName
        varchar Manufacturer
        varchar BatchNo
        int RegFlag
        int RecNo
        varchar Label
    }
```

### Foreign-key targets
- NHSNUMBERMAP.PersonID -> PERSON.PersonID
- PERSONREGISTRATION.PersonID -> PERSON.PersonID
- PERSONREGISTRATION.PracticeID -> PRACTICE.PracticeID
- EVENT.PersonID -> PERSON.PersonID
- EVENT.PracticeID -> PRACTICE.PracticeID
- PRESCRIPTION.PersonID -> PERSON.PersonID
- IMMUNISATIONBYNAME.PersonID -> PERSON.PersonID
- IMMUNISATIONBYNAME.PracticeID -> PRACTICE.PracticeID

## Relationship summary

- A `Person` can have multiple `NHSNumberMap`, `PersonRegistration`, `Event`, `Prescription`, and `ImmunisationByName` records.
- A `Practice` can cover many `PersonRegistration`, and can be associated with many `Event` and `ImmunisationByName` rows.
- `PersonRegistration` links each person to the practice they were registered with at a given time.
- `Event` and `ImmunisationByName` are practice- and person-linked clinical observations.
- `Prescription` is linked to the person who received the prescription, without a direct `PracticeID` in the current schema.
