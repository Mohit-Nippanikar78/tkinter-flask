import tkinter as tk
from tkinter import ttk, messagebox

students_db = []

def add_student():
    name    = entry_name.get().strip()
    roll_no = entry_roll.get().strip()
    branch  = entry_branch.get().strip()

    if not name or not roll_no or not branch:
        messagebox.showwarning("Missing Fields", "Please fill in all fields.")
        return

    student = {"name": name, "roll_no": roll_no, "branch": branch}
    students_db.append(student)
    messagebox.showinfo("Success", f"Student '{name}' added successfully!")
    clear_fields()
    load_students()

def load_students():
    for item in tree.get_children():
        tree.delete(item)
    for doc in students_db:
        tree.insert("", tk.END, values=(doc['roll_no'], doc['name'], doc['branch']))

def delete_student():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("No Selection", "Please select a student to delete.")
        return

    item = tree.item(selected[0])
    roll_no = str(item['values'][0])

    confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete student with Roll No: {roll_no}?")
    if confirm:
        global students_db
        students_db = [student for student in students_db if str(student["roll_no"]) != roll_no]
        messagebox.showinfo("Deleted", f"Student with Roll No {roll_no} deleted.")
        load_students()

def clear_fields():
    entry_name.delete(0, tk.END)
    entry_roll.delete(0, tk.END)
    entry_branch.delete(0, tk.END)
    entry_name.focus()

root = tk.Tk()
root.title("Student Record Manager")
root.geometry("650x550")
root.minsize(650, 550)

# Apply a custom light-mode theme using standard tkinter styling principles
# to avoid Apple's macOS system colors which are making backgrounds and inputs transparent grey.

# Create Custom Styles
style = ttk.Style(root)
style.theme_use('default')

# Main colors
BG_COLOR = "#FFFFFF"         # Pure white background
FRAME_BG = "#F8F9FA"         # Light grey for frames
TEXT_COLOR = "#2C3E50"       # Dark grey/black for text
ACCENT = "#3498DB"           # Blue accent

root.configure(bg=BG_COLOR)

# Configure ttk styles
style.configure("TFrame", background=BG_COLOR)
style.configure("Card.TFrame", background=FRAME_BG, relief="solid", borderwidth=1)
style.configure("Header.TLabel", background=BG_COLOR, foreground=TEXT_COLOR, font=("Helvetica", 24, "bold"))
style.configure("Field.TLabel", background=FRAME_BG, foreground=TEXT_COLOR, font=("Helvetica", 12))
style.configure("TButton", background=ACCENT, foreground="white", font=("Helvetica", 12, "bold"), padding=6)
style.map("TButton", background=[("active", "#2980B9")])

# ── Main Container ──
main_frame = ttk.Frame(root, padding=20)
main_frame.pack(fill=tk.BOTH, expand=True)

# ── Title Label ──
title_label = ttk.Label(main_frame, text="🎓 Student Record Manager", style="Header.TLabel")
title_label.pack(pady=(10, 20))

# ── Form Frame ──
form_frame = ttk.Frame(main_frame, style="Card.TFrame", padding=20)
form_frame.pack(fill=tk.X, pady=(0, 15))

# We use standard tk.Entry but explicitly set borderwidth and white background
# so macOS doesn't render it as a transparent, invisible gray box.
ENTRY_KWARGS = {"font": ("Helvetica", 14), "bg": "white", "fg": "black", "bd": 1, "relief": "solid", "insertbackground": "black", "highlightthickness": 1, "highlightbackground": "#CCCCCC"}

ttk.Label(form_frame, text="Name:", style="Field.TLabel").grid(row=0, column=0, sticky="e", padx=(0, 10), pady=10)
entry_name = tk.Entry(form_frame, width=35, **ENTRY_KWARGS)
entry_name.grid(row=0, column=1, sticky="w", pady=10)

ttk.Label(form_frame, text="Roll No:", style="Field.TLabel").grid(row=1, column=0, sticky="e", padx=(0, 10), pady=10)
entry_roll = tk.Entry(form_frame, width=35, **ENTRY_KWARGS)
entry_roll.grid(row=1, column=1, sticky="w", pady=10)

ttk.Label(form_frame, text="Branch:", style="Field.TLabel").grid(row=2, column=0, sticky="e", padx=(0, 10), pady=10)
entry_branch = tk.Entry(form_frame, width=35, **ENTRY_KWARGS)
entry_branch.grid(row=2, column=1, sticky="w", pady=10)

form_frame.columnconfigure(1, weight=1)

# ── Button Bar ──
btn_frame = ttk.Frame(main_frame)
btn_frame.pack(fill=tk.X, pady=(0, 20))

add_btn = tk.Button(btn_frame, text="Add Student", command=add_student, bg="#2ECC71", fg="black", font=("Helvetica", 14), padx=10, pady=5)
add_btn.pack(side=tk.LEFT, padx=(0, 10))

del_btn = tk.Button(btn_frame, text="Delete Selected", command=delete_student, bg="#E74C3C", fg="black", font=("Helvetica", 14), padx=10, pady=5)
del_btn.pack(side=tk.LEFT, padx=(0, 10))

clr_btn = tk.Button(btn_frame, text="Clear Fields", command=clear_fields, bg="#95A5A6", fg="black", font=("Helvetica", 14), padx=10, pady=5)
clr_btn.pack(side=tk.LEFT)

# ── Treeview (Listbox) Frame ──
list_frame = ttk.Frame(main_frame)
list_frame.pack(fill=tk.BOTH, expand=True)

# Custom Style for Treeview
style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"), background="#E0E0E0")
style.configure("Treeview", font=("Helvetica", 12), rowheight=30, background="white", fieldbackground="white", foreground="black")
style.map("Treeview", background=[("selected", ACCENT)], foreground=[("selected", "white")])

columns = ("roll_no", "name", "branch")
tree = ttk.Treeview(list_frame, columns=columns, show="headings", style="Treeview")

tree.heading("roll_no", text="Roll No")
tree.heading("name", text="Name")
tree.heading("branch", text="Branch")

tree.column("roll_no", width=120, anchor="center")
tree.column("name", width=300, anchor="w")
tree.column("branch", width=150, anchor="w")

scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)

tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

load_students()
entry_name.focus()
root.update_idletasks()
root.mainloop()
