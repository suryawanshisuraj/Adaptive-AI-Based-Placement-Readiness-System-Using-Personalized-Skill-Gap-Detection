import re
from typing import Dict, Any, List
from ..data.role_profiles import get_role_profile

KNOWN_SKILLS_ONTOLOGY = {
    "Java": ["java", "jvm", "spring", "spring boot", "hibernate", "maven", "gradle", "jpa", "multithreading"],
    "OOP": ["oop", "object-oriented", "polymorphism", "inheritance", "encapsulation", "solid", "design patterns"],
    "SQL": ["sql", "mysql", "postgresql", "oracle", "joins", "subqueries", "indexing", "stored procedures", "window functions"],
    "DBMS": ["dbms", "database", "acid", "normalization", "nosql", "mongodb", "redis", "transactions", "concurrency"],
    "Coding": ["data structures", "algorithms", "dsa", "leetcode", "arrays", "trees", "graphs", "recursion", "dynamic programming", "python", "c++"],
    "Aptitude": ["quantitative aptitude", "statistics", "probability", "combinatorics", "linear algebra", "calculus"],
    "DevOps & Cloud": ["docker", "kubernetes", "aws", "gcp", "azure", "ci/cd", "linux", "git", "bash", "terraform"],
    "Communication": ["presentation", "leadership", "agile", "scrum", "teamwork", "technical documentation", "communication"]
}

def analyze_resume_text(resume_text: str, target_role: str) -> Dict[str, Any]:
    """
    Extracts skills, calculates role match percentage, and detects missing prerequisite keywords.
    """
    text_lower = resume_text.lower()
    
    # 1. Extract detected skills
    detected_skills_by_category: Dict[str, List[str]] = {}
    total_detected_count = 0
    
    for category, skill_keywords in KNOWN_SKILLS_ONTOLOGY.items():
        found = []
        for kw in skill_keywords:
            pattern = r'\b' + re.escape(kw) + r'\b'
            if re.search(pattern, text_lower):
                found.append(kw)
        if found:
            detected_skills_by_category[category] = found
            total_detected_count += len(found)
            
    # 2. Match against target role profile
    role_info = get_role_profile(target_role)
    critical_subtopics = role_info.get("critical_subtopics", [])
    
    # Check matching critical keywords
    matched_critical = []
    missing_critical = []
    
    for sub in critical_subtopics:
        # Extract main tokens (e.g. "SQL JOINs" -> "join", "Multithreading" -> "multithread")
        sub_tokens = [t.lower() for t in re.findall(r'\w+', sub) if len(t) > 2]
        is_matched = any(re.search(r'\b' + re.escape(token) + r'\b', text_lower) for token in sub_tokens)
        if is_matched:
            matched_critical.append(sub)
        else:
            missing_critical.append(sub)
            
    # Match percentage calculation
    match_pct = round((len(matched_critical) / max(1, len(critical_subtopics))) * 100.0, 1)
    
    # Word count and ATS score heuristic
    words = text_lower.split()
    word_count = len(words)
    ats_score = round(min(100.0, (match_pct * 0.6) + min(40.0, (total_detected_count * 3.5))), 1)
    
    # Recommendations
    recommendations = []
    if missing_critical:
        recommendations.append(f"Add projects and explicit keywords for critical missing competencies: {', '.join(missing_critical[:4])}.")
    if "git" not in text_lower and "github" not in text_lower:
        recommendations.append("Include links to your GitHub profile or version-controlled technical repositories.")
    if word_count < 100:
        recommendations.append("Resume description is concise. Elaborate on measurable impact using metrics and STAR action verbs.")
        
    return {
        "target_role": target_role,
        "target_role_title": role_info["title"],
        "ats_score": ats_score,
        "role_match_percentage": match_pct,
        "total_skills_detected": total_detected_count,
        "detected_skills_breakdown": detected_skills_by_category,
        "matched_critical_requirements": matched_critical,
        "missing_critical_gaps": missing_critical,
        "actionable_recommendations": recommendations
    }
