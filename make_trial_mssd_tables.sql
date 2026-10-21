

-- Drop child tables before parent tables so reruns succeed with FK constraints.
IF OBJECT_ID('dbo.ImmunisationByName', 'U') IS NOT NULL DROP TABLE dbo.ImmunisationByName;
IF OBJECT_ID('dbo.Prescription', 'U') IS NOT NULL DROP TABLE dbo.Prescription;
IF OBJECT_ID('dbo.Event', 'U') IS NOT NULL DROP TABLE dbo.Event;
IF OBJECT_ID('dbo.PersonRegistration', 'U') IS NOT NULL DROP TABLE dbo.PersonRegistration;
IF OBJECT_ID('dbo.NHSNumberMap', 'U') IS NOT NULL DROP TABLE dbo.NHSNumberMap;
IF OBJECT_ID('dbo.Practice', 'U') IS NOT NULL DROP TABLE dbo.Practice;
IF OBJECT_ID('dbo.Person', 'U') IS NOT NULL DROP TABLE dbo.Person;


CREATE TABLE dbo.Person (
    [PersonID] int NOT NULL,
    [Birthday] date NOT NULL,
    [Sex] varchar(1) NOT NULL,
    [Ethnicity19Pt] varchar(50) NULL,
    [DateOfDeath] date NULL,
    CONSTRAINT [PK_Person] PRIMARY KEY ([PersonID])
);


CREATE TABLE dbo.Practice (
    [PracticeID] varchar(6) NOT NULL,
    [ClinicalSystem] varchar(20) NOT NULL,
    [DataSource] varchar(1) NOT NULL,
    [LatestExtractDate] date NOT NULL,
    [PracticeName] varchar(100) NOT NULL,
    [NHSRegion] varchar(24) NULL,
    [ICBCode] varchar(5) NULL,
    [ICBName] varchar(100) NULL,
    [LSOA2021] varchar(9) NULL,
    [PracticeIMDQuintile] int NULL,
    [PracticeUrbanRural] varchar(5) NULL,
    CONSTRAINT [PK_Practice] PRIMARY KEY ([PracticeID]),
    CONSTRAINT [CK_Practice_ClinicalSystem] CHECK ([ClinicalSystem] IN ('Software-A', 'Software-B')),
    CONSTRAINT [CK_Practice_PracticeUrbanRural] CHECK ([PracticeUrbanRural] IS NULL OR [PracticeUrbanRural] IN ('Urban', 'Rural')),
    CONSTRAINT [CK_Practice_PracticeIMDQuintile] CHECK ([PracticeIMDQuintile] IS NULL OR [PracticeIMDQuintile] IN (1, 2, 3, 4, 5))
);


CREATE TABLE dbo.NHSNumberMap (
    [PersonID] int NOT NULL,
    [HashedNHSNumber] varchar(128) NOT NULL,
    CONSTRAINT [FK_NHSNumberMap_Person_PersonID] FOREIGN KEY ([PersonID]) REFERENCES dbo.Person([PersonID])
);


CREATE TABLE dbo.PersonRegistration (
    [PersonID] int NOT NULL,
    [PracticeID] varchar(6) NOT NULL,
    [RegistrationDate] date NOT NULL,
    [DeRegistrationDateNoNulls] datetime NOT NULL,
    [PatientType] varchar(100) NOT NULL,
    [LSOA2021] varchar(9) NULL,
    [NHSRegion] varchar(255) NULL,
    [IMDQuintile] varchar(255) NULL,
    [UrbanRuralCode] varchar(6) NOT NULL,
    [Rank] int NOT NULL,
    CONSTRAINT [FK_PersonRegistration_Person_PersonID] FOREIGN KEY ([PersonID]) REFERENCES dbo.Person([PersonID]),
    CONSTRAINT [FK_PersonRegistration_Practice_PracticeID] FOREIGN KEY ([PracticeID]) REFERENCES dbo.Practice([PracticeID])
);


CREATE TABLE dbo.Event (
    [PersonID] int NOT NULL,
    [PracticeID] varchar(6) NOT NULL,
    [EventDate] date NOT NULL,
    [SnomedConceptID] bigint NOT NULL,
    [Term] nvarchar(255) NULL,
    [RegFlag] int NOT NULL,
    CONSTRAINT [FK_Event_Person_PersonID] FOREIGN KEY ([PersonID]) REFERENCES dbo.Person([PersonID]),
    CONSTRAINT [FK_Event_Practice_PracticeID] FOREIGN KEY ([PracticeID]) REFERENCES dbo.Practice([PracticeID])
);


CREATE TABLE dbo.Prescription (
    [PersonID] int NOT NULL,
    [IssueDate] date NOT NULL,
    [DMDCode] bigint NOT NULL,
    [Term] varchar(255) NULL,
    [Quantity] decimal(20,4) NULL,
    [Units] varchar(400) NULL,
    [Directions] varchar(1000) NULL,
    [RegFlag] int NULL,
    CONSTRAINT [FK_Prescription_Person_PersonID] FOREIGN KEY ([PersonID]) REFERENCES dbo.Person([PersonID])
);


CREATE TABLE dbo.ImmunisationByName (
    [PersonID] int NOT NULL,
    [PracticeID] varchar(6) NOT NULL,
    [VaccinationDate] date NOT NULL,
    [SnomedConceptID] bigint NULL,
    [Compound] varchar(100) NULL,
    [Term] varchar(255) NULL,
    [Source] varchar(100) NOT NULL,
    [VaccineName] varchar(100) NULL,
    [Manufacturer] varchar(1000) NULL,
    [BatchNo] varchar(255) NULL,
    [RegFlag] int NOT NULL,
    [RecNo] int NOT NULL,
    [Label] varchar(30) NOT NULL,
    CONSTRAINT [FK_ImmunisationByName_Person_PersonID] FOREIGN KEY ([PersonID]) REFERENCES dbo.Person([PersonID]),
    CONSTRAINT [FK_ImmunisationByName_Practice_PracticeID] FOREIGN KEY ([PracticeID]) REFERENCES dbo.Practice([PracticeID])
);


-- IF OBJECT_ID('dbo.DiseaseCodeList', 'U') IS NOT NULL DROP TABLE dbo.DiseaseCodeList;
-- CREATE TABLE dbo.DiseaseCodeList (
--     [ConditionID] smallint NOT NULL,
--     [ConceptID] bigint NOT NULL,
--     [ConditionName] varchar(50) NOT NULL,
--     [Term] varchar(255) NOT NULL
-- );
-- 

-- IF OBJECT_ID('dbo.PrescriptionCodeList', 'U') IS NOT NULL DROP TABLE dbo.PrescriptionCodeList;
-- CREATE TABLE dbo.PrescriptionCodeList (
--     [ConditionID] smallint NOT NULL,
--     [ConceptID] bigint NOT NULL,
--     [ConditionName] varchar(50) NOT NULL,
--     [Term] varchar(255) NOT NULL
-- );

