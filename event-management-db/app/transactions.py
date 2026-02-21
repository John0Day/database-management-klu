from db import transaction, execute, fetch_all_dict

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