import os
import re
import sqlite3
import random
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    jsonify
)

from werkzeug.utils import secure_filename


# ============================================================
# PATH CONFIGURATION
# ============================================================

BASE = os.path.dirname(os.path.abspath(__file__))

DATA_FOLDER = os.path.join(BASE, "data")
UPLOAD_FOLDER = os.path.join(BASE, "uploads")

os.makedirs(DATA_FOLDER, exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

DB = os.path.join(DATA_FOLDER, "jobs.db")


# ============================================================
# FLASK APP
# ============================================================

app = Flask(__name__)

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "resume-demo-secret"
)


# ============================================================
# ALLOWED FILE TYPES
# ============================================================

ALLOWED = {
    "pdf",
    "docx",
    "txt"
}


# ============================================================
# SKILL DATABASE
# ============================================================

SKILLS = [
    "Python",
    "Java",
    "JavaScript",
    "TypeScript",
    "C",
    "C++",
    "C#",
    "SQL",
    "R",
    "HTML",
    "CSS",
    "React",
    "Angular",
    "Vue.js",
    "Node.js",
    "Express.js",
    "Django",
    "Flask",
    "Spring Boot",
    "REST API",
    "Git",
    "GitHub",
    "Docker",
    "Kubernetes",
    "AWS",
    "Azure",
    "GCP",
    "Linux",
    "Power BI",
    "Tableau",
    "Excel",
    "Statistics",
    "Machine Learning",
    "Deep Learning",
    "TensorFlow",
    "PyTorch",
    "NLP",
    "Computer Vision",
    "OpenCV",
    "Pandas",
    "NumPy",
    "Scikit-learn",
    "Spark",
    "Hadoop",
    "ETL",
    "Data Visualization",
    "Figma",
    "Selenium",
    "Jenkins",
    "Terraform",
    "Cybersecurity",
    "Networking",
    "Agile",
    "Jira",
    "Communication",
    "Leadership"
]


# ============================================================
# MAIN JOB ROLES + REQUIRED SKILLS
# ============================================================

ROLE_BASE = [

    (
        "Data Analyst",
        [
            "Python",
            "SQL",
            "Excel",
            "Statistics",
            "Power BI",
            "Data Visualization"
        ]
    ),

    (
        "Data Scientist",
        [
            "Python",
            "SQL",
            "Statistics",
            "Machine Learning",
            "Pandas",
            "NumPy",
            "Scikit-learn"
        ]
    ),

    (
        "Machine Learning Engineer",
        [
            "Python",
            "SQL",
            "Machine Learning",
            "Deep Learning",
            "TensorFlow",
            "Docker",
            "Git"
        ]
    ),

    (
        "AI Engineer",
        [
            "Python",
            "Machine Learning",
            "Deep Learning",
            "TensorFlow",
            "PyTorch",
            "Git",
            "Docker"
        ]
    ),

    (
        "Data Engineer",
        [
            "Python",
            "SQL",
            "ETL",
            "Spark",
            "Hadoop",
            "AWS",
            "Docker"
        ]
    ),

    (
        "Software Engineer",
        [
            "Java",
            "Python",
            "SQL",
            "Git",
            "REST API",
            "Docker"
        ]
    ),

    (
        "Full Stack Developer",
        [
            "JavaScript",
            "React",
            "Node.js",
            "HTML",
            "CSS",
            "SQL",
            "Git"
        ]
    ),

    (
        "Frontend Developer",
        [
            "JavaScript",
            "React",
            "HTML",
            "CSS",
            "Git",
            "Figma"
        ]
    ),

    (
        "Backend Developer",
        [
            "Java",
            "Python",
            "Node.js",
            "SQL",
            "REST API",
            "Docker"
        ]
    ),

    (
        "Cloud Engineer",
        [
            "Linux",
            "AWS",
            "Docker",
            "Kubernetes",
            "Terraform",
            "Networking"
        ]
    ),

    (
        "DevOps Engineer",
        [
            "Linux",
            "Docker",
            "Kubernetes",
            "Jenkins",
            "AWS",
            "Terraform",
            "Git"
        ]
    ),

    (
        "Cybersecurity Analyst",
        [
            "Cybersecurity",
            "Networking",
            "Linux",
            "Python",
            "SQL"
        ]
    ),

    (
        "Business Analyst",
        [
            "SQL",
            "Excel",
            "Power BI",
            "Communication",
            "Agile",
            "Jira"
        ]
    ),

    (
        "AI Research Intern",
        [
            "Python",
            "Machine Learning",
            "Statistics",
            "PyTorch",
            "TensorFlow"
        ]
    ),

    (
        "QA Automation Engineer",
        [
            "Python",
            "Java",
            "Selenium",
            "Git",
            "Jenkins",
            "SQL"
        ]
    ),

    (
        "UI/UX Designer",
        [
            "Figma",
            "HTML",
            "CSS",
            "Communication"
        ]
    ),

    (
        "Product Analyst",
        [
            "SQL",
            "Excel",
            "Statistics",
            "Power BI",
            "Communication"
        ]
    ),

    (
        "NLP Engineer",
        [
            "Python",
            "NLP",
            "Machine Learning",
            "Deep Learning",
            "PyTorch",
            "TensorFlow"
        ]
    ),

    (
        "Computer Vision Engineer",
        [
            "Python",
            "Computer Vision",
            "OpenCV",
            "Deep Learning",
            "PyTorch"
        ]
    ),

    (
        "Database Administrator",
        [
            "SQL",
            "Linux",
            "Networking",
            "Python"
        ]
    )
]


