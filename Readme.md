# 🤖 kam  - kaj Job Portal

A full-stack **AI-powered Job Portal** built with **Python, Streamlit, SQLite, and Generative AI**. The platform connects **Candidates**, **Employers**, and **Administrators** in a modern recruitment system with AI-assisted resume screening, ATS scoring, job matching, analytics, notifications, and comprehensive management dashboards.

---

# 📌 Project Overview

The AI Job Portal simplifies the hiring process by providing:

* Secure authentication
* AI-based resume analysis
* ATS score calculation
* Intelligent job matching
* Employer recruitment dashboard
* Candidate dashboard
* Admin management panel
* Real-time analytics
* Notifications
* Audit logging
* Resume management

The project demonstrates full-stack Python development, database management, data visualization, AI integration, and professional software architecture.

---

# 🚀 Features

## 👨‍💻 Candidate Module

* User Registration & Login
* Secure Password Encryption (bcrypt)
* Browse Available Jobs
* Apply for Jobs
* AI Resume Analysis
* ATS Score Evaluation
* Resume Skill Matching
* AI Candidate Dashboard
* Application Tracking
* Notifications

---

## 🏢 Employer Module

* Employer Registration & Login
* Post New Jobs
* Manage Posted Jobs
* View Applications
* Candidate Search & Filtering
* ATS Score Comparison
* Resume Match Percentage
* Shortlist Candidates
* Reject Applications
* Schedule Interviews
* Recruiter Dashboard
* Analytics Charts
* Activity Timeline
* Excel Export

---

## 👨‍💼 Admin Module

* Admin Authentication
* User Management
* Job Management
* Application Management
* Platform Statistics
* Dashboard Analytics
* Activity Monitoring
* Enable / Disable Users
* Delete Users
* Delete Jobs
* Delete Applications

---

## 🤖 AI Features

* Resume Parsing
* ATS Score Generation
* Resume Skill Extraction
* Job Recommendation
* Resume-Job Matching
* Candidate Ranking

---

## 📊 Analytics

* Recruiter Dashboard
* ATS Score Charts
* Match Percentage Charts
* Job Statistics
* Platform Statistics
* User Statistics
* Application Statistics

---

## 🔐 Security Features

* Password Hashing using bcrypt
* Session-Based Authentication
* Role-Based Access Control
* Audit Logging
* Input Validation
* Error Handling
* Logging System

---

# 🛠️ Technology Stack

## Programming Language

* Python 3.x

## Frontend

* Streamlit

## Database

* SQLite

## Data Processing

* Pandas

## AI & NLP

* Google Gemini API

## Data Visualization

* Matplotlib

## Security

* bcrypt

## Environment Management

* python-dotenv

## Excel Export

* openpyxl

---

# 📂 Project Structure

```text
kam-kaj Job-Portal/
│
├── app.py
├── constants.py
├── requirements.txt
├── README.md
├── .env
│
├── components/
├── database/
├── pages/
├── services/
├── utils/
├── uploads/
├── logs/
└── assets/
```

---

# ⚙️ Installation

## 1. Clone Repository

```bash
git clone https://github.com/jashan-0001/kam-kaj-Job-Portal.git
```

---

## 2. Move into Project

```bash
cd kam-kaj-Job-Portal
```

---

## 3. Create Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

---

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 5. Configure Environment Variables

Create a `.env` file.

Example:

```env
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

---

## 6. Initialize Database

```bash
python -m database.init_db
```

---

## 7. Create Default Admin

```bash
python -m database.seed_admin
```

---

## 8. Run the Application

```bash
streamlit run app.py
```

---

# 👤 Default Admin Login

Email

```text
admin@portal.com
```

Password

```text
Admin@123
```

---

# 📊 User Roles

## Candidate

* Browse Jobs
* Apply for Jobs
* AI Resume Analysis
* Notifications

---

## Employer

* Post Jobs
* Manage Jobs
* Review Applications
* Analytics
* Activity Timeline

---

## Admin

* Manage Users
* Manage Jobs
* Manage Applications
* Platform Analytics
* Audit Logs

---

# 📸 Screenshots

Add screenshots here after deployment.

Example:

```
assets/
    home.png
    candidate_dashboard.png
    employer_dashboard.png
    admin_dashboard.png
```

---

# Future Improvements

* Email Verification
* Password Reset
* Resume Builder
* AI Interview Assistant
* Video Interview Module
* Multi-language Support
* Cloud Database
* Docker Support
* REST API
* Mobile Responsive UI

---

# 👨‍💻 Author

**Jashanpreet Singh**

Python Developer | AI Enthusiast | Data Analytics

GitHub:
https://github.com/jashan-0001

LinkedIn:
https://linkedin.com/in/Jashanpreet Singh

---

# License

This project is developed for educational and portfolio purposes.

---

# ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.

Feedback and contributions are always welcome.
