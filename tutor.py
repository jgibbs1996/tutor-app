import streamlit as st
import pandas as pd
import datetime
import os

# 1. Setup the "Database" (A CSV file)
DATA_FILE = "tutoring_data.csv"

def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=["Student", "Date", "Grade", "Notes"])

# 2. Page Styling
st.set_page_config(page_title="TutorTrack Pro", layout="wide")
st.title("📚 TutorTrack Pro")
st.write("Track student progress and session history.")

# 3. Sidebar - Student Selection
df = load_data()
students = ["Select a Student", "Alex Smith", "Jamie Lannister", "Sarah Parker", "+ Add New Student"]
selected_student = st.sidebar.selectbox("Current Student", students)

if selected_student != "Select a Student" and selected_student != "+ Add New Student":
    
    # --- SECTION A: NEW ENTRY ---
    st.header(f"New Session for {selected_student}")
    
    col1, col2 = st.columns(2)
    with col1:
        grade = st.number_input("Current Grade (%)", min_value=0, max_value=100, value=85)
    with col2:
        date = st.date_input("Session Date", datetime.date.today())
        
    notes = st.text_area("Session Notes (What did you cover today?)")
    
    if st.button("Save Session"):
        new_data = pd.DataFrame([[selected_student, date, grade, notes]], 
                                columns=["Student", "Date", "Grade", "Notes"])
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success(f"History updated for {selected_student}!")
        st.rerun()

    # --- SECTION B: HISTORY ---
    st.divider()
    st.header("📈 Progress History")
    
    # Filter the data for just this student
    student_history = df[df["Student"] == selected_student]
    
    if not student_history.empty:
        # Show a progress chart of grades
        st.line_chart(student_history.set_index("Date")["Grade"])
        
        # Show the raw notes
        st.table(student_history[["Date", "Grade", "Notes"]])
    else:
        st.info("No history found for this student yet.")

else:
    st.info("👈 Please select a student from the sidebar to begin.")
