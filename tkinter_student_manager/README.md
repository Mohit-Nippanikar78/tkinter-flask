# Experiment 16 — GUI Design with Tkinter 
**Course:** Programming Laboratory (DJS23ILPC403) | S.Y. B.Tech | D.J. Sanghvi College of Engineering

---

## 📌 Aim / Objective

Write Python programs to understand **GUI designing and database operations** — specifically:
- GUI design using **Tkinter**
- MySQL database creation & connectivity with **DML operations**

---

## 🧠 What is Tkinter?

**Tkinter** is Python's standard GUI (Graphical User Interface) library. It is an interface to the **Tk GUI toolkit** and is the most commonly used method for building desktop GUI applications in Python.

> Tkinter is **pre-installed** with Python — no extra installation needed!

**Note:** The module is called `Tkinter` in Python 2.x and `tkinter` (lowercase) in Python 3.x.

---

## ⚙️ Setting Up a Tkinter App

### The 4-Step Recipe

```
1. Import the tkinter module
2. Create the main window (root/container)
3. Add widgets to the window
4. Apply event triggers on widgets
5. Start the main event loop
```

### Minimal Tkinter Application

```python
import tkinter

# Step 1: Create the main window
m = tkinter.Tk()

# Step 2: (Add widgets here)

# Step 3: Start the event loop
m.mainloop()
```

### Two Essential Methods

| Method | Purpose |
|--------|---------|
| `Tk()` | Creates the main application window |
| `mainloop()` | Starts the infinite event loop — listens for events until window is closed |

---

## 📐 Geometry Managers

Geometry managers control **how widgets are positioned** inside the window. There are three:

| Manager | Syntax | Description |
|---------|--------|-------------|
| `pack()` | `widget.pack()` | Organizes widgets in blocks (top-to-bottom or left-to-right) |
| `grid()` | `widget.grid(row=r, column=c)` | Organizes widgets in a table/grid structure |
| `place()` | `widget.place(x=X, y=Y)` | Places widgets at exact pixel coordinates |

```python
# pack() example
label = Label(root, text="Hello")
label.pack()

# grid() example
label.grid(row=0, column=0)

# place() example
label.place(x=50, y=100)
```

---

## 🧩 Tkinter Widgets — Complete Reference

All widgets follow this general syntax:
```python
widget = WidgetClass(master, option=value, ...)
widget.pack()  # or .grid() or .place()
```

`master` — the parent window or frame this widget belongs to.

---

### 1. Button

Adds a clickable button to trigger a function.

```python
import tkinter as tk

root = tk.Tk()

def on_click():
    print("Button clicked!")

btn = tk.Button(root,
                text="Click Me",
                bg="blue",
                fg="white",
                command=on_click)
btn.pack()
root.mainloop()
```

**Key Options:**

| Option | Description |
|--------|-------------|
| `text` | Label shown on the button |
| `command` | Function to call when clicked |
| `bg` | Normal background color |
| `fg` | Text (foreground) color |
| `activebackground` | Background when mouse hovers |
| `activeforeground` | Foreground when mouse hovers |
| `font` | Font of the button label |
| `image` | Set an image on the button |
| `width` | Width of the button |
| `height` | Height of the button |

---

### 2. Canvas

Used to draw graphics, shapes, lines, and embed other widgets.

```python
canvas = tk.Canvas(root, width=300, height=200, bg="white")
canvas.pack()

# Draw a rectangle
canvas.create_rectangle(50, 50, 200, 150, fill="lightblue")

# Draw a line
canvas.create_line(0, 0, 300, 200, fill="red", width=2)

# Draw text
canvas.create_text(150, 100, text="Hello Canvas!")
```

**Key Options:**

| Option | Description |
|--------|-------------|
| `width` | Width of the canvas |
| `height` | Height of the canvas |
| `bg` | Background color |
| `bd` | Border width in pixels |
| `cursor` | Cursor style when hovering |
| `highlightcolor` | Color of the focus highlight |

---

### 3. Checkbutton

Displays a checkbox — allows the user to select/deselect options.

```python
var1 = tk.IntVar()  # Holds 1 (checked) or 0 (unchecked)
var2 = tk.IntVar()

chk1 = tk.Checkbutton(root, text="Option A", variable=var1)
chk2 = tk.Checkbutton(root, text="Option B", variable=var2)
chk1.pack()
chk2.pack()
```

