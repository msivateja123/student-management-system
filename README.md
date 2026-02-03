# 🎓 Student Management System (Flask)

A full-stack **Student Management System** built using **Flask, SQLite, HTML, and CSS**.  
The system provides **role-based authentication** with separate dashboards for **Admin** and **Students**.

---

## 🚀 Features

### 👨‍💼 Admin Module
- Secure Admin Login
- Admin Dashboard with statistics
- Add / Edit / Delete Students
- View all registered students
- Search students by name or roll number

### 👨‍🎓 Student Module
- Student Registration & Login
- Personalized Student Dashboard
- View personal details (Roll No, Course, Email)
- Add & manage skills with proficiency levels
- Add & manage academic projects
- Secure logout

### 🔐 Authentication
- Role-based login (Admin / Student)
- Session management
- Forgot password feature

---

## 🛠️ Tech Stack

- **Backend:** Python (Flask)
- **Frontend:** HTML, CSS
- **Database:** SQLite
- **Version Control:** Git & GitHub

---

## 📂 Project Structure

student-management-system/
│
├── app.py
├── database.db (ignored)
├── requirements.txt
├── .gitignore
├── README.md
│
├── static/
│ ├── style.css
│ └── admin.css
│
└── templates/
├── login.html
├── signup.html
├── forgot.html
├── admin_dashboard.html
├── dashboard.html
├── add_student.html
├── edit_student.html
└── student_home.html


---

## ⚙️ Installation & Setup

```bash
# Clone repository
git clone https://github.com/msivateja123/student-management-system.git

# Move into folder
cd student-management-system

# Install dependencies
pip install -r requirements.txt

# Run application
python app.py

Open browser 👉 http://127.0.0.1:500

🔑 Default Admin Credentials
Username: admin
Password: admin

🌱 Future Enhancements

Password hashing (bcrypt)

Admin role management

Student profile picture upload

Deployment on Render / Railway

REST API support

👨‍💻 Author

Sivateja
GitHub: https://github.com/msivateja123

