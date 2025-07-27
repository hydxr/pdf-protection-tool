import tkinter as tk
from tkinter import filedialog, messagebox
import PyPDF2
import os

def protect_pdf(input_pdf, output_pdf, password):
    try:
        with open(input_pdf, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            pdf_writer = PyPDF2.PdfWriter()

            for page in pdf_reader.pages:
                pdf_writer.add_page(page)

            pdf_writer.encrypt(password)

            with open(output_pdf, 'wb') as output_file:
                pdf_writer.write(output_file)

        messagebox.showinfo("Success", f"Protected PDF saved as:\n{output_pdf}")
    except FileNotFoundError:
        messagebox.showerror("Error", f"The file {input_pdf} was not found.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, file_path)

def encrypt_pdf():
    input_pdf = file_entry.get()
    password = password_entry.get()

    if not input_pdf.lower().endswith(".pdf"):
        messagebox.showerror("Invalid File", "Please select a valid PDF file.")
        return

    if not os.path.exists(input_pdf):
        messagebox.showerror("File Not Found", "Selected file does not exist.")
        return

    if not password:
        messagebox.showwarning("Missing Password", "Please enter a password.")
        return

    output_pdf = os.path.splitext(input_pdf)[0] + "_protected.pdf"
    protect_pdf(input_pdf, output_pdf, password)

# GUI Setup
root = tk.Tk()
root.title("PDF Password Protector")
root.geometry("500x250")
root.resizable(False, False)
root.configure(bg="#1e1e2f")

# File Selection
tk.Label(root, text="Select PDF:", fg="white", bg="#1e1e2f", font=("Arial", 12)).pack(pady=(20, 5))
file_frame = tk.Frame(root, bg="#1e1e2f")
file_frame.pack(pady=5)

file_entry = tk.Entry(file_frame, width=40, font=("Arial", 10))
file_entry.pack(side=tk.LEFT, padx=10)

browse_button = tk.Button(file_frame, text="Browse", command=browse_file, bg="#5c5cff", fg="white")
browse_button.pack(side=tk.LEFT)

# Password Entry
tk.Label(root, text="Enter Password:", fg="white", bg="#1e1e2f", font=("Arial", 12)).pack(pady=(15, 5))
password_entry = tk.Entry(root, show="*", width=30, font=("Arial", 10))
password_entry.pack(pady=5)

# Encrypt Button
encrypt_button = tk.Button(root, text="Protect PDF", command=encrypt_pdf, bg="#00b894", fg="white", font=("Arial", 12, "bold"), width=20)
encrypt_button.pack(pady=20)

root.mainloop()
