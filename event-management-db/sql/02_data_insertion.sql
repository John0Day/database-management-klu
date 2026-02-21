-- ============================================================
-- data_insertion.sql
-- Inserts: at least 10 tuples per relation (all tables in this schema)
-- Target DBMS: PostgreSQL
-- ============================================================

BEGIN;

-- -------------------------
-- Venue (10)
-- -------------------------
INSERT INTO Venue (Venue_ID, Address, Room_Number, Total_Capacity) VALUES
(1,  'Hamburg, Campus Center',        'A101', 250),
(2,  'Hamburg, Tech Park',            'B210', 180),
(3,  'Berlin, Conference Hall',       'C12',  400),
(4,  'Munich, Expo Center',           'M3',   600),
(5,  'Cologne, Rhine Venue',          'R8',   300),
(6,  'Frankfurt, Skyline Rooms',      'S5',   220),
(7,  'Stuttgart, Innovation Hub',     'I2',   160),
(8,  'Dresden, Science Forum',        'F1',   200),
(9,  'Leipzig, City Congress',        'L7',   280),
(10, 'Bremen, Harbor Center',         'H4',   190);

-- -------------------------
-- Organizer (10)
-- -------------------------
INSERT INTO Organizer (Organizer_ID, Org_Name, Contact_Person, Email) VALUES
(1,  'KLU Events Office',     'Anna Keller',     'anna.keller@klu.example'),
(2,  'Tech Society',          'Markus Hahn',     'markus.hahn@techsoc.example'),
(3,  'Data Science Circle',   'Lena Vogt',       'lena.vogt@dsc.example'),
(4,  'Business Forum',        'Tom Berger',      'tom.berger@bizforum.example'),
(5,  'AI Network',            'Sara Winter',     'sara.winter@ainet.example'),
(6,  'Operations Group',      'Nils Brandt',     'nils.brandt@opsgrp.example'),
(7,  'Research Council',      'Eva Stein',       'eva.stein@research.example'),
(8,  'Industry Alliance',     'Jonas Meier',     'jonas.meier@industry.example'),
(9,  'Finance Summit Team',   'Mira Scholz',     'mira.scholz@fin.example'),
(10, 'Sustainability Office', 'Paul Neumann',    'paul.neumann@sustain.example');

-- -------------------------
-- Attendee (10)
-- -------------------------
INSERT INTO Attendee (Attendee_ID, Name, Institution, Email) VALUES
(1,  'John Fischer',   'KLU',           'john.fischer@klu.example'),
(2,  'Mila Braun',     'TU Berlin',     'mila.braun@tub.example'),
(3,  'Noah Wagner',    'LMU Munich',    'noah.wagner@lmu.example'),
(4,  'Sofia Hoffmann', 'Uni Hamburg',   'sofia.hoffmann@uhh.example'),
(5,  'Lukas Becker',   'Uni Cologne',   'lukas.becker@uk.example'),
(6,  'Emma Schäfer',   'Goethe Uni',    'emma.schaefer@gu.example'),
(7,  'Ben Krüger',     'KIT',           'ben.krueger@kit.example'),
(8,  'Lea Richter',    'TU Dresden',    'lea.richter@tud.example'),
(9,  'Paul Koch',      'Uni Leipzig',   'paul.koch@ul.example'),
(10, 'Hanna Bauer',    'Uni Bremen',    'hanna.bauer@ub.example');

-- -------------------------
-- Speaker (10)
-- -------------------------
INSERT INTO Speaker (Speaker_ID, Shift_Start, Shift_End, Duty) VALUES
(1,  '08:00', '12:00', 'Keynote'),
(2,  '09:00', '13:00', 'Workshop lead'),
(3,  '10:00', '14:00', 'Panelist'),
(4,  '11:00', '15:00', 'Talk'),
(5,  '12:00', '16:00', 'Talk'),
(6,  '13:00', '17:00', 'Panelist'),
(7,  '14:00', '18:00', 'Workshop lead'),
(8,  '08:30', '12:30', 'Talk'),
(9,  '09:30', '13:30', 'Talk'),
(10, '10:30', '14:30', 'Keynote');

