# AI Resume Skill Gap Analyzer

Full working Flask portfolio demo.

## Features
- Resume upload: PDF, DOCX, TXT
- Keyword-based AI-style skill extraction
- 220+ job roles and 220+ company entries
- Historical/demo vacancy records (2022-2025)
- Target company + role skill-gap analysis
- Match percentage, matched/missing skills
- Alternative role/company recommendations
- Skill-priority roadmap
- Responsive dashboard

## Local run
```bash
python -m venv venv
# Windows: venv\\Scripts\\activate
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
python app.py
```
Open http://127.0.0.1:5000

## Data note
Company/role/vacancy records are synthetic historical/demo data for portfolio demonstration. They are NOT live vacancies and should not be represented as current openings.
