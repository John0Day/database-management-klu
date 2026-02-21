import streamlit as st
import pandas as pd
from psycopg2 import OperationalError, IntegrityError
from transactions import tx1_inclusion, tx2_update, tx3_deletion, tx4_negative_test

st.set_page_config(page_title="Event DB App", layout="wide")

st.title("Event Management DB Application")
st.caption("Runs Assignment-6 transactions via buttons, connects to PostgreSQL.")

with st.sidebar:
    st.header("Transaction Parameters")

    st.subheader("Tx1 Inclusion")
    tx1_event_id = st.number_input("Event_ID", min_value=1, value=1, step=1, key="tx1_event")
    tx1_attendee_id = st.number_input("New Attendee_ID", min_value=11, value=11, step=1, key="tx1_att")
    tx1_payment_id = st.number_input("New Transaction_ID", min_value=11, value=11, step=1, key="tx1_pay")

    st.subheader("Tx2 Update")
    tx2_attendee_id = st.number_input("Attendee_ID", min_value=1, value=2, step=1, key="tx2_att")
    tx2_event_id = st.number_input("Event_ID", min_value=1, value=2, step=1, key="tx2_event")
    tx2_payment_id = st.number_input("New Transaction_ID", min_value=12, value=12, step=1, key="tx2_pay")

    st.subheader("Tx3 Deletion")
    tx3_event_id = st.number_input("Event_ID", min_value=1, value=1, step=1, key="tx3_event")
    tx3_topic = st.text_input("Topic", value="Intro to Predictive Modeling", key="tx3_topic")
    tx3_start_time = st.text_input("Start_Time (HH:MM)", value="09:00", key="tx3_start")

    st.subheader("Tx4 Negative Test")
    tx4_attendee_id = st.number_input("Attendee_ID", min_value=1, value=3, step=1, key="tx4_att")
    tx4_event_id = st.number_input("Event_ID", min_value=1, value=2, step=1, key="tx4_event")

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
    if st.button("Run Tx1, Inclusion", use_container_width=True):
        try:
            res = tx1_inclusion(event_id=tx1_event_id, attendee_id=tx1_attendee_id, tx_id=tx1_payment_id)
            st.success("Tx1 committed.")
            show_result("Tx1 Output", res)
        except (OperationalError, IntegrityError) as e:
            st.error(f"Tx1 failed, {e}")
        except Exception as e:
            st.error(f"Tx1 failed, {e}")

with col2:
    if st.button("Run Tx2, Update", use_container_width=True):
        try:
            res = tx2_update(attendee_id=tx2_attendee_id, event_id=tx2_event_id, tx_id=tx2_payment_id)
            st.success("Tx2 committed.")
            show_result("Tx2 Output", res)
        except (OperationalError, IntegrityError) as e:
            st.error(f"Tx2 failed, {e}")
        except Exception as e:
            st.error(f"Tx2 failed, {e}")

with col3:
    if st.button("Run Tx3, Deletion", use_container_width=True):
        try:
            res = tx3_deletion(event_id=tx3_event_id, topic=tx3_topic, start_time=tx3_start_time)
            st.success("Tx3 committed.")
            show_result("Tx3 Output", res)
        except (OperationalError, IntegrityError) as e:
            st.error(f"Tx3 failed, {e}")
        except Exception as e:
            st.error(f"Tx3 failed, {e}")

with col4:
    if st.button("Run Tx4, Negative Test", use_container_width=True):
        try:
            res = tx4_negative_test(attendee_id=tx4_attendee_id, event_id=tx4_event_id)
            st.warning("Tx4 committed, unexpected, your trigger might be missing.")
            show_result("Tx4 Output", res)
        except Exception as e:
            st.info("Tx4 failed as expected, trigger blocked invalid confirmation.")
            st.code(str(e))

st.divider()
st.markdown("### Notes")
st.write(
    "Tx1 and Tx2 should succeed if your Assignment-5 schema is loaded. "
    "Tx4 should fail if your trigger is active. "
    "Tx3 demonstrates ON DELETE CASCADE and re-queries the feedback summary view."
)