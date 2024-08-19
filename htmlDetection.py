import re
import os
import tkinter as tk


class HTMLColorizer:
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.file_path = None
        self.file_extension = None

        # Define tag patterns
        self.tag_pattern = re.compile(r'<\s*([^\s/<>]+)\s*([^<>]*)>|<\/\s*([^\s/<>]+)\s*>|<!--.*?-->')
        self.attr_pattern = re.compile(r'(\w+)\s*=\s*["\']([^"\']*)["\']')

        # Configure tag colors
        self.text_widget.tag_config('red_tag', foreground='#BA484C')
        self.text_widget.tag_config('blue_tag', foreground='#259F9B')
        self.text_widget.tag_config('grey_tag', foreground='grey')

    def load_file(self, file_path):
        self.file_path = file_path
        self.file_extension = os.path.splitext(file_path)[1]

        if self.file_extension in ['.html', '.htm']:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                file_content = f.read()
            self.text_widget.delete('1.0', tk.END)
            self.text_widget.insert(tk.END, file_content)
            self.colorize_html()

            # Bind text widget to detect changes
            self.text_widget.bind("<KeyRelease>", self.on_text_change)
        else:
            self.text_widget.delete('1.0', tk.END)

    def colorize_html(self):
        # Remove previous tags, attributes, and comments
        self.text_widget.tag_remove('red_tag', '1.0', tk.END)
        self.text_widget.tag_remove('blue_tag', '1.0', tk.END)
        self.text_widget.tag_remove('grey_tag', '1.0', tk.END)

        # Get the current text
        text = self.text_widget.get("1.0", tk.END)

        # Apply colorization to tags (including closing tags)
        for match in self.tag_pattern.finditer(text):
            # Opening tag
            if match.group(1):
                start, end = match.span(1)
                start_index = f"1.0 + {start} chars"
                end_index = f"1.0 + {end} chars"
                self.text_widget.tag_add('red_tag', start_index, end_index)
                self.text_widget.tag_configure('red_tag', font=('Arial', 10, 'bold'))  # Bold font
            # Closing tag
            elif match.group(3):
                start, end = match.span(3)
                start_index = f"1.0 + {start} chars"
                end_index = f"1.0 + {end} chars"
                self.text_widget.tag_add('red_tag', start_index, end_index)
                self.text_widget.tag_configure('red_tag', font=('Arial', 12, 'bold'))  # Bold font

        # Apply colorization to attributes
        for match in self.attr_pattern.finditer(text):
            attr_name = match.group(1)
            start, end = match.span(2)  # Group 2 captures the attribute value
            start_index = f"1.0 + {start} chars"
            end_index = f"1.0 + {end} chars"
            self.text_widget.tag_add('blue_tag', start_index, end_index)

        # Apply colorization to comments
        comment_pattern = re.compile(r'<!--.*?-->', re.DOTALL)
        for match in comment_pattern.finditer(text):
            start, end = match.span()
            start_index = f"1.0 + {start} chars"
            end_index = f"1.0 + {end} chars"
            self.text_widget.tag_add('grey_tag', start_index, end_index)

    def on_text_change(self, event):
        # # Apply colorization if file extension is .html or .htm
        if self.file_extension in ['.html', '.htm']:
            self.colorize_html()


# Create the main window
# root = tk.Tk()
# root.title("HTML Tag and Attribute Colorizer")
# root.configure(background='black')  # Set root background color
#
# # Create a text widget
# text_widget = tk.Text(root, wrap='word', font=('Arial', 12))
# text_widget.pack(expand=True, fill='both')
#
# # Initialize the HTMLColorizer instance
# html_colorizer = HTMLColorizer(text_widget)
#
# # Load an initial HTML file
# html_colorizer.load_file(r"D:\Auth Project\public\otp.html")  # Replace with your initial file path
#
# # Start the Tkinter event loop
# root.mainloop()
