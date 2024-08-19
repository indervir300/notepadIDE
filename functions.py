import os.path
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
import htmlDetection as colorHtml


def new_file(text_area, root, event=None):
    text_area.delete(1.0, tk.END)
    root.title("Untitled - IDE")


def file_ext(root, file_path, text_area):
    # Extract the file ext and display
    root.file_extension = os.path.splitext(file_path)[1][1:]
    root.file_extension_label.configure(text=f" {root.file_extension}")
    if root.file_extension in ["html", "htm"]:
        print("Html opened")
        colorizer = colorHtml.HTMLColorizer(text_area)
        # colorizer.load_file(file_path)
        colorizer.colorize_html()
        text_area.bind("KeyRelease", colorizer.on_text_change)


def open_file(text_area, root, event=None):
    file_path = filedialog.askopenfilename(defaultextension=".html",
                                           filetypes=[("Text Files", "*.txt"), ("Python", "*.py"),
                                                      ("HTML", "*.html"), ("CSS", "*.css"),
                                                      ("Javascript", "*.js"), ("HTML", "*.htm"),
                                                      ("Ejs", "*.ejs"), ("JAVA", "*.java"), 
                                                      ("TSX", "*.tsx"), ("JSX", "*.jsx"), 
                                                      ("JSON", "*.json")])
    if file_path:
        with open(file_path, "r") as file:
            text_area.delete(1.0, tk.END)
            text_area.insert(1.0, file.read())
        root.title(f"{file_path} - IDE")

        # # Extract the file ext and display
        file_ext(root, file_path, text_area)


def save_file(text_area, root, event=None):
    try:
        title = root.title()
        if title.startswith("Untitled"):
            save_as_file(text_area, root)
        else:
            file_path = title.split(" - ")[0]
            with open(file_path, "w") as file:
                file.write(text_area.get(1.0, tk.END))
            show_success_label(root)
            file_ext(root, file_path, text_area)
    except Exception as e:
        messagebox.showerror("Save File", f"Error: {e}")


def save_as_file(text_area, root, event=None):
    file_path = filedialog.asksaveasfilename(defaultextension=".html",
                                           filetypes=[("Text Files", "*.txt"), ("Python", "*.py"),
                                                      ("HTML", "*.html"), ("CSS", "*.css"),
                                                      ("Javascript", "*.js"), ("HTML", "*.htm"),
                                                      ("Ejs", "*.ejs"), ("JAVA", "*.java"), 
                                                      ("TSX", "*.tsx"), ("JSX", "*.jsx"), 
                                                      ("JSON", "*.json")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(text_area.get(1.0, tk.END))
        root.title(f"{file_path} - IDE")
        show_success_label(root)
        file_ext(root, file_path, text_area)


def show_success_label(root):
    success_label = ctk.CTkLabel(root, text="Saved", width=80, font=("Segoe UI Variable Text", 12), fg_color="#202020")
    success_label.place(relx=0.5, rely=0.9, anchor='s')
    root.after(1000, success_label.destroy)


def bind_shortcuts(app):
    app.root.bind('<Control-n>', lambda event: new_file(app.text_area, app.root, event))
    app.root.bind('<Control-o>', lambda event: open_file(app.text_area, app.root, event))
    app.root.bind('<Control-s>', lambda event: save_file(app.text_area, app.root, event))
    app.root.bind('<Control-Shift-KeyPress-S>',
                  lambda event: save_as_file(app.text_area, app.root, event))


def exit_app():
    quit()


def undo_action():
    print("Undo action")


def redo_action():
    print("Redo action")


def cut_action():
    print("Cut action")


def copy_action():
    print("Copy action")


def paste_action():
    print("Paste action")


def delete_action():
    print("Delete action")
