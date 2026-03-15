import os
import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from collections import Counter
import matplotlib.pyplot as plt
import csv

DB_FILE = "student_dss.db"

#-------------------------***USERS***--------------------------------------------------------
USERS = {
    "teacher": {"password": "teacher123", "role": "teacher"},
    "parent": {"password": "parent123", "role": "parent"}
}

current_role = None
students = []
tree = None

#--------------------------***STUDENT CLASS***-------------------------------------------------
class Student:
    def __init__(self, student_id, name, module, average, attendance=100, homework_complete=1):
        self.student_id = student_id
        self.name = name
        self.module = module
        self.average = average
        self.attendance = attendance
        self.homework_complete = homework_complete
    # ------------------*** AT-RISK DETENTION FUNCTION***----------------------------- ------------------
    def at_risk(self):
        return "Yes" if self.average < 50 else "No"
    # ------------------ ***PREDICTED GRADE FUNCTION***-------------------------------- ------
    def predicted_grade(self):
        score = self.average
        if self.attendance < 75:
            score -= 10
        elif self.attendance < 90:
            score -= 5
        if not self.homework_complete:
            score -= 5
        score = max(0, min(100, score))
        if score >= 70:
            return "A"
        if score >= 60:
            return "B"
        if score >= 50:
            return "C"
        if score >= 40:
            return "D"
        return "E"
    # ------------------***SUGGESTED INTERVENTION FUNCTION***---------------------------- ----------------
    def suggested_intervention(self):
        if self.average >= 70:
            return "None"
        elif self.average >= 60:
            return "Encourage Practice"
        elif self.average >= 50:
            return "Extra Tutoring"
        else:
            return "Immediate Intervention"

#------------***freeCodeCamp.org (2020). SQLite Databases With Python - Full Course. YouTube. Available at: https://www.youtube.com/watch?v=byHcYRpMgI4.
# -----------------***creating the student table***--------------------------------------------
def db_connect():
    return sqlite3.connect(DB_FILE)

