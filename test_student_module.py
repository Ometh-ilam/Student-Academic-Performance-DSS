#------------***THIS FILE IS CREATED TO TEST THE STUDENT_MODULE***----------------------------------

from student_model import Student  

# ----------- ***CREATE SAMPLE STUDENT DATA***------------------------------------------ -------------
s1 = Student("S001", "Alice Johnson", "Mathematics", 75, "A", 4, 95, 1)
s2 = Student("S002", "Bob Smith", "Science", 62, "B", 3, 88, 1)
s3 = Student("S003", "Charlie Brown", "English", 48, "D", 1, 70, 0)

students = [s1, s2, s3]

# ----------- ***TEST EACH FUNCTION WRITTEN UNDER STUDENT MODULE***--------------------------------
for s in students:
    print(f"Student: {s.name} ({s.student_id})")
    print(f"Module: {s.module}")
    print(f"Average: {s.average}")
    print(f"Letter Grade: {s.letter_grade}")
    print(f"GPA: {s.gpa}")
    print(f"Attendance: {s.attendance}%")
    print(f"Homework Complete: {'Yes' if s.homework_complete else 'No'}")
    print(f"At Risk: {s.at_risk()}")
    print(f"Predicted Grade: {s.predicted_grade()}")
    print(f"Suggested Intervention: {s.suggested_intervention()}")
    print("-" * 50)