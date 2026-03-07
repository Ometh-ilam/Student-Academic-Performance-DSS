#---------------------**Schafer, C. (2017). Python Tutorial: CSV Module - How to Read, Parse, and Write CSV Files. YouTube. Available at: https://www.youtube.com/watch?v=q5uM4VKywbA.
import csv
from student_model import Student

#--------------------------***IMPORTING STUDENT RECORDS FROM CSV file***--------------------------------
def import_csv(path):
    
    students = []
    
    with open(path, newline='', encoding="utf-8") as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            student_id = row["Student ID"]
            name = row["Name"]
            module = row["Module"]
            average = float(row["Average"])
            letter_grade = row["Letter Grade"]
            gpa = float(row["GPA"])
            attendance = float(row.get("Attendance", 100))
            homework_complete = 1 if row.get("Homework", "Yes").lower() in ["yes","1","true"] else 0
            
            #----------------***CREATE STUDENT OBJECT***---------------------------------------------
            student = Student(
                student_id, name, module, average, letter_grade, gpa, attendance, homework_complete
            )
            students.append(student)
            
          
    return students


