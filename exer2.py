import random
from tkinter import *

class AlexaJokeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Exercise 2 | Alexa Tell me a Joke")
        self.root.geometry("700x400")
        self.root.resizable(False, False)
        self.root.configure(bg="dark green")
        self.root.option_add("*Font", "Arial 16")
        
        self.setup_ui()
        self.jokes = self.read_jokefile(r"C:\\Users\\gamet\\School Files\\jokes.txt")
        
    def setup_ui(self):
        #Set up the user interface components
        self.header = Label(self.root, text="Make alexa tell u a joke", fg="#00ff00", bg="dark green", font=("Arial", 24, "bold"), padx=10, pady=10)
        self.header.pack(pady=10)
        self.subheader = Label(self.root, text="PS: type 'alexa tell me a joke'", fg="#00ff00", bg="dark green", font=("Arial", 14), padx=10, pady=5)
        self.subheader.pack(pady=5)
        
        self.input_entry = Entry(self.root, width=30)
        self.input_entry.pack(pady=20)
        self.input_entry.bind("<Return>", self.process_input)
        
        self.suggestion_label = Label(self.root, text="", fg="red", bg="dark green")
        self.suggestion_label.pack(pady=5)
        
        self.joke_label = Label(self.root, text="", fg="#00ff00", bg="dark green")
        self.joke_label.pack(pady=20)
        
        self.punchline_button = Button(self.root, text="Tell me", command=self.display_joke_punchline, bg="dark green", fg="black")
        self.punchline_button.pack_forget()
        
        self.quit_button = Button(self.root, text="Exit", command=self.root.quit, bg="dark green", fg="black")
        self.quit_button.pack(pady=10)
    
    def read_jokefile(self, filename):
        #Read jokes from the text file
        with open(filename, 'r') as file:
            return [line.strip().split('?') for line in file]
    
    def display_suggestion(self):
        #Display a suggestion if the input is incorrect
        self.suggestion_label.config(text="Alexa can't answer that. Maybe try typing 'Alexa tell me a joke'?")
        self.root.after(2000, self.clear_suggestion)
    
    def clear_suggestion(self):
        #Clear the suggestion text
        self.suggestion_label.config(text="")
    
    def process_input(self, event=None):
        #Process the user's input
        user_input = self.input_entry.get().strip().lower()
        if "alexa tell me a joke" in user_input:
            self.display_joke()
        else:
            self.display_suggestion()
        self.input_entry.delete(0, END)
    
    def display_joke(self):
        #Display the initial joke setup
        self.setup, self.punchline = random.choice(self.jokes)
        self.input_entry.pack_forget()
        self.suggestion_label.pack_forget()
        self.quit_button.pack_forget()
        self.joke_label.config(text=self.setup + "?")
        self.punchline_button.pack()
    
    def display_joke_punchline(self):
        #"Display the punchline of the joke
        self.joke_label.config(text=self.punchline)
        self.punchline_button.pack_forget()
        for widget in self.root.pack_slaves():
            if isinstance(widget, Button) and widget.cget("text") in ["Tell Another Joke", "Ask a Different Prompt"]:
                widget.pack_forget()
        Button(self.root, text="Tell Another Joke", command=self.display_joke, bg="dark green", fg="black").pack(side=LEFT, padx=20, pady=10)
        Button(self.root, text="Ask a Different Prompt", command=self.reset_to_prompt, bg="dark green", fg="black").pack(side=RIGHT, padx=20, pady=10)
    
    def reset_to_prompt(self):
        #Reset the interface to the initial state
        self.joke_label.config(text="")
        for widget in self.root.pack_slaves():
            widget.pack_forget()
        self.header.pack(pady=10)
        self.subheader.pack(pady=5)
        self.input_entry.pack(pady=5)
        self.suggestion_label.pack(pady=5)
        self.quit_button.pack(pady=10)
        self.joke_label.pack(pady=5)
        self.punchline_button.pack_forget()
        
# Main Program window
root = Tk()
app = AlexaJokeApp(root)
root.mainloop()
