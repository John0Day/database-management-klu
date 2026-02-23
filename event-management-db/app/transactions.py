from db import transaction, execute, fetch_all_dict


# ---------- Lookup helpers (for dropdowns) ----------

def list_events():
    with transaction() as (_, cur):
        return fetch_all_dict(cur, "SELECT Event_ID, Title FROM Event ORDER BY Event_ID;")


def list_venues():
    with transaction() as (_, cur):
        return fetch_all_dict(cur, "SELECT Venue_ID, Address, Room_Number FROM Venue ORDER BY Venue_ID;")


def list_organizers():
    with transaction() as (_, cur):
        return fetch_all_dict(cur, "SELECT Organizer_ID, Org_Name FROM Organizer ORDER BY Organizer_ID;")


def list_speakers():
    with transaction() as (_, cur):
        return fetch_all_dict(cur, "SELECT Speaker_ID, Duty FROM Speaker ORDER BY Speaker_ID;")


def list_attendees():
    with transaction() as (_, cur):
        return fetch_all_dict(cur, "SELECT Attendee_ID, Name FROM Attendee ORDER BY Attendee_ID;")


def list_sponsors():
    with transaction() as (_, cur):
        return fetch_all_dict(cur, "SELECT Sponsor_ID, Company_Name FROM Sponsor ORDER BY Sponsor_ID;")


def list_equipment():
    with transaction() as (_, cur):
        return fetch_all_dict(cur, "SELECT Serial_Number, Item_Type FROM Equipment ORDER BY Serial_Number;")


def list_staff():
    with transaction() as (_, cur):
        return fetch_all_dict(cur, "SELECT Staff_ID, First_Name, Last_Name FROM Staff ORDER BY Staff_ID;")


# ---------- Creation helpers ----------

def create_venue(venue_id: int, address: str, room_number: str, total_capacity: int):
    with transaction() as (_, cur):
        execute(
            cur,
            """
            INSERT INTO Venue (Venue_ID, Address, Room_Number, Total_Capacity)
            VALUES (%s, %s, %s, %s);
            """,
            (venue_id, address, room_number, total_capacity),
        )
    return {"venue_id": venue_id}


def create_organizer(organizer_id: int, org_name: str, contact_person: str, email: str):
    with transaction() as (_, cur):
        execute(
            cur,
            """
            INSERT INTO Organizer (Organizer_ID, Org_Name, Contact_Person, Email)
            VALUES (%s, %s, %s, %s);
            """,
            (organizer_id, org_name, contact_person, email),
        )
    return {"organizer_id": organizer_id}


def create_event(event_id: int, title: str, start_date: str, end_date: str, venue_id: int, organizer_id: int):
    with transaction() as (_, cur):
        execute(
            cur,
            """
            INSERT INTO Event (Event_ID, Title, Start_Date, End_Date, Venue_ID, Organizer_ID)
            VALUES (%s, %s, %s, %s, %s, %s);
            """,
            (event_id, title, start_date, end_date, venue_id, organizer_id),
        )
    return {"event_id": event_id}


def create_session(event_id: int, topic: str, start_time: str, speaker_id: int):
    with transaction() as (_, cur):
        execute(
            cur,
            """
            INSERT INTO Session (Event_ID, Topic, Start_Time, Speaker_ID)
            VALUES (%s, %s, %s, %s);
            """,
            (event_id, topic, start_time, speaker_id),
        )
    return {"event_id": event_id, "topic": topic, "start_time": start_time}


def register_attendee(attendee_id: int, event_id: int, registration_date: str, status: str = "pending"):
    with transaction() as (_, cur):
        execute(
            cur,
            """
            INSERT INTO Registration (Attendee_ID, Event_ID, Registration_Date, Status, Transaction_ID)
            VALUES (%s, %s, %s, %s, NULL);
            """,
            (attendee_id, event_id, registration_date, status),
        )

        row = fetch_all_dict(
            cur,
            """
            SELECT Attendee_ID, Event_ID, Registration_Date, Status
            FROM Registration
            WHERE Attendee_ID = %s AND Event_ID = %s;
            """,
            (attendee_id, event_id),
        )
        return {"registration": row}