-- -------------------------
-- Staff (10)
-- -------------------------
INSERT INTO Staff (Staff_ID, First_Name, Last_Name, Role, Shift_Time) VALUES
(1,  'Lara',  'Klein',   'Check-in',      '08:00-12:00'),
(2,  'Tim',   'Schmidt', 'AV Support',    '09:00-17:00'),
(3,  'Nina',  'Fischer', 'Security',      '08:00-18:00'),
(4,  'Omar',  'Ali',     'Logistics',     '07:00-15:00'),
(5,  'Maja',  'Weber',   'Stage Manager', '10:00-18:00'),
(6,  'Jan',   'Krause',  'Runner',        '09:00-16:00'),
(7,  'Ella',  'König',   'Helpdesk',      '08:30-14:30'),
(8,  'Felix', 'Hart',    'AV Support',    '10:00-18:00'),
(9,  'Ida',   'Seidel',  'Check-in',      '07:30-11:30'),
(10, 'Kai',   'Vogel',   'Security',      '12:00-20:00');

-- -------------------------
-- Equipment (10)
-- -------------------------
INSERT INTO Equipment (Serial_Number, Item_Type) VALUES
('EQ-1001', 'Projector'),
('EQ-1002', 'Microphone'),
('EQ-1003', 'Speaker System'),
('EQ-1004', 'Laptop'),
('EQ-1005', 'Laser Pointer'),
('EQ-1006', 'Camera'),
('EQ-1007', 'Mixer'),
('EQ-1008', 'HDMI Switch'),
('EQ-1009', 'Lighting Kit'),
('EQ-1010', 'Wireless Router');

-- -------------------------
-- Sponsor (10)
-- -------------------------
INSERT INTO Sponsor (Sponsor_ID, Company_Name, Contact_Info) VALUES
(1,  'DataCorp',       'sponsor@datacorp.example'),
(2,  'CloudNine',      'contact@cloudnine.example'),
(3,  'FinEdge',        'partners@finedge.example'),
(4,  'GreenLogix',     'hello@greenlogix.example'),
(5,  'AutoML Works',   'biz@automlworks.example'),
(6,  'SecureStack',    'bd@securestack.example'),
(7,  'QuantIQ',        'team@quantiq.example'),
(8,  'OpsFlow',        'sponsorship@opsflow.example'),
(9,  'VisionAI',       'alliances@visionai.example'),
(10, 'SupplyNet',      'partner@supplynet.example');

-- -------------------------
-- Payment (10)
-- -------------------------
INSERT INTO Payment (Transaction_ID, Amount, Payment_Method) VALUES
(1,  49.00,  'card'),
(2,  79.00,  'card'),
(3,  99.00,  'bank_transfer'),
(4,  59.00,  'card'),
(5,  129.00, 'bank_transfer'),
(6,  39.00,  'cash'),
(7,  89.00,  'card'),
(8,  109.00, 'bank_transfer'),
(9,  69.00,  'card'),
(10, 149.00, 'bank_transfer');

-- -------------------------
-- Event (10)
-- -------------------------
INSERT INTO Event (Event_ID, Title, Start_Date, End_Date, Venue_ID, Organizer_ID) VALUES
(1,  'Applied Analytics Summit',     '2026-03-10', '2026-03-12', 1,  3),
(2,  'Operations Excellence Day',    '2026-03-18', '2026-03-18', 2,  6),
(3,  'AI Governance Forum',          '2026-04-02', '2026-04-03', 3,  5),
(4,  'Finance & Risk Conference',    '2026-04-20', '2026-04-22', 6,  9),
(5,  'Sustainable Supply Chains',    '2026-05-05', '2026-05-06', 5,  10),
(6,  'Cloud Architecture Workshop',  '2026-05-12', '2026-05-12', 4,  2),
(7,  'Industry Research Symposium',  '2026-05-20', '2026-05-21', 7,  7),
(8,  'Security Engineering Meetup',  '2026-06-03', '2026-06-03', 6,  6),
(9,  'Computer Vision Days',         '2026-06-10', '2026-06-11', 8,  8),
(10, 'Logistics Innovation Forum',   '2026-06-18', '2026-06-19', 10, 1);

-- -------------------------
-- Session (>=10, here 10)
-- -------------------------
INSERT INTO Session (Event_ID, Topic, Start_Time, Speaker_ID) VALUES
(1,  'Intro to Predictive Modeling', '09:00', 2),
(1,  'Data Pipelines at Scale',      '11:00', 7),
(2,  'Lean Process Mapping',         '10:00', 4),
(3,  'Policy and Compliance',        '09:30', 10),
(3,  'Model Risk Management',        '11:30', 3),
(4,  'Credit Risk Analytics',        '09:00', 9),
(5,  'Carbon Accounting',            '10:30', 8),
(6,  'Kubernetes Patterns',          '09:00', 1),
(9,  'Vision Transformers',          '11:00', 5),
(10, 'Warehouse Optimization',       '13:00', 6);

