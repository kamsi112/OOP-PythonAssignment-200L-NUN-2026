import tkinter as tk
from tkinter import filedialog, messagebox
from flashcard_engine import (extract_pdf_text,
    clean_text,
    split_sentences,
    generate_all_flashcards,
    filter_flashcards,
    shuffle_flashcards,
    save_flashcards,)
# Import  functions
from flashcard_engine import (extract_pdf_text,clean_text,split_sentences,generate_all_flashcards,filter_flashcards, shuffle_flashcards,)

# Global Variables
flashcards = []
selected_cards = []
current_question = 0
score = 0

# Browse for PDF
def browse_pdf():
    filename = filedialog.askopenfilename(title="Select PDF",filetypes=[("PDF Files", "*.pdf")])
    if filename:
        pdf_entry.delete(0, tk.END)
        pdf_entry.insert(0, filename)

# Generate Flashcards
def generate_cards():
    global flashcards
    pdf_file = pdf_entry.get()
    if not pdf_file:
        messagebox.showerror("Error", "Please select a PDF.")
        return
    output_file = pdf_file.replace(".pdf", ".txt")
    text = extract_pdf_text(pdf_file, output_file)
    if not text:
        messagebox.showerror("Error", "Could not extract text.")
        return
    cleaned = clean_text(text)
    sentences = split_sentences(cleaned)
    flashcards = generate_all_flashcards(sentences)
    messagebox.showinfo( "Success", f"{len(flashcards)} flashcards generated!")

# Start Quiz
def start_quiz():
    global selected_cards
    global current_question
    global score
    if not flashcards:
        messagebox.showerror( "Error", "Generate flashcards first.")
        return
    difficulty = difficulty_var.get()
    selected_cards = filter_flashcards(flashcards,difficulty)
    if not selected_cards:
        messagebox.showerror("Error","No flashcards available.")
        return
    shuffle_flashcards(selected_cards)
    current_question = 0
    score = 0
    show_question()

# Display Question
def show_question():
    if current_question >= len(selected_cards):
        percentage = ( score / len(selected_cards)) * 100
        messagebox.showinfo("Quiz Finished", f"Score: {score}/{len(selected_cards)}\n"f"Percentage: {percentage:.1f}%")
        question_label.config(text="Quiz Complete!")
        answer_entry.delete(0, tk.END)
        return
    question_label.config(text=selected_cards[current_question]["question"])
    answer_entry.delete(0, tk.END)


# Check Answer
def submit_answer():
    global current_question
    global score
    answer = answer_entry.get().strip().lower()
    correct = (selected_cards[current_question]["answer"].strip().lower())
    if answer == correct:
        score += 1
        messagebox.showinfo( "Correct", "Correct!")
    else:
        messagebox.showinfo("Incorrect",f"Correct Answer:\n{correct}")
    current_question += 1

# GUI
window = tk.Tk()
window.title("Flashcard Quiz Generator")
window.geometry("700x500")
# Title
title = tk.Label(window,text="Flashcard Quiz Generator",font=("Arial", 20, "bold"))
title.pack(pady=15)
# PDF
frame = tk.Frame(window)
frame.pack()
pdf_entry = tk.Entry(frame,width=50)
pdf_entry.pack(side=tk.LEFT,padx=5)
browse_button = tk.Button(frame,text="Browse",command=browse_pdf)
browse_button.pack(side=tk.LEFT)
# Difficulty
difficulty_var = tk.StringVar(value="easy")
difficulty_frame = tk.Frame(window)
difficulty_frame.pack(pady=10)
tk.Label(difficulty_frame,text="Difficulty:").pack(side=tk.LEFT)
tk.Radiobutton(difficulty_frame,text="Easy",variable=difficulty_var,value="easy").pack(side=tk.LEFT)
tk.Radiobutton(difficulty_frame,text="Hard",variable=difficulty_var,value="hard").pack(side=tk.LEFT)
# Buttons
generate_button = tk.Button(window,text="Generate Flashcards",command=generate_cards)
generate_button.pack(pady=10)
start_button = tk.Button(window,text="Start Quiz",command=start_quiz)
start_button.pack()
# Question
question_label = tk.Label(window,text="",wraplength=600,font=("Arial", 14))
question_label.pack(pady=20)
# Answer
answer_entry = tk.Entry(window,width=50)
answer_entry.pack()
submit_button = tk.Button(window,text="Submit Answer",command=submit_answer)
submit_button.pack(pady=10)
window.mainloop()