**Key Options:**

| Option | Description |
|--------|-------------|
| `text` | Label next to the checkbox |
| `variable` | Tkinter variable (`IntVar`) to track state |
| `command` | Function to call when toggled |
| `bg` | Background color |
| `font` | Font of the label |
| `activebackground` | Background when under cursor |

---

### 4. Entry

Single-line text input field.

```python
entry = tk.Entry(root, width=30)
entry.pack()

# Get text entered by user
user_input = entry.get()
```

**Key Options:**

| Option | Description |
|--------|-------------|
| `width` | Width of the entry box |
| `bg` | Background color |
| `bd` | Border width in pixels |
| `show` | Replace input display (e.g., `show="*"` for passwords) |
| `cursor` | Cursor style |
| `highlightcolor` | Focus highlight color |

---

### 5. Frame

An invisible **container** used to group and organize other widgets.

```python
frame = tk.Frame(root, bg="lightgrey", width=300, height=100, bd=2)
frame.pack()

# Place widgets inside the frame
label = tk.Label(frame, text="Inside Frame")
label.pack()
```

**Key Options:**

| Option | Description |
|--------|-------------|
| `bg` | Background color |
| `bd` | Border width |
| `width` | Width of the frame |
| `height` | Height of the frame |
| `cursor` | Cursor style |
| `highlightcolor` | Focus highlight color |

---

### 6. Label

Displays text or an image. Can be updated dynamically.

```python
lbl = tk.Label(root, text="Hello, Tkinter!", font=("Arial", 16), fg="darkblue")
lbl.pack()

# Update label text later
lbl.config(text="Updated Text!")
```

**Key Options:**

| Option | Description |
|--------|-------------|
| `text` | Text to display |
| `bg` | Background color |
| `fg` | Foreground (text) color |
| `font` | Font name and size |
| `image` | Image to display |
| `width` | Width in characters |
| `height` | Height in lines |

---

### 7. Listbox

Displays a list of items; user can select one or more.

```python
listbox = tk.Listbox(root, height=5)
items = ["Apple", "Banana", "Cherry", "Date"]

for item in items:
    listbox.insert(tk.END, item)

listbox.pack()

# Get selected item
selection = listbox.get(listbox.curselection())
```

**Key Options:**

| Option | Description |
|--------|-------------|
| `height` | Number of visible rows |
| `width` | Width in characters |
| `bg` | Background color |
| `font` | Font of the list items |
| `bd` | Border width |
| `highlightcolor` | Focus highlight color |

---

### 8. Menubutton

A button that opens a dropdown menu when clicked.

```python
mbtn = tk.Menubutton(root, text="Options", relief=tk.RAISED)
mbtn.pack()

menu = tk.Menu(mbtn, tearoff=0)
menu.add_command(label="Item 1")
menu.add_command(label="Item 2")

mbtn["menu"] = menu
```

**Key Options:**

| Option | Description |
|--------|-------------|
| `text` | Button label |
| `bg` | Background color |
| `activebackground` | Background on hover |
| `image` | Image on widget |
| `width` | Width of the widget |
| `highlightcolor` | Focus highlight color |

---

### 9. Menu

Creates a menu bar or context menu.

```python
menubar = tk.Menu(root)

file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label="Open")
file_menu.add_command(label="Save")
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

menubar.add_cascade(label="File", menu=file_menu)
root.config(menu=menubar)
```

**Key Options:**

| Option | Description |
|--------|-------------|
| `bg` | Background color |
| `activebackground` | Background on hover |
| `font` | Font of menu items |
| `cursor` | Cursor on hover |

---

### 10. Message

Multi-line, non-editable text display. Similar to Label but wraps text automatically.

```python
msg = tk.Message(root, text="This is a longer message that will automatically wrap.", width=200)
msg.pack()
```

**Key Options:**

| Option | Description |
|--------|-------------|
| `text` | Text to display |
| `width` | Width triggers word wrapping |
| `bg` | Background color |
| `font` | Font |
| `bd` | Border around the indicator |

---

### 11. Radiobutton

Allows a user to select **one option** from a set of choices.

