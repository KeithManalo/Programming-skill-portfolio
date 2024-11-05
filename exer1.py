import tkinter as tk
from tkinter import messagebox
import random

class ArithmeticQuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Arithmetic Quiz")
        self.root.configure(bg="dark green")
        root.geometry("700x400")
        
        # Header label for the title of the quiz
        self.header_label = tk.Label(root, text="Arithmetic Math Quiz Simulator", font=("Overlock", 24), fg="white", bg="dark green")
        self.header_label.pack(pady=10)
        
        # Subtext label for displaying instructions and messages
        self.subtext_label = tk.Label(root, text="", font=("Overlock", 14), fg="black", bg="light green")
        self.subtext_label.pack(pady=5)
        
        # Initialize score, question count, difficulty level, and attempts
        self.score = 0
        self.question_count = 0
        self.difficulty = 'Easy'
        self.attempts = 0
        
        # Display the main menu
        self.displayMenu()

    def clearScreen(self):
        #Clears all widgets except the header and subtext labels
        for widget in self.root.winfo_children():
            if widget not in (self.header_label, self.subtext_label):
                widget.destroy()
                
    def displayMenu(self):
        #Displays the main menu with difficulty options
        self.clearScreen()
        self.header_label.config(text="Arithmetic Math Quiz Simulator", font=("Overlock", 24), fg="white", bg="dark green")
        self.subtext_label.config(text="Please select a difficulty", font=("Overlock", 14), fg="black", bg="forest green")
        tk.Button(self.root, text="Easy", command=lambda: self.set_difficulty('Easy'), font=("Overlock", 12), bg="forest green").pack(pady=5)
        tk.Button(self.root, text="Moderate", command=lambda: self.set_difficulty('Moderate'), font=("Overlock", 12), bg="forest green").pack(pady=5)
        tk.Button(self.root, text="Advanced", command=lambda: self.set_difficulty('Advanced'), font=("Overlock", 12), bg="forest green").pack(pady=5)
    
    def set_difficulty(self, level):
        #Sets the difficulty level and starts the quiz
        self.difficulty = level
        self.clearScreen()
        self.startQuiz()

    def randomInt(self):
        #Generates random integers based on the difficulty level
        if self.difficulty == 'Easy':
            return random.randint(1, 9), random.randint(1, 9)
        elif self.difficulty == 'Moderate':
            return random.randint(10, 99), random.randint(10, 99)
        elif self.difficulty == 'Advanced':
            return random.randint(1000, 9999), random.randint(1000, 9999)

    def decideOperation(self):
        #Randomly decides the operation addition or subtraction
        return random.choice(['+', '-'])
    
    def displayProblem(self):
        #Displays the math problem to the user
        self.num1, self.num2 = self.randomInt()
        self.operation = self.decideOperation()
        self.problem_label.config(text=f"{self.num1} {self.operation} {self.num2} = ?", font=("Overlock", 16), bg="light green")
        self.answer_entry.delete(0, tk.END)
        self.attempts = 0
        self.subtext_label.config(text=f"Question {self.question_count + 1}", font=("Overlock", 14), fg="black", bg="light green")
        
    def isCorrect(self, user_answer):
        #Checks if the user's inputted answer is correct
        correct_answer = eval(f"{self.num1} {self.operation} {self.num2}")
        return user_answer == correct_answer

    def checkAnswer(self):
        #Provides feedback to the user and updates the score accordingly
        try:
            user_answer = int(self.answer_entry.get())
            if self.isCorrect(user_answer):
                if self.attempts == 0:
                    self.score += 1
                else:
                    self.score += 0.5
                self.feedback_label.config(text="Correct!", fg="dark green", bg="light green")
                self.nextQuestion()
            else:
                self.attempts += 1
                if self.attempts < 2:
                    self.feedback_label.config(text="Incorrect, try again!", fg="black", bg="light green")
                else:
                    self.feedback_label.config(text=f"Incorrect, the correct answer was {eval(f'{self.num1} {self.operation} {self.num2}')}", fg="red", bg="lightgrey")
                    self.nextQuestion()
        except ValueError:
            self.feedback_label.config(text="Please enter a valid number.", fg="red", bg="dark green")
            
    def nextQuestion(self):
        #Moves to the next question or displays results if the quiz is over
        self.question_count += 1
        if self.question_count < 10:
            self.displayProblem()
        else:
            self.displayResults()

    def displayResults(self):
        #Displays the final results and grade
        self.problem_label.pack_forget()
        self.answer_entry.pack_forget()
        self.submit_button.pack_forget()
        
        grade = self.calculateGrade()
        
        self.feedback_label.config(text=f"Your final score is {self.score}/10\nGrade: {grade}", fg="blue", bg="light green")
        self.subtext_label.config(text="Would you like to play again?", font=("Overlock", 14), fg="black", bg="light green")
        
        button_frame = tk.Frame(self.root, bg="dark green")
        button_frame.pack(pady=5)
        
        tk.Button(button_frame, text="Yes", command=self.resetQuiz, font=("Overlock", 12), bg="lightgrey").pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="No", command=self.root.destroy, font=("Overlock", 12), bg="lightgrey").pack(side=tk.LEFT, padx=10)

    def calculateGrade(self):
        #Calculates the grade based on the score
        if self.score > 9:
            return "A+"
        elif self.score > 8:
            return "A"
        elif self.score > 7:
            return "B"
        elif self.score > 6:
            return "C"
        else:
            return "D"

    def resetQuiz(self):
        #Resets the quiz to the initial state
        self.score = 0
        self.question_count = 0
        self.clearScreen()
        self.displayMenu()

    def startQuiz(self):
        #Starts the quiz by displaying the first problem
        self.header_label.config(text="Arithmetic Math Quiz Simulator", font=("Overlock", 24, "bold"), fg="white", bg="dark green")
        self.subtext_label.config(text=f"Question {self.question_count + 1}", font=("Overlock", 14), fg="black", bg="light green")
        self.problem_label = tk.Label(self.root, text="", font=("Overlock", 16), bg="light green")
        self.problem_label.pack(pady=20)
        self.answer_entry = tk.Entry(self.root, font=("Overlock", 16))
        self.answer_entry.pack(pady=10)
        self.submit_button = tk.Button(self.root, text="Submit", command=self.checkAnswer, font=("Overlock", 12), bg="light green")
        self.submit_button.pack(pady=20)
        self.feedback_label = tk.Label(self.root, text="", font=("Overlock", 12), bg="light green")
        self.feedback_label.pack(pady=10)
        self.displayProblem()

# Main Program window
root = tk.Tk()
app = ArithmeticQuizApp(root)
root.mainloop()