def init_db():
    con = db_connect()
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            module TEXT NOT NULL,
            average REAL NOT NULL,
            attendance REAL DEFAULT 100,
            homework_complete INTEGER DEFAULT 1
        )
    """)
    con.commit()
    con.close()

def load_students():
    students.clear()
    con = db_connect()
    cur = con.cursor()
    cur.execute("""
        SELECT student_id,name,module,average,attendance,homework_complete
        FROM students
        ORDER BY student_id
    """)
    for sid, name, module, avg, att, hw in cur.fetchall():
        students.append(Student(sid, name, module, avg, att, hw))
    con.close()

#-----------------------------***STUDENT TREE VIEW REFRESH FUNCTION----------------------------------------------
def refresh_table(data=None):
    if tree is None:
        return
    for r in tree.get_children():
        tree.delete(r)
    for s in data if data else students:
        tree.insert("", "end", values=(
            s.student_id,
            s.name,
            s.module,
            s.average,
            s.attendance,
            "Yes" if s.homework_complete else "No"
        ))

def refresh_table_button():
    refresh_table(students)

#------------------***W3schools.com. (2025). W3Schools.com. [online]
# Available at: https://www.w3schools.com/python/python_dsa_bubblesort.asp***---------------------

#-------------***SORTING STUDENT TABLE***---------------------------------------------------------
def sort_students(student_list, ascending=True):
    
     #--------------------***INPUT VALIDATION***---------------------------------------
    if student_list is None or not isinstance(student_list, list):
        return []
    n = len(student_list)
    
    #-------------***BUBBLE SORT TO SORT STUDENT TABLE IN ASCENDING & DESCENDING ORDER***-------
    for i in range(n):
        for j in range(0, n - i - 1):
            a = student_list[j]
            b = student_list[j + 1]
            #-----------------------****CREATE COMPARISON KEYS***--------------------------------
            key_a = (a.student_id, a.name, a.module, a.average)
            key_b = (b.student_id, b.name, b.module, b.average)
            #-------------------------***SORTING IN ASCENDING & DESCENDING ORDERS***-------------
            if ascending:
                if key_a > key_b:
                    student_list[j], student_list[j+1] = student_list[j+1], student_list[j]
            else:
                if key_a < key_b:
                    student_list[j], student_list[j+1] = student_list[j+1], student_list[j]
    return student_list

#------GeeksforGeeks (2016). Linear Search Python. [online] GeeksforGeeks.
# Available at: https://www.geeksforgeeks.org/python/python-program-for-linear-search/

#--------------------***SEARCH STUDENTS FUNCTION***------------------------------------------------
def search_students(students, search_term):
    if not search_term:
        return []
    search_term = search_term.lower()
    matches = []
    for s in students:
        if search_term in s.name.lower() or search_term in s.student_id.lower():
            matches.append(s)
    return matches

def search_ui():
    term = simpledialog.askstring("Search", "Enter Student ID or Name")

    if term is None:
        return  #------------***FOR CANCEL SEARCH***----------------

    valid, error_message = is_valid_search_term(term)

    if not valid:
        messagebox.showerror("Invalid Input", error_message)
        return

    results = search_students(students, term)

    if current_role == "teacher":
        if results:
            refresh_table(results)
        else:
            messagebox.showinfo("No Result", "No student found with that ID or name.")

    elif current_role == "parent":
        if results:
            s = results[0]  
            messagebox.showinfo(
                "Student Found",
                f"Name: {s.name}\n"
                f"Module: {s.module}\n"
                f"Average: {s.average}\n"
                f"At Risk: {s.at_risk()}\n"
                f"Predicted Grade: {s.predicted_grade()}\n"
                f"Suggested Intervention: {s.suggested_intervention()}"
            )
        else:
            messagebox.showinfo("No Result", "No student found with that ID or name.")

#----------------------***TO VALIDATE SEARCH TERMS***----------------------------
def is_valid_search_term(term):
    term = term.strip()

    #---------------***FOR EMPTY INPUT***------------------------------------
    if not term:
        return False, "Search term cannot be empty."

    #--------------***STUDENT ID VALIDATION***---------------------------------
    if term.replace(" ", "").isalnum():
        return True, None

    #---------------***STUDENT NAME VALIDATION***--------------------------------
    if all(c.isalpha() or c.isspace() for c in term):
        return True, None

    return False, "Invalid search format. Enter a valid name or student ID."

# ---------------- ***SELECT STUDENT*** --------------------------------------------------------
def get_selected_student():
    """
    Returns the currently selected student from the table.
    Works only for roles that can see the table (teachers). when 
    student object if selected, None otherwise.
          
    """
    try:
        if tree is None:
            #---------- ***TO NOTIFY THE USER THAT SELECT STUDENT IS NOT AVAILABLE***-------------------
            messagebox.showwarning("Select Student", "Table is not available for this role.")
            return None

        sel = tree.focus() 
        if not sel:
            messagebox.showwarning("Select Student", "No student selected.")
            return None

        sid = tree.item(sel)["values"][0]
        for s in students:
            if s.student_id == sid:
                return s

        messagebox.showwarning("Select Student", "Selected student not found in records.")
        return None
    except Exception as e:
        messagebox.showerror("Error", f"Error selecting student: {e}")
        return None

# ---------------- ***ROLE BASED AT RISK LEVEL STATUS***------------------------ ----------------
def show_at_risk():
    """
    Display whether a student is at risk.
    - Parents: Search for their child first
    - Teachers: Use selected row from table
    """
    try:
        if current_role == "parent":
            search_ui()  
            return

        s = get_selected_student()
        if s:
            messagebox.showinfo("At Risk Status", f"{s.name} At Risk: {s.at_risk()}")
    except Exception as e:
        messagebox.showerror("Error", f"Sorry, cannot display At Risk status: {e}")

# ---------------- ***ROLE BASED PREDICTED GRADE STATUS***------------------------ --------------
def show_predicted_grade():
    """
    Display predicted grade for a student.
    - Parents: Search for their child first
    - Teachers: Use selected row from table
    """
    try:
        if current_role == "parent":
            search_ui()
            return

        s = get_selected_student()
        if s:
            messagebox.showinfo("Predicted Grade", f"{s.name} Predicted Grade: {s.predicted_grade()}")
    except Exception as e:
        messagebox.showerror("Error", f"Cannot display Predicted Grade: {e}")

# ---------------- ***ROLE SHOW INTERVENTION STATUS***------------------------ --------------
def show_intervention():
    """
    Display suggested intervention for a student.
    - Teachers: Use the selected row from the table
    - Parents: Search for their child first
    """
    try:
        if current_role == "parent":
            search_ui()
            return

        #--------------*** Teacher selects from table***------------------------
        s = get_selected_student()
        if s:
            messagebox.showinfo(
                "Suggested Intervention",
                f"{s.name} - Suggested Intervention: {s.suggested_intervention()}"
            )
        else:
            messagebox.showwarning("No Selection", "Please select a student from the table.")

    except Exception as e:
        messagebox.showerror("Error", f"Cannot display suggested intervention: {e}")

#--------------***ReportLab PDF Library User Guide. (n.d.). Available at: https://www.reportlab.com/docs/reportlab-userguide.pdf
# ---------------- ---------***EXPORT REPORT***------------------------------ ----------------
def export_student_report():
    #-----------------------***PARENT SEARCH FOR THEIR CHILD***--------------------------------     
    if current_role == "parent":
        term = simpledialog.askstring("Search", "Enter Student ID or Name")
        if not term:
            return
        results = search_students(students, term)
        if not results:
            messagebox.showinfo("No Result", "No student found with that ID or name.")
            return
        s = results[0]
    #-----------------------***TEACHER SELECT STUDENT FROM TABLE***---------------------------
    else:
        s = get_selected_student()
        if not s:
            return

    module_students = [st for st in students if st.module == s.module]
    grades = Counter(st.predicted_grade() for st in module_students)

    #------***matplotlib.org. (n.d.). Basic pie chart — Matplotlib 3.3.4 documentation. [online] Available at: https://matplotlib.org/stable/gallery/pie_and_polar_charts/pie_features.html.
    #-----------------------***CREATE MODULE GRADE DISTRIBUTION PIE CHART***------------------
    fig = plt.Figure(figsize=(4,4))
    ax = fig.add_subplot(111)
    ax.pie(list(grades.values()), labels=list(grades.keys()), autopct="%1.1f%%")
    ax.set_title(f"{s.module} - Grade Distribution")
    #-----------------------***SAVE TEMPORARY CHART IMAGE***----------------------------------
    pie_path = "temp_pie.png"
    fig.savefig(pie_path, bbox_inches="tight", dpi=150)
    plt.close(fig)
    #-----------------------***SELECT LOCATION TO SAVE PDF REPORT***--------------------------
    pdf_filename = filedialog.asksaveasfilename(defaultextension=".pdf")
    if not pdf_filename:
        os.remove(pie_path)
        return
    #--------------***ReportLab PDF Library User Guide. (n.d.). Available at: https://www.reportlab.com/docs/reportlab-userguide.pdf
    #-----------------------***CREATE PDF REPORT***--------------------------------------------
    c = canvas.Canvas(pdf_filename, pagesize=A4)
    width, height = A4
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, f"Student Report - {s.name}")
    c.setFont("Helvetica", 12)
    y = height - 80

    #-----------------------***ADD STUDENT DETAILS TO REPORT***--------------------------------
    fields = [
        ("Student ID", s.student_id),
        ("Name", s.name),
        ("Module", s.module),
        ("Average", s.average),
        ("Attendance", s.attendance),
        ("Homework Complete", "Yes" if s.homework_complete else "No"),
        ("At Risk", s.at_risk()),
        ("Suggested Intervention", s.suggested_intervention()),
        ("Predicted Grade", s.predicted_grade())
    ]
    for label, value in fields:
        c.drawString(50, y, f"{label}: {value}")
        y -= 18
    

    #-----------------------***INSERT PIE CHART INTO PDF***-----------------------------------
    y -= 10
    image_height = min(y - 40, 300)
    image_width = image_height
    x_pos = (width - image_width) / 2
    y_pos = y - image_height
    c.drawImage(pie_path, x_pos, y_pos, width=image_width, height=image_height)
    c.save()
    os.remove(pie_path)

    messagebox.showinfo("Success", "Report Exported Successfully")

#---------------------**Schafer, C. (2017). Python Tutorial: CSV Module - How to Read, Parse, and Write CSV Files. YouTube. Available at: https://www.youtube.com/watch?v=q5uM4VKywbA.
#--------------------------***IMPORTING STUDENT RECORDS FROM CSV file***--------------------------------
def import_csv():

    #-----------------------***OPEN FILE DIALOG TO SELECT CSV FILE***--------------------------
    try:
        path = filedialog.askopenfilename(filetypes=[("CSV","*.csv")])
        if not path:
            return

        #-----------------------***ENSURE STUDENT TABLE EXISTS***------------------------------
        init_db()

        con = db_connect()
        cur = con.cursor()

        #-----------------------***READ CSV FILE AND INSERT DATA INTO DATABASE***--------------
        with open(path, "r", newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                cur.execute("""
                    INSERT OR REPLACE INTO students
                    (student_id, name, module, average, attendance, homework_complete)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    row["Student ID"],
                    row["Name"],
                    row["Module"],
                    float(row["Average"]),
                    float(row.get("Attendance", 100)),
                    1 if row.get("Homework", "Yes").lower() in ["yes","1","true"] else 0
                ))

    

        #-----------------------***SAVE CHANGES AND CLOSE DATABASE***--------------------------
        con.commit()
        con.close()
        
        load_students()
        refresh_table()

        messagebox.showinfo("Success", "CSV Data Imported Successfully")

    #-----------------------***HANDLE FILE OR DATA ERRORS***----------------------------------
    except FileNotFoundError:
        messagebox.showerror("Error", "CSV file not found.")

    except ValueError:
        messagebox.showerror("Error", "Invalid data format in CSV file.")
    
    except KeyError as e:
            messagebox.showerror("CSV Error", f"Missing column: {e}")
            return
  # ----------------***MODULE DISTRIBUTION FUNCTION***-------- ----------------
