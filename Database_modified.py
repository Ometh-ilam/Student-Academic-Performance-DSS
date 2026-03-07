import sqlite3

DB_FILE = "student_dss.db"


def connect():
    return sqlite3.connect(DB_FILE)

# -----------------***creating the student table***--------------------------------------------
def init_db():
    try:
        con = connect()
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                module TEXT NOT NULL,
                average REAL NOT NULL,
                letter_grade TEXT,       -- New column from CSV
                gpa REAL,               -- New column from CSV
                attendance REAL DEFAULT 100,
                homework_complete INTEGER DEFAULT 1
            )
        """)
        con.commit()
        con.close()
    except sqlite3.IntegrityError:
        print("Error: Student ID already exists.")

# ----------------***Insert Student***------------------------------------------------------------
def load_students():
    con = connect()
    cur = con.cursor()
    cur.execute("""
        SELECT student_id, name, module, average, letter_grade, gpa, attendance, homework_complete
        FROM students
    """)
    rows = cur.fetchall()
    con.close()
    return rows

# ----------------***Add Students***---------------------------------------------------
def add_student(student_id, name, module, average, attendance=100, homework_complete=1, letter_grade=None, gpa=None):
    con = connect()
    cur = con.cursor()
    try:
        cur.execute("""
            INSERT OR IGNORE INTO students
            (student_id, name, module, average, letter_grade, gpa, attendance, homework_complete)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (student_id, name, module, average, letter_grade, gpa, attendance, homework_complete))
        con.commit()
    except sqlite3.IntegrityError:
        print(f"Error: Student ID {student_id} already exists!")
    finally:
        con.close()

#-------------------------***Insert sample records***-------------------------------------------
def insert_sample_students():
    add_student("S001", "Alice Johnson", "Mathematics", 75, letter_grade="A", gpa=4)
    add_student("S002", "Bob Smith", "Science", 62, letter_grade="B", gpa=3)
    add_student("S003", "Charlie Brown", "English", 48, letter_grade="D", gpa=1)

# --------------***Testing the DB***------------------------------------------------------------
if __name__ == "__main__":
    init_db()
    insert_sample_students()
    data = load_students()
    for d in data:
        print(d)