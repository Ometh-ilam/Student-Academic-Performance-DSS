#-------------------------***Matplotlib.org. (2025). pie(x) — Matplotlib 3.10.6 documentation. [online] Available at: https://matplotlib.org/stable/plot_types/stats/pie.html.----------------------------------***Data Analytics Module***--------------------------------------
#-------------------------***DATA ANALYTICS MODULE***-----------------------------------------------
import matplotlib.pyplot as plt
from collections import Counter

#--------------------------------***STUDENT CLASS FOR CALLING STUDENT INFOMATION***-------------
class Student:
    def __init__(self, student_id, name, module, grade):
        self.student_id = student_id
        self.name = name
        self.module = module
        self.grade = grade

    def letter_grade(self):
        return self.grade

def module_distribution(students, module):

 try:
    module_students = []

    #------------------------***FIND STUDENTS IN A SELECTED MODULE***------------------------------
    for student in students:
        if student.module.lower() == module.lower():
            module_students.append(student)

    grades = []

    #-------------------------***COLLECT STUDENT GRADES***-------------------------------------------
    for student in module_students:
        grades.append(student.letter_grade())

    grade_count = Counter(grades)
    #------***matplotlib.org. (n.d.). Basic pie chart — Matplotlib 3.3.4 documentation. [online] Available at: https://matplotlib.org/stable/gallery/pie_and_polar_charts/pie_features.html.
    #----------------------------***PLOT THE PIE CHART***----------------------------------------
    plt.pie(grade_count.values(), labels=grade_count.keys(), autopct="%1.1f%%")

    plt.title(module + " Grade Distribution")

    plt.show()

 except AttributeError:
        print("Error: Student data is missing required attributes.")

 except TypeError:
        print("Error: Invalid student data format.")

    #--------------------------***SAMPLE STUDENT DATA FOR TESTING***------------------------------
students = [
    Student("S01", "Alice", "Math", "A"),
    Student("S02", "Bob", "Math", "B"),
    Student("S03", "Charlie", "Math", "A"),
    Student("S04", "David", "Science", "C"),
    Student("S05", "Emma", "Math", "B")
]

#----------------------------------***TESTING THE VISUAL GRAPH***------------------------------------
module_distribution(students, "Math")