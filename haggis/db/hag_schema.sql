
--
-- Table: Htb
-- Desc: Historical Address Table
--
DROP TABLE if exists Htb;
CREATE TABLE Htb (
    Id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    Hid integer NOT NULL,
    Name text,
    Num text,
    Street text,
    HPCode text,
    Locality text,
    Town text,
	HYear text,
    DistCode text
);

--
-- Table: Ctb
-- Desc: Contemporary Address Table
--
DROP TABLE if exists Ctb;
CREATE TABLE Ctb (
    Id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    Cid integer NOT NULL,
    Name text,
    Num text,
    Street text,
    CPCode text,
    Locality text,
    Town text,
    GREasting real,
    GRNorthing real,
	DistCode text
);

--
-- Table: Atb
-- Desc: Aliases Table
--
DROP TABLE if exists Atb;
CREATE TABLE Atb (
    Id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    Alias text NOT NULL,
    Name text NOT NULL,
    Freq integer NOT NULL DEFAULT 1
);

--
-- Table: Stb
-- Desc: Street/Farm Name Table
--
DROP TABLE if exists Stb;
CREATE TABLE Stb (
    SNId integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    Name text,
    Street text,
    HPCode text,
    Locality text,
    Town text
);

--
-- Table: Ttb
-- Desc: Timestamped Address Table
--
DROP TABLE if exists Ttb;
CREATE TABLE Ttb (
    Id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    Cid integer,
    Hid integer,
    Num text,
    SNId integer NOT NULL,
    CPCode text,
    GREasting real,
    GRNorthing real,
    StartYear text,
    EndYear text,
    AutoEval integer NOT NULL DEFAULT 0,
    ManEval integer NOT NULL DEFAULT 0,
    DistCode text,
	AssignedCode text,
	AssignedDens integer NOT NULL DEFAULT 0,
	Status integer NOT NULL DEFAULT 0, 
	ThiesId integer NOT NULL DEFAULT 0, 
    FOREIGN KEY (SNId) REFERENCES Stb (SNId)
);

--
-- Table: SSCtb
-- Desc: Street Segment Changes Table
--
DROP TABLE if exists SSCtb;
CREATE TABLE SSCtb (
	SSCId integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    SNId integer NOT NULL,
    Year text NOT NULL,
    FOREIGN KEY (SNId) REFERENCES Stb (SNId)
);

--
-- Table: SNCtb
-- Desc: Street/Farm Name Changes Table
--
DROP TABLE if exists SNCtb;
CREATE TABLE SNCtb (
	SNCId integer NOT NULL PRIMARY KEY AUTOINCREMENT,
    SNId integer NOT NULL,
    Name text,
	Street text,
    PCode text,
    Year text NOT NULL,
    FOREIGN KEY (SNId) REFERENCES Stb (SNId)
);

--
-- Table: STtb
-- Desc: Names of Saints Table
--
DROP TABLE if exists STtb;
CREATE TABLE STtb (
    Id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
	Name text,
    FOREIGN KEY (Id) REFERENCES STtb (Id)
);