def create_attendee(attendee_id: int, name: str, institution: str, email: str):
    with transaction() as (_, cur):
        execute(
            cur,
            """
            INSERT INTO Attendee (Attendee_ID, Name, Institution, Email)
            VALUES (%s, %s, %s, %s);
            """,
            (attendee_id, name, institution, email),
        )
    return {"attendee_id": attendee_id}


def create_sponsor(sponsor_id: int, company_name: str, contact_info: str):
    with transaction() as (_, cur):
        execute(
            cur,
            """
            INSERT INTO Sponsor (Sponsor_ID, Company_Name, Contact_Info)
            VALUES (%s, %s, %s);
            """,
            (sponsor_id, company_name, contact_info),
        )
    return {"sponsor_id": sponsor_id}


def create_equipment(serial_number: str, item_type: str):
    with transaction() as (_, cur):
        execute(
            cur,
            """
            INSERT INTO Equipment (Serial_Number, Item_Type)
            VALUES (%s, %s);
            """,
            (serial_number, item_type),
        )
    return {"serial_number": serial_number}


def create_staff(staff_id: int, first_name: str, last_name: str, role: str, shift_time: str):
    with transaction() as (_, cur):
        execute(
            cur,
            """
            INSERT INTO Staff (Staff_ID, First_Name, Last_Name, Role, Shift_Time)
            VALUES (%s, %s, %s, %s, %s);
            """,
            (staff_id, first_name, last_name, role, shift_time),
        )
    return {"staff_id": staff_id}


def create_speaker(speaker_id: int, shift_start: str, shift_end: str, duty: str):
    with transaction() as (_, cur):
        execute(
            cur,
            """
            INSERT INTO Speaker (Speaker_ID, Shift_Start, Shift_End, Duty)
            VALUES (%s, %s, %s, %s);
            """,
            (speaker_id, shift_start, shift_end, duty),
        )
    return {"speaker_id": speaker_id}

def tx1_inclusion(event_id=1, attendee_id=11, tx_id=11):
    with transaction() as (_, cur):
        overview = fetch_all_dict(
            cur,
            "SELECT * FROM v_event_overview WHERE Event_ID = %s;",
            (event_id,),
        )

        execute(
            cur,
            """
            INSERT INTO Attendee (Attendee_ID, Name, Institution, Email)
            VALUES (%s, %s, %s, %s);
            """,
            (attendee_id, "Clara Sommer", "HS Munich", f"clara.sommer{attendee_id}@hsm.example"),
        )

        execute(
            cur,
            """
            INSERT INTO Payment (Transaction_ID, Amount, Payment_Method)
            VALUES (%s, %s, %s);
            """,
            (tx_id, 79.00, "card"),
        )

        execute(
            cur,
            """
            INSERT INTO Registration (Attendee_ID, Event_ID, Registration_Date, Status, Transaction_ID)
            VALUES (%s, %s, %s, %s, %s);
            """,
            (attendee_id, event_id, "2026-03-03", "confirmed", tx_id),
        )

        regs = fetch_all_dict(
            cur,
            """
            SELECT Attendee_ID, Event_ID, Status, Transaction_ID
            FROM Registration
            WHERE Event_ID = %s
            ORDER BY Attendee_ID;
            """,
            (event_id,),
        )
        return {"event_overview": overview, "registrations": regs}

