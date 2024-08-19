import tkinter as tk
import tkinter.ttk as ttk  # Import ttk for themed widgets
import customtkinter as ctk
from customMenu import CustomMenuBar
import functions as fn
import htmlDetection as colorHtml

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class IdeEnv:
    def __init__(self, root):
        super().__init__()
        self.root = root
        self.root.title("Untitled - IDE")
        self.root.geometry("800x450")

        # Set transparency level (0.0 to 1.0, where 0.0 is fully transparent and 1.0 is fully opaque)
        self.root.attributes('-alpha', 0.98)

        self.button_bg_color = "#202020"
        self.button_hover_color = "#252525"

        self.font_family = "Cascadia Code SemiLight"
        self.font_size = 10
        self.min_font_size = 5  # Minimum font size
        self.max_font_size = 25  # Maximum font size
        self.font = (self.font_family, self.font_size)
        self.numbers_font = (self.font_family, self.font_size)
        self.font_color = "#D1D9E0"

        self.create_widgets()
        fn.bind_shortcuts(self)  # Bind shortcuts here

        self.last_cursor_position = "1.0"

        self.root.file_extension = ""  # Initialize the file extension

    def menu_instance(self):
        self.menu_bar = CustomMenuBar(self.root, self.text_area, self.button_bg_color, self.button_hover_color)
        self.menu_bar.create_menus()
        self.menu_bar.create_buttons()
        self.menu_bar.bind_events()

    def create_widgets(self):
        self.frame = ctk.CTkFrame(self.root)
        self.line_numbers = ctk.CTkCanvas(self.frame, width=55, bg="#191919", highlightthickness=0)
        self.bottom_widgets_frame = ctk.CTkFrame(self.frame, height=25, corner_radius=0, fg_color="#212121")

        self.row_col_label = ctk.CTkLabel(self.bottom_widgets_frame, text="Row: 1, Col: 1", fg_color="#212121")
        self.row_col_label.pack(side=tk.LEFT, padx=10)

        # Add a vertical separator
        self.separator = ttk.Separator(self.bottom_widgets_frame, orient='vertical')
        self.separator.pack(side=tk.LEFT, padx=20, pady=6, fill=tk.Y)

        # Add the character count label
        self.char_count_label = ctk.CTkLabel(self.bottom_widgets_frame, text="Chars: 0", fg_color="#212121")
        self.char_count_label.pack(side=tk.LEFT, padx=10)

        self.separator = ttk.Separator(self.bottom_widgets_frame, orient='vertical')
        self.separator.pack(side=tk.LEFT, padx=20, pady=6, fill=tk.Y)

        self.zoom_label = ctk.CTkLabel(self.bottom_widgets_frame, text="100%", fg_color="#212121")
        self.zoom_label.pack(side=tk.LEFT, padx=10)

        # Add the file extension label
        self.root.file_extension_label = ctk.CTkLabel(self.bottom_widgets_frame, text="", fg_color="#212121")
        self.root.file_extension_label.pack(side=tk.RIGHT, padx=15)

        self.bottom_widgets_frame.pack(side=ctk.BOTTOM, fill=ctk.X, anchor="s")

        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)
        self.text_area = tk.Text(self.frame, undo=True, wrap="none", bg="#191919", fg=self.font_color,
                                 insertbackground="#d1d1d1", font=self.font, highlightthickness=0,
                                 border=0, highlightbackground="#d0d0d0")

        self.menu_instance()
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.scrollbar = ctk.CTkScrollbar(self.frame, command=self.on_scroll, width=14, corner_radius=10)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.text_area.configure(yscrollcommand=self.on_scroll_text_area)

        self.text_area.bind("<KeyRelease>", self.update_line_numbers)
        self.text_area.bind("<MouseWheel>", self.update_line_numbers)
        self.text_area.bind("<ButtonRelease>", self.update_line_numbers)
        self.text_area.bind("<Configure>", self.update_line_numbers)
        self.text_area.bind("<FocusIn>", self.update_line_numbers)
        self.text_area.bind("<Key>", self.update_line_numbers)
        self.text_area.bind("<Motion>", self.update_cursor_position)  # Bind cursor motion
        self.text_area.bind("<Button-1>", self.update_cursor_position)  # Bind left click to update cursor position
        self.text_area.bind("<Tab>", self.on_tab_pressed)  # Bind Tab key press

        # Bind zoom in and zoom out using mouse wheel with Ctrl key
        self.text_area.bind("<Control-MouseWheel>", self.zoom)

    def on_scroll(self, *args):
        self.text_area.yview(*args)
        self.line_numbers.yview(*args)
        self.update_line_numbers()

    def on_scroll_text_area(self, *args):
        self.scrollbar.set(*args)
        self.line_numbers.yview_moveto(args[0])
        self.update_line_numbers()

    def update_line_numbers(self, event=None):
        self.line_numbers.delete("all")
        i = self.text_area.index("@0,0")
        while True:
            dline = self.text_area.dlineinfo(i)
            if dline is None:
                break
            y = dline[1]
            line_num = str(i).split(".")[0]
            self.line_numbers.create_text(17, y, anchor=tk.N, text=line_num, fill="#949494",
                                          font=self.numbers_font)
            i = self.text_area.index(f"{i}+1line")

        # Update row and column label
        cursor_pos = self.text_area.index(tk.INSERT)
        row, col = cursor_pos.split(".")
        self.row_col_label.configure(text=f"Row: {row}, Col: {col}")

        # Update character count label
        num_chars = len(self.text_area.get("1.0", tk.END)) - 1  # Exclude the last newline character
        self.char_count_label.configure(text=f"Chars: {num_chars}")

    def update_cursor_position(self, event):
        # Update row and column label on cursor movement or click
        current_cursor_position = self.text_area.index(tk.INSERT)

        if current_cursor_position != self.last_cursor_position:
            self.last_cursor_position = current_cursor_position

            # Adjust column number for Tab key
            col = self._calculate_column(current_cursor_position)

            self.row_col_label.configure(text=f"Row: {current_cursor_position.split('.')[0]}, Col: {col}")

    def _calculate_column(self, position):
        line_start = self.text_area.index(f"{position} linestart")
        col = int(position.split('.')[1])  # Get column from current position

        line_text = self.text_area.get(line_start, f"{position} lineend")

        # Calculate the column adjusting for tabs
        col_adjusted = 0
        for char in line_text[:col]:
            if char == '\t':
                col_adjusted += 4 - (col_adjusted % 4)  # Adjust for tab spacing
            else:
                col_adjusted += 1

        return col_adjusted

    def on_tab_pressed(self, event):
        self.text_area.insert(tk.INSERT, "    ")  # Insert 4 spaces on Tab press
        return 'break'  # Prevent default behavior

    def zoom(self, event):
        if event.delta > 0:
            self.font_size += 1
        elif event.delta < 0:
            self.font_size -= 1
        # Clamp the font size within the min and max limits
        self.font_size = max(self.min_font_size, min(self.font_size, self.max_font_size))
        # Calculate and display the zoom percentage
        zoom_percentage = int((self.font_size / 10) * 100)
        self.zoom_label.configure(text=f"{zoom_percentage}%")
        self.update_font()
        self.on_scroll("moveto", self.scrollbar.get()[0])  # Ensure scrollbar remains in position

    def update_font(self):
        self.font = (self.font_family, self.font_size)
        self.numbers_font = (self.font_family, self.font_size)
        self.text_area.configure(font=self.font)
        self.update_line_numbers()


if __name__ == "__main__":
    root = ctk.CTk()
    app = IdeEnv(root)
    root.mainloop()
