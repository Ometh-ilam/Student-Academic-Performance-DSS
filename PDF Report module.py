# ----------------------*** EXPORT PDF REPORT MODULE ***------------------------------------

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


# ----------------------*** EXPORT REPORT FUNCTION ***--------------------------------------
def export_report(student, filename):

    try:
        #--------------***VALIDATE THAT A STUDENT OBJECT HAS BEEN PROVIDED***------------------
        if student is None:
            raise ValueError("No student data provided")

        #--------------***VALIDATE FILE NAME***-------------------------------------------------
        if not filename:
            raise ValueError("Invalid filename")

        
        #--------------***ReportLab PDF Library User Guide. (n.d.). Available at: https://www.reportlab.com/docs/reportlab-userguide.pdf
        #---------------***CREATING THE REPORT***--------------------------------------------
        report_canvas = canvas.Canvas(filename, pagesize=A4)
        width, height = A4
        report_canvas.setFont("Helvetica-Bold", 16)
        report_canvas.drawString(50, height - 50, f"Student Report - {student.name}")
        report_canvas.setFont("Helvetica", 12)

        #--------------------***ADDING REPORT DATA FIELDS***-------------------------------
        data = [

            ("Student ID", student.student_id),
            ("Name", student.name),
            ("Module", student.module),
            ("Average", student.average),
            ("Letter Grade", student.letter_grade()),
            ("GPA", student.gpa()),
            ("Attendance", student.attendance),
            ("At Risk", student.at_risk()),
            ("Predicted Grade", student.predicted_grade())

        ]

        y = height - 100

        for label, value in data:

            report_canvas.drawString(50, y, f"{label}: {value}")
            y -= 20

        report_canvas.save()
        print("Report exported successfully.")
   #--------------------------------***REPORT VALIDATIONS***--------------------------------------
    except ValueError as validation_error:
        print("Validation Error:", validation_error)

    except IOError:
        print("File Error: Unable to write the PDF file.")

    except Exception as unexpected_error:
        print("Unexpected Error:", unexpected_error)