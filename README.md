# Adaptive AI-Based Placement Readiness System Using Personalized Skill-Gap Detection

An intelligent, research-grade web application and diagnostic AI platform designed to evaluate, diagnose, and accelerate student placement readiness through fine-grained skill-gap detection, role-parameterized scoring, explainable AI justifications, and dynamic learning path generation.

---

## 🎯 Core Research Innovation

Instead of generic quiz platforms that offer uniform question banks:
1. **Multi-Factor Skill-Gap Detection**: Evaluates accuracy, question difficulty weighting ($Diff_{norm}$), response time latency penalties (distinguishing rapid blind guesses from slow hesitation), and repeated error patterns.
2. **Role-Weighted Placement Readiness Model**: Computes an adaptive placement readiness score tailored to specific target job roles:
   $$\text{Readiness} = \left( \sum_{i} W_{\text{role}, i} \cdot S_i \right) \times C_{\text{consistency}}$$
3. **Explainable AI (XAI) Diagnostic Layer**: Formulates clear human-interpretable reasoning trees for why a student has a specific readiness score and provides direct recommendations.
4. **Dynamic 5-Day Remediation Roadmap**: Automatically sequences the candidate's highest impact gaps $(\text{Weight}_{\text{role}} \times \text{Gap}_{\text{subtopic}})$ into daily micro-lessons and drills.
5. **Research Lab & Empirical A/B Benchmarking**: Evaluates **Group A (Fixed Question Bank)** vs **Group B (Adaptive AI System)** calculating paired $t$-tests, $p$-values, Cohen's $d$ effect sizes, and time-efficiency gains.

---

## 🏗️ Architecture

```
Adaptive AI System/
├── backend/
│   └── app/
│       ├── main.py                     # FastAPI application & static mounting
│       ├── database.py                 # SQLite database & session management
│       ├── models.py / schemas.py      # Pydantic schemas & data models
│       ├── data/
│       │   ├── question_bank.py        # Question bank across Java, SQL, DSA, etc.
│       │   ├── role_profiles.py        # Role weights & target career specs
│       │   └── learning_resources.py   # Concept cheatsheets & pitfalls
│       ├── engine/
│       │   ├── skill_gap.py            # Granular Bayesian skill-gap detector
│       │   ├── readiness.py            # Job-role placement readiness index
│       │   ├── recommender.py          # Adaptive question & roadmap generator
│       │   ├── xai.py                  # Explainable AI diagnostic engine
│       │   └── research_experiment.py  # Statistical A/B testing simulator
│       └── api/                        # REST API Routers
├── frontend/
│   ├── index.html                      # Single Page Application
│   ├── css/style.css                   # Modern dark/light responsive styling
│   └── js/
│       ├── api.js                      # REST API client
│       ├── charts.js                   # Chart.js radar, dial, and comparisons
│       └── app.js                      # UI state & interactive quiz engine
├── tests/
│   └── test_engines.py                 # Pytest engine & statistical unit tests
└── run_server.py                       # One-click server launcher
```

---

## 🚀 Getting Started

### 1. Launch Server
Run the launcher script:
```bash
python run_server.py
```
Open your browser at **`http://127.0.0.1:8000`**.

### 2. Run Test Suite
Run automated unit tests:
```bash
python -m pytest tests/test_engines.py -v
```

---

## 📊 Viva Defense Highlights

- **Why is this novel?**
  Most systems average general scores. This system isolates exact subtopic gaps (e.g. *SQL JOINs* vs *Subqueries*), adjusts readiness by target job role weights, explains the root causes via Explainable AI, and provides empirical evidence of learning velocity improvements via Cohen's $d$ and statistical hypothesis testing.
