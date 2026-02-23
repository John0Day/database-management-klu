import streamlit as st
import pandas as pd
from db import transaction, fetch_all_dict
from psycopg2 import OperationalError, IntegrityError
from transactions import (
    tx1_inclusion,
    tx2_update,
    tx3_deletion,
    tx4_negative_test,
    tx5_add_sponsor_to_event,
    tx6_assign_equipment_to_session,
    tx7_submit_feedback,
    tx8_assign_staff_to_event,
    create_venue,
    create_organizer,
    create_event,
    create_session,
    register_attendee,
    create_attendee,
    create_sponsor,
    create_equipment,
    create_staff,
    create_speaker,
    list_events,
    list_venues,
    list_organizers,
    list_speakers,
    list_attendees,
    list_sponsors,
    list_equipment,
    list_staff,
)

st.set_page_config(page_title="Event DB App", layout="wide")

st.title("Event Management DB Application")
st.caption("Runs database transactions via buttons, connected to PostgreSQL.")

with st.sidebar:
    st.header("Master data")

    st.subheader("Create venue")
    v_id = st.number_input("Venue_ID", min_value=1, value=1, step=1, key="venue_id")
    v_addr = st.text_input("Address", value="123 Main St", key="venue_address")
    v_room = st.text_input("Room_Number", value="Room 101", key="venue_room")
    v_cap = st.number_input("Total_Capacity", min_value=1, value=100, step=1, key="venue_cap")
    if st.button("Create venue", use_container_width=True):
        try:
            res = create_venue(v_id, v_addr, v_room, v_cap)
            st.success("Venue created.")
            st.json(res)
        except Exception as e:
            st.error(f"Error: {e}")

    st.subheader("Create organizer")
    o_id = st.number_input("Organizer_ID", min_value=1, value=1, step=1, key="org_id")
    o_name = st.text_input("Org_Name", value="DataConf GmbH", key="org_name")
    o_contact = st.text_input("Contact_Person", value="Alex Example", key="org_contact")
    o_email = st.text_input("Email", value="contact@example.com", key="org_email")
    if st.button("Create organizer", use_container_width=True):
        try:
            res = create_organizer(o_id, o_name, o_contact, o_email)
            st.success("Organizer created.")
            st.json(res)
        except Exception as e:
            st.error(f"Error: {e}")

    st.subheader("Create attendee")
    a_id = st.number_input("Attendee_ID", min_value=1, value=100, step=1, key="att_id")
    a_name = st.text_input("Name", value="Jamie Demo", key="att_name")
    a_inst = st.text_input("Institution", value="Demo Univ", key="att_inst")
    a_mail = st.text_input("Email", value="jamie@example.com", key="att_email")
    if st.button("Create attendee", use_container_width=True):
        try:
            res = create_attendee(a_id, a_name, a_inst, a_mail)
            st.success("Attendee created.")
            st.json(res)
        except Exception as e:
            st.error(f"Error: {e}")

    st.subheader("Create speaker")
    sp_id = st.number_input("Speaker_ID", min_value=1, value=10, step=1, key="sp_id")
    sp_start = st.text_input("Shift_Start (HH:MM)", value="09:00", key="sp_start")
    sp_end = st.text_input("Shift_End (HH:MM)", value="12:00", key="sp_end")
    sp_duty = st.text_input("Duty", value="Keynote", key="sp_duty")
    if st.button("Create speaker", use_container_width=True):
        try:
            res = create_speaker(sp_id, sp_start, sp_end, sp_duty)
            st.success("Speaker created.")
            st.json(res)
        except Exception as e:
            st.error(f"Error: {e}")

    st.subheader("Create sponsor")
    s_id = st.number_input("Sponsor_ID", min_value=1, value=1, step=1, key="s_id")
    s_name = st.text_input("Company_Name", value="ACME Corp", key="s_name")
    s_contact = st.text_input("Contact_Info", value="acme@example.com", key="s_contact")
    if st.button("Create sponsor", use_container_width=True):
        try:
            res = create_sponsor(s_id, s_name, s_contact)
            st.success("Sponsor created.")
            st.json(res)
        except Exception as e:
            st.error(f"Error: {e}")

    st.subheader("Create equipment")
    eq_sn = st.text_input("Serial_Number", value="EQ-2000", key="eq_sn")
    eq_type = st.text_input("Item_Type", value="Projector", key="eq_type")
    if st.button("Create equipment", use_container_width=True):
        try:
            res = create_equipment(eq_sn, eq_type)
            st.success("Equipment created.")
            st.json(res)
        except Exception as e:
            st.error(f"Error: {e}")

    st.subheader("Create staff")
    st_id = st.number_input("Staff_ID", min_value=1, value=1, step=1, key="st_id")
    st_fn = st.text_input("First_Name", value="Sam", key="st_fn")
    st_ln = st.text_input("Last_Name", value="Smith", key="st_ln")
    st_role = st.text_input("Role", value="Usher", key="st_role")
    st_shift = st.text_input("Shift_Time", value="Morning", key="st_shift")
    if st.button("Create staff", use_container_width=True):
        try:
            res = create_staff(st_id, st_fn, st_ln, st_role, st_shift)
            st.success("Staff created.")
            st.json(res)
        except Exception as e:
            st.error(f"Error: {e}")

    st.divider()
    st.header("Transactions (inputs)")

    with st.expander("Create paid registration", expanded=False):
        tx1_event_id = st.number_input("Event_ID", min_value=1, value=1, step=1, key="tx1_event")
        tx1_attendee_id = st.number_input("New Attendee_ID", min_value=1, value=100, step=1, key="tx1_att")
        tx1_payment_id = st.number_input("New Transaction_ID", min_value=1, value=100, step=1, key="tx1_pay")

    with st.expander("Confirm existing registration", expanded=False):
        tx2_attendee_id = st.number_input("Attendee_ID", min_value=1, value=2, step=1, key="tx2_att")
        tx2_event_id = st.number_input("Event_ID", min_value=1, value=2, step=1, key="tx2_event")
        tx2_payment_id = st.number_input("New Transaction_ID", min_value=1, value=101, step=1, key="tx2_pay")

    with st.expander("Delete session (cascade)", expanded=False):
        tx3_event_id = st.number_input("Event_ID", min_value=1, value=1, step=1, key="tx3_event")
        tx3_topic = st.text_input("Topic", value="Intro to Predictive Modeling", key="tx3_topic")
        tx3_start_time = st.text_input("Start_Time (HH:MM)", value="09:00", key="tx3_start")

    with st.expander("Trigger test (invalid confirmation)", expanded=False):
        tx4_attendee_id = st.number_input("Attendee_ID", min_value=1, value=3, step=1, key="tx4_att")
        tx4_event_id = st.number_input("Event_ID", min_value=1, value=2, step=1, key="tx4_event")

    with st.expander("Add sponsor to event", expanded=False):
        tx5_event_id = st.number_input("Event_ID", min_value=1, value=1, step=1, key="tx5_event")
        tx5_sponsor_id = st.number_input("Sponsor_ID", min_value=1, value=1, step=1, key="tx5_sponsor")
        tx5_level = st.selectbox("Sponsorship_Level", ["Gold", "Silver", "Bronze"], index=0, key="tx5_level")
        tx5_amount = st.number_input("Contribution_Amount", min_value=0.0, value=5000.0, step=100.0, key="tx5_amount")

    with st.expander("Assign equipment to session", expanded=False):
        tx6_event_id = st.number_input("Event_ID", min_value=1, value=1, step=1, key="tx6_event")
        tx6_topic = st.text_input("Topic", value="Intro to Predictive Modeling", key="tx6_topic")
        tx6_start_time = st.text_input("Start_Time (HH:MM)", value="09:00", key="tx6_start")
        tx6_serial = st.text_input("Serial_Number", value="EQ-1001", key="tx6_serial")

    with st.expander("Submit session feedback", expanded=False):
        tx7_feedback_id = st.number_input("New Feedback_ID", min_value=1, value=200, step=1, key="tx7_feedback")
        tx7_event_id = st.number_input("Event_ID", min_value=1, value=1, step=1, key="tx7_event")
        tx7_topic = st.text_input("Topic", value="Intro to Predictive Modeling", key="tx7_topic")
        tx7_start_time = st.text_input("Start_Time (HH:MM)", value="09:00", key="tx7_start")
        tx7_rating = st.slider("Rating", min_value=1, max_value=5, value=5, step=1, key="tx7_rating")
        tx7_comments = st.text_area("Comments", value="Clear structure and useful examples.", key="tx7_comments")

    with st.expander("Assign staff to event", expanded=False):
        tx8_event_id = st.number_input("Event_ID", min_value=1, value=1, step=1, key="tx8_event")
        tx8_staff_id = st.number_input("Staff_ID", min_value=1, value=1, step=1, key="tx8_staff")

