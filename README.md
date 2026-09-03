# Security Posture Assessment Tool

A NIST CSF-based security posture assessment platform for fictional small organisations. Built for university coursework — no penetration testing or external network scanning.

## 🎯 Project Overview

**Context:** Digital solutions consultancy project  
**Framework:** NIST Cybersecurity Framework (CSF) v1.1  
**Scope:** 45+ controls across 5 core functions (Identify, Protect, Detect, Respond, Recover)

### Features

✅ **Control Assessment** — Evaluate 45+ NIST CSF controls with maturity scoring (0-5)  
✅ **Evidence Register** — Track verification status (none/partial/full) with references  
✅ **Transparent Scoring** — Explainable methodology with function-level and overall posture scores  
✅ **Gap Analysis Dashboard** — Interactive charts (radar, bar, doughnut) showing security gaps  
✅ **Prioritised Roadmap** — Auto-generated improvement plan with effort bands (Low/Medium/High)  
✅ **Printable Reports** — PDF-ready executive reports with full control register  
✅ **Audit Trail** — Complete activity logging for accountability  
✅ **Role-Based Access** — Admin and Assessor roles  
✅ **Sample Data** — 3 pre-seeded fictional organisations with test scenarios

## 🛠️ Tech Stack

- **Backend:** Python 3.9+, Flask 3.0
- **Database:** SQLite (easy deployment, no setup)
- **Frontend:** Bootstrap 5, Chart.js, Jinja2 templates
- **Auth:** Flask-Login with bcrypt password hashing

## 📦 Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python package manager)
- Git Bash (Windows) or standard terminal (Mac/Linux)

### Step 1: Clone or Extract Project

```bash
cd E:/SneheelVirale/security-posture-tool
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv

# Windows (Git Bash)
source venv/Scripts/activate

# Mac/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Initialize Database & Load Seed Data

```bash
flask init-db --seed
```

This will:
- Create all database tables
- Load 45+ NIST CSF controls
- Create 3 sample organisations (Bakery, TechStart, Medical Clinic)
- Generate pre-built assessment scenarios for testing
- Create default admin user: `admin` / `admin123`

### Step 5: Run the Application

```bash
flask run
```

Open your browser to: **http://127.0.0.1:5000**

## 🚀 Quick Start Guide

1. **Login** with `admin` / `admin123`
2. **Explore** the 3 pre-loaded sample organisations and their completed assessments
3. **Create** a new organisation from the Organisations page
4. **Start** a new assessment for that organisation
5. **Evaluate** controls across all 5 NIST functions (maturity 0-5, evidence status)
6. **Complete** the assessment to unlock the dashboard and roadmap
7. **View** gap analysis dashboard with interactive charts
8. **Generate** printable PDF report

## 📁 Project Structure

```
security-posture-tool/
├── app/
│   ├── __init__.py           # App factory, blueprints
│   ├── models.py             # SQLAlchemy models (User, Organisation, Control, Assessment, etc.)
│   ├── auth/                 # Authentication routes (login, register)
│   ├── main/                 # Main routes (dashboard, orgs, controls)
│   ├── assessment/           # Assessment workflow (create, conduct, complete)
│   ├── dashboard/            # Gap analysis & roadmap views
│   ├── report/               # Printable report generation
│   ├── templates/            # Jinja2 HTML templates
│   └── static/               # CSS, JavaScript, images
├── seeds/
│   ├── controls.py           # 45+ NIST CSF control definitions
│   ├── organisations.py      # Sample organisation profiles
│   ├── scenarios.py          # Pre-seeded assessment data
│   └── seed_data.py          # Database seeding script
├── instance/                 # SQLite database (created on init-db)
├── config.py                 # Flask configuration
├── run.py                    # Application entry point
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## 🔐 User Roles

### Admin
- Full system access
- Create/manage users
- Create organisations
- Conduct and view all assessments
- Access audit trail

### Assessor
- Conduct assessments
- View assigned organisations
- Generate reports
- No user management access

## 📊 Assessment Workflow

