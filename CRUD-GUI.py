import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel, QLineEdit, QPushButton, QMessageBox
import psycopg2

#posgresql credentials
DATABASE_NAME = "A3-Q1"
DATABASE_USER = "postgres"
DATABASE_PASSWORD = "student"
DATABASE_HOST = "localhost"
DATABASE_PORT = "5432"

#execute the query passed in
#with the parameters sepeaated to avoid SQL injection
def execute_query(query, params= None):
    #connect to the database with the credentials above
    conn = psycopg2.connect(
        dbname=DATABASE_NAME,
        user=DATABASE_USER,
        password=DATABASE_PASSWORD,
        host=DATABASE_HOST,
        port=DATABASE_PORT)
    
    try:
        cur = conn.cursor()
        if params:
            cur.execute(query, params)
        else:
            cur.execute(query)

        #return the rows for printing get all students
        if query.strip().lower().startswith("select"):
            student_rows = cur.fetchall()
            cur.close()
            conn.close()
            return student_rows
        else:
            conn.commit()
            cur.close()
            conn.close()
    except psycopg2.Error as e:
        QMessageBox.critical(None, "Query Execution Error", f"Error executing query: {e}")
        return -1
        
#function to get all the students from the database
def get_all_students():
    query = "SELECT * FROM students"
    rows = execute_query(query)
    if rows:
        QMessageBox.information(None, "All Students", "\n".join(str(row) for row in rows))

#function to add a student with their first and last name, email and enrollment date
def add_student(first_name, last_name, email, date_of_enrollment):
    query = "INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES (%s, %s, %s, %s)"
    params = (first_name, last_name, email, date_of_enrollment)
    result = execute_query(query, params)
    if result != -1:
        QMessageBox.information(None, "Success", "Student added successfully")

##function to update student email with id and new email
def update_student_email(student_id, new_email):
    query = "UPDATE students SET email = %s WHERE student_id = %s"
    params = (new_email, student_id)
    result = execute_query(query, params)
    if result != -1:
        QMessageBox.information(None, "Success", "Student email updated successfully")

#function to delete the student based on their id
def delete_student(student_id):
    query = "DELETE FROM students WHERE student_id = %s"
    params = (student_id,)
    result = execute_query(query, params)
    if result != -1:
        QMessageBox.information(None, "Success", "Student deleted successfully")

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Student Database CRUD Operations")

gui_layout = QVBoxLayout()

# add students widget setup
# groupboxes are usde to differenciate the sections of the gui
# add, get and delete/update based on the text fields they use
#everything gets added to the "layout" which is the main window
add_student_groupbox = QGroupBox("Add Student")
gui_layout.addWidget(add_student_groupbox)

add_student_layout = QVBoxLayout()
add_student_groupbox.setLayout(add_student_layout)

#create the textboxes and titles for the names
student_name_layout = QHBoxLayout()
student_name_layout.addWidget(QLabel("First Name:"))
first_name_textbox = QLineEdit()
student_name_layout.addWidget(first_name_textbox)
student_name_layout.addWidget(QLabel("Last Name:"))
last_name_textbox = QLineEdit()
student_name_layout.addWidget(last_name_textbox)
add_student_layout.addLayout(student_name_layout)

#create the textboxes and titles for the email
student_email_layout = QHBoxLayout()
student_email_layout.addWidget(QLabel("Email:"))
student_email_textbox = QLineEdit()
student_email_layout.addWidget(student_email_textbox)
student_email_layout.addWidget(QLabel("(abc@123.com)"))
add_student_layout.addLayout(student_email_layout)

student_enrollment_layout = QHBoxLayout()
student_enrollment_layout.addWidget(QLabel("Enrollment Date:"))
student_enrollment_textbox = QLineEdit()
student_enrollment_layout.addWidget(student_enrollment_textbox)
student_enrollment_layout.addWidget(QLabel("(YYYY,MM,DD)"))
add_student_layout.addLayout(student_enrollment_layout)

#pass in the proper variabled for addstudent
def add_button_clicked():
    add_student(first_name_textbox.text(), last_name_textbox.text(), student_email_textbox.text(), student_enrollment_textbox.text())

add_student_button = QPushButton("Add Student")
add_student_button.clicked.connect(add_button_clicked)
add_student_layout.addWidget(add_student_button)

# get students 
getall_student_groupbox = QGroupBox("Get All Students")
gui_layout.addWidget(getall_student_groupbox)

getall_student_layout = QVBoxLayout()
getall_student_groupbox.setLayout(getall_student_layout)

def get_all_button_clicked():
    get_all_students()

#get students button, connect it to the function get_all_button_clicked
getall_students_button = QPushButton("Get All Students")
getall_students_button.clicked.connect(get_all_button_clicked)
getall_student_layout.addWidget(getall_students_button)

# update / delete widget setup
update_or_delete_groupbox = QGroupBox("Update/Delete Student")
gui_layout.addWidget(update_or_delete_groupbox)

update_or_delete_layout = QVBoxLayout()
update_or_delete_groupbox.setLayout(update_or_delete_layout)

#create the textboxes and titles for the studentID/email
student_id_layout = QHBoxLayout()
student_id_layout.addWidget(QLabel("Student ID:"))
student_id_textbox = QLineEdit()
student_id_layout.addWidget(student_id_textbox)
update_or_delete_layout.addLayout(student_id_layout)

student_new_email_layout = QHBoxLayout()
student_new_email_layout.addWidget(QLabel("New Email:"))
student_new_email_textbox = QLineEdit()
student_new_email_layout.addWidget(student_new_email_textbox)
update_or_delete_layout.addLayout(student_new_email_layout)

#pass in the proper variables for update
def update_button_clicked():
    update_student_email(student_id_textbox.text(), student_new_email_textbox.text())

#button used to update the student email, connected to update_button_clicked
update_email_button = QPushButton("Update Student Email")
update_email_button.clicked.connect(update_button_clicked)
update_or_delete_layout.addWidget(update_email_button)

def delete_button_clicked():
    delete_student(student_id_textbox.text())

#button used to delete the student, connected to delete_button_clicked
delete_student_button = QPushButton("Delete Student")
delete_student_button.clicked.connect(delete_button_clicked)
update_or_delete_layout.addWidget(delete_student_button)

window.setLayout(gui_layout)
window.show()

sys.exit(app.exec_())