st.divider()
# Event creation and session creation
venues = list_venues()
organizers = list_organizers()
events = list_events()
speakers = list_speakers()
attendees = list_attendees()

colA, colB = st.columns(2)
with colA:
    st.subheader("Create event")
    ev_id = st.number_input("Event_ID", min_value=1, value=10, step=1, key="ev_id")
    ev_title = st.text_input("Title", value="AI Summit", key="ev_title")
    ev_start = st.date_input("Start_Date", key="ev_start")
    ev_end = st.date_input("End_Date", key="ev_end")

    venue_opts = [v["venue_id"] for v in venues]
    org_opts = [o["organizer_id"] for o in organizers]

    if not venue_opts:
        st.info("No venue available. Please create one first.")
    if not org_opts:
        st.info("No organizer available. Please create one first.")

    venue_choice = st.selectbox(
        "Venue_ID",
        options=venue_opts if venue_opts else ["-"],
        format_func=lambda vid: "Please create a venue" if vid == "-" else f"{vid} - {next((v['address'] for v in venues if v['venue_id']==vid), vid)}",
        disabled=not bool(venue_opts),
    )
    org_choice = st.selectbox(
        "Organizer_ID",
        options=org_opts if org_opts else ["-"],
        format_func=lambda oid: "Please create an organizer" if oid == "-" else f"{oid} - {next((o['org_name'] for o in organizers if o['organizer_id']==oid), oid)}",
        disabled=not bool(org_opts),
    )
    if st.button("Create event", use_container_width=True, disabled=not (venue_opts and org_opts)):
        try:
            res = create_event(ev_id, ev_title, str(ev_start), str(ev_end), int(venue_choice), int(org_choice))
            st.success("Event created.")
            st.json(res)
        except Exception as e:
            st.error(f"Error: {e}")