-- -------------------------
-- Registration (10)
-- Ensure confirmed has Transaction_ID (trigger + assertion)
-- -------------------------
INSERT INTO Registration (Attendee_ID, Event_ID, Registration_Date, Status, Transaction_ID) VALUES
(1,  1,  '2026-03-01', 'confirmed', 1),
(2,  1,  '2026-03-02', 'confirmed', 2),
(3,  3,  '2026-03-20', 'confirmed', 3),
(4,  4,  '2026-04-01', 'confirmed', 4),
(5,  5,  '2026-04-20', 'confirmed', 5),
(6,  6,  '2026-05-01', 'confirmed', 6),
(7,  7,  '2026-05-10', 'confirmed', 7),
(8,  8,  '2026-05-25', 'confirmed', 8),
(9,  9,  '2026-05-30', 'confirmed', 9),
(10, 10, '2026-06-05', 'confirmed', 10);

-- -------------------------
-- Event_Sponsor (10)
-- -------------------------
INSERT INTO Event_Sponsor (Event_ID, Sponsor_ID, Sponsorship_Level, Contribution_Amount) VALUES
(1,  1,  'Gold',   5000.00),
(2,  2,  'Silver', 2500.00),
(3,  3,  'Gold',   6000.00),
(4,  4,  'Bronze', 1200.00),
(5,  5,  'Silver', 3000.00),
(6,  6,  'Gold',   5500.00),
(7,  7,  'Bronze', 1500.00),
(8,  8,  'Silver', 2800.00),
(9,  9,  'Gold',   7000.00),
(10, 10, 'Bronze', 1100.00);

-- -------------------------
-- Event_Staff (10)
-- -------------------------
INSERT INTO Event_Staff (Event_ID, Staff_ID) VALUES
(1,  1),
(1,  2),
(2,  3),
(3,  4),
(4,  5),
(5,  6),
(6,  7),
(7,  8),
(8,  9),
(10, 10);

-- -------------------------
-- Session_Equipment (10)
-- -------------------------
INSERT INTO Session_Equipment (Event_ID, Topic, Start_Time, Serial_Number) VALUES
(1,  'Intro to Predictive Modeling', '09:00', 'EQ-1001'),
(1,  'Intro to Predictive Modeling', '09:00', 'EQ-1002'),
(1,  'Data Pipelines at Scale',      '11:00', 'EQ-1003'),
(2,  'Lean Process Mapping',         '10:00', 'EQ-1004'),
(3,  'Policy and Compliance',        '09:30', 'EQ-1006'),
(3,  'Model Risk Management',        '11:30', 'EQ-1007'),
(4,  'Credit Risk Analytics',        '09:00', 'EQ-1008'),
(5,  'Carbon Accounting',            '10:30', 'EQ-1009'),
(6,  'Kubernetes Patterns',          '09:00', 'EQ-1010'),
(10, 'Warehouse Optimization',       '13:00', 'EQ-1005');

-- -------------------------
-- Feedback (10)
-- -------------------------
INSERT INTO Feedback (Feedback_ID, Event_ID, Topic, Start_Time, Rating, Comments) VALUES
(1,  1,  'Intro to Predictive Modeling', '09:00', 5, 'Clear structure and useful examples.'),
(2,  1,  'Intro to Predictive Modeling', '09:00', 4, 'Good pace, minor Q&A time shortage.'),
(3,  1,  'Data Pipelines at Scale',      '11:00', 5, 'Strong practical insights.'),
(4,  2,  'Lean Process Mapping',         '10:00', 4, 'Solid overview, could add more cases.'),
(5,  3,  'Policy and Compliance',        '09:30', 3, 'Content ok, delivery could improve.'),
(6,  3,  'Model Risk Management',        '11:30', 5, 'Excellent depth, well explained.'),
(7,  4,  'Credit Risk Analytics',        '09:00', 4, 'Relevant content for practitioners.'),
(8,  5,  'Carbon Accounting',            '10:30', 5, 'Very actionable, good references.'),
(9,  6,  'Kubernetes Patterns',          '09:00', 4, 'Nice patterns, more demos desired.'),
(10, 10, 'Warehouse Optimization',       '13:00', 5, 'Great optimization framing and steps.');

COMMIT;