```python
choice = tk.StringVar()  # Tracks selected option

r1 = tk.Radiobutton(root, text="Option A", variable=choice, value="A")
r2 = tk.Radiobutton(root, text="Option B", variable=choice, value="B")
r3 = tk.Radiobutton(root, text="Option C", variable=choice, value="C")

r1.pack()
r2.pack()
r3.pack()
```

**Key Options:**

| Option | Description |
|--------|-------------|
| `text` | Label for the option |
| `variable` | Shared `StringVar` or `IntVar` |
| `value` | Value assigned when selected |
| `command` | Function called on selection |
| `bg` | Background color |

---

### 12. Scale

A graphical slider for selecting a numeric value from a range.

```python
scale = tk.Scale(root,
                 from_=0,
                 to=100,
                 orient=tk.HORIZONTAL,
                 label="Volume")
scale.pack()

# Get current value
val = scale.get()
```

**Key Options:**

| Option | Description |
|--------|-------------|
| `from_` | Start value of the range |
| `to` | End value of the range |
| `orient` | `HORIZONTAL` or `VERTICAL` |
| `bg` | Background color |
| `activebackground` | Background on hover |
| `cursor` | Cursor on hover |
| `width` | Width of the widget |

---

### 13. Scrollbar

Adds a scroll controller for widgets like `Listbox`, `Text`, or `Canvas`.

```python
scrollbar = tk.Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox = tk.Listbox(root, yscrollcommand=scrollbar.set)
for i in range(50):
    listbox.insert(tk.END, f"Item {i}")
listbox.pack(side=tk.LEFT, fill=tk.BOTH)

scrollbar.config(command=listbox.yview)
```

**Key Options:**

| Option | Description |
|--------|-------------|
| `width` | Width of the scrollbar |
| `bg` | Background color |
| `activebackground` | Background on hover |
| `bd` | Border size |
| `cursor` | Cursor on hover |

---

### 14. Text

Multi-line text editor widget.

```python
text_area = tk.Text(root, height=10, width=40, font=("Courier", 12))
text_area.pack()

# Insert default text
text_area.insert(tk.END, "Start typing here...\n")

# Get all text
content = text_area.get("1.0", tk.END)
```

**Key Options:**

| Option | Description |
|--------|-------------|
| `height` | Height in lines |
| `width` | Width in characters |
| `bg` | Background color |
| `font` | Font of the text |
| `highlightcolor` | Focus highlight color |
| `insertbackground` | Color of the text cursor |

---

### 15. Toplevel

Creates a **secondary window** managed independently by the window manager.

```python
def open_new_window():
    new_win = tk.Toplevel(root)
    new_win.title("New Window")
    new_win.geometry("200x150")
    tk.Label(new_win, text="This is a new window").pack()

btn = tk.Button(root, text="Open Window", command=open_new_window)
btn.pack()
```

**Key Options:**

| Option | Description |
|--------|-------------|
| `bg` | Background color |
| `bd` | Border size |
| `width` | Width of the window |
| `height` | Height of the window |
| `cursor` | Cursor style |

---

### 16. Spinbox

An `Entry`-like widget where value is selected from a fixed range by clicking up/down arrows.

```python
spinbox = tk.Spinbox(root, from_=1, to=10, width=5)
spinbox.pack()

# Get current value
val = spinbox.get()
```

**Key Options:**

| Option | Description |
|--------|-------------|
| `from_` | Start of the numeric range |
| `to` | End of the numeric range |
| `bg` | Background color |
| `activebackground` | Background on hover |
| `disabledbackground` | Background when disabled |
| `command` | Function called on value change |
| `width` | Width of the widget |

---

### 17. PanedWindow

A container that holds multiple **resizable panes** side-by-side or top-to-bottom.

```python
paned = tk.PanedWindow(root, orient=tk.HORIZONTAL)
paned.pack(fill=tk.BOTH, expand=True)

left_frame = tk.Frame(paned, bg="lightblue", width=150)
right_frame = tk.Frame(paned, bg="lightyellow", width=150)

paned.add(left_frame)
paned.add(right_frame)
```

**Key Options:**

| Option | Description |
|--------|-------------|
| `bg` | Background color |
| `bd` | Border width |
| `cursor` | Cursor style |
| `width` | Width of the widget |
| `height` | Height of the widget |

