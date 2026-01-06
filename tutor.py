import streamlit as st
import pandas as pd
import datetime
import os

# 1. Setup the Database
DATA_FILE = "tutoring_data.csv"

def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=["Student", "Date", "Grade", "Notes"])

df = load_data()

# 2. Page Styling
st.set_page_config(page_title="TutorTrack Pro", layout="wide")
st.title("📚 TutorTrack Pro")

# --- SIDEBAR: STUDENT MANAGEMENT ---
st.sidebar.header("Manage Roster")

# Get unique list of students currently in the data
existing_students = sorted(df["Student"].unique().tolist())

# Add a New Student
new_student_name = st.sidebar.text_input("Add New Student Name")
if st.sidebar.button("Add Student"):
    if new_student_name and new_student_name not in existing_students:
        # We add a "blank" entry to 'register' them in our CSV
        blank_entry = pd.DataFrame([[new_student_name, datetime.date.today(), 0, "Student added to roster"]], 
                                    columns=["Student", "Date", "Grade", "Notes"])
        df = pd.concat([df, blank_entry], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.sidebar.success(f"Added {new_student_name}!")
        st.rerun()

# Delete a Student
if existing_students:
    student_to_delete = st.sidebar.selectbox("Remove a Student", ["None"] + existing_students)
    if st.sidebar.button("🗑️ Delete Student") and student_to_delete != "None":
        df = df[df["Student"] != student_to_delete]
        df.to_csv(DATA_FILE, index=False)
        st.sidebar.warning(f"Deleted {student_to_delete}")
        st.rerun()

st.sidebar.divider()

# --- MAIN INTERFACE: SESSION TRACKER ---
selected_student = st.sidebar.selectbox("Select Student for Session", ["Select..."] + existing_students)

if selected_student != "Select...":
    st.header(f"Session for {selected_student}")
    
    col1, col2 = st.columns(2)
    with col1:
        grade = st.number_input("Current Grade (%)", 0, 100, 85)
    with col2:
        date = st.date_input("Session Date", datetime.date.today())
        
    notes = st.text_area("Notes")
    
    if st.button("Save Session"):
        new_data = pd.DataFrame([[selected_student, date, grade, notes]], 
                                columns=["Student", "Date", "Grade", "Notes"])
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("Saved!")
        st.rerun()

    # History
    st.divider()
    student_history = df[df["Student"] == selected_student]
    if not student_history.empty:
        st.table(student_history[["Date", "Grade", "Notes"]])
else:
    st.info("👈 Add a student or select one from the sidebar.")
    
