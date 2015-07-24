--
-- Indexes for Table Htb
--
CREATE INDEX Htb_idx_Id
ON Htb (Id ASC)
;
CREATE INDEX Htb_idx_Hid
ON Htb (Hid ASC)
;
CREATE INDEX Htb_idx_Name
ON Htb (Name ASC)
;
CREATE INDEX Htb_idx_Street
ON Htb (Street ASC)
;
CREATE INDEX Htb_idx_Locality
ON Htb (Locality ASC)
;
CREATE INDEX Htb_idx_Town
ON Htb (Town ASC)
;

--
-- Indexes for Table Ctb
--
CREATE INDEX Ctb_idx_Id
ON Ctb (Id ASC)
;
CREATE INDEX Ctb_idx_Cid
ON Ctb (Cid ASC)
;
CREATE INDEX Ctb_idx_Name
ON Ctb (Name ASC)
;
CREATE INDEX Ctb_idx_Street
ON Ctb (Street ASC)
;
CREATE INDEX Ctb_idx_Locality
ON Ctb (Locality ASC)
;
CREATE INDEX Ctb_idx_Town
ON Ctb (Town ASC)
;
CREATE INDEX Ctb_idx_GREasting
ON Ctb (GREasting ASC)
;
CREATE INDEX Ctb_idx_GRNorthing
ON Ctb (GRNorthing ASC)
;

--
-- Indexes for Table Atb
--
CREATE INDEX Atb_idx_Id
ON Atb (Id ASC)
;
CREATE INDEX Atb_idx_Alias
ON Atb (Alias ASC)
;
CREATE INDEX Atb_idx_Name
ON Atb (Name ASC)
;

--
-- Indexes for Table Ttb
--
CREATE INDEX Ttb_idx_Id
ON Ttb (Id ASC)
;
CREATE INDEX Ttb_idx_Cid
ON Ttb (Cid ASC)
;
CREATE INDEX Ttb_idx_Hid
ON Ttb (Hid ASC)
;
CREATE INDEX Ttb_idx_SNId
ON Ttb (SNId ASC)
;
CREATE INDEX Ttb_idx_AutoEval
ON Ttb (AutoEval ASC)
;
CREATE INDEX Ttb_idx_ThiesId
ON Ttb (ThiesId ASC)
;
CREATE INDEX Ttb_idx_DistCode
ON Ttb (DistCode ASC)
;


--
-- Indexes for Table Stb
--
CREATE INDEX Stb_idx_SNId
ON Stb (SNId ASC)
;

--
-- Indexes for Table SSCtb
--
CREATE INDEX SSCtb_idx_SSId
ON SSCtb (SNId ASC)
;

--
-- Indexes for Table SNCtb
--
CREATE INDEX SNCtb_idx_SNId
ON SNCtb (SNId ASC)
;

--
-- Indexes for Table STtb
--
CREATE INDEX STtb_idx_Name
ON STtb (Name ASC)
;
CREATE INDEX STtb_idx_Id
ON STtb (Id ASC)
;