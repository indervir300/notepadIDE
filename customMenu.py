import customtkinter as ctk
from functions import *
from functools import partial
from tkinter import font


class CustomMenuBar:
    def __init__(self, root, text_area, button_bg_color, button_hover_color):
        # print(font.families())
        self.root = root
        self.text_area = text_area
        self.button_bg_color = button_bg_color
        self.button_hover_color = button_hover_color
        self.width = 60
        self.menus = []
        self.menu_frame = ctk.CTkFrame(self.root, corner_radius=0, fg_color="#202020")
        self.menu_frame.pack(side="top", fill="x")
        self.shortcuts = {
            "New": "Ctrl+N",
            "Open": "Ctrl+O",
            "Save": "Ctrl+S",
            "Save as": "Ctrl+Shift+S",
            "Exit": "Alt+F4",
            "Undo": "Ctrl+Z",
            "Redo": "Ctrl+Y",
            "Cut": "Ctrl+X",
            "Copy": "Ctrl+C",
            "Paste": "Ctrl+V",
            "Delete": "Del",
        }

    def format_text_with_shortcut(self, text):
        action = f"{text:<5}"
        shortcut = f"{self.shortcuts.get(text, ''):>25}"
        return f"{action}{shortcut}"

    def menu(self, options):
        menu_window = ctk.CTkFrame(self.root, fg_color=self.button_bg_color, border_width=12)
        for option, func in options.items():
            if option == "Exit" or option == "Cut" or option == "Delete":
                # Separator line before the buttons
                separator = tk.Canvas(menu_window, height=1, bg="#505050", highlightthickness=0, width=60)
                separator.pack(fill="x")
                separator.create_line(0, 0, self.width, 0, fill="#505050", width=1)
            button_text = self.format_text_with_shortcut(option)
            button = ctk.CTkButton(menu_window, text=button_text, anchor="w", width=self.width,
                                   fg_color=self.button_bg_color, hover_color=self.button_hover_color,
                                   command=func, height=37, corner_radius=5, font=("Segoe UI Semibold", 14),
                                   text_color="#D1D9E0")
            button.pack(fill="x")
        self.menus.append(menu_window)  # Add the menu to the list
        return menu_window

    def create_menus(self):
        # Create menus with options and corresponding functions
        self.root.file_menu = self.menu(
            {"New": partial(new_file, self.text_area, self.root),
             "Open": partial(open_file, self.text_area, self.root),
             "Save": partial(save_file, self.text_area, self.root),
             "Save as": partial(save_as_file, self.text_area, self.root),
             "Exit": exit_app})
        self.root.edit_menu = self.menu(
            {"Undo": undo_action, "Redo": redo_action, "Cut": cut_action, "Copy": copy_action,
             "Paste": paste_action, "Delete": delete_action})

    def create_buttons(self):
        self.root.file_button = ctk.CTkButton(self.menu_frame, text="File", width=self.width,
                                              fg_color=self.button_bg_color, hover_color=self.button_hover_color,
                                              corner_radius=8, font=("Arial", 13, "bold"), text_color="#BDBDBD")
        self.root.edit_button = ctk.CTkButton(self.menu_frame, text="Edit", width=self.width,
                                              fg_color=self.button_bg_color, hover_color=self.button_hover_color,
                                              corner_radius=8, font=("Arial", 13, "bold"), text_color="#BDBDBD")

        self.root.file_button.pack(side="left", padx=1, pady=5)
        self.root.edit_button.pack(side="left", padx=1, pady=5)

    def show_menu(self, menu_bar, button):
        y = self.menu_frame.winfo_height()
        x = button.winfo_x()
        menu_bar.place(x=x, y=y)

    def hide_menus(self, event=None):
        for menu_bar in self.menus:
            menu_bar.place_forget()

    def bind_events(self):
        # Click event to the root window to hide menus
        self.root.bind("<Button-1>", self.hide_menus)

        # Prevent hiding menus when clicking on the menu buttons
        self.root.file_button.bind("<Button-1>", lambda event: self.on_button_click(event, self.root.file_menu,
                                                                                    self.root.file_button))
        self.root.edit_button.bind("<Button-1>", lambda event: self.on_button_click(event, self.root.edit_menu,
                                                                                    self.root.edit_button))

    def on_button_click(self, event, menu_bar, button):
        if menu_bar.winfo_ismapped():
            self.hide_menus()
        else:
            self.hide_menus()
            self.show_menu(menu_bar, button)
        return "break"

# Assuming you have a functions module with the corresponding functions defined
