#------GeeksforGeeks (2016). Linear Search Python. [online] GeeksforGeeks.
# Available at: https://www.geeksforgeeks.org/python/python-program-for-linear-search/

#--------------------***SEARCH STUDENTS FUNCTION***---------------------------------------------------
def search_students(students, search_term):

    # ---------------***INPUT VALIDATIONS***---------------------------------------------------------
    if students is None or len(students) == 0:
        print("Student list is empty.")
        return []

    if not isinstance(search_term, str) or search_term.strip() == "":
        print("Invalid search term.")
        return []

    search_term = search_term.lower().strip()
    matches = []

    try:
        for student in students:

            #--------------------***CHECKING FOR NAME AND ID ATTRIBUTES***---------------------------
            if not hasattr(student, "name") or not hasattr(student, "student_id"):
                continue

            #------------***CHECK STUDENT ID OR NAME EXISTS***----------------------------------------
            if search_term in student.name.lower() or search_term in student.student_id.lower():
                matches.append(student)

    except Exception as e:
        print("Error occurred during search:", e)

    return matches
