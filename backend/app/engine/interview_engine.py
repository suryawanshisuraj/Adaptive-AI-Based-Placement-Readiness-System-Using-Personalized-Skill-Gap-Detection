from typing import List, Dict, Any

INTERVIEW_QUESTIONS: Dict[str, List[Dict[str, Any]]] = {
    "java_developer": [
        {
            "id": "int_java_01",
            "type": "Technical Core",
            "question": "How does Java's Garbage Collector (G1 GC) manage heap memory into regions, and how would you diagnose an OutOfMemoryError in production?",
            "keywords": ["heap", "g1", "regions", "eden", "tenured", "humongous", "heap dump", "jcmd", "profiler"],
            "ideal_points": [
                "G1 GC partitions heap into equal-sized virtual memory regions rather than contiguous generations.",
                "Uses concurrent marking and mixed collection cycles prioritizing regions with highest garbage density.",
                "Diagnose OOM by enabling -XX:+HeapDumpOnOutOfMemoryError and analyzing dumps using Eclipse MAT or VisualVM to find memory leaks."
            ]
        },
        {
            "id": "int_java_02",
            "type": "System & DB",
            "question": "Explain how you would optimize a slow relational SQL query involving multiple JOINs and subqueries in an enterprise backend.",
            "keywords": ["explain", "indexes", "b-tree", "composite index", "subqueries", "joins", "n+1"],
            "ideal_points": [
                "Run EXPLAIN ANALYZE to inspect query plan (sequential scans vs index scans).",
                "Create appropriate B-Tree or composite indexes on foreign keys and WHERE filters.",
                "Convert unindexed correlated subqueries into INNER/LEFT JOINs or Common Table Expressions (CTEs)."
            ]
        },
        {
            "id": "int_java_03",
            "type": "Behavioral / STAR",
            "question": "Tell me about a challenging technical bug or performance bottleneck you resolved in a software project. Use the STAR method.",
            "keywords": ["situation", "task", "action", "result", "metrics", "debugging", "team"],
            "ideal_points": [
                "Clear Situation & Task framing.",
                "Detailed technical Action taken (profiling, testing hypotheses, code refactoring).",
                "Quantified Result (e.g., reduced latency by 45%, zero downtime)."
            ]
        }
    ],
    "data_analyst": [
        {
            "id": "int_data_01",
            "type": "Technical SQL",
            "question": "What is the difference between Window Functions (such as ROW_NUMBER, RANK, DENSE_RANK) and GROUP BY in SQL, and when would you use PARTITION BY?",
            "keywords": ["window", "row_number", "rank", "dense_rank", "group by", "partition by", "aggregation"],
            "ideal_points": [
                "GROUP BY aggregates rows and collapses them into a single summary row per group.",
                "Window functions perform calculations across a set of rows while retaining individual row identities.",
                "PARTITION BY divides the result set into partitions to apply the window function independently."
            ]
        },
        {
            "id": "int_data_02",
            "type": "Business Analytics",
            "question": "Suppose our user churn rate increased by 15% last month. How would you structure your data investigation to uncover the root cause?",
            "keywords": ["segmentation", "cohorts", "funnel", "correlation", "product release", "a/b test", "anomaly"],
            "ideal_points": [
                "Segment data by user cohorts (new vs returning, geography, device type, acquisition channel).",
                "Analyze user activity funnels to identify where drop-offs spiked.",
                "Cross-reference churn date against product deployments, pricing changes, or server outages."
            ]
        }
    ],
    "fullstack_developer": [
        {
            "id": "int_fs_01",
            "type": "Architecture",
            "question": "How do you handle state management, API caching, and optimistic UI updates in a modern web application?",
            "keywords": ["state", "caching", "optimistic", "rest", "graphql", "jwt", "latency"],
            "ideal_points": [
                "Single source of truth for application state with localized component caching.",
                "Optimistic UI updates immediately render expected result, then roll back gracefully if backend rejects.",
                "Cache invalidation strategies (ETags, Stale-While-Revalidate)."
            ]
        }
    ]
}

def get_interview_questions_for_role(role_id: str) -> List[Dict[str, Any]]:
    return INTERVIEW_QUESTIONS.get(role_id, INTERVIEW_QUESTIONS["java_developer"])

def evaluate_interview_response(question_id: str, candidate_answer: str) -> Dict[str, Any]:
    """
    Evaluates candidate's written or spoken response based on keyword presence,
    technical depth, structural completeness, and clarity.
    """
    # Find question
    target_q = None
    for q_list in INTERVIEW_QUESTIONS.values():
        for q in q_list:
            if q["id"] == question_id:
                target_q = q
                break
        if target_q:
            break
            
    if not target_q:
        target_q = INTERVIEW_QUESTIONS["java_developer"][0]
        
    answer_lower = candidate_answer.lower()
    words = answer_lower.split()
    word_count = len(words)
    
    # 1. Keyword coverage
    keywords = target_q["keywords"]
    matched_keywords = [k for k in keywords if k.lower() in answer_lower]
    keyword_score = (len(matched_keywords) / max(1, len(keywords))) * 100.0
    
    # 2. Length & Depth Score
    if word_count < 15:
        length_score = 30.0
        depth_feedback = "Answer is too brief. Provide deeper technical explanation and examples."
    elif word_count < 40:
        length_score = 65.0
        depth_feedback = "Good foundation, but expand further on edge cases and practical resolution steps."
    elif word_count <= 250:
        length_score = 95.0
        depth_feedback = "Comprehensive and structured explanation with strong detail."
    else:
        length_score = 85.0
        depth_feedback = "Very thorough, though ensure answers remain concise during real interview time limits."
        
    # 3. Structural Rubric
    has_structure = any(token in answer_lower for token in ["first", "second", "because", "furthermore", "for example", "result", "in order to"])
    structure_score = 90.0 if has_structure else 70.0
    
    # Overall Composite Interview Score
    overall_score = round((0.45 * keyword_score) + (0.35 * length_score) + (0.20 * structure_score), 1)
    overall_score = max(10.0, min(100.0, overall_score))
    
    # Readiness impact calculation
    if overall_score >= 80.0:
        status = "Strong Hire / Excellent"
        readiness_boost = "+3.5%"
    elif overall_score >= 60.0:
        status = "Satisfactory / Clear Potential"
        readiness_boost = "+1.8%"
    else:
        status = "Needs Practice / Review Concepts"
        readiness_boost = "+0.5%"
        
    return {
        "question_id": question_id,
        "question_text": target_q["question"],
        "overall_score": overall_score,
        "status": status,
        "matched_keywords": matched_keywords,
        "missing_key_concepts": [k for k in keywords if k not in matched_keywords],
        "depth_feedback": depth_feedback,
        "readiness_boost": readiness_boost,
        "ideal_points": target_q["ideal_points"]
    }