with colB:
    st.subheader("Create session")
    event_opts = [e["event_id"] for e in events]
    speaker_opts = [s["speaker_id"] for s in speakers]

    if not event_opts:
        st.info("No event available. Please create one first.")
    if not speaker_opts:
        st.info("No speaker available. Please create one first.")

    sess_event = st.selectbox(
        "Event_ID",
        options=event_opts if event_opts else ["-"],
        format_func=lambda eid: "Please create an event" if eid == "-" else f"{eid} - {next((e['title'] for e in events if e['event_id']==eid), eid)}",
        key="sess_event",
        disabled=not bool(event_opts),
    )
    sess_topic = st.text_input("Topic", value="Data Pipelines", key="sess_topic")
    sess_start = st.text_input("Start_Time (HH:MM)", value="10:00", key="sess_start")
    speaker_choice = st.selectbox(
        "Speaker_ID",
        options=speaker_opts if speaker_opts else ["-"],
        format_func=lambda sid: "Please create a speaker" if sid == "-" else f"{sid} - {next((s['duty'] for s in speakers if s['speaker_id']==sid), sid)}",
        key="sess_speaker",
        disabled=not bool(speaker_opts),
    )
    if st.button("Create session", use_container_width=True, disabled=not (event_opts and speaker_opts)):
        try:
            res = create_session(int(sess_event), sess_topic, sess_start, int(speaker_choice))
            st.success("Session created.")
            st.json(res)
        except Exception as e:
            st.error(f"Error: {e}")

st.subheader("Register attendee (pending)")
reg_col1, reg_col2 = st.columns(2)
with reg_col1:
    reg_att_opts = [a["attendee_id"] for a in attendees]
    reg_event_opts = [e["event_id"] for e in events]

    if not reg_att_opts:
        st.info("No attendee available. Please create one first.")
    if not reg_event_opts:
        st.info("No event available. Please create one first.")

    reg_att = st.selectbox(
        "Attendee_ID",
        options=reg_att_opts if reg_att_opts else ["-"],
        format_func=lambda aid: "Please create an attendee" if aid == "-" else f"{aid} - {next((a['name'] for a in attendees if a['attendee_id']==aid), aid)}",
        key="reg_attendee",
        disabled=not bool(reg_att_opts),
    )
    reg_event = st.selectbox(
        "Event_ID",
        options=reg_event_opts if reg_event_opts else ["-"],
        format_func=lambda eid: "Please create an event" if eid == "-" else f"{eid} - {next((e['title'] for e in events if e['event_id']==eid), eid)}",
        key="reg_event",
        disabled=not bool(reg_event_opts),
    )