def tx2_update(attendee_id=2, event_id=2, tx_id=12):
    with transaction() as (_, cur):
        execute(
            cur,
            """
            INSERT INTO Payment (Transaction_ID, Amount, Payment_Method)
            VALUES (%s, %s, %s);
            """,
            (tx_id, 49.00, "bank_transfer"),
        )

        execute(
            cur,
            """
            INSERT INTO Registration (Attendee_ID, Event_ID, Registration_Date, Status, Transaction_ID)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (Attendee_ID, Event_ID) DO NOTHING;
            """,
            (attendee_id, event_id, "2026-03-10", "pending", None),
        )

        execute(
            cur,
            """
            UPDATE Registration
            SET Status = 'confirmed',
                Transaction_ID = %s
            WHERE Attendee_ID = %s
              AND Event_ID = %s;
            """,
            (tx_id, attendee_id, event_id),
        )

        row = fetch_all_dict(
            cur,
            """
            SELECT Attendee_ID, Event_ID, Status, Transaction_ID
            FROM Registration
            WHERE Attendee_ID = %s AND Event_ID = %s;
            """,
            (attendee_id, event_id),
        )
        return {"updated_registration": row}

def tx3_deletion(event_id=1, topic="Intro to Predictive Modeling", start_time="09:00"):
    with transaction() as (_, cur):
        before_summary = fetch_all_dict(
            cur,
            """
            SELECT *
            FROM v_session_feedback_summary
            WHERE Event_ID = %s
            ORDER BY Start_Time, Topic;
            """,
            (event_id,),
        )

        session_before = fetch_all_dict(
            cur,
            """
            SELECT *
            FROM Session
            WHERE Event_ID = %s AND Topic = %s AND Start_Time = %s;
            """,
            (event_id, topic, start_time),
        )

        equip_before = fetch_all_dict(
            cur,
            """
            SELECT *
            FROM Session_Equipment
            WHERE Event_ID = %s AND Topic = %s AND Start_Time = %s
            ORDER BY Serial_Number;
            """,
            (event_id, topic, start_time),
        )

        feedback_before = fetch_all_dict(
            cur,
            """
            SELECT *
            FROM Feedback
            WHERE Event_ID = %s AND Topic = %s AND Start_Time = %s
            ORDER BY Feedback_ID;
            """,
            (event_id, topic, start_time),
        )

        execute(
            cur,
            """
            DELETE FROM Session
            WHERE Event_ID = %s AND Topic = %s AND Start_Time = %s;
            """,
            (event_id, topic, start_time),
        )

        session_after = fetch_all_dict(
            cur,
            """
            SELECT *
            FROM Session
            WHERE Event_ID = %s AND Topic = %s AND Start_Time = %s;
            """,
            (event_id, topic, start_time),
        )

        equip_after = fetch_all_dict(
            cur,
            """
            SELECT *
            FROM Session_Equipment
            WHERE Event_ID = %s AND Topic = %s AND Start_Time = %s;
            """,
            (event_id, topic, start_time),
        )

        feedback_after = fetch_all_dict(
            cur,
            """
            SELECT *
            FROM Feedback
            WHERE Event_ID = %s AND Topic = %s AND Start_Time = %s;
            """,
            (event_id, topic, start_time),
        )

        after_summary = fetch_all_dict(
            cur,
            """
            SELECT *
            FROM v_session_feedback_summary
            WHERE Event_ID = %s
            ORDER BY Start_Time, Topic;
            """,
            (event_id,),
        )

        return {
            "before_summary": before_summary,
            "session_before": session_before,
            "equip_before": equip_before,
            "feedback_before": feedback_before,
            "session_after": session_after,
            "equip_after": equip_after,
            "feedback_after": feedback_after,
            "after_summary": after_summary,
        }

def tx4_negative_test(attendee_id=3, event_id=2):
    with transaction() as (_, cur):
        execute(
            cur,
            """
            INSERT INTO Registration (Attendee_ID, Event_ID, Registration_Date, Status, Transaction_ID)
            VALUES (%s, %s, %s, %s, %s);
            """,
            (attendee_id, event_id, "2026-03-11", "confirmed", None),
        )
        return {"status": "unexpected_success"}