# ============================================================
# COMPANY DATABASE
# ============================================================

COMPANIES = [
    "TCS",
    "Infosys",
    "Wipro",
    "HCLTech",
    "Tech Mahindra",
    "Accenture",
    "Cognizant",
    "Capgemini",
    "IBM",
    "Microsoft",
    "Amazon",
    "Google",
    "Oracle",
    "SAP",
    "Deloitte",
    "EY",
    "KPMG",
    "PwC",
    "Zoho",
    "Freshworks",
    "Mphasis",
    "LTIMindtree",
    "Persistent Systems",
    "Hexaware",
    "Coforge",
    "CitiusTech",
    "Genpact",
    "DXC Technology",
    "Cognizant Technology Solutions",
    "Cisco",
    "Intel",
    "Adobe",
    "Salesforce",
    "ServiceNow",
    "Dell Technologies",
    "HP",
    "Qualcomm",
    "NVIDIA",
    "Walmart Global Tech",
    "Flipkart",
    "Swiggy",
    "Zomato",
    "Razorpay",
    "PhonePe",
    "Paytm",
    "Jio Platforms",
    "Airtel",
    "Ola",
    "Uber",
    "Atlassian"
]


# Add demo companies to make the portfolio dataset large.
COMPANIES += [
    f"DemoTech Solutions {i:03d}"
    for i in range(1, 171)
]


# ============================================================
# ROLE DATABASE
# ============================================================

ROLE_NAMES = [
    role[0]
    for role in ROLE_BASE
]


ROLE_NAMES += [
    f"{x} Specialist"
    for x in [
        "AI",
        "Data",
        "Cloud",
        "Software",
        "Security",
        "Analytics",
        "ML",
        "Business",
        "Product",
        "Automation",
        "Platform",
        "DevOps",
        "Web",
        "Database",
        "NLP",
        "Vision",
        "Research",
        "QA",
        "Systems",
        "Application"
    ]
]


ROLE_NAMES += [
    f"{x} Engineer"
    for x in [
        "Applied AI",
        "Data Platform",
        "Cloud Security",
        "MLOps",
        "Analytics",
        "Solutions",
        "Platform",
        "AI/ML",
        "Software",
        "Systems",
        "Integration",
        "Site Reliability",
        "Data Quality",
        "Computer Vision",
        "NLP",
        "Prompt"
    ]
]


ROLE_NAMES += [
    f"{x} Analyst"
    for x in [
        "Risk",
        "Operations",
        "Marketing",
        "Product",
        "BI",
        "Security",
        "Data Quality",
        "Business Intelligence",
        "Fraud",
        "Research",
        "Cloud"
    ]
]


# Remove duplicate roles
ROLE_NAMES = list(dict.fromkeys(ROLE_NAMES))


# Ensure 220+ roles
while len(ROLE_NAMES) < 220:
    ROLE_NAMES.append(
        f"Digital Technology Role {len(ROLE_NAMES) + 1:03d}"
    )


# ============================================================
# DATABASE CONNECTION
# ============================================================

def conn():
    connection = sqlite3.connect(DB)
    connection.row_factory = sqlite3.Row
    return connection


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

