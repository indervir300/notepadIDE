import customtkinter as ctk
from functions import *

# Create the main window
root = ctk.CTk()
root.title("Custom Dark Menu Example")
root.geometry("400x300")

# Set the appearance mode to dark
ctk.set_appearance_mode("dark")

# Create a frame for the menu bar
menu_frame = ctk.CTkFrame(root)
menu_frame.pack(side="top", fill="x")

width = 130

# Define button colors
button_bg_color = "#2E2E2E"  # Dark grey color
button_hover_color = "#444444"  # Slightly lighter grey for hover effect

# Create a list to track menus
menus = []


# Create the menu function
def menu(options):
    menu_window = ctk.CTkFrame(root, fg_color=button_bg_color)
    for option, func in options.items():
        button = ctk.CTkButton(menu_window, text=option, width=width, fg_color=button_bg_color,
                               hover_color=button_hover_color, command=func)
        button.pack(fill="x")
    menus.append(menu_window)  # Add the menu to the list
    return menu_window


# Create menus with options and corresponding functions
file_menu = menu({"New": new_file, "Open": open_file, "Save": save_file, "Save as": save_as_file, "Exit": exit_app})
edit_menu = menu({"Undo": undo_action, "Redo": redo_action, "Cut": cut_action, "Copy": copy_action,
                  "Paste": paste_action, "Delete": delete_action})
window_menu = menu({"Settings": settings_action, "Change Theme": change_theme_action})
help_menu = menu({"Help": help_action, "About": about_action})

# Create buttons for the menu items with min and max widths
file_button = ctk.CTkButton(menu_frame, text="File", width=width, fg_color=button_bg_color,
                            hover_color=button_hover_color)
file_button.configure(cursor="")
edit_button = ctk.CTkButton(menu_frame, text="Edit", width=width, fg_color=button_bg_color,
                            hover_color=button_hover_color)
edit_button.configure(cursor="")
help_button = ctk.CTkButton(menu_frame, text="Help", width=width, fg_color=button_bg_color,
                            hover_color=button_hover_color)
help_button.configure(cursor="")
window_button = ctk.CTkButton(menu_frame, text="Window", width=width, fg_color=button_bg_color,
                              hover_color=button_hover_color)
window_button.configure(cursor="")

# Pack the buttons into the menu frame
file_button.pack(side="left", padx=1, pady=3)
edit_button.pack(side="left", padx=1, pady=3)
window_button.pack(side="left", padx=1, pady=3)
help_button.pack(side="left", padx=1, pady=3)


# Function to show the selected menu
def show_menu(menu_bar, button):
    y = menu_frame.winfo_height()
    x = button.winfo_x()
    menu_bar.place(x=x, y=y)


# Function to hide all menus
def hide_menus(event=None):
    for menu_bar in menus:
        menu_bar.place_forget()


# Bind the click event to the root window to hide menus
root.bind("<Button-1>", hide_menus)


# Prevent hiding menus when clicking on the menu buttons
def on_button_click(event, menu_bar, button):
    if menu_bar.winfo_ismapped():
        hide_menus()
    else:
        hide_menus()
        show_menu(menu_bar, button)
    return "break"


file_button.bind("<Button-1>", lambda event: on_button_click(event, file_menu, file_button))
edit_button.bind("<Button-1>", lambda event: on_button_click(event, edit_menu, edit_button))
window_button.bind("<Button-1>", lambda event: on_button_click(event, window_menu, window_button))
help_button.bind("<Button-1>", lambda event: on_button_click(event, help_menu, help_button))

root.mainloop()
