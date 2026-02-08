from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "fallback-secret")

# ---------------- DATABASE ----------------

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        role TEXT
    )
    """)

    # Students table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        roll TEXT,
        course TEXT,
        email TEXT UNIQUE
    )
    """)

    # Skills table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS skills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_email TEXT,
        skill_name TEXT,
        skill_level TEXT
    )
    """)

    # Projects table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_email TEXT,
        project_name TEXT,
        description TEXT
    )
    """)

    # Default admin
    cursor.execute("""
    INSERT OR IGNORE INTO users (username, password, role)
    VALUES ('admin', 'admin', 'admin')
    """)

    conn.commit()
    conn.close()

# ✅ VERY IMPORTANT
init_db()

# ---------------- LOGIN ----------------

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]

        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE username=? AND password=? AND role=?",
            (username, password, role)
        ).fetchone()
        conn.close()

        if user:
            session["user"] = username
            session["role"] = role

            if role == "admin":
                return redirect("/admin")
            else:
                return redirect("/student")

    return render_template("login.html")

# ---------------- ADMIN DASHBOARD ----------------

@app.route("/admin")
def admin_dashboard():
    if "user" not in session or session.get("role") != "admin":
        return redirect("/")

    conn = get_db()
    students_count = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]
    users_count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    conn.close()

    return render_template(
        "admin_dashboard.html",
        students_count=students_count,
        users_count=users_count,
        teachers_count=5,
        departments_count=4,
        programs_count=5
    )

# ---------------- STUDENT LIST (ADMIN) ----------------

@app.route("/dashboard")
def dashboard():
    if "user" not in session or session.get("role") != "admin":
        return redirect("/")

    search = request.args.get("search")
    conn = get_db()

    if search:
        students = conn.execute(
            "SELECT * FROM students WHERE name LIKE ? OR roll LIKE ?",
            (f"%{search}%", f"%{search}%")
        ).fetchall()
    else:
        students = conn.execute("SELECT * FROM students").fetchall()

    conn.close()
    return render_template("dashboard.html", students=students)

# ---------------- ADD STUDENT ----------------

@app.route("/add", methods=["GET", "POST"])
def add_student():
    if "user" not in session or session.get("role") != "admin":
        return redirect("/")

    if request.method == "POST":
        conn = get_db()
        conn.execute(
            "INSERT INTO students (name, roll, course, email) VALUES (?,?,?,?)",
            (
                request.form["name"],
                request.form["roll"],
                request.form["course"],
                request.form["email"]
            )
        )
        conn.commit()
        conn.close()
        return redirect("/dashboard")

    return render_template("add_student.html")

# ---------------- EDIT STUDENT ----------------

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_student(id):
    if "user" not in session or session.get("role") != "admin":
        return redirect("/")

    conn = get_db()
    student = conn.execute(
        "SELECT * FROM students WHERE id=?", (id,)
    ).fetchone()

    if request.method == "POST":
        conn.execute("""
            UPDATE students
            SET name=?, roll=?, course=?, email=?
            WHERE id=?
        """, (
            request.form["name"],
            request.form["roll"],
            request.form["course"],
            request.form["email"],
            id
        ))
        conn.commit()
        conn.close()
        return redirect("/dashboard")

    conn.close()
    return render_template("edit_student.html", student=student)

# ---------------- DELETE STUDENT ----------------

@app.route("/delete/<int:id>")
def delete_student(id):
    if "user" not in session or session.get("role") != "admin":
        return redirect("/")

    conn = get_db()
    conn.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/dashboard")

# ---------------- STUDENT DASHBOARD ----------------

@app.route("/student")
def student_home():
    if "user" not in session or session.get("role") != "student":
        return redirect("/")

    email = session["user"]
    conn = get_db()

    student = conn.execute(
        "SELECT * FROM students WHERE email=?",
        (email,)
    ).fetchone()

    skills = conn.execute(
        "SELECT * FROM skills WHERE student_email=?",
        (email,)
    ).fetchall()

    projects = conn.execute(
        "SELECT * FROM projects WHERE student_email=?",
        (email,)
    ).fetchall()

    conn.close()

    return render_template(
        "student_home.html",
        student=student,
        skills=skills,
        projects=projects
    )

# ---------------- SIGNUP ----------------

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        roll = request.form["roll"]
        course = request.form["course"]
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db()

        try:
            # Create login user
            conn.execute(
                "INSERT INTO users (username, password, role) VALUES (?,?,?)",
                (email, password, "student")
            )

            # Create student profile
            conn.execute(
                "INSERT INTO students (name, roll, course, email) VALUES (?,?,?,?)",
                (name, roll, course, email)
            )

            conn.commit()
        except:
            pass

        conn.close()
        return redirect("/")

    return render_template("signup.html")

# ---------------- FORGOT PASSWORD ----------------

@app.route("/forgot", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        conn = get_db()
        user = conn.execute(
            "SELECT * FROM users WHERE username=?",
            (request.form["username"],)
        ).fetchone()

        if user:
            conn.execute(
                "UPDATE users SET password=? WHERE username=?",
                (request.form["password"], request.form["username"])
            )
            conn.commit()
            conn.close()
            return redirect("/")
        else:
            conn.close()
            return render_template("forgot.html", error="User not found")

    return render_template("forgot.html")

# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

# ---------------- RUN ----------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