def init_db():

    connection = conn()

    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS companies(
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE
        );

        CREATE TABLE IF NOT EXISTS roles(
            id INTEGER PRIMARY KEY,
            name TEXT UNIQUE,
            skills TEXT
        );

        CREATE TABLE IF NOT EXISTS jobs(
            id INTEGER PRIMARY KEY,
            company_id INTEGER,
            role_id INTEGER,
            location TEXT,
            experience TEXT,
            vacancies INTEGER,
            year INTEGER,
            skills TEXT
        );
        """
    )

    # --------------------------------------------------------
    # Insert companies
    # --------------------------------------------------------

    for company_name in COMPANIES:

        connection.execute(
            """
            INSERT OR IGNORE INTO companies(name)
            VALUES(?)
            """,
            (company_name,)
        )

    # --------------------------------------------------------
    # Insert main roles
    # --------------------------------------------------------

    for role_name, skills in ROLE_BASE:

        connection.execute(
            """
            INSERT OR IGNORE INTO roles(name, skills)
            VALUES(?, ?)
            """,
            (
                role_name,
                ",".join(skills)
            )
        )

    # --------------------------------------------------------
    # Insert generated roles
    # --------------------------------------------------------

    for role_name in ROLE_NAMES:

        exists = connection.execute(
            """
            SELECT 1
            FROM roles
            WHERE name = ?
            """,
            (role_name,)
        ).fetchone()

        if not exists:

            generated_skills = random.Random(
                role_name
            ).sample(
                SKILLS,
                min(6, len(SKILLS))
            )

            connection.execute(
                """
                INSERT INTO roles(name, skills)
                VALUES(?, ?)
                """,
                (
                    role_name,
                    ",".join(generated_skills)
                )
            )

    # --------------------------------------------------------
    # IMPORTANT FIX:
    # fetchall() must be called on execute() result
    # --------------------------------------------------------

    companies = connection.execute(
        """
        SELECT id, name
        FROM companies
        """
    ).fetchall()

    roles = connection.execute(
        """
        SELECT id, name, skills
        FROM roles
        """
    ).fetchall()

    # --------------------------------------------------------
    # Generate demo job data only once
    # --------------------------------------------------------

    job_count = connection.execute(
        """
        SELECT COUNT(*) AS n
        FROM jobs
        """
    ).fetchone()["n"]

    if job_count == 0:

        rng = random.Random(42)

        locations = [
            "Bengaluru",
            "Chennai",
            "Hyderabad",
            "Pune",
            "Mumbai",
            "Delhi NCR",
            "Coimbatore",
            "Remote"
        ]

        years = [
            2022,
            2023,
            2024,
            2025
        ]

        experience_levels = [
            "0-2 years",
            "1-3 years",
            "2-5 years",
            "3-6 years"
        ]

        for company in companies:

            selected_roles = rng.sample(
                roles,
                min(5, len(roles))
            )

            for role in selected_roles:

                role_skills = [
                    skill
                    for skill in role["skills"].split(",")
                    if skill
                ]

                connection.execute(
                    """
                    INSERT INTO jobs(
                        company_id,
                        role_id,
                        location,
                        experience,
                        vacancies,
                        year,
                        skills
                    )
                    VALUES(?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        company["id"],
                        role["id"],
                        rng.choice(locations),
                        rng.choice(experience_levels),
                        rng.randint(3, 65),
                        rng.choice(years),
                        ",".join(role_skills)
                    )
                )

    connection.commit()
    connection.close()


# ============================================================
# RESUME TEXT EXTRACTION
# ============================================================

def extract_text(path):

    extension = path.rsplit(
        ".",
        1
    )[-1].lower()

    # TXT
    if extension == "txt":

        try:
            with open(
                path,
                "r",
                encoding="utf-8",
                errors="ignore"
            ) as file:

                return file.read()

        except Exception:
            return ""

    # PDF
    if extension == "pdf":

        try:

            import pypdf

            reader = pypdf.PdfReader(path)

            pages = []

            for page in reader.pages:

                pages.append(
                    page.extract_text() or ""
                )

            return "\n".join(pages)

        except Exception:
            return ""

    # DOCX
    if extension == "docx":

        try:

            from docx import Document

            document = Document(path)

            return "\n".join(
                paragraph.text
                for paragraph in document.paragraphs
            )

        except Exception:
            return ""

    return ""


