#------------------***W3schools.com. (2025). W3Schools.com. [online] Available at: https://www.w3schools.com/python/python_dsa_bubblesort.asp***--------
#-------------***SOTRING STUDENT TABLE***---------------------------------------------
def sort_students(student_list, ascending=True):
    n = len(student_list)
    
    #-------------***BUBBLE SORT TO SORT STUDENT TABLE IN ASCENDING & DESCENDING ORDER***-------
    for i in range(n):
        for j in range(0, n - i - 1):
            
            student_a = student_list[j]
            student_b = student_list[j+1]
            
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
            
            #----------------------------***PERFORM SWAP IF THE CONDITION IS MET***--------------------
            if should_swap:
                student_list[j] = student_b
                student_list[j+1] = student_a
                
    return student_list