def tx5_add_sponsor_to_event(event_id=1, sponsor_id=1, level="Gold", amount=5000.00):
    """Insert or update a sponsor assignment for an event."""
    with transaction() as (_, cur):
        execute(
            cur,
            """
            INSERT INTO Event_Sponsor (Event_ID, Sponsor_ID, Sponsorship_Level, Contribution_Amount)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (Event_ID, Sponsor_ID)
            DO UPDATE SET
              Sponsorship_Level = EXCLUDED.Sponsorship_Level,
              Contribution_Amount = EXCLUDED.Contribution_Amount;
            """,
            (event_id, sponsor_id, level, amount),
        )

        rows = fetch_all_dict(
            cur,
            """
            SELECT Event_ID, Sponsor_ID, Sponsorship_Level, Contribution_Amount
            FROM Event_Sponsor
            WHERE Event_ID = %s
            ORDER BY Sponsor_ID;
            """,
            (event_id,),
        )
        return {"event_sponsors": rows}



def tx6_assign_equipment_to_session(
    event_id=1,
    topic="Intro to Predictive Modeling",
    start_time="09:00",
    serial_number="EQ-1001",
):
    """Assign a piece of equipment to a session (idempotent)."""
    with transaction() as (_, cur):
        execute(
            cur,
            """
            INSERT INTO Session_Equipment (Event_ID, Topic, Start_Time, Serial_Number)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (Event_ID, Topic, Start_Time, Serial_Number) DO NOTHING;
            """,
            (event_id, topic, start_time, serial_number),
        )

        rows = fetch_all_dict(
            cur,
            """
            SELECT se.Event_ID, se.Topic, se.Start_Time, se.Serial_Number, e.Item_Type
            FROM Session_Equipment se
            JOIN Equipment e ON e.Serial_Number = se.Serial_Number
            WHERE se.Event_ID = %s AND se.Topic = %s AND se.Start_Time = %s
            ORDER BY se.Serial_Number;
            """,
            (event_id, topic, start_time),
        )
        return {"session_equipment": rows}



def tx7_submit_feedback(
    feedback_id=200,
    event_id=1,
    topic="Intro to Predictive Modeling",
    start_time="09:00",
    rating=5,
    comments="Great session",
):
    """Insert feedback for a session and show updated aggregation via the view."""
    with transaction() as (_, cur):
        execute(
            cur,
            """
            INSERT INTO Feedback (Feedback_ID, Event_ID, Topic, Start_Time, Rating, Comments)
            VALUES (%s, %s, %s, %s, %s, %s);
            """,
            (feedback_id, event_id, topic, start_time, rating, comments),
        )

        summary = fetch_all_dict(
            cur,
            """
            SELECT *
            FROM v_session_feedback_summary
            WHERE Event_ID = %s AND Topic = %s AND Start_Time = %s;
            """,
            (event_id, topic, start_time),
        )

        latest = fetch_all_dict(
            cur,
            """
            SELECT Feedback_ID, Rating, Comments
            FROM Feedback
            WHERE Event_ID = %s AND Topic = %s AND Start_Time = %s
            ORDER BY Feedback_ID DESC
            LIMIT 10;
            """,
            (event_id, topic, start_time),
        )

        return {"feedback_summary": summary, "latest_feedback": latest}



def tx8_assign_staff_to_event(event_id=1, staff_id=1):
    """Assign staff to an event (idempotent)."""
    with transaction() as (_, cur):
        execute(
            cur,
            """
            INSERT INTO Event_Staff (Event_ID, Staff_ID)
            VALUES (%s, %s)
            ON CONFLICT (Event_ID, Staff_ID) DO NOTHING;
            """,
            (event_id, staff_id),
        )

        rows = fetch_all_dict(
            cur,
            """
            SELECT es.Event_ID, s.Staff_ID, s.First_Name, s.Last_Name, s.Role, s.Shift_Time
            FROM Event_Staff es
            JOIN Staff s ON s.Staff_ID = es.Staff_ID
            WHERE es.Event_ID = %s
            ORDER BY s.Staff_ID;
            """,
            (event_id,),
        )
        return {"event_staff": rows}