# ============================================================
# SKILL DETECTION
# ============================================================

def find_skills(text):

    if not text:
        return []

    lower_text = text.lower()

    found = []

    for skill in SKILLS:

        pattern = (
            r"(?<![a-z0-9])"
            + re.escape(skill.lower())
            + r"(?![a-z0-9])"
        )

        if re.search(
            pattern,
            lower_text
        ):

            found.append(skill)

    return found


# ============================================================
# SKILL GAP ANALYSIS
# ============================================================

def analyze(user_skills, role_skills):

    user_skill_set = {
        skill.lower()
        for skill in user_skills
    }

    matched = [
        skill
        for skill in role_skills
        if skill.lower() in user_skill_set
    ]

    missing = [
        skill
        for skill in role_skills
        if skill.lower() not in user_skill_set
    ]

    score = round(
        len(matched)
        / max(1, len(role_skills))
        * 100
    )

    return matched, missing, score


# ============================================================
# TEMPLATE GLOBAL VARIABLES
# ============================================================

@app.context_processor
def inject():

    return {
        "user": session.get("user")
    }


# ============================================================
# LOGIN
# ============================================================

@app.route(
    "/",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        name = request.form.get(
            "name",
            "User"
        ).strip()

        if not name:
            name = "User"

        session["user"] = name

        return redirect(
            url_for("dashboard")
        )

    return render_template(
        "login.html"
    )


# ============================================================
# DASHBOARD
# ============================================================

@app.route("/dashboard")
def dashboard():

    if "user" not in session:

        return redirect(
            url_for("login")
        )

    connection = conn()

    companies = connection.execute(
        """
        SELECT id, name
        FROM companies
        ORDER BY name
        """
    ).fetchall()

    roles = connection.execute(
        """
        SELECT id, name
        FROM roles
        ORDER BY name
        """
    ).fetchall()

    connection.close()

    return render_template(
        "dashboard.html",
        companies=companies,
        roles=roles,
        skills=SKILLS
    )


# ============================================================
# RESUME ANALYSIS
# ============================================================

@app.route(
    "/analyze",
    methods=["POST"]
)
def do_analyze():

    if "user" not in session:

        return redirect(
            url_for("login")
        )

    # --------------------------------------------------------
    # Get company
    # --------------------------------------------------------

    try:

        company_id = int(
            request.form.get(
                "company_id",
                0
            )
        )

        role_id = int(
            request.form.get(
                "role_id",
                0
            )
        )

    except ValueError:

        flash(
            "Please select a valid company and role."
        )

        return redirect(
            url_for("dashboard")
        )

    # --------------------------------------------------------
    # Get uploaded resume
    # --------------------------------------------------------

    uploaded_file = request.files.get(
        "resume"
    )

    resume_text = request.form.get(
        "resume_text",
        ""
    )

    filename = ""

    # --------------------------------------------------------
    # Process uploaded file
    # --------------------------------------------------------

    if uploaded_file and uploaded_file.filename:

        original_name = uploaded_file.filename

        if "." not in original_name:

            flash(
                "Please upload PDF, DOCX or TXT file."
            )

            return redirect(
                url_for("dashboard")
            )

        extension = original_name.rsplit(
            ".",
            1
        )[-1].lower()

        if extension not in ALLOWED:

            flash(
                "Upload only PDF, DOCX or TXT files."
            )

            return redirect(
                url_for("dashboard")
            )

        filename = secure_filename(
            original_name
        )

        # Avoid accidental overwrite
        filename = (
            str(random.randint(1000, 9999))
            + "_"
            + filename
        )

        file_path = os.path.join(
            UPLOAD_FOLDER,
            filename
        )

        uploaded_file.save(
            file_path
        )

        resume_text = extract_text(
            file_path
        )

    # --------------------------------------------------------
    # If no readable resume, use manual skills/text
    # --------------------------------------------------------

    if not resume_text.strip():

        resume_text = request.form.get(
            "skills",
            ""
        )

    # --------------------------------------------------------
    # Find skills
    # --------------------------------------------------------

    user_skills = find_skills(
        resume_text
    )

    # --------------------------------------------------------
    # Database
    # --------------------------------------------------------

    connection = conn()

    company = connection.execute(
        """
        SELECT *
        FROM companies
        WHERE id = ?
        """,
        (company_id,)
    ).fetchone()

    role = connection.execute(
        """
        SELECT *
        FROM roles
        WHERE id = ?
        """,
        (role_id,)
    ).fetchone()

    if not company or not role:

        connection.close()

        flash(
            "Invalid company or role selected."
        )

        return redirect(
            url_for("dashboard")
        )

    # --------------------------------------------------------
    # Main skill analysis
    # --------------------------------------------------------

    required_skills = [
        skill.strip()
        for skill in role["skills"].split(",")
        if skill.strip()
    ]

    matched, missing, score = analyze(
        user_skills,
        required_skills
    )

    # --------------------------------------------------------
    # Matching jobs for selected company + role
    # --------------------------------------------------------

    jobs = connection.execute(
        """
        SELECT
            j.*,
            r.name AS role_name,
            co.name AS company_name
        FROM jobs j
        JOIN roles r
            ON r.id = j.role_id
        JOIN companies co
            ON co.id = j.company_id
        WHERE j.company_id = ?
          AND j.role_id = ?
        ORDER BY j.year DESC
        """,
        (
            company_id,
            role_id
        )
    ).fetchall()

    # --------------------------------------------------------
    # Alternative career options
    # --------------------------------------------------------

    alternatives = []

    all_roles = connection.execute(
        """
        SELECT *
        FROM roles
        """
    ).fetchall()

    for alternative_role in all_roles:

        if alternative_role["id"] == role_id:
            continue

        alternative_skills = [
            skill.strip()
            for skill in alternative_role["skills"].split(",")
            if skill.strip()
        ]

        alt_matched, alt_missing, alt_score = analyze(
            user_skills,
            alternative_skills
        )

        alternative_jobs = connection.execute(
            """
            SELECT
                j.*,
                co.name AS company_name
            FROM jobs j
            JOIN companies co
                ON co.id = j.company_id
            WHERE j.role_id = ?
            ORDER BY j.year DESC
            LIMIT 3
            """,
            (
                alternative_role["id"],
            )
        ).fetchall()

        if alternative_jobs:

            total_vacancies = sum(
                job["vacancies"]
                for job in alternative_jobs
            )

            alternatives.append(
                {
                    "role": alternative_role["name"],
                    "score": alt_score,
                    "missing": alt_missing,
                    "company": alternative_jobs[0]["company_name"],
                    "vacancies": total_vacancies,
                    "year": alternative_jobs[0]["year"]
                }
            )

    # Sort alternatives by matching percentage
    alternatives = sorted(
        alternatives,
        key=lambda item: (
            -item["score"],
            item["role"]
        )
    )[:8]

    # --------------------------------------------------------
    # Learning roadmap
    # --------------------------------------------------------

    roadmap = []

    for index, skill in enumerate(missing):

        roadmap.append(
            {
                "skill": skill,
                "priority": (
                    "High"
                    if index < 2
                    else "Medium"
                )
            }
        )

    connection.close()

    # --------------------------------------------------------
    # Save analysis in session
    # --------------------------------------------------------

    session["analysis"] = {
        "company": company["name"],
        "role": role["name"],
        "score": score,
        "matched": matched,
        "missing": missing,
        "user_skills": user_skills,
        "jobs": [
            dict(job)
            for job in jobs
        ],
        "alternatives": alternatives,
        "roadmap": roadmap,
        "filename": filename
    }

    return redirect(
        url_for("results")
    )


# ============================================================
# RESULTS
# ============================================================

@app.route("/results")
def results():

    if "analysis" not in session:

        return redirect(
            url_for("dashboard")
        )

    return render_template(
        "results.html",
        a=session["analysis"]
    )


# ============================================================
# LOGOUT
# ============================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("login")
    )


# ============================================================
# ROLE API
# ============================================================

@app.route(
    "/api/roles/<int:rid>"
)
def role_api(rid):

    connection = conn()

    role = connection.execute(
        """
        SELECT *
        FROM roles
        WHERE id = ?
        """,
        (rid,)
    ).fetchone()

    connection.close()

    if role:

        return jsonify(
            dict(role)
        )

    return jsonify({})


# ============================================================
# SIMPLE HEALTH CHECK
# ============================================================

@app.route("/health")
def health():

    return jsonify(
        {
            "status": "ok",
            "application": "AI Resume Skill Gap Analyzer"
        }
    )


# ============================================================
# START APPLICATION
# ============================================================

if __name__ == "__main__":

    init_db()

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )