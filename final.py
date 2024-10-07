import fitz  # PyMuPDF
import pytesseract
import cv2
from docx import Document
import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
import difflib
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

def extract_text_from_pdf(pdf_path):
    text = ""
    doc = fitz.open(pdf_path)
    for page in doc:
        text += page.get_text()
    return text

def extract_text_from_image(image_path):
    image = cv2.imread(image_path)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    text = pytesseract.image_to_string(rgb_image)
    return text

def extract_text_from_docx(docx_path):
    text = ""
    doc = Document(docx_path)
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

def extract_text_from_txt(txt_path):
    with open(txt_path, 'r', encoding='utf-8') as file:
        return file.read()

def load_document(file_path):
    logging.info(f"Loading document: {file_path}")
    if file_path.endswith('.pdf'):
        return extract_text_from_pdf(file_path)
    elif file_path.endswith('.docx'):
        return extract_text_from_docx(file_path)
    elif file_path.endswith('.txt'):
        return extract_text_from_txt(file_path)
    else:
        return extract_text_from_image(file_path)

def load_file():
    file_path = filedialog.askopenfilename(title="Select Document")
    if not file_path:
        messagebox.showwarning("Warning", "Please select a document.")
        return

    text = load_document(file_path)
    if text:
        if text_area1.get("1.0", tk.END).strip() == "":
            text_area1.insert(tk.END, text)
            update_status(f"Loaded document: {file_path}")
        elif text_area2.get("1.0", tk.END).strip() == "":
            text_area2.insert(tk.END, text)
            update_status(f"Loaded document: {file_path}")
            show_differences(text_area1.get("1.0", tk.END).strip(), text_area2.get("1.0", tk.END).strip())
        else:
            messagebox.showinfo("Info", "Both documents are already loaded. Please clear before loading again.")

def show_differences(text1, text2):
    text_area1.delete(1.0, tk.END)
    text_area2.delete(1.0, tk.END)

    d = difflib.ndiff(text1.splitlines(), text2.splitlines())
    diff = list(d)

    for line in diff:
        if line.startswith('+ '):
            text_area2.insert(tk.END, line[2:] + '\n', 'added')
        elif line.startswith('- '):
            text_area1.insert(tk.END, line[2:] + '\n', 'removed')
        else:
            text_area1.insert(tk.END, line[2:] + '\n')
            text_area2.insert(tk.END, line[2:] + '\n')

    text_area1.tag_config('removed', foreground='red')
    text_area2.tag_config('added', foreground='green')

def clear_text():
    text_area1.delete(1.0, tk.END)
    text_area2.delete(1.0, tk.END)
    update_status("Ready")

def update_status(message):
    logging.info(message)

# Create the main application window
root = tk.Tk()
root.title("Document Comparison - By xd932")

# Configure initial grid weights
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
root.rowconfigure(0, weight=1)  # Adjust weight for text areas

# Create frames for layout
frame = tk.Frame(root)
frame.grid(sticky='nsew')

# Create text areas with adjusted heights
text_area1 = scrolledtext.ScrolledText(frame, wrap=tk.WORD, height=30)  # Adjust height as needed
text_area1.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
text_area2 = scrolledtext.ScrolledText(frame, wrap=tk.WORD, height=30)  # Adjust height as needed
text_area2.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)


# Create Load and Clear buttons
button_frame = tk.Frame(root)
button_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky='ew')

load_button = tk.Button(button_frame, text="Load Document", command=load_file)
load_button.grid(row=0, column=0, padx=5)

clear_button = tk.Button(button_frame, text="Clear", command=clear_text)
clear_button.grid(row=0, column=1, padx=5)

# Function to update the grid weights based on window size
def update_grid_weights(event):
    window_width = root.winfo_width()
    if window_width < 800:
        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=1)
    else:
        root.columnconfigure(0, weight=2)
        root.columnconfigure(1, weight=3)


    # Update text area heights based on window height
    window_height = root.winfo_height()
    text_area1.config(height=int(window_height * 0.8))
    text_area2.config(height=int(window_height * 0.8))
# Bind the update_grid_weights function to the window's resize event
root.bind("<Configure>", update_grid_weights)

# Run the application
root.mainloop()
