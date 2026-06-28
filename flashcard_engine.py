from PyPDF2 import PdfReader
import json
import random
#STAGE 2 -PDF EXTRACTION
def extract_pdf_text(pdf_file, output_file):
    try:
        reader = PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted 
        if text.strip():
            with open(output_file, "w", encoding ="utf-8") as file:
                file.write(text)
            print(f"Text extracted and saved to {output_file}")
            return text
        else:
            print("No text extracted.")
            return None
    except FileNotFoundError:
        print("Unable to find PDF file.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
       

        
# STAGE 4 - CLEAN TEXT
def clean_text(text):
    text = text.replace("\n", " ")
    text = " ".join(text.split())
    text = text.strip()
    return text

# STAGE 5 - SPLIT SENTENCES
def split_sentences(text):
    sentences = text.split(".")
    cleaned_sentences = []
    for sentence in sentences:
        sentence = sentence.strip()
        if sentence:
            if len(sentence) > 10:
                cleaned_sentences.append(sentence)
    return cleaned_sentences
# STAGE 6  - EASY FLASHCARDS
def generate_flashcard(sentence):
    if " is " in sentence:
        parts = sentence.split(" is ", 1)
        flashcard = { "question": f"What is {parts[0].strip()}?",
                       "answer" : parts[1].strip(),
                        "difficulty":  "easy"}
        return flashcard
    else:
        return None
#STAGE 8 - HARD FLASHCARD
def generate_hard_flashcard(sentence):
    words = sentence.split()
    if len(words) < 4:
        return None
    answer = words[-1]
    words[-1] = "_____"
    return {
        "question": " ".join(words),
        "answer": answer,
        "difficulty": "hard"}
        
# STAGE 9 - ALL FLASHCARDS
def generate_all_flashcards(sentences):
    flashcards = []
    for sentence in sentences:
        easy = generate_flashcard(sentence)
        if easy:
            flashcards.append(easy)
        hard = generate_hard_flashcard(sentence)
        if hard:
            flashcards.append(hard)
    return flashcards

# STAGE 10 - QUIZ ENGINE
def run_quiz(flashcards):
    score = 0
    for card in flashcards:
        user_answer = input(card["question"] + "\n> ")
        if (user_answer.strip().lower()==card["answer"].lower()):
            print("✓ Correct")
            score += 1
        else:
            print("✗ Wrong")
            print("Answer:", card["answer"])
    return score


# STAGE 11 - DIFFICULTY FILTER
def filter_flashcards(flashcards,difficulty):
    selected = []
    for card in flashcards:
        if card["difficulty"] == difficulty:
            selected.append(card)
    return selected

# STAGE 12 - SAVE FLASHCARDS
def save_flashcards(flashcards,filename):
    with open(filename,"w",encoding="utf-8") as file:
        json.dump(flashcards,file,indent=4,ensure_ascii=False)

# STAGE 13 - LOAD FLASHCARDS
def load_flashcards(filename):
    with open(filename,"r",encoding="utf-8") as file:
        return json.load(file)

# STAGE 14 - RANDOMIZE ORDER
def shuffle_flashcards(flashcards):
    random.shuffle(flashcards)
    return flashcards
