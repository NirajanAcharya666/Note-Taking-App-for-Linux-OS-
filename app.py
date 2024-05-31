import tkinter as tk
from tkinter import filedialog, messagebox, font, ttk

class NoteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Your Notes")
        self.root.geometry("400x250")
        self.root.resizable(True, True)

        self.text_area = tk.Text(self.root, wrap='word', undo=True, font=("Arial", 12), bg="black", fg="white", insertbackground="white")
        self.text_area.pack(expand=1, fill='both', padx=5, pady=5)

        self.create_menu()
        self.create_status_bar()
    
    def create_menu(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TMenubutton', background='#444', foreground='white')
        style.configure('TMenu', background='#333', foreground='white', activebackground='#666', activeforeground='white')
        
        menubar = tk.Menu(self.root, bg="#333", fg="white", activebackground="#666", activeforeground="white")

        file_menu = tk.Menu(menubar, tearoff=0, bg="#333", fg="white", activebackground="#666", activeforeground="white")
        file_menu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Open", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit, accelerator="Ctrl+Q")

        edit_menu = tk.Menu(menubar, tearoff=0, bg="#333", fg="white", activebackground="#666", activeforeground="white")
        edit_menu.add_command(label="Undo", command=self.text_area.edit_undo, accelerator="Ctrl+Z")
        edit_menu.add_command(label="Redo", command=self.text_area.edit_redo, accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=lambda: self.text_event("cut"), accelerator="Ctrl+X")
        edit_menu.add_command(label="Copy", command=lambda: self.text_event("copy"), accelerator="Ctrl+C")
        edit_menu.add_command(label="Paste", command=lambda: self.text_event("paste"), accelerator="Ctrl+V")
        edit_menu.add_command(label="Select All", command=self.select_all, accelerator="Ctrl+A")

        format_menu = tk.Menu(menubar, tearoff=0, bg="#333", fg="white", activebackground="#666", activeforeground="white")
        format_menu.add_command(label="Font", command=self.choose_font)

        menubar.add_cascade(label="File", menu=file_menu)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        menubar.add_cascade(label="Format", menu=format_menu)

        self.root.config(menu=menubar)

        self.root.bind_all("<Control-n>", lambda event: self.new_file())
        self.root.bind_all("<Control-o>", lambda event: self.open_file())
        self.root.bind_all("<Control-s>", lambda event: self.save_file())
        self.root.bind_all("<Control-q>", lambda event: self.root.quit())
        self.root.bind_all("<Control-x>", lambda event: self.text_event("cut"))
        self.root.bind_all("<Control-c>", lambda event: self.text_event("copy"))
        self.root.bind_all("<Control-v>", lambda event: self.text_event("paste"))
        self.root.bind_all("<Control-z>", lambda event: self.text_area.edit_undo())
        self.root.bind_all("<Control-y>", lambda event: self.text_area.edit_redo())
        self.root.bind_all("<Control-a>", lambda event: self.select_all())

    def create_status_bar(self):
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = tk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor='w', bg="#333", fg="white")
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def new_file(self):
        self.text_area.delete(1.0, tk.END)
        self.status_var.set("New file")

    def open_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, content)
                self.status_var.set(f"Opened file: {file_path}")

    def save_file(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, "w") as file:
                    content = self.text_area.get(1.0, tk.END)
                    file.write(content)
                messagebox.showinfo("Success", "File saved successfully")
                self.status_var.set(f"Saved file: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")
                self.status_var.set("Save failed")

    def text_event(self, action):
        self.text_area.event_generate(f'<<{action.capitalize()}>>')

    def select_all(self):
        self.text_area.tag_add('sel', '1.0', 'end')

    def choose_font(self):
        font_choice = tk.Toplevel(self.root)
        font_choice.title("Choose Font")

        tk.Label(font_choice, text="Font Family").grid(row=0, column=0)
        tk.Label(font_choice, text="Font Size").grid(row=0, column=1)

        font_family = tk.StringVar(value="Arial")
        font_size = tk.IntVar(value=12)

        font_families = list(font.families())
        font_family_dropdown = tk.OptionMenu(font_choice, font_family, *font_families)
        font_family_dropdown.grid(row=1, column=0)

        font_size_spinbox = tk.Spinbox(font_choice, from_=8, to=72, textvariable=font_size)
        font_size_spinbox.grid(row=1, column=1)

        def apply_font():
            selected_font = (font_family.get(), font_size.get())
            self.text_area.config(font=selected_font)
            font_choice.destroy()

        apply_button = tk.Button(font_choice, text="Apply", command=apply_font)
        apply_button.grid(row=2, column=0, columnspan=2)

if __name__ == "__main__":
    root = tk.Tk()
    app = NoteApp(root)
    root.mainloop()