---

## 🗃️ Complete Example: DBMS Login Page (Tkinter + MySQL)

This is the **main application** from the experiment — a login form that connects to a MySQL database.

### Prerequisites

```bash
pip install mysql-connector-python
```

Ensure you have:
- MySQL running on `localhost`
- A database called `College`
- A table called `STUDENT`

### Full Code

```python
import tkinter as tk
from tkinter import *

import mysql.connector

def submitact():
    user = Username.get()
    passw = password.get()
    print(f"The name entered by you is {user} {passw}")
    logintodb(user, passw)

def logintodb(user, passw):
    try:
        # Connect to MySQL — with or without password
        if passw:
            db = mysql.connector.connect(
                host="localhost",
                user=user,
                password=passw,
                db="College"
            )
        else:
            db = mysql.connector.connect(
                host="localhost",
                user=user,
                db="College"
            )

        cursor = db.cursor()

        # Execute a SELECT query
        savequery = "SELECT * FROM STUDENT"
        cursor.execute(savequery)
        myresult = cursor.fetchall()

        # Print results
        for x in myresult:
            print(x)
        print("Query Executed successfully")

    except Exception as e:
        db.rollback()
        print(f"Error occurred: {e}")


# ---- GUI Setup ----
root = tk.Tk()
root.geometry("300x300")
root.title("DBMS Login Page")

# Username row
lblfrstrow = tk.Label(root, text="Username -")
lblfrstrow.place(x=50, y=20)

Username = tk.Entry(root, width=35)
Username.place(x=150, y=20, width=100)

# Password row
lblsecrow = tk.Label(root, text="Password -")
lblsecrow.place(x=50, y=50)

password = tk.Entry(root, width=35, show="*")  # show="*" masks password
password.place(x=150, y=50, width=100)

# Login button
submitbtn = tk.Button(root, text="Login", bg='blue', fg='white', command=submitact)
submitbtn.place(x=150, y=135, width=55)

# Start the app
root.mainloop()
```

### Code Walkthrough

| Part | Description |
|------|-------------|
| `submitact()` | Called when Login button is clicked; reads Entry fields |
| `Username.get()` | Retrieves text from the Username Entry widget |
| `password.get()` | Retrieves text from Password Entry widget |
| `mysql.connector.connect(...)` | Connects to MySQL with provided credentials |
| `cursor.execute(query)` | Runs the SQL query |
| `cursor.fetchall()` | Returns all rows from the result |
| `db.rollback()` | Rolls back any uncommitted transactions on error |

---

## 📦 Tkinter Variables (Control Variables)

Tkinter provides special variable types that link widgets to Python values:

| Class | Holds |
|-------|-------|
| `StringVar()` | String values |
| `IntVar()` | Integer values |
| `DoubleVar()` | Float values |
| `BooleanVar()` | Boolean values |

```python
# Example: StringVar with Entry and Label
name = tk.StringVar()
entry = tk.Entry(root, textvariable=name)
label = tk.Label(root, textvariable=name)  # Updates automatically!
```

---

## 🎨 Widget Styling Tips

```python
# Set a custom font
from tkinter import font
my_font = ("Arial", 14, "bold")
tk.Label(root, text="Styled Label", font=my_font)

# Set window geometry and title
root.geometry("400x300")  # width x height
root.title("My App")

# Prevent resizing
root.resizable(False, False)
```

---

## ❓ Lab Questions

1. **Write Python programs to understand GUI designing using Tkinter.**
   > Use `tkinter.Tk()` to create a window, add widgets like `Label`, `Entry`, `Button`, and call `mainloop()`.

2. **How do you connect Tkinter to a MySQL database?**
   > Install `mysql-connector-python`, use `mysql.connector.connect()` with `host`, `user`, `password`, and `db` parameters. Use `cursor.execute()` to run SQL and `cursor.fetchall()` to get results.

---

## 📚 References

- [https://www.w3schools.com/python](https://www.w3schools.com/python)
- [Tkinter Official Documentation](https://docs.python.org/3/library/tkinter.html)
- [MySQL Connector Python Docs](https://dev.mysql.com/doc/connector-python/en/)