with reg_col2:
    reg_date = st.date_input("Registration_Date", key="reg_date")
    reg_status = st.selectbox("Status", ["pending", "confirmed", "cancelled"], index=0, key="reg_status")

if st.button("Register attendee", use_container_width=True, disabled=not (reg_att_opts and reg_event_opts)):
    try:
        res = register_attendee(int(reg_att), int(reg_event), str(reg_date), reg_status)
        st.success("Registration saved.")
        st.json(res)
    except (OperationalError, IntegrityError) as e:
        st.error(f"Transaction failed, {e}")
    except Exception as e:
        st.error(f"Transaction failed, {e}")

st.divider()
st.header("Transactions")

def show_result(title, obj):
    st.subheader(title)
    if isinstance(obj, list):
        if len(obj) == 0:
            st.info("No rows.")
        else:
            st.dataframe(pd.DataFrame(obj), use_container_width=True)
    elif isinstance(obj, dict):
        for k, v in obj.items():
            st.markdown(f"#### {k}")
            if isinstance(v, list):
                if len(v) == 0:
                    st.info("No rows.")
                else:
                    st.dataframe(pd.DataFrame(v), use_container_width=True)
            else:
                st.write(v)
    else:
        st.write(obj)

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("Create paid registration", use_container_width=True):
        try:
            res = tx1_inclusion(event_id=tx1_event_id, attendee_id=tx1_attendee_id, tx_id=tx1_payment_id)
            st.success("Transaction committed.")
            show_result("Create paid registration, output", res)
        except (OperationalError, IntegrityError) as e:
            st.error(f"Transaction failed, {e}")
        except Exception as e:
            st.error(f"Transaction failed, {e}")

with col2:
    if st.button("Confirm registration", use_container_width=True):
        try:
            res = tx2_update(attendee_id=tx2_attendee_id, event_id=tx2_event_id, tx_id=tx2_payment_id)
            st.success("Transaction committed.")
            show_result("Confirm registration, output", res)
        except (OperationalError, IntegrityError) as e:
            st.error(f"Transaction failed, {e}")
        except Exception as e:
            st.error(f"Transaction failed, {e}")

with col3:
    if st.button("Delete session (cascade)", use_container_width=True):
        try:
            res = tx3_deletion(event_id=tx3_event_id, topic=tx3_topic, start_time=tx3_start_time)
            st.success("Transaction committed.")
            show_result("Delete session (cascade), output", res)
        except (OperationalError, IntegrityError) as e:
            st.error(f"Transaction failed, {e}")
        except Exception as e:
            st.error(f"Transaction failed, {e}")

with col4:
    if st.button("Trigger test (invalid confirmation)", use_container_width=True):
        try:
            res = tx4_negative_test(attendee_id=tx4_attendee_id, event_id=tx4_event_id)
            st.warning("Transaction committed unexpectedly, your trigger might be missing.")
            show_result("Trigger test, output", res)
        except Exception as e:
            st.info("Transaction failed as expected, trigger blocked invalid confirmation.")
            st.code(str(e))

st.divider()

col5, col6, col7, col8 = st.columns(4)

with col5:
    if st.button("Add sponsor to event", use_container_width=True):
        try:
            res = tx5_add_sponsor_to_event(
                event_id=tx5_event_id,
                sponsor_id=tx5_sponsor_id,
                level=tx5_level,
                amount=tx5_amount,
            )
            st.success("Transaction committed.")
            show_result("Add sponsor to event, output", res)
        except (OperationalError, IntegrityError) as e:
            st.error(f"Transaction failed, {e}")
        except Exception as e:
            st.error(f"Transaction failed, {e}")

