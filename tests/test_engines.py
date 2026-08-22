import pytest
from backend.app.engine.skill_gap import compute_subtopic_mastery, calculate_response_time_factor, analyze_all_skill_gaps
from backend.app.engine.readiness import calculate_placement_readiness
from backend.app.engine.recommender import select_next_adaptive_question, generate_personalized_roadmap
from backend.app.engine.xai import generate_xai_explanation
from backend.app.engine.research_experiment import run_ab_experiment_simulation

def test_response_time_factor():
    # Correct and fast
    f_fast_correct = calculate_response_time_factor(20.0, 45.0, True)
    assert f_fast_correct > 1.0
    
    # Correct but very slow
    f_slow_correct = calculate_response_time_factor(110.0, 45.0, True)
    assert f_slow_correct < 1.0
    
    # Incorrect and rushed (blind guess)
    f_guess_incorrect = calculate_response_time_factor(8.0, 45.0, False)
    assert f_guess_incorrect <= 0.60

def test_subtopic_mastery_calculation():
    # Simulated responses for SQL JOINs: 1 correct, 2 incorrect
    responses = [
        {"subtopic": "SQL JOINs", "is_correct": 0, "response_time_sec": 55.0, "difficulty": 2, "expected_time_sec": 40},
        {"subtopic": "SQL JOINs", "is_correct": 0, "response_time_sec": 60.0, "difficulty": 3, "expected_time_sec": 50},
        {"subtopic": "SQL JOINs", "is_correct": 1, "response_time_sec": 42.0, "difficulty": 2, "expected_time_sec": 40}
    ]
    diag = compute_subtopic_mastery(responses, "SQL JOINs", prior_mastery=50.0)
    assert diag["attempts"] == 3
    assert diag["correct_count"] == 1
    assert diag["accuracy"] == 33.3
    assert diag["status"] in ["Critical Gap", "Needs Improvement"]
    assert diag["gap_severity"] > 0.3

def test_placement_readiness_role_differentiation():
    """
    Candidate with high Java/OOP but low SQL/DBMS should score higher
    in Java Developer role than in Data Analyst role.
    """
    responses = [
        # Strong in Java / OOP
        {"subtopic": "Collections Framework", "is_correct": 1, "response_time_sec": 25.0, "difficulty": 3, "expected_time_sec": 35},
        {"subtopic": "Multithreading & Concurrency", "is_correct": 1, "response_time_sec": 30.0, "difficulty": 4, "expected_time_sec": 45},
        {"subtopic": "OOP Polymorphism", "is_correct": 1, "response_time_sec": 20.0, "difficulty": 2, "expected_time_sec": 30},
        # Weak in SQL / DBMS
        {"subtopic": "SQL JOINs", "is_correct": 0, "response_time_sec": 60.0, "difficulty": 2, "expected_time_sec": 40},
        {"subtopic": "SQL Subqueries", "is_correct": 0, "response_time_sec": 55.0, "difficulty": 3, "expected_time_sec": 45},
        {"subtopic": "Normalization", "is_correct": 0, "response_time_sec": 50.0, "difficulty": 3, "expected_time_sec": 40}
    ]
    
    java_report = calculate_placement_readiness("test_user", "java_developer", responses)
    data_report = calculate_placement_readiness("test_user", "data_analyst", responses)
    
    # Java Dev weights Java/OOP much higher (50% combined) than SQL (15%)
    # Data Analyst weights SQL/DBMS much higher (55% combined) than Java/OOP (10%)
    assert java_report["overall_readiness_score"] > data_report["overall_readiness_score"]
    assert "critical_skill_gaps" in java_report
    assert len(java_report["skill_breakdown"]) > 0

def test_adaptive_recommender():
    responses = [
        {"subtopic": "SQL JOINs", "is_correct": 0, "response_time_sec": 65.0, "difficulty": 2, "expected_time_sec": 40},
        {"subtopic": "Collections Framework", "is_correct": 1, "response_time_sec": 22.0, "difficulty": 3, "expected_time_sec": 35}
    ]
    next_q = select_next_adaptive_question("java_developer", responses)
    assert next_q is not None
    assert "id" in next_q
    assert "question_text" in next_q

def test_dynamic_roadmap_generation():
    responses = [
        {"subtopic": "SQL JOINs", "is_correct": 0, "response_time_sec": 65.0, "difficulty": 2, "expected_time_sec": 40},
        {"subtopic": "Recursion", "is_correct": 0, "response_time_sec": 55.0, "difficulty": 3, "expected_time_sec": 45},
        {"subtopic": "Normalization", "is_correct": 0, "response_time_sec": 50.0, "difficulty": 3, "expected_time_sec": 40}
    ]
    roadmap = generate_personalized_roadmap("test_user", "java_developer", responses)
    assert len(roadmap) == 5
    assert roadmap[0]["day_number"] == 1
    # Day 1 should target top weak subtopic
    assert "Remediation" in roadmap[0]["action_title"]

def test_xai_explanation():
    responses = [
        {"subtopic": "SQL JOINs", "is_correct": 0, "response_time_sec": 65.0, "difficulty": 2, "expected_time_sec": 40},
        {"subtopic": "Collections Framework", "is_correct": 1, "response_time_sec": 22.0, "difficulty": 3, "expected_time_sec": 35}
    ]
    xai = generate_xai_explanation("test_user", "java_developer", responses)
    assert "executive_summary" in xai
    assert "main_bottlenecks" in xai
    assert "recommended_immediate_action" in xai
    assert "diagnostic_reasoning_tree" in xai
    assert len(xai["diagnostic_reasoning_tree"]) == 5

def test_research_ab_simulation():
    res = run_ab_experiment_simulation(sample_size_per_group=40, target_role="java_developer", learning_days=14)
    assert "group_a_fixed" in res
    assert "group_b_adaptive" in res
    assert "statistics" in res
    
    stats = res["statistics"]
    assert stats["is_statistically_significant"] is True
    assert stats["p_value"] < 0.05
    assert stats["cohens_d"] > 0.5
    assert stats["time_efficiency_gain_pct"] > 0

def test_mock_interview_evaluator():
    from backend.app.engine.interview_engine import evaluate_interview_response
    sample_ans = (
        "In our Java backend project, we resolved a critical OutOfMemoryError in G1 GC heap regions. "
        "First, I analyzed the heap dump using Eclipse MAT to locate tenured memory leaks. "
        "Second, we refactored unindexed subqueries and optimized our database connection pool, reducing memory pressure by 40%."
    )
    eval_res = evaluate_interview_response("int_java_01", sample_ans)
    assert eval_res["overall_score"] >= 70.0
    assert len(eval_res["matched_keywords"]) > 0
    assert "readiness_boost" in eval_res

def test_resume_analyzer():
    from backend.app.engine.resume_analyzer import analyze_resume_text
    sample_resume = """
    Alex Rivera - Software Engineer
    Technical Skills: Java, Spring Boot, MySQL, Relational Database, SQL JOINs, Hibernate, Git, Multithreading, OOP, Arrays, Recursion.
    Experience: Built scalable REST APIs, optimized complex SQL subqueries, and resolved concurrency race conditions.
    """
    res_analysis = analyze_resume_text(sample_resume, "java_developer")
    assert res_analysis["role_match_percentage"] > 40.0
    assert res_analysis["total_skills_detected"] >= 5
    assert "Java" in res_analysis["detected_skills_breakdown"]