def module_distribution():
    module = simpledialog.askstring("Module", "Enter Module Name")
    if not module:
        return
    module_students = [s for s in students if s.module.lower() == module.lower()]
    if not module_students:
        messagebox.showinfo("No Data", f"No students found for module: {module}")
        return
    grades = [s.predicted_grade() for s in module_students]
    grade_count = Counter(grades)
    plt.pie(grade_count.values(), labels=grade_count.keys(), autopct="%1.1f%%")
    plt.title(module + " Grade Distribution")
    plt.show()

# ---------------- ***SORT STUDENTS UI FUNCTION*** ---------------------------
sort_ascending = True

def sort_students_ui():
    global students, sort_ascending
    students = sort_students(students, ascending=sort_ascending)
    sort_ascending = not sort_ascending
    refresh_table(students)

#----------***freeCodeCamp.org (2019). Tkinter Course - Create Graphic User Interfaces in Python Tutorial. YouTube. Available at: https://www.youtube.com/watch?v=YXPyB4XeYLA
#-------------------------***Main Window (Dashboard) UI***-------------------------
def build_main_window(role):
    global tree
    tree = None

    root = tk.Tk()
    root.title("Academic Performance DSS")
    root.geometry("1400x600")

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)

    if role == "teacher":
        tk.Button(btn_frame, text="Import CSV", width=15, command=import_csv).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Refresh", width=15, command=refresh_table_button).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Module Distribution", width=18, command=module_distribution).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Sort", width=18, command=sort_students_ui).pack(side=tk.LEFT, padx=5)

    tk.Button(btn_frame, text="Search Student", width=18, command=search_ui).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="At Risk Status", width=18, command=show_at_risk).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Predicted Grade", width=18, command=show_predicted_grade).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Export Report", width=18, command=export_student_report).pack(side=tk.LEFT, padx=5)
    tk.Button(btn_frame, text="Suggested Intervention", width=18, command=show_intervention).pack(side=tk.LEFT, padx=5)
    #tk.Button(root, text="Close", width=15, command=root.destroy).pack(pady=10)
   
    #--------------***ROLE BASED (UI)***--------------------------------------
    if role == "teacher":
        table_frame = tk.Frame(root)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        columns = ("Student ID", "Name", "Module", "Average", "Attendance", "Homework")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=160, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        refresh_table()

    root.mainloop()

# ----------------***LOGIN FUNCTION***--------------------- ----------------
def login():
    global current_role
    username = username_entry.get()
    password = password_entry.get()
    if username in USERS and USERS[username]["password"] == password:
        current_role = USERS[username]["role"]
        messagebox.showinfo("Login Successful", f"Welcome! Role: {current_role}")
        login_window.destroy()
        build_main_window(current_role)
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

def reset_fields():
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

#----------***freeCodeCamp.org (2019). Tkinter Course - Create Graphic User Interfaces in Python Tutorial. YouTube. Available at: https://www.youtube.com/watch?v=YXPyB4XeYLA
# ---------------- ***START PROGRAM***---------------------- ----------------
init_db()
load_students()

login_window = tk.Tk()
login_window.title("Login")
login_window.geometry("350x280")

tk.Label(login_window, text="Username").pack(pady=5)
username_entry = tk.Entry(login_window, width=25)
username_entry.pack()

tk.Label(login_window, text="Password").pack(pady=5)
password_entry = tk.Entry(login_window, show="*", width=25)
password_entry.pack()

tk.Button(login_window, text="Login", width=20, command=login).pack(pady=8)
tk.Button(login_window, text="Reset", width=20, command=reset_fields).pack(pady=5)

login_window.mainloop()
