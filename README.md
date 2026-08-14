# SnapClass — AI Powered Attendance System

SnapClass is an AI-powered classroom attendance management system designed to make attendance faster, smarter, and more reliable using **Face Recognition** and **Voice Recognition**.

The system provides separate workflows for teachers and students, allowing teachers to manage courses and attendance while students can enroll and track their attendance.

---

## 🚀 Features

### 👨‍🏫 Teacher Features

* Secure teacher login
* Teacher dashboard
* Create and manage courses
* Generate course enrollment codes
* Manage student rosters
* Take attendance using **Face Recognition**
* Take attendance using **Voice Recognition**
* View historical attendance records
* View attendance confidence scores
* Track student attendance
* Download attendance records as CSV

### 👨‍🎓 Student Features

* Student registration and login
* Join courses using unique course codes / QR codes
* Face biometric registration
* Voice biometric registration
* Student dashboard
* View attendance percentage
* View attendance across enrolled subjects

---

## 🤖 AI Features

### Face Recognition

SnapClass uses computer vision and facial embeddings to identify students from classroom images.

The face recognition pipeline uses:

* `face_recognition`
* `dlib`
* NumPy
* Facial embeddings

Students register their facial biometric information once. During attendance, the system compares detected faces against the stored student embeddings.

### Voice Recognition

SnapClass also supports voice-based attendance.

The system uses:

* Resemblyzer
* Librosa
* Voice embeddings

Students can register their voice once and subsequently verify their identity by speaking during attendance.

---

## 🏗️ System Architecture

```text
                    ┌─────────────────────┐
                    │      SnapClass       │
                    │   Streamlit App      │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
        Teacher Flow      Student Flow      AI Layer
              │                │                │
              │                │        ┌───────┴────────┐
              │                │        │                │
              │                │        ▼                ▼
              │                │   Face Recognition  Voice Recognition
              │                │        │                │
              └────────────────┴────────┼────────────────┘
                                       │
                                       ▼
                              ┌─────────────────┐
                              │    Supabase     │
                              │ PostgreSQL DB   │
                              └─────────────────┘
```

---

## 🛠️ Technology Stack

| Component             | Technology                |
| --------------------- | ------------------------- |
| Application Framework | Streamlit                 |
| Programming Language  | Python                    |
| Face Recognition      | face_recognition + Dlib   |
| Computer Vision       | OpenCV                    |
| Voice Recognition     | Resemblyzer + Librosa     |
| Database              | Supabase PostgreSQL       |
| Data Processing       | NumPy                     |
| Authentication        | Supabase                  |
| Attendance Storage    | Supabase                  |
| Deployment            | Streamlit Community Cloud |

---

## 📂 Project Structure

```text
SnapClass/
│
├── app.py
├── requirements.txt
├── README.md
│
├── src/
│   ├── screens/
│   │   ├── home_screen.py
│   │   ├── teacher_screen.py
│   │   └── student_screen.py
│   │
│   ├── components/
│   │   └── dialog_auto_enroll.py
│   │
│   ├── database/
│   │   └── ...
│   │
│   └── ...
│
├── data/
│   └── ...
│
└── ...
```

> The exact contents of `src/` may vary depending on the current implementation.

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/SnapClass.git
cd SnapClass
```

### 2. Create a virtual environment

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

SnapClass uses Supabase for its backend database and authentication.

Create a `.env` file in the project root:

```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
```

Never commit your actual Supabase credentials to GitHub.

Add the following to `.gitignore`:

```gitignore
.env
venv/
__pycache__/
*.pyc
.streamlit/secrets.toml
```

---

## ▶️ Running the Application

Start the Streamlit application with:

```bash
streamlit run app.py
```

The application will normally be available at:

```text
http://localhost:8501
```

---

## 👨‍🏫 Teacher Workflow

```text
Teacher Login
     ↓
Teacher Dashboard
     ↓
Create / Select Course
     ↓
Manage Student Roster
     ↓
Start Attendance
     ↓
┌───────────────────────┐
│                       │
▼                       ▼
Face Attendance     Voice Attendance
│                       │
└───────────┬───────────┘
            ↓
      Attendance Record
            ↓
       View / Export
```

---

## 👨‍🎓 Student Workflow

```text
Student Login
      ↓
Join Course
      ↓
Biometric Registration
      ↓
┌───────────────────────┐
│                       │
▼                       ▼
Register Face       Register Voice
│                       │
└───────────┬───────────┘
            ↓
      Student Dashboard
            ↓
    View Attendance Data
```

---

## 📸 Face Attendance

The face attendance system identifies students using facial embeddings.

The general process is:

```text
Classroom Image
      ↓
Face Detection
      ↓
Face Encoding
      ↓
Compare with Registered Encodings
      ↓
Student Identification
      ↓
Attendance Marked
```

The system is designed to allow attendance to be taken from a classroom image rather than requiring the teacher to manually call every student.

---

## 🎙️ Voice Attendance

The voice attendance workflow is:

```text
Student Speaks
      ↓
Audio Processing
      ↓
Voice Embedding
      ↓
Compare with Stored Voice Embeddings
      ↓
Student Verification
      ↓
Attendance Marked
```

This provides an alternative attendance mechanism when face-based attendance is not suitable.

---

## 🔗 Course Enrollment

Students can join courses using a course-specific enrollment code.

The application also supports enrollment through a URL containing a `join-code`.

Example:

```text
?join-code=COURSE_CODE
```

The Streamlit application detects the join code and directs the student through the enrollment process.

---

## 📊 Attendance Records

Attendance records are stored in the application's database and can be accessed through the teacher interface.

Teachers can:

* View attendance history
* Review student attendance
* Check recognition confidence
* Manage attendance records
* Export attendance information

---

## ☁️ Deployment

SnapClass is designed to run as a Streamlit application.

For deployment:

1. Push the project to GitHub.
2. Create a Streamlit Community Cloud application.
3. Select the GitHub repository.
4. Select the main Streamlit file:

```text
app.py
```

5. Configure the required secrets.
6. Deploy the application.

The required Supabase credentials should be added through Streamlit's **Secrets** configuration rather than committing them to the repository.

---

## 🔒 Security

The project uses environment variables / application secrets for sensitive configuration.

Do **not** upload:

```text
.env
.streamlit/secrets.toml
Supabase private keys
Database passwords
Private API keys
```

to GitHub.

For production deployment, additional security measures should be implemented around biometric data, authentication, authorization, and database access.

---

## 🧪 Current Application

The main Streamlit application controls the user experience based on the login type:

```python
match st.session_state['login_type']:
    case 'teacher':
        teacher_screen()

    case 'student':
        student_screen()

    case None:
        home_screen()
```

This provides separate interfaces for teachers and students.

---

## 🎯 Project Objective

SnapClass aims to reduce the time and manual effort required for classroom attendance by combining:

* Computer vision
* Facial recognition
* Voice biometrics
* Cloud database infrastructure
* Automated attendance records
* Teacher and student dashboards

The goal is to provide a faster and more modern alternative to traditional manual attendance systems.

---

## 🔮 Future Improvements

Potential future improvements include:

* Improved anti-spoofing / liveness detection
* More robust face recognition under different lighting conditions
* Advanced voice anti-spoofing
* Mobile application
* Advanced attendance analytics
* Automated attendance reports
* Role-based administrative dashboard
* Improved biometric privacy controls
* Notification system
* Integration with institutional student-management systems

---

## 👨‍💻 Author

**Riya Jain**
