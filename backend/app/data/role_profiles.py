from typing import Dict, Any

ROLE_PROFILES: Dict[str, Dict[str, Any]] = {
    "java_developer": {
        "id": "java_developer",
        "title": "Java Backend Developer",
        "description": "Designs, builds, and optimizes enterprise Java backend services, microservices, and database interactions.",
        "icon": "☕",
        "weights": {
            "Java": 0.30,
            "OOP": 0.20,
            "Coding": 0.20,
            "SQL": 0.15,
            "DBMS": 0.08,
            "Aptitude": 0.07,
            "Communication": 0.05
        },
        "critical_subtopics": [
            "SQL JOINs", "SQL Subqueries", "OOP Polymorphism", "Collections Framework",
            "Multithreading", "Recursion", "Binary Trees", "Normalization (BCNF/3NF)"
        ],
        "readiness_threshold": 75.0
    },
    "data_analyst": {
        "id": "data_analyst",
        "title": "Data Analyst & BI Specialist",
        "description": "Analyzes complex datasets, builds automated SQL data pipelines, and translates business metrics into visual insights.",
        "icon": "📊",
        "weights": {
            "SQL": 0.35,
            "DBMS": 0.20,
            "Aptitude": 0.20,
            "Java": 0.05,
            "OOP": 0.05,
            "Coding": 0.10,
            "Communication": 0.05
        },
        "critical_subtopics": [
            "SQL Aggregations & Grouping", "SQL Window Functions", "SQL JOINs", "SQL Subqueries",
            "Relational Modeling", "Statistical Averages & Probability", "Normalization"
        ],
        "readiness_threshold": 70.0
    },
    "fullstack_developer": {
        "id": "fullstack_developer",
        "title": "Full-Stack Software Engineer",
        "description": "Builds robust end-to-end web architectures, REST APIs, and database schemas with strong algorithmic problem solving.",
        "icon": "⚡",
        "weights": {
            "Coding": 0.25,
            "Java": 0.20,
            "SQL": 0.20,
            "OOP": 0.15,
            "DBMS": 0.10,
            "Communication": 0.05,
            "Aptitude": 0.05
        },
        "critical_subtopics": [
            "Arrays & Strings", "Two Pointers & Sliding Window", "SQL Indexing & Optimization",
            "REST Architecture", "Inheritance & Interfaces", "ACID Transactions"
        ],
        "readiness_threshold": 78.0
    },
    "ml_engineer": {
        "id": "ml_engineer",
        "title": "Machine Learning Engineer",
        "description": "Develops predictive AI pipelines, statistical models, and efficient algorithmic data structures.",
        "icon": "🧠",
        "weights": {
            "Coding": 0.30,
            "Aptitude": 0.25,
            "SQL": 0.15,
            "OOP": 0.10,
            "Java": 0.10,
            "DBMS": 0.05,
            "Communication": 0.05
        },
        "critical_subtopics": [
            "Recursion & Dynamic Programming", "Probability & Combinatorics", "Time Complexity Optimization",
            "Matrix Operations", "SQL Aggregations"
        ],
        "readiness_threshold": 80.0
    },
    "devops_cloud_engineer": {
        "id": "devops_cloud_engineer",
        "title": "DevOps & Cloud Systems Engineer",
        "description": "Automates CI/CD pipelines, oversees infrastructure reliability, network topologies, and high availability systems.",
        "icon": "☁️",
        "weights": {
            "DBMS": 0.25,
            "SQL": 0.20,
            "Coding": 0.20,
            "Aptitude": 0.15,
            "Java": 0.10,
            "OOP": 0.05,
            "Communication": 0.05
        },
        "critical_subtopics": [
            "Concurrency & Locks", "Database Indexing", "Process Scheduling", "Subqueries", "Shell/Script Logic"
        ],
        "readiness_threshold": 72.0
    }
}

def get_role_profile(role_id: str) -> Dict[str, Any]:
    return ROLE_PROFILES.get(role_id, ROLE_PROFILES["java_developer"])

def get_all_roles() -> Dict[str, Dict[str, Any]]:
    return ROLE_PROFILES
