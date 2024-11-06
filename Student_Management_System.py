# question = Write a program that allows users to manage student records.
# Input = The program will prompt users for inputs based on actions like adding or deleting a student.
# Output = Display the student records or confirmation of actions taken.

# Define a class `Student` to represent a student's information
class Student:
    # Initialize the student with ID, name, age, and grade
    def __init__(self, student_id, name, age, grade):
        self.student_id = student_id  # Unique ID for the student
        self.name = name              # Name of the student
        self.age = age                # Age of the student
        self.grade = grade            # Grade of the student

    # Method to display student information in a formatted way
    def display_info(self):
        print(f"ID: {self.student_id}, Name: {self.name}, Age: {self.age}, Grade: {self.grade}")

# Define a `StudentManagementSystem` class to manage multiple student records
class StudentManagementSystem:
    # Initialize an empty list to store student objects
    def __init__(self):
        self.students = []  # List to store Student objects

    # Method to add a new student to the system
    def add_student(self, student_id, name, age, grade):
        # Create a new `Student` object and append it to the students list
        student = Student(student_id, name, age, grade)
        self.students.append(student)  # Add student to the system
        print(f"Student {name} added successfully!")  # Confirmation message

    # Method to delete a student by their ID
    def delete_student(self, student_id):
        # Iterate over each student to find the matching ID
        for student in self.students:
            if student.student_id == student_id:  # Check if ID matches
                self.students.remove(student)  # Remove student from list
                print(f"Student {student.name} with ID {student_id} removed successfully!")
                return  # Exit after deletion
        print(f"No student found with ID {student_id}.")  # If no match, display message

    # Method to display all student records
    def display_students(self):
        # Check if there are any students to display
        if not self.students:
            print("No students to display.")  # Message if list is empty
        else:
            print("Student Records:")
            for student in self.students:  # Loop through all students
                student.display_info()  # Display each student's information

# Main function to interact with the Student Management System
def main():
    system = StudentManagementSystem()  # Create an instance of the system
    
    # Loop to keep the program running until the user chooses to exit
    while True:
        # Display the menu options to the user
        print("\n1. Add Student\n2. Delete Student\n3. Display All Students\n4. Exit")
        choice = input("Enter your choice: ")

        # Option to add a new student
        if choice == '1':
            student_id = input("Enter student ID: ")  # Get student ID from user
            name = input("Enter student name: ")      # Get student name from user
            age = input("Enter student age: ")        # Get student age from user
            grade = input("Enter student grade: ")    # Get student grade from user
            system.add_student(student_id, name, age, grade)  # Add student to system

        # Option to delete an existing student
        elif choice == '2':
            student_id = input("Enter student ID to delete: ")  # Get ID of student to delete
            system.delete_student(student_id)  # Delete student from system

        # Option to display all student records
        elif choice == '3':
            system.display_students()  # Display all students in the system

        # Option to exit the program
        elif choice == '4':
            print("Exiting the program.")  # Print exit message
            break  # Exit the loop and end the program

        # Handle invalid menu choices
        else:
            print("Invalid choice. Please try again.")  # Error message for invalid input

# Run the main function when the script is executed
if __name__ == "__main__":
    main()
