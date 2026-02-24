-- ============================================================
-- database_creation.sql
-- Scenario: Conference / Event Management System
-- Target DBMS: PostgreSQL
-- ============================================================

BEGIN;

-- Drop order (child tables first)
DROP VIEW IF EXISTS v_session_feedback_summary;
DROP VIEW IF EXISTS v_event_overview;

DROP TABLE IF EXISTS Feedback CASCADE;
DROP TABLE IF EXISTS Session_Equipment CASCADE;
DROP TABLE IF EXISTS Event_Staff CASCADE;
DROP TABLE IF EXISTS Event_Sponsor CASCADE;
DROP TABLE IF EXISTS Registration CASCADE;
DROP TABLE IF EXISTS Session CASCADE;

DROP TABLE IF EXISTS Payment CASCADE;
DROP TABLE IF EXISTS Sponsor CASCADE;
DROP TABLE IF EXISTS Equipment CASCADE;
DROP TABLE IF EXISTS Staff CASCADE;
DROP TABLE IF EXISTS Speaker CASCADE;
DROP TABLE IF EXISTS Attendee CASCADE;
DROP TABLE IF EXISTS Event CASCADE;
DROP TABLE IF EXISTS Organizer CASCADE;
DROP TABLE IF EXISTS Venue CASCADE;

-- Core tables

CREATE TABLE Venue (
  Venue_ID        INT PRIMARY KEY,
  Address         VARCHAR(200) NOT NULL,
  Room_Number     VARCHAR(20)  NOT NULL,
  Total_Capacity  INT NOT NULL CHECK (Total_Capacity > 0),  -- attribute-level constraint
  UNIQUE (Address, Room_Number)
);

CREATE TABLE Organizer (
  Organizer_ID    INT PRIMARY KEY,
  Org_Name        VARCHAR(120) NOT NULL,
  Contact_Person  VARCHAR(120) NOT NULL,
  Email           VARCHAR(160) NOT NULL,
  UNIQUE (Email)
);

