import tkinter as tk
from tkinter import messagebox

# Main Program Window
root = tk.Tk()
root.title("Student Manager")
root.geometry("1000x800")
root.resizable(False, False)
root.configure(bg="dark green")
root.option_add("*Font", "Overlock 16")

class Student:
    def __init__(self, number, name, coursework1, coursework2, coursework3, exam_mark):
        self.number = number
        self.name = name
        self.coursework_mark = coursework1 + coursework2 + coursework3
        self.exam_mark = exam_mark
        self.total_score = self.coursework_mark + exam_mark
        self.percentage = (self.total_score / 160) * 100
        self.grade = self.calculate_grade()

    def calculate_grade(self):
        #Calculate the student's grade based on percentage
        if self.percentage >= 70:
            return 'A'
        elif self.percentage >= 60:
            return 'B'
        elif self.percentage >= 50:
            return 'C'
        elif self.percentage >= 40:
            return 'D'
        else:
            return 'F'

def load_students_from_file(filename):
    #Load students from a file and return a list of Student objects
    students = []
    with open(filename, 'r') as file:
        for line in file:
            number, name, coursework1, coursework2, coursework3, exam_mark = line.strip().split(',')
            students.append(Student(number, name, int(coursework1), int(coursework2), int(coursework3), int(exam_mark)))
    return students

def save_students_to_file(filename, students):
    #Save students to a file
    with open(filename, 'w') as file:
        for student in students:
            file.write(f"{student.number},{student.name},{student.coursework_mark // 3},{student.coursework_mark // 3},{student.coursework_mark // 3},{student.exam_mark}\n")

# File path for storing student data
file_path = r"C:\\Users\\gamet\\School Files\\studentMarks.txt"
students = load_students_from_file(file_path)

def custom_askstring(title, prompt):
    #Create a custom input dialog
    dialog = tk.Toplevel(root)
    dialog.title(title)
    dialog.configure(bg="dark green")
    dialog.geometry("800x400")
    dialog.transient(root)
    dialog.grab_set()

    tk.Label(dialog, text=prompt, font=("Overlock", 20, "underline"), bg="dark green", fg="white").pack(pady=10)
    entry = tk.Entry(dialog, width=20)
    entry.pack(pady=10)

    button_frame = tk.Frame(dialog, bg="dark green")
    button_frame.pack(pady=20)

    def on_ok():
        dialog.result = entry.get()
        dialog.destroy()

    def on_cancel():
        dialog.result = None
        dialog.destroy()

    tk.Button(button_frame, text="OK", command=on_ok, bg="forest green", fg="white", width=10).pack(side=tk.LEFT, padx=10)
    tk.Button(button_frame, text="Cancel", command=on_cancel, bg="forest green", fg="white", width=10).pack(side=tk.LEFT, padx=10)

    dialog.wait_window(dialog)
    return dialog.result

def display_message(message, title="Message", type="info"):
    #Display a message box
    if type == "info":
        messagebox.showinfo(title, message)
    elif type == "error":
        messagebox.showerror(title, message)

def display_student_info(student):
    #Display information of a single student
    output_box.insert(tk.END, f"{'_'*30}\n{''*30}\n")
    output_box.insert(tk.END, f"Number: {student.number}\n")
    output_box.insert(tk.END, f"Name: {student.name}\n")
    output_box.insert(tk.END, f"Coursework Mark: {student.coursework_mark}\n")
    output_box.insert(tk.END, f"Exam Mark: {student.exam_mark}\n")
    output_box.insert(tk.END, f"Overall Percentage: {student.percentage:.2f}%\n")
    output_box.insert(tk.END, f"Grade: {student.grade}\n")

def view_all_records():
    #View all student records
    output_box.delete(1.0, tk.END)
    total_percentage = sum(student.percentage for student in students)
    for student in students:
        display_student_info(student)
    output_box.insert(tk.END, f"\nTotal Students: {len(students)}\n")
    output_box.insert(tk.END, f"Average Percentage: {total_percentage / len(students):.2f}%\n")

def view_individual_record():
    #View an individual student's record based on number or name
    identifier = custom_askstring("Input", "Enter student number or name:")
    if identifier is None:
        return
    output_box.delete(1.0, tk.END)
    for student in students:
        if student.number == identifier or student.name.lower() == identifier.lower():
            display_student_info(student)
            return
    display_message("Student not found", type="error")

def show_highest_score():
    #Display the student with the highest score
    highest = max(students, key=lambda s: s.total_score)
    output_box.delete(1.0, tk.END)
    output_box.insert(tk.END, "Student with Highest Score:\n")
    display_student_info(highest)

def show_lowest_score():
    #Display the student with the lowest score
    lowest = min(students, key=lambda s: s.total_score)
    output_box.delete(1.0, tk.END)
    output_box.insert(tk.END, "Student with Lowest Score:\n")
    display_student_info(lowest)

