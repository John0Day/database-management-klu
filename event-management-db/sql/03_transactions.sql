-- ============================================================
-- transactions.sql
-- Target DBMS: PostgreSQL
-- Scenario: Conference / Event Management System
-- Requires: Schema from database_creation.sql + initial data_insertion.sql
-- ============================================================

-- ------------------------------------------------------------
-- Transaction 1: Inclusion (INSERT)
-- Goal: Create a new attendee, create a payment, then insert a confirmed registration.
-- Uses:
--  - Trigger: before_registration_ins_upd (confirmed requires Transaction_ID)
--  - Assertion-equivalent constraint trigger: assertion_confirmed_payment (checked at COMMIT)
--  - View: v_event_overview
--  - Indexes: idx_registration_event (queries by Event_ID)
-- ------------------------------------------------------------
BEGIN;

-- Show event context via the view
SELECT *
FROM v_event_overview
WHERE Event_ID = 1;

-- New attendee (choose ID not used in initial data)
INSERT INTO Attendee (Attendee_ID, Name, Institution, Email)
VALUES (11, 'Clara Sommer', 'HS Munich', 'clara.sommer@hsm.example');

-- New payment
INSERT INTO Payment (Transaction_ID, Amount, Payment_Method)
VALUES (11, 79.00, 'card');

-- Confirmed registration (trigger enforces Transaction_ID is not NULL)
INSERT INTO Registration (Attendee_ID, Event_ID, Registration_Date, Status, Transaction_ID)
VALUES (11, 1, '2026-03-03', 'confirmed', 11);

-- Verify (planner can use idx_registration_event)
SELECT Attendee_ID, Event_ID, Status, Transaction_ID
FROM Registration
WHERE Event_ID = 1
ORDER BY Attendee_ID;

COMMIT;


-- ------------------------------------------------------------
-- Transaction 2: Update (UPDATE)
-- Goal: Create a PENDING registration, then confirm it by attaching a payment.
-- Uses:
--  - Trigger: blocks confirming without Transaction_ID
--  - Assertion-equivalent: ensures confirmed has payment at COMMIT
--  - Index: idx_registration_event
-- ------------------------------------------------------------
BEGIN;

-- Create a second new attendee to avoid conflicts with existing data
INSERT INTO Attendee (Attendee_ID, Name, Institution, Email)
VALUES (12, 'Max Neumann', 'TU Hamburg', 'max.neumann@tuh.example');

-- Insert pending registration WITHOUT payment (allowed)
INSERT INTO Registration (Attendee_ID, Event_ID, Registration_Date, Status, Transaction_ID)
VALUES (12, 2, '2026-03-10', 'pending', NULL);

-- Create payment for this registration
INSERT INTO Payment (Transaction_ID, Amount, Payment_Method)
VALUES (12, 49.00, 'bank_transfer');

-- Confirm registration properly (trigger enforces non-null Transaction_ID)
UPDATE Registration
SET Status = 'confirmed',
    Transaction_ID = 12
WHERE Attendee_ID = 12
  AND Event_ID = 2;

-- Check updated row
SELECT Attendee_ID, Event_ID, Status, Transaction_ID
FROM Registration
WHERE Attendee_ID = 12 AND Event_ID = 2;

COMMIT;


-- ------------------------------------------------------------
-- Transaction 3: Deletion (DELETE) with cascade effects
-- Goal: Delete a session; cascades should remove related Feedback and Session_Equipment
-- because both reference Session with ON DELETE CASCADE.
-- Uses:
--  - View: v_session_feedback_summary
--  - Index: idx_feedback_session (lookups by (Event_ID, Topic, Start_Time))
-- ------------------------------------------------------------
BEGIN;

-- Feedback summary before deletion (view)
SELECT *
FROM v_session_feedback_summary
WHERE Event_ID = 1
ORDER BY Start_Time, Topic;

-- Show the session and its dependent rows before deletion
SELECT *
FROM Session
WHERE Event_ID = 1 AND Topic = 'Intro to Predictive Modeling' AND Start_Time = '09:00';

SELECT *
FROM Session_Equipment
WHERE Event_ID = 1 AND Topic = 'Intro to Predictive Modeling' AND Start_Time = '09:00'
ORDER BY Serial_Number;

SELECT *
FROM Feedback
WHERE Event_ID = 1 AND Topic = 'Intro to Predictive Modeling' AND Start_Time = '09:00'
ORDER BY Feedback_ID;

-- Delete the session (cascades to Session_Equipment and Feedback)
DELETE FROM Session
WHERE Event_ID = 1 AND Topic = 'Intro to Predictive Modeling' AND Start_Time = '09:00';

-- Verify cascade results (should return 0 rows)
SELECT *
FROM Session
WHERE Event_ID = 1 AND Topic = 'Intro to Predictive Modeling' AND Start_Time = '09:00';

SELECT *
FROM Session_Equipment
WHERE Event_ID = 1 AND Topic = 'Intro to Predictive Modeling' AND Start_Time = '09:00';

SELECT *
FROM Feedback
WHERE Event_ID = 1 AND Topic = 'Intro to Predictive Modeling' AND Start_Time = '09:00';

-- Feedback summary after deletion (view)
SELECT *
FROM v_session_feedback_summary
WHERE Event_ID = 1
ORDER BY Start_Time, Topic;

COMMIT;


-- ------------------------------------------------------------
-- Transaction 4: Negative test (trigger protection) WITHOUT breaking the script
-- Goal: Demonstrate that the trigger blocks confirming without payment.
-- Uses SAVEPOINT so we can recover and COMMIT cleanly.
-- ------------------------------------------------------------
BEGIN;

SAVEPOINT sp_invalid_confirm;

-- This should fail: confirmed registration without Transaction_ID
-- Trigger trg_registration_enforce_payment raises an exception.
INSERT INTO Registration (Attendee_ID, Event_ID, Registration_Date, Status, Transaction_ID)
VALUES (3, 2, '2026-03-11', 'confirmed', NULL);

-- If the INSERT fails (expected), roll back to savepoint and continue
ROLLBACK TO SAVEPOINT sp_invalid_confirm;

-- End transaction cleanly
COMMIT;
