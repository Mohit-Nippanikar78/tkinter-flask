# Experiment 17 — Flask Framework
**Course:** Programming Laboratory (DJS23ILPC403) | S.Y. B.Tech | D.J. Sanghvi College of Engineering

---

## 📌 Aim / Objective

Write a Python program to implement a **Web Based Application** using the Flask Framework.

---

## 🧠 What is Flask?

Flask is a **lightweight Python web framework** that provides tools and libraries for building web applications quickly and easily.

> Flask follows the **WSGI (Web Server Gateway Interface)** standard and is built on top of the **Werkzeug** toolkit and **Jinja2** templating engine.

**Key Features:**
- Minimal and lightweight — no boilerplate
- Built-in development server and debugger
- Uses **Jinja2** for HTML templates
- Easily extensible with plugins/extensions

---

## ⚙️ Setup

### Step 1 — Install Flask

```bash
pip install Flask
```

### Step 2 — Project Structure (Todo App Example)

```
my_flask_app/
│
├── app.py              ← Main application file
└── templates/
    ├── index.html      ← Home page template
    ├── about.html      ← About page template
    └── task.html       ← Task edit template
```

---

## 🚀 Step-by-Step: Building a Flask App

### Step 3 — Create the Flask Application (`app.py`)

#### Hello World (Minimal App)

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(debug=True)
```

**How it works:**
| Line | Purpose |
|------|---------|
| `Flask(__name__)` | Creates an instance of the Flask app |
| `@app.route('/')` | Defines a URL route (the home page `/`) |
| `def hello()` | View function — runs when route is visited |
| `app.run(debug=True)` | Starts the development server with auto-reload |

---

### Step 4 — Running the Application

```bash
python app.py
```

Open your browser and navigate to:
```
http://localhost:5000
```

---

### Step 5 — Building Routes and Views

Routes define the **URL endpoints** of your application. Use `render_template()` to serve HTML files.

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')
```

| Route | Function | Template rendered |
|-------|----------|-------------------|
| `/` | `index()` | `templates/index.html` |
| `/about` | `about()` | `templates/about.html` |

---

### Step 6 — Create HTML Templates

Flask uses **Jinja2** templating. Templates live in a folder called `templates/`.

#### `templates/index.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Home</title>
</head>
<body>
    <h1>Welcome to our website!</h1>
</body>
</html>
```

#### `templates/about.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>About</title>
</head>
<body>
    <h1>About Us</h1>
    <p>This is a brief description of our company.</p>
</body>
</html>
```

---

## 🗂️ Full Example: Todo List Application

This app demonstrates **routing, form handling, and template rendering** — the core pillars of Flask.

### `app.py` — Todo Application Backend

```python
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# In-memory task storage (no database)
tasks = []

@app.route('/')
def index():
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task_content = request.form['content']  # Get data from HTML form
    tasks.append(task_content)
    return redirect(url_for('index'))       # Redirect back to home

@app.route('/delete/<int:index>')
def delete_task(index):
    del tasks[index]                        # Remove task by its index
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
```

**Route Summary:**

| Route | Method | Purpose |
|-------|--------|---------|
| `/` | GET | Display all tasks |
| `/add` | POST | Add a new task from form |
| `/delete/<index>` | GET | Delete task at given index |

---

### `templates/index.html` — Display & Add Tasks

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Todo List</title>
</head>
<body>
    <h1>Todo List</h1>

    <!-- List all tasks -->
    <ul>
        {% for task in tasks %}
            <li>
                {{ task }}
                <a href="/delete/{{ loop.index0 }}">Delete</a>
            </li>
        {% endfor %}
    </ul>

    <!-- Form to add a new task -->
    <form action="/add" method="post">
        <input type="text" name="content" placeholder="Enter task">
        <button type="submit">Add Task</button>
    </form>
</body>
</html>
```

**Jinja2 Template Syntax used:**

| Syntax | Purpose |
|--------|---------|
| `{% for task in tasks %}` | Loop over tasks list |
| `{{ task }}` | Output the value of `task` |
| `{{ loop.index0 }}` | Zero-based loop counter |
| `{% endfor %}` | End the for loop |

---

### `templates/task.html` — Edit a Task

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Edit Task</title>
</head>
<body>
    <h1>Edit Task</h1>
    <form action="{{ url_for('update_task', index=index) }}" method="post">
        <input type="text" name="content" value="{{ task }}">
        <button type="submit">Update Task</button>
    </form>
</body>
</html>
```

---

## 🔑 Key Flask Concepts — Quick Reference

### 1. Request Object (`request`)
Used to access incoming data from forms or URLs.

```python
from flask import request

# Get data from a POST form
data = request.form['field_name']

# Get data from a URL query string (?key=value)
value = request.args.get('key')
```

### 2. `redirect()` and `url_for()`
Used to redirect the user to another page.

```python
from flask import redirect, url_for

return redirect(url_for('index'))  # Redirect to the index() view function
```

### 3. Dynamic Routes
URL segments can be passed as function arguments.

```python
@app.route('/user/<username>')
def show_user(username):
    return f'Hello, {username}!'

@app.route('/item/<int:item_id>')
def show_item(item_id):
    return f'Item ID: {item_id}'
```

### 4. HTTP Methods
By default, routes only accept `GET`. Use `methods` to allow `POST`.

```python
@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        # Handle form submission
        pass
    return render_template('form.html')
```

---

## 📋 Jinja2 Templating — Quick Reference

| Syntax | Purpose |
|--------|---------|
| `{{ variable }}` | Output a variable's value |
| `{% if condition %}` | Conditional block |
| `{% for item in list %}` | Loop block |
| `{% extends "base.html" %}` | Template inheritance |
| `{% block content %}` | Define a block for child templates |
| `{{ url_for('view_name') }}` | Generate a URL for a view |

---

## ❓ Lab Questions

1. **How do you handle form submissions in Flask?**
   > Using `request.form['field_name']` inside a route that accepts `methods=['POST']`. The HTML form's `method` attribute must be set to `POST` and the `action` to the correct route.

2. **How does Flask handle requests and responses?**
   > Flask receives an HTTP request, matches it to a registered route using the `@app.route()` decorator, calls the associated view function, and returns the result as an HTTP response. The `request` object gives access to incoming data, and you return strings, HTML, or use `render_template()` to build the response.

---

## 📚 References

- [https://www.w3schools.com/python](https://www.w3schools.com/python)
- [Flask Official Documentation](https://flask.palletsprojects.com/)
- [Jinja2 Documentation](https://jinja.palletsprojects.com/)