with col6:
    if st.button("Assign equipment to session", use_container_width=True):
        try:
            res = tx6_assign_equipment_to_session(
                event_id=tx6_event_id,
                topic=tx6_topic,
                start_time=tx6_start_time,
                serial_number=tx6_serial,
            )
            st.success("Transaction committed.")
            show_result("Assign equipment to session, output", res)
        except (OperationalError, IntegrityError) as e:
            st.error(f"Transaction failed, {e}")
        except Exception as e:
            st.error(f"Transaction failed, {e}")

with col7:
    if st.button("Submit session feedback", use_container_width=True):
        try:
            res = tx7_submit_feedback(
                feedback_id=tx7_feedback_id,
                event_id=tx7_event_id,
                topic=tx7_topic,
                start_time=tx7_start_time,
                rating=tx7_rating,
                comments=tx7_comments,
            )
            st.success("Transaction committed.")
            show_result("Submit session feedback, output", res)
        except (OperationalError, IntegrityError) as e:
            st.error(f"Transaction failed, {e}")
        except Exception as e:
            st.error(f"Transaction failed, {e}")

with col8:
    if st.button("Assign staff to event", use_container_width=True):
        try:
            res = tx8_assign_staff_to_event(event_id=tx8_event_id, staff_id=tx8_staff_id)
            st.success("Transaction committed.")
            show_result("Assign staff to event, output", res)
        except (OperationalError, IntegrityError) as e:
            st.error(f"Transaction failed, {e}")
        except Exception as e:
            st.error(f"Transaction failed, {e}")

st.divider()
st.markdown("### Database snapshot")

snapshot_options = {
    "Event overview (view)": "SELECT * FROM v_event_overview ORDER BY Event_ID LIMIT %s;",
    "Session feedback summary (view)": "SELECT * FROM v_session_feedback_summary ORDER BY Event_ID, Start_Time, Topic LIMIT %s;",
    "Registrations": "SELECT Attendee_ID, Event_ID, Registration_Date, Status, Transaction_ID FROM Registration ORDER BY Event_ID, Attendee_ID LIMIT %s;",
    "Payments": "SELECT Transaction_ID, Amount, Payment_Method FROM Payment ORDER BY Transaction_ID LIMIT %s;",
    "Events": "SELECT Event_ID, Title, Start_Date, End_Date, Venue_ID, Organizer_ID FROM Event ORDER BY Event_ID LIMIT %s;",
    "Sessions": "SELECT Event_ID, Topic, Start_Time, Speaker_ID FROM Session ORDER BY Event_ID, Start_Time, Topic LIMIT %s;",
    "Sponsors": "SELECT Sponsor_ID, Company_Name, Contact_Info FROM Sponsor ORDER BY Sponsor_ID LIMIT %s;",
    "Event sponsors": "SELECT Event_ID, Sponsor_ID, Sponsorship_Level, Contribution_Amount FROM Event_Sponsor ORDER BY Event_ID, Sponsor_ID LIMIT %s;",
    "Equipment": "SELECT Serial_Number, Item_Type FROM Equipment ORDER BY Serial_Number LIMIT %s;",
    "Session equipment": "SELECT Event_ID, Topic, Start_Time, Serial_Number FROM Session_Equipment ORDER BY Event_ID, Start_Time, Topic, Serial_Number LIMIT %s;",
    "Staff": "SELECT Staff_ID, First_Name, Last_Name, Role, Shift_Time FROM Staff ORDER BY Staff_ID LIMIT %s;",
    "Event staff": "SELECT Event_ID, Staff_ID FROM Event_Staff ORDER BY Event_ID, Staff_ID LIMIT %s;",
    "Feedback": "SELECT Feedback_ID, Event_ID, Topic, Start_Time, Rating, Comments FROM Feedback ORDER BY Feedback_ID DESC LIMIT %s;",
}

snap_col1, snap_col2 = st.columns([2, 1])
with snap_col1:
    snapshot_choice = st.selectbox("Choose what to display", list(snapshot_options.keys()))
with snap_col2:
    snapshot_limit = st.number_input("Rows", min_value=5, max_value=200, value=50, step=5)

with st.container(border=True):
    try:
        with transaction() as (_, cur):
            rows = fetch_all_dict(cur, snapshot_options[snapshot_choice], (int(snapshot_limit),))
        if len(rows) == 0:
            st.info("No rows found.")
        else:
            st.dataframe(pd.DataFrame(rows), use_container_width=True)
    except Exception as e:
        st.error(f"Could not load snapshot, {e}")
