import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk

class MyLangTextEditor:
    def __init__(self, master):
        self.master = master
        self.master.title("MyLang Text Editor - Visual Studio Style")
        self.master.geometry("800x600")

        self.create_menu()
        self.create_editor_area()
        self.create_status_bar()

        # Track if file is modified
        self.file_path = None
        self.text_area.bind('<KeyRelease>', self.highlight_syntax)
        self.text_area.bind("<<Modified>>", self.on_modified)

        # Line numbers
        self.text_area.bind("<KeyPress>", self.update_line_numbers)
        self.text_area.bind("<Button-1>", self.update_line_numbers)
        self.text_area.bind("<MouseWheel>", self.update_line_numbers)

        self.create_tags()

    def create_menu(self):
        """Create a menu bar with file options."""
        self.menu_bar = tk.Menu(self.master)
        self.master.config(menu=self.menu_bar)

        # File Menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.master.quit)

    def create_editor_area(self):
        """Create the main text editor with line numbers."""
        self.container = tk.Frame(self.master)
        self.container.pack(fill=tk.BOTH, expand=1)

        # Line numbers
        self.line_numbers = tk.Text(self.container, width=4, padx=3, takefocus=0, bd=0, 
                                    background="lightgray", state='disabled', wrap='none')
        self.line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        # Text area with scrollbar
        self.text_area = scrolledtext.ScrolledText(self.container, wrap=tk.WORD, undo=True)
        self.text_area.pack(expand=1, fill=tk.BOTH, side=tk.RIGHT)

    def create_status_bar(self):
        """Create a status bar for the editor."""
        self.status_bar = ttk.Label(self.master, text="Ln 1, Col 1  |  Unsaved", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def update_line_numbers(self, event=None):
        """Update the line numbers."""
        line_count = self.text_area.index('end').split('.')[0]
        self.line_numbers.config(state=tk.NORMAL)
        self.line_numbers.delete('1.0', tk.END)
        for i in range(1, int(line_count)):
            self.line_numbers.insert(tk.END, f"{i}\n")
        self.line_numbers.config(state=tk.DISABLED)

    def update_status_bar(self):
        """Update the status bar with current line and column."""
        line, col = self.text_area.index(tk.INSERT).split('.')
        self.status_bar.config(text=f"Ln {line}, Col {int(col) + 1}  |  {'Unsaved' if self.text_area.edit_modified() else 'Saved'}")

    def on_modified(self, event=None):
        """Callback for when text is modified."""
        self.text_area.edit_modified(False)
        self.update_status_bar()

    def create_tags(self):
        """Create tags for syntax highlighting."""
        self.text_area.tag_configure("command", foreground="blue")
        self.text_area.tag_configure("variable", foreground="green")
        self.text_area.tag_configure("string", foreground="dark orange")

    def highlight_syntax(self, event=None):
        """Apply syntax highlighting."""
        self.text_area.tag_remove("command", "1.0", "end")
        self.text_area.tag_remove("variable", "1.0", "end")
        self.text_area.tag_remove("string", "1.0", "end")

        lines = self.text_area.get("1.0", "end-1c").splitlines()
        for line_number, line in enumerate(lines):
            words = line.split()
            for word in words:
                if word in ["p", "i", "new", "create_character", "attack", "add_item", "show_inventory", "narrate", "open", "import"]:
                    self.apply_tag("command", line_number, word)
                elif word.startswith("$"):
                    self.apply_tag("variable", line_number, word)
                elif word.startswith("\"") and word.endswith("\""):
                    self.apply_tag("string", line_number, word)

    def apply_tag(self, tag, line_number, word):
        """Helper function to apply a specific tag to a word."""
        start_index = f"{line_number + 1}.{self.text_area.get(f'{line_number + 1}.0', f'{line_number + 1}.end').index(word)}"
        end_index = f"{line_number + 1}.{self.text_area.get(f'{line_number + 1}.0', f'{line_number + 1}.end').index(word) + len(word)}"
        self.text_area.tag_add(tag, start_index, end_index)

    def new_file(self):
        """Clear the text area for a new file."""
        self.text_area.delete(1.0, tk.END)
        self.file_path = None
        self.update_status_bar()

    def open_file(self):
        """Open and display a file in the text editor."""
        file_path = filedialog.askopenfilename(defaultextension=".cla",
                                                filetypes=[("CLA files", "*.cla"), ("All files", "*.*")])
        if file_path:
            try:
                with open(file_path, "r") as file:
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(tk.END, file.read())
                    self.highlight_syntax()  # Ensure syntax is highlighted after opening
                    self.file_path = file_path
                    self.update_status_bar()
            except Exception as e:
                messagebox.showerror("Error", f"Could not open file: {e}")

    def save_file(self):
        """Save the current content of the text area to a file."""
        if not self.file_path:
            self.file_path = filedialog.asksaveasfilename(defaultextension=".cla",
                                                   filetypes=[("CLA files", "*.cla"), ("All files", "*.*")])
        if self.file_path:
            try:
                with open(self.file_path, "w") as file:
                    file.write(self.text_area.get(1.0, tk.END))
                    self.text_area.edit_modified(False)
                    self.update_status_bar()
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    editor = MyLangTextEditor(root)
    root.mainloop()
