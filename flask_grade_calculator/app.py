from flask import Flask, render_template, request

app = Flask(__name__)

SUBJECTS = ["Maths", "Physics", "Chemistry", "Python", "English"]

def calculate_grade(percentage):
    if percentage >= 90:
        return "O", "Outstanding", "#2ecc71"
    elif percentage >= 80:
        return "A+", "Excellent", "#27ae60"
    elif percentage >= 70:
        return "A", "Very Good", "#3498db"
    elif percentage >= 60:
        return "B", "Good", "#f39c12"
    elif percentage >= 50:
        return "C", "Average", "#e67e22"
    else:
        return "F", "Fail", "#e74c3c"

@app.route('/')
def index():
    return render_template('index.html', subjects=SUBJECTS)

@app.route('/result', methods=['POST'])
def result():
    marks = []
    errors = []

    for subject in SUBJECTS:
        try:
            mark = int(request.form[subject])
            if mark < 0 or mark > 100:
                errors.append(f"{subject}: Marks must be between 0 and 100.")
            else:
                marks.append((subject, mark))
        except ValueError:
            errors.append(f"{subject}: Please enter a valid number.")

    if errors:
        return render_template('index.html', subjects=SUBJECTS, errors=errors)

    total = sum(m for _, m in marks)
    max_total = len(SUBJECTS) * 100
    percentage = round((total / max_total) * 100, 2)
    grade, grade_label, grade_color = calculate_grade(percentage)

    return render_template(
        'result.html',
        marks=marks,
        total=total,
        max_total=max_total,
        percentage=percentage,
        grade=grade,
        grade_label=grade_label,
        grade_color=grade_color,
        subjects=SUBJECTS
    )

if __name__ == '__main__':
    app.run(debug=True)
