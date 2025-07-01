import argparse
import tkinter as tk
from tkinter import ttk, messagebox
import time
from zxcvbn import zxcvbn
from wordlist_generator import generate_wordlist
import os
import sys

def analyze_password(password):
    result = zxcvbn(password)
    score = result['score']
    feedback = result['feedback']
    return score, feedback

def run_cli():
    parser = argparse.ArgumentParser(description="Password Strength Analyzer and Wordlist Generator")
    parser.add_argument("--password", type=str, required=True, help="Password to analyze")
    parser.add_argument("--name", type=str, required=True, help="User's name")
    parser.add_argument("--pet", type=str, required=True, help="Pet's name")
    parser.add_argument("--year", type=str, required=True, help="Year (e.g. birth year)")
    args = parser.parse_args()

    score, feedback = analyze_password(args.password)
    print(f"Password Strength Score: {score}/4")
    print("Feedback:", feedback.get('warning', ''), " | Suggestions:", ', '.join(feedback.get('suggestions', [])))

    wordlist = generate_wordlist(args.name, args.pet, args.year)
    os.makedirs("output", exist_ok=True)
    with open("output/rockyou.txt", "w") as f:
        for word in wordlist:
            f.write(word + "\n")
    print("Wordlist saved to output/rockyou.txt")

def run_gui():
    def gui_analyze_password():
        password = password_entry.get()
        score, feedback = analyze_password(password)
        score_label.config(text=f"Password Strength: {score}/4", fg="blue")
        suggestion_label.config(text="Suggestions: " + ", ".join(feedback.get('suggestions', [])))

    def generate_and_save_wordlist():
        name = name_entry.get()
        pet = pet_entry.get()
        year = year_entry.get()

        if not name or not pet or not year:
            messagebox.showerror("Missing Info", "Please fill all fields to generate wordlist.")
            return

        progress_bar['value'] = 0
        root.update_idletasks()
        for _ in range(5):
            progress_bar['value'] += 20
            root.update_idletasks()
            time.sleep(0.1)

        wordlist = generate_wordlist(name, pet, year)

        with open("output/rockyou.txt", "w") as f:
            for word in wordlist:
                f.write(word + "\n")

        progress_bar['value'] = 100
        messagebox.showinfo("Success", "Wordlist saved to output/rockyou.txt")

    root = tk.Tk()
    root.title("Password Strength Analyzer + Wordlist Generator")
    root.geometry("450x450")
    root.resizable(False, False)

    font_label = ("Arial", 11)
    font_entry = ("Arial", 10)

    frame = tk.Frame(root, padx=20, pady=10)
    frame.pack(expand=True, fill="both")

    tk.Label(frame, text="Enter Password:", font=font_label).pack(anchor="w", pady=(0, 2))
    password_entry = tk.Entry(frame, show="*", width=40, font=font_entry)
    password_entry.pack(pady=(0, 5))

    tk.Button(frame, text="Analyze Password", command=gui_analyze_password).pack(pady=(0, 5))
    score_label = tk.Label(frame, text="", font=font_label)
    score_label.pack()
    suggestion_label = tk.Label(frame, text="", font=font_entry, wraplength=400, justify="left")
    suggestion_label.pack(pady=(0, 10))

    tk.Label(frame, text="Generate Wordlist", font=("Arial", 12, "bold")).pack(pady=(10, 4))
    tk.Label(frame, text="Name:", font=font_label).pack(anchor="w")
    name_entry = tk.Entry(frame, width=40, font=font_entry)
    name_entry.pack(pady=(0, 5))

    tk.Label(frame, text="Pet Name:", font=font_label).pack(anchor="w")
    pet_entry = tk.Entry(frame, width=40, font=font_entry)
    pet_entry.pack(pady=(0, 5))

    tk.Label(frame, text="Birth Year (YYYY):", font=font_label).pack(anchor="w")
    year_entry = tk.Entry(frame, width=40, font=font_entry)
    year_entry.pack(pady=(0, 10))

    tk.Button(frame, text="Generate Wordlist", command=generate_and_save_wordlist).pack(pady=10)
    progress_bar = ttk.Progressbar(frame, orient="horizontal", length=300, mode="determinate")
    progress_bar.pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_cli()
    else:
        run_gui()