import os
import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import filedialog, messagebox
from langdetect import detect
import time

def translate_with_google_translate(text, source_lang, target_lang):
    url = f'https://translate.google.com/m?hl={target_lang}&sl={source_lang}&q={text}'
    
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        translation = soup.find('div', {'class': 'result-container'}).text.strip()
        return translation
    else:
        return f"Translation request failed with status code: {response.status_code}"

def translate_and_save_to_user_path():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    
    if not file_path:
        return

    detected_language = detect(open(file_path, 'r', encoding='utf-8').read())
    
    detected_language_label = tk.Label(app, text=f"Language: {detected_language}")
    detected_language_label.pack()
    
    app.update_idletasks()  # Update the GUI to show the detected language
    
    save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    
    if not save_path:
        return
    
    with open(file_path, 'r', encoding='utf-8') as input_file:
        with open(save_path, 'w', encoding='utf-8') as translated_file:
            for line in input_file:
                line = line.strip()
                if line:
                    translated_line = translate_with_google_translate(line, detected_language, "en")
                    translated_file.write(translated_line + '\n')
    
    messagebox.showinfo("Success", f"Translation saved to '{save_path}'")
    messagebox.showinfo("File Uploaded", "File Uploaded")

app = tk.Tk()
app.title("Text Translator")
app.geometry("200x200")  # Set the GUI size to 200x200

upload_button = tk.Button(app, text="Upload Text File", command=translate_and_save_to_user_path)
upload_button.pack()

app.mainloop()