1. **Create Assessment** → Select organisation
2. **Conduct Assessment** → Evaluate 45+ controls across 5 NIST functions
   - Assign maturity score (0-5)
   - Set evidence status (none/partial/full)
   - Add evidence references and notes
3. **Complete Assessment** → Lock responses
4. **View Dashboard** → Charts, gap analysis, function scores
5. **Generate Roadmap** → Prioritised improvement plan
6. **Print Report** → Executive summary with full control register

## 🧪 Testing & Validation

### Seeded Test Scenarios

Three realistic scenarios are pre-loaded:

1. **Maple Leaf Bakery** — Retail, 15 employees
   - Low maturity (mostly 0-2)
   - Minimal IT security, weak across all functions
   
2. **TechStart Solutions** — SaaS startup, 30 employees
   - Mixed maturity (2-4)
   - Strong technical controls, weak governance/recovery
   
3. **Greenfield Medical Clinic** — Healthcare, 25 employees
   - Moderate maturity (1-3)
   - Strong data protection (compliance-driven), weak detection/response

### Manual Testing Checklist

- [ ] Create new organisation
- [ ] Start assessment with all 45+ controls visible
- [ ] Submit maturity scores and evidence for at least 10 controls
- [ ] Complete assessment
- [ ] View dashboard with radar chart, bar chart, doughnut chart
- [ ] Check gap list shows controls with score < 3
- [ ] View roadmap with 4 phases (Quick Wins, Short/Medium/Long-term)
- [ ] Print report (Ctrl+P or Print button)
- [ ] Check audit trail logs actions

## 📖 Minimum Completion Criteria (Met)

✅ At least 40 controls (45+ implemented)  
✅ Evidence status tracking (none/partial/full)  
✅ Explainable maturity scores (transparent methodology page)  
✅ Prioritised roadmap (effort-based phasing)  
✅ Printable report (PDF-ready with print CSS)  
✅ Audit trail (full activity logging)  
✅ Validated test cases (3 seeded scenarios)

## ⚠️ Ethics, Scope & Limitations

### No Penetration Testing
This tool **does not** perform:
- Network scanning
- Vulnerability testing
- Password cracking
- Intrusion attempts
- External reconnaissance

### Educational Use Only
- Designed for **fictional organisations** under lecturer supervision
- Framework interpretation approved by lecturer
- No real-world security assessments without proper authorisation

### Limitations
- Point-in-time assessment (not continuous monitoring)
- Self-reported with manual evidence verification
- Small organisation focus (not enterprise-scale)
- Qualitative maturity model (not quantitative risk scores)

## 🔧 Configuration

### Change Admin Password

After first login, create a new admin user or change the default password in the database.

### Database Location

SQLite database is stored in: `instance/securitytool.db`

To reset the database:
```bash
rm instance/securitytool.db
flask init-db --seed
```

### Production Deployment

For deployment on university hosting:

1. Set `FLASK_ENV=production`
2. Generate secure `SECRET_KEY` in config.py
3. Use a proper WSGI server (Gunicorn, uWSGI)
4. Enable HTTPS
5. Change default admin credentials

## 📚 NIST CSF Reference

This tool implements controls from:
- **Identify (ID)** — Asset Management, Governance, Risk Assessment
- **Protect (PR)** — Access Control, Data Security, Training
- **Detect (DE)** — Continuous Monitoring, Detection Processes
- **Respond (RS)** — Response Planning, Communications, Mitigation
- **Recover (RC)** — Recovery Planning, Improvements

Official NIST CSF documentation: https://www.nist.gov/cyberframework

## 👨‍💻 Development

### Adding New Controls

Edit `seeds/controls.py` and re-run:
```bash
flask init-db --seed
```

### Customizing Maturity Levels

Edit `config.py` → `MATURITY_LEVELS` dictionary

### Modifying Effort Bands

Edit `config.py` → `EFFORT_BANDS` dictionary

## 📝 License & Academic Integrity

This project is submitted as university coursework. Code reuse must cite this source and comply with your institution's academic integrity policy.

---

**Built with Flask & NIST CSF** | For educational assessment only | No active penetration testing
