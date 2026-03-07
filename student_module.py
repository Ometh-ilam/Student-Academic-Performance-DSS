#--------------------------***STUDENT CLASS***-------------------------------------------------
class Student:
    def __init__(self, student_id, name, module, average, letter_grade, gpa, attendance=100, homework_complete=1):
        self.student_id = student_id
        self.name = name
        self.module = module
        self.average = average
        self.letter_grade = letter_grade  
        self.gpa = gpa                    
        self.attendance = attendance
        self.homework_complete = homework_complete

    # ------------------*** AT-RISK DETENTION FUNCTION***----------------------------- ------------------
    def at_risk(self):
        return "Yes" if self.average < 50 else "No"

    # ------------------ ***PREDICTED GRADE FUNCTION***-------------------------------- ------------------
    def predicted_grade(self):
        score = self.average
        if self.attendance < 75:
            score -= 10
        elif self.attendance < 90:
            score -= 5
        if not self.homework_complete:
            score -= 5
        score = max(0, min(100, score))
        if score >= 70: return "A"
        if score >= 60: return "B"
        if score >= 50: return "C"
        if score >= 40: return "D"
        return "E"

    # ------------------***SUGGESTED INTERVENTION FUNCTION***---------------------------- ------------------
    def suggested_intervention(self):
        if self.average >= 70:
            return "None"
        elif self.average >= 60:
            return "Encourage Practice"
        elif self.average >= 50:
            return "Extra Tutoring"
        else:
            return "Immediate Intervention"