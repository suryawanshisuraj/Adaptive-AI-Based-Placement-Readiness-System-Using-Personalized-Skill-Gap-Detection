import math
from typing import List, Dict, Any, Tuple
from ..data.question_bank import get_all_questions

def calculate_response_time_factor(actual_time: float, expected_time: float, is_correct: bool) -> float:
    """
    Evaluates response efficiency:
    - If correct and within normal time (0.5x to 1.5x expected), multiplier ~ 1.05 to 1.15
    - If correct but took excessively long (>2.0x expected), slight hesitation penalty
    - If incorrect and ultra fast (<0.25x expected), rapid guessing penalty
    """
    if expected_time <= 0:
        expected_time = 45.0
    
    ratio = actual_time / expected_time
    
    if is_correct:
        if ratio <= 0.8:
            return 1.10 # Fluent mastery
        elif ratio <= 1.5:
            return 1.00 # Standard competent pace
        else:
            return 0.85 # Slow hesitation (knows concept but lacks problem-solving speed)
    else:
        if ratio < 0.3:
            return 0.60 # Careless / guessing behavior
        else:
            return 0.75 # Genuine conceptual difficulty

def compute_subtopic_mastery(
    responses: List[Dict[str, Any]],
    subtopic: str,
    prior_mastery: float = 50.0
) -> Dict[str, Any]:
    """
    Computes fine-grained mastery for a given subtopic using Bayesian / weighted multi-factor logic.
    """
    sub_responses = [r for r in responses if r.get("subtopic", "").lower() == subtopic.lower()]
    
    if not sub_responses:
        return {
            "subtopic": subtopic,
            "mastery_score": prior_mastery,
            "attempts": 0,
            "correct_count": 0,
            "accuracy": 0.0,
            "avg_latency_sec": 0.0,
            "status": "Unassessed",
            "gap_severity": max(0.0, (100.0 - prior_mastery) / 100.0)
        }
    
    attempts = len(sub_responses)
    correct_count = sum(1 for r in sub_responses if r.get("is_correct") in (1, True))
    raw_accuracy = (correct_count / attempts) * 100.0
    
    total_latency = sum(r.get("response_time_sec", 45.0) for r in sub_responses)
    avg_latency = total_latency / attempts
    
    # Difficulty and time weighted accumulation
    weighted_score = 0.0
    total_weight = 0.0
    
    for r in sub_responses:
        diff = r.get("difficulty", 2)
        diff_weight = 1.0 + (diff - 1) * 0.25 # Diff 1: 1.0, Diff 5: 2.0
        exp_time = r.get("expected_time_sec", 45)
        act_time = r.get("response_time_sec", 45)
        is_corr = bool(r.get("is_correct"))
        
        time_factor = calculate_response_time_factor(act_time, exp_time, is_corr)
        
        score_point = (100.0 if is_corr else 10.0) * time_factor * (diff / 3.0)
        weighted_score += score_point * diff_weight
        total_weight += diff_weight
        
    calculated_mastery = weighted_score / max(1.0, total_weight)
    
    # Smooth with prior mastery (exponential decay / Bayesian update)
    alpha = min(1.0, attempts * 0.3)
    final_mastery = (alpha * calculated_mastery) + ((1.0 - alpha) * prior_mastery)
    final_mastery = max(5.0, min(100.0, round(final_mastery, 1)))
    
    # Determine gap severity & status
    gap_severity = max(0.0, min(1.0, (100.0 - final_mastery) / 100.0))
    
    if final_mastery < 50.0:
        status = "Critical Gap"
    elif final_mastery < 70.0:
        status = "Needs Improvement"
    elif final_mastery < 85.0:
        status = "Proficient"
    else:
        status = "Mastered"
        
    return {
        "subtopic": subtopic,
        "mastery_score": final_mastery,
        "attempts": attempts,
        "correct_count": correct_count,
        "accuracy": round(raw_accuracy, 1),
        "avg_latency_sec": round(avg_latency, 1),
        "status": status,
        "gap_severity": round(gap_severity, 2)
    }

def analyze_all_skill_gaps(
    responses: List[Dict[str, Any]],
    user_priors: Dict[str, float] = None
) -> Dict[str, Dict[str, Any]]:
    """
    Returns diagnostic analysis for all unique subtopics in the system.
    """
    if user_priors is None:
        user_priors = {}
        
    all_questions = get_all_questions()
    subtopic_to_meta: Dict[str, Dict[str, str]] = {}
    for q in all_questions:
        subtopic_to_meta[q["subtopic"]] = {
            "skill": q["skill"],
            "topic": q["topic"]
        }
        
    results = {}
    for subtopic, meta in subtopic_to_meta.items():
        prior = user_priors.get(subtopic, user_priors.get(meta["skill"], 50.0))
        diag = compute_subtopic_mastery(responses, subtopic, prior)
        diag["skill"] = meta["skill"]
        diag["topic"] = meta["topic"]
        results[subtopic] = diag
        
    return results