def manage_student_record(action):
    #Manage student record by updating or deleting based on user input
    identifier = custom_askstring("Input", "Enter student number or name:")
    if identifier is None:
        return
    for student in students:
        if student.number == identifier or student.name.lower() == identifier.lower():
            if action == "delete":
                students.remove(student)
                save_students_to_file(file_path, students)
                display_message("Student record deleted successfully")
            elif action == "update":
                name = custom_askstring("Input", "Enter new student name:")
                if name is None:
                    return
                coursework1 = custom_askstring("Input", "Enter new coursework mark 1 (out of 20):")
                if coursework1 is None:
                    return
                coursework2 = custom_askstring("Input", "Enter new coursework mark 2 (out of 20):")
                if coursework2 is None:
                    return
                coursework3 = custom_askstring("Input", "Enter new coursework mark 3 (out of 20):")
                if coursework3 is None:
                    return
                exam_mark = custom_askstring("Input", "Enter new exam mark (out of 100):")
                if exam_mark is None:
                    return
                student.name = name
                student.coursework_mark = int(coursework1) + int(coursework2) + int(coursework3)
                student.exam_mark = int(exam_mark)
                student.total_score = student.coursework_mark + student.exam_mark
                student.percentage = (student.total_score / 160) * 100
                student.grade = student.calculate_grade()
                save_students_to_file(file_path, students)
                display_message("Student record updated successfully")
            return
    display_message("Student not found", type="error")

def add_student_record():
    #Add a new student record based on user input
    number = custom_askstring("Input", "Enter student number:")
    if number is None:
        return
    name = custom_askstring("Input", "Enter student name:")
    if name is None:
        return
    coursework1 = custom_askstring("Input", "Enter coursework mark 1 (out of 20):")
    if coursework1 is None:
        return
    coursework2 = custom_askstring("Input", "Enter coursework mark 2 (out of 20):")
    if coursework2 is None:
        return
    coursework3 = custom_askstring("Input", "Enter coursework mark 3 (out of 20):")
    if coursework3 is None:
        return
    exam_mark = custom_askstring("Input", "Enter exam mark (out of 100):")
    if exam_mark is None:
        return

    students.append(Student(number, name, int(coursework1), int(coursework2), int(coursework3), int(exam_mark)))
    save_students_to_file(file_path, students)
    display_message("Student record added successfully")

def sort_student_records():
    #Sort student records based on selected criteria
    dialog = tk.Toplevel(root)
    dialog.title("Sort Students")
    dialog.configure(bg="dark green")
    dialog.geometry("600x300")
    dialog.transient(root)
    dialog.grab_set()

    tk.Label(dialog, text="Sort by:", font=("Overlock", 20, "underline"), bg="dark green", fg="white").pack(pady=10)

    button_frame = tk.Frame(dialog, bg="dark green")
    button_frame.pack(pady=20)

    def sort_and_display(key, reverse=False):
        students.sort(key=key, reverse=reverse)
        dialog.destroy()
        view_all_records()

    
    tk.Button(button_frame, text="Number", command=lambda: sort_and_display(lambda s: s.number), bg="forest green", fg="white", width=10).pack(side=tk.LEFT, padx=10)
    tk.Button(button_frame, text="Name", command=lambda: sort_and_display(lambda s: s.name), bg="forest green", fg="white", width=10).pack(side=tk.LEFT, padx=10)
    tk.Button(button_frame, text="Total Score", command=lambda: sort_and_display(lambda s: s.total_score, reverse=True), bg="forest green", fg="white", width=10).pack(side=tk.LEFT, padx=10)
    tk.Button(button_frame, text="Cancel", command=dialog.destroy, bg="forest green", fg="white", width=10).pack(side=tk.LEFT, padx=10)

    dialog.wait_window(dialog)

# Header
header = tk.Label(root, text="Student Manager", font=("Overlock", 25, "underline", "italic", "bold"), bg="dark green", fg="white")
header.pack(pady=20)

# Frame for buttons
frame1 = tk.Frame(root, bg="forest green")
frame1.pack(pady=10)

# Buttons for viewing student records
view_all_button = tk.Button(frame1, text="View All Student Records", font=("Overlock", 18), command=view_all_records, width=25, bg="dark green", fg="white")
view_all_button.grid(row=0, column=0, padx=5, pady=5)

view_individual_button = tk.Button(frame1, text="View Individual Student Record", font=("Overlock", 18), command=view_individual_record, width=25, bg="dark green", fg="white")
view_individual_button.grid(row=0, column=1, padx=5, pady=5)

highest_score_button = tk.Button(frame1, text="View Student with Highest Score", font=("Overlock", 18), command=show_highest_score, width=25, bg="dark green", fg="white")
highest_score_button.grid(row=1, column=0, padx=5, pady=5)

lowest_score_button = tk.Button(frame1, text="View Student with Lowest Score", font=("Overlock", 18), command=show_lowest_score, width=25, bg="dark green", fg="white")
lowest_score_button.grid(row=1, column=1, padx=5, pady=5)

# Output Box for displaying student information
output_box = tk.Text(root, height=15, width=80)
output_box.pack(pady=10)

# Frame for add/update/delete/sort buttons
frame2 = tk.Frame(root, bg="forest green")
frame2.pack(pady=10)

add_student_button = tk.Button(frame2, text="Add Student Record", font=("Overlock", 18), command=add_student_record, width=25, bg="dark green", fg="white")
add_student_button.grid(row=0, column=0, padx=5, pady=5)

delete_student_button = tk.Button(frame2, text="Delete Student Record", font=("Overlock", 18), command=lambda: manage_student_record("delete"), width=25, bg="dark green", fg="white")
delete_student_button.grid(row=0, column=1, padx=5, pady=5)

update_student_button = tk.Button(frame2, text="Update Student Record", font=("Overlock", 18), command=lambda: manage_student_record("update"), width=25, bg="dark green", fg="white")
update_student_button.grid(row=1, column=0, padx=5, pady=5)

sort_student_button = tk.Button(frame2, text="Sort Student Records", font=("Overlock", 18), command=sort_student_records, width=25, bg="dark green", fg="white")
sort_student_button.grid(row=1, column=1, padx=5, pady=5)

# Start the main event loop
root.mainloop()