CREATE TABLE Event (
  Event_ID      INT PRIMARY KEY,
  Title         VARCHAR(200) NOT NULL,
  Start_Date    DATE NOT NULL,
  End_Date      DATE NOT NULL,
  Venue_ID      INT NOT NULL,
  Organizer_ID  INT NOT NULL,
  -- tuple-level constraint (multi-attribute)
  CHECK (Start_Date <= End_Date),
  FOREIGN KEY (Venue_ID) REFERENCES Venue(Venue_ID)
    ON UPDATE CASCADE ON DELETE RESTRICT,
  FOREIGN KEY (Organizer_ID) REFERENCES Organizer(Organizer_ID)
    ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE Attendee (
  Attendee_ID  INT PRIMARY KEY,
  Name         VARCHAR(140) NOT NULL,
  Institution  VARCHAR(140) NOT NULL,
  Email        VARCHAR(160) NOT NULL,
  UNIQUE (Email)
);

CREATE TABLE Speaker (
  Speaker_ID   INT PRIMARY KEY,
  Shift_Start  TIME NOT NULL,
  Shift_End    TIME NOT NULL,
  Duty         VARCHAR(140) NOT NULL,
  CHECK (Shift_Start < Shift_End) -- tuple-level constraint inside relation (still fine)
);

CREATE TABLE Staff (
  Staff_ID    INT PRIMARY KEY,
  First_Name  VARCHAR(80) NOT NULL,
  Last_Name   VARCHAR(80) NOT NULL,
  Role        VARCHAR(80) NOT NULL,
  Shift_Time  VARCHAR(40) NOT NULL
);

CREATE TABLE Equipment (
  Serial_Number  VARCHAR(40) PRIMARY KEY,
  Item_Type      VARCHAR(80) NOT NULL
);

CREATE TABLE Sponsor (
  Sponsor_ID     INT PRIMARY KEY,
  Company_Name   VARCHAR(160) NOT NULL,
  Contact_Info   VARCHAR(200) NOT NULL,
  UNIQUE (Company_Name)
);

CREATE TABLE Payment (
  Transaction_ID   INT PRIMARY KEY,
  Amount           NUMERIC(10,2) NOT NULL CHECK (Amount >= 0), -- attribute-level constraint
  Payment_Method   VARCHAR(40) NOT NULL
);

-- Relationship / weak-entity tables

-- Weak entity Session identified by (Event_ID, Topic, Start_Time)
CREATE TABLE Session (
  Event_ID     INT NOT NULL,
  Topic        VARCHAR(160) NOT NULL,
  Start_Time   TIME NOT NULL,
  Speaker_ID   INT NOT NULL,
  PRIMARY KEY (Event_ID, Topic, Start_Time),
  FOREIGN KEY (Event_ID) REFERENCES Event(Event_ID)
    ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (Speaker_ID) REFERENCES Speaker(Speaker_ID)
    ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE Registration (
  Attendee_ID        INT NOT NULL,
  Event_ID           INT NOT NULL,
  Registration_Date  DATE NOT NULL,
  Status             VARCHAR(20) NOT NULL,
  Transaction_ID     INT NULL,
  PRIMARY KEY (Attendee_ID, Event_ID),
  FOREIGN KEY (Attendee_ID) REFERENCES Attendee(Attendee_ID)
    ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (Event_ID) REFERENCES Event(Event_ID)
    ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (Transaction_ID) REFERENCES Payment(Transaction_ID)
    ON UPDATE CASCADE ON DELETE SET NULL,
  CHECK (Status IN ('pending', 'confirmed', 'cancelled')) -- attribute-level constraint
);

CREATE TABLE Event_Sponsor (
  Event_ID            INT NOT NULL,
  Sponsor_ID          INT NOT NULL,
  Sponsorship_Level   VARCHAR(40) NOT NULL,
  Contribution_Amount NUMERIC(10,2) NOT NULL CHECK (Contribution_Amount >= 0),
  PRIMARY KEY (Event_ID, Sponsor_ID),
  FOREIGN KEY (Event_ID) REFERENCES Event(Event_ID)
    ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (Sponsor_ID) REFERENCES Sponsor(Sponsor_ID)
    ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Event_Staff (
  Event_ID  INT NOT NULL,
  Staff_ID  INT NOT NULL,
  PRIMARY KEY (Event_ID, Staff_ID),
  FOREIGN KEY (Event_ID) REFERENCES Event(Event_ID)
    ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (Staff_ID) REFERENCES Staff(Staff_ID)
    ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Session_Equipment (
  Event_ID       INT NOT NULL,
  Topic          VARCHAR(160) NOT NULL,
  Start_Time     TIME NOT NULL,
  Serial_Number  VARCHAR(40) NOT NULL,
  PRIMARY KEY (Event_ID, Topic, Start_Time, Serial_Number),
  FOREIGN KEY (Event_ID, Topic, Start_Time)
    REFERENCES Session(Event_ID, Topic, Start_Time)
    ON UPDATE CASCADE ON DELETE CASCADE,
  FOREIGN KEY (Serial_Number) REFERENCES Equipment(Serial_Number)
    ON UPDATE CASCADE ON DELETE RESTRICT
);

CREATE TABLE Feedback (
  Feedback_ID  INT PRIMARY KEY,
  Event_ID     INT NOT NULL,
  Topic        VARCHAR(160) NOT NULL,
  Start_Time   TIME NOT NULL,
  Rating       INT NOT NULL CHECK (Rating BETWEEN 1 AND 5), -- attribute-level constraint
  Comments     VARCHAR(400) NULL,
  FOREIGN KEY (Event_ID, Topic, Start_Time)
    REFERENCES Session(Event_ID, Topic, Start_Time)
    ON UPDATE CASCADE ON DELETE CASCADE
);

-- Index 

CREATE INDEX idx_registration_event ON Registration(Event_ID);
CREATE INDEX idx_session_event ON Session(Event_ID);
CREATE INDEX idx_feedback_session ON Feedback(Event_ID, Topic, Start_Time);

-- View

CREATE VIEW v_event_overview AS
SELECT
  e.Event_ID,
  e.Title,
  e.Start_Date,
  e.End_Date,
  v.Address,
  v.Room_Number,
  v.Total_Capacity,
  o.Org_Name,
  o.Contact_Person,
  o.Email AS Organizer_Email
FROM Event e
JOIN Venue v ON v.Venue_ID = e.Venue_ID
JOIN Organizer o ON o.Organizer_ID = e.Organizer_ID;

CREATE VIEW v_session_feedback_summary AS
SELECT
  f.Event_ID,
  f.Topic,
  f.Start_Time,
  COUNT(*) AS Feedback_Count,
  AVG(f.Rating)::NUMERIC(10,2) AS Avg_Rating
FROM Feedback f
GROUP BY f.Event_ID, f.Topic, f.Start_Time;

-- Trigger
-- Business rule: If Status = 'confirmed', Transaction_ID must be NOT NULL.
-- Additionally, default Status = 'pending' if empty string (defensive).

CREATE OR REPLACE FUNCTION trg_registration_enforce_payment()
RETURNS TRIGGER AS $$
BEGIN
  IF NEW.Status IS NULL OR btrim(NEW.Status) = '' THEN
    NEW.Status := 'pending';
  END IF;

  IF NEW.Status = 'confirmed' AND NEW.Transaction_ID IS NULL THEN
    RAISE EXCEPTION 'Confirmed registration requires a Transaction_ID (payment).';
  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER before_registration_ins_upd
BEFORE INSERT OR UPDATE ON Registration
FOR EACH ROW
EXECUTE FUNCTION trg_registration_enforce_payment();

-- Assertion equivalent for SQL (DBMS-compatible)
-- Global-ish constraint enforced at COMMIT time:
-- For any confirmed registration, there must exist a referenced payment row.
-- This is redundant with FK+trigger, but it behaves like an ASSERTION check
-- and is DEFERRABLE, so it runs at transaction end.

CREATE OR REPLACE FUNCTION assert_confirmed_has_payment()
RETURNS TRIGGER AS $$
BEGIN
  IF EXISTS (
    SELECT 1
    FROM Registration r
    LEFT JOIN Payment p ON p.Transaction_ID = r.Transaction_ID
    WHERE r.Status = 'confirmed'
      AND (r.Transaction_ID IS NULL OR p.Transaction_ID IS NULL)
  ) THEN
    RAISE EXCEPTION 'Assertion failed: confirmed registrations must reference an existing payment.';
  END IF;

  RETURN NULL;
END;
$$ LANGUAGE plpgsql;

CREATE CONSTRAINT TRIGGER assertion_confirmed_payment
AFTER INSERT OR UPDATE OR DELETE ON Registration
DEFERRABLE INITIALLY DEFERRED
FOR EACH ROW
EXECUTE FUNCTION assert_confirmed_has_payment();

COMMIT;
