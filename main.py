import re
import tkinter as tk
from tkinter.scrolledtext import ScrolledText

import nltk
from nltk.corpus import words
from difflib import get_close_matches
import time

nltk.download("words")

class SpellChecker:

    def __init__(self, file_path):
        self.file_path = file_path
        self.root = tk.Tk()
        self.root.geometry("600x500")

        self.text = ScrolledText(self.root, font=("Arial", 14))
        self.text.pack()

        self.load_file()
        self.correct()
        self.root.mainloop()

    def load_file(self):
        try:
            with open(self.file_path, 'r') as file:
                content = file.read()
                self.text.insert("1.0", content)
        except FileNotFoundError:
            print(f"File not found: {self.file_path}")

    def correct(self):
        start_time = time.time()

        content = self.text.get("1.0", tk.END)
        corrected_content = ""

        for word in content.split(" "):
            cleaned_word = re.sub(r"[^\w]", "", word.lower())
            if cleaned_word not in words.words():
                suggestions = get_close_matches(cleaned_word, words.words())
                if suggestions:
                    closest_match = suggestions[0]
                    corrected_content += closest_match + " "
                    self.text.tag_add(closest_match, f"1.{len(corrected_content) - len(word)}", f"1.{len(corrected_content)}")
                    self.text.tag_config(closest_match, foreground="green")
                else:
                    corrected_content += word + " "
                    self.text.tag_add(word, f"1.{len(corrected_content) - len(word)}", f"1.{len(corrected_content)}")
                    self.text.tag_config(word, foreground="red")
            else:
                corrected_content += word + " "

        self.text.delete("1.0", tk.END)
        self.text.insert("1.0", corrected_content)

        end_time = time.time()
        elapsed_time = end_time - start_time
        word_count = len(content.split())
        response_time_per_1000_words = (elapsed_time / word_count) * 1000
        print(f"Response time per 1000 words: {response_time_per_1000_words:.2f} seconds")

    def save_file(self):
        corrected_content = self.text.get("1.0", tk.END)
        with open(self.file_path, 'w') as file:
            file.write(corrected_content)

file_path = "Check.txt"
checker = SpellChecker(file_path)
checker.save_file()
