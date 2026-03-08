#------GeeksforGeeks (2016). Linear Search Python. [online] GeeksforGeeks. Available at: https://www.geeksforgeeks.org/python/python-program-for-linear-search/.
#--------------------***SEARCH STUDENTS FUNCTION***-----------------------------------------------
def search_students(students, search_term):
    search_term = search_term.lower()
    matches = []

    for student in students:
        #------------***CHECK STUDENT ID OR NAME EXISTS***----------------------------------------
        if search_term in student.name.lower() or search_term in student.student_id.lower():
            matches.append(student)

    return matches