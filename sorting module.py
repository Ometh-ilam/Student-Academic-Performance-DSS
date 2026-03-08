#------------------***W3schools.com. (2025). W3Schools.com. [online]
# Available at: https://www.w3schools.com/python/python_dsa_bubblesort.asp***--------

#-------------***SORTING STUDENT TABLE***---------------------------------------------
def sort_students(student_list, ascending=True):

    #--------------------***INPUT VALIDATION***---------------------------------------
    if student_list is None:
        print("Error: Student list is None.")
        return []

    if not isinstance(student_list, list):
        print("Error: Student data must be provided as a list.")
        return []

    if len(student_list) == 0:
        print("Student list is empty.")
        return []

    if not isinstance(ascending, bool):
        print("Error: 'ascending' must be True or False.")
        return student_list

    try:
        n = len(student_list)

        #-------------***BUBBLE SORT TO SORT STUDENT TABLE IN ASCENDING & DESCENDING ORDER***-------
        for i in range(n):
            for j in range(0, n - i - 1):

                student_a = student_list[j]
                student_b = student_list[j+1]

                #-------------***CHECK REQUIRED STUDENT ATTRIBUTES***------------------------------
                required_attrs = ["student_id", "name", "module", "average"]

                for attr in required_attrs:
                    if not hasattr(student_a, attr) or not hasattr(student_b, attr):
                        print("Error: Student object missing required attributes.")
                        return student_list

                #-----------------------****CREATE COMPARISON KEYS***--------------------------------
                key_a = (student_a.student_id, student_a.name, student_a.module, student_a.average)
                key_b = (student_b.student_id, student_b.name, student_b.module, student_b.average)

                #------------------------***SWAPPING BASED ON THE ORDER***----------------------------
                should_swap = False

                if ascending:
                    if key_a > key_b:
                        should_swap = True
                else:
                    if key_a < key_b:
                        should_swap = True

                #----------------------------***PERFORM SWAP IF THE CONDITION IS MET***---------------
                if should_swap:
                    student_list[j] = student_b
                    student_list[j+1] = student_a

        return student_list

    except Exception as e:
        print("Unexpected error during sorting:", e)
        return student_list
