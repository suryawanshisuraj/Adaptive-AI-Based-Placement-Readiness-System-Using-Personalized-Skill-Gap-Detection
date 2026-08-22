import random
from typing import List, Dict, Any, Optional
from ..data.question_bank import get_all_questions, get_questions_by_subtopic, get_questions_by_skill
from ..data.role_profiles import get_role_profile
from ..data.learning_resources import get_resource_for_subtopic
from .skill_gap import analyze_all_skill_gaps

def select_next_adaptive_question(
    target_role: str,
    responses: List[Dict[str, Any]],
    user_priors: Dict[str, float] = None,
    exclude_question_ids: List[str] = None
) -> Optional[Dict[str, Any]]:
    """
    Selects the next optimal question according to:
    1. Highest Priority Subtopic: Role Weight * Subtopic Gap Severity
    2. Zone of Proximal Development (ZPD) Difficulty:
       - Low Mastery (<45%): Difficulty 1 or 2
       - Medium Mastery (45-75%): Difficulty 2 or 3
       - High Mastery (>75%): Difficulty 4 or 5
    """
    if exclude_question_ids is None:
        exclude_question_ids = []
        
    role_info = get_role_profile(target_role)
    role_weights = role_info.get("weights", {})
    subtopic_diags = analyze_all_skill_gaps(responses, user_priors)
    all_questions = get_all_questions()
    
    # Filter out already answered questions in current session
    candidate_questions = [q for q in all_questions if q["id"] not in exclude_question_ids]
    if not candidate_questions:
        # If all exhausted, allow re-practicing
        candidate_questions = all_questions
        
    # Calculate prioritization score for each subtopic
    subtopic_priorities: Dict[str, float] = {}
    for subtopic, diag in subtopic_diags.items():
        skill = diag["skill"]
        skill_wt = role_weights.get(skill, 0.1)
        gap = diag["gap_severity"] # 0.0 to 1.0
        
        # Priority formula: skill importance in role * gap severity + slight exploration bonus
        attempts = diag["attempts"]
        exploration_bonus = 0.2 / (1 + attempts)
        priority = (skill_wt * (gap + 0.1)) + exploration_bonus
        subtopic_priorities[subtopic] = priority
        
    # Sort subtopics by priority
    sorted_subtopics = sorted(subtopic_priorities.items(), key=lambda x: x[1], reverse=True)
    
    # Try finding question in top priority subtopics
    for target_subtopic, _ in sorted_subtopics:
        diag = subtopic_diags.get(target_subtopic, {})
        mastery = diag.get("mastery_score", 50.0)
        
        # Target difficulty based on ZPD
        if mastery < 45.0:
            target_diffs = [1, 2, 3]
        elif mastery < 75.0:
            target_diffs = [2, 3, 4]
        else:
            target_diffs = [3, 4, 5]
            
        matching_q = [
            q for q in candidate_questions
            if q["subtopic"].lower() == target_subtopic.lower() and q["difficulty"] in target_diffs
        ]
        
        if matching_q:
            return random.choice(matching_q)
            
        # Fallback to any difficulty in this subtopic
        matching_q_any = [
            q for q in candidate_questions
            if q["subtopic"].lower() == target_subtopic.lower()
        ]
        if matching_q_any:
            return random.choice(matching_q_any)
            
    # Fallback to random candidate
    return random.choice(candidate_questions) if candidate_questions else None

def generate_personalized_roadmap(
    user_id: str,
    target_role: str,
    responses: List[Dict[str, Any]],
    user_priors: Dict[str, float] = None
) -> List[Dict[str, Any]]:
    """
    Generates a 5-day adaptive learning path specifically targeting
    the candidate's identified weak subtopics for the selected role.
    """
    role_info = get_role_profile(target_role)
    role_weights = role_info.get("weights", {})
    subtopic_diags = analyze_all_skill_gaps(responses, user_priors)
    
    # Rank subtopics by (Role Weight * Gap Severity)
    ranked_gaps = []
    for subtopic, diag in subtopic_diags.items():
        skill = diag["skill"]
        wt = role_weights.get(skill, 0.1)
        severity = diag["gap_severity"]
        score = diag["mastery_score"]
        impact = wt * (100.0 - score)
        ranked_gaps.append((impact, subtopic, diag))
        
    ranked_gaps.sort(key=lambda x: x[0], reverse=True)
    
    roadmap_steps = []
    day = 1
    
    # Pick top weak subtopics
    for impact, subtopic, diag in ranked_gaps:
        if day > 5:
            break
            
        res = get_resource_for_subtopic(subtopic)
        skill = diag["skill"]
        topic = diag["topic"]
        
        action_title = f"Day {day}: Remediation on {subtopic}"
        summary = (
            f"Focus on {subtopic} (Current Mastery: {diag['mastery_score']}%). "
            f"Review key concepts on {topic} and solve 5 targeted adaptive questions."
        )
        
        roadmap_steps.append({
            "id": f"step_{day}_{subtopic.replace(' ', '_').lower()}",
            "day_number": day,
            "skill": skill,
            "topic": topic,
            "subtopic": subtopic,
            "action_title": action_title,
            "explanation_summary": summary,
            "target_questions_count": 5,
            "is_completed": False,
            "score_achieved": None,
            "recommended_resources": res.get("curated_links", [])
        })
        day += 1
        
    # If fewer than 5 weak topics detected, fill with mixed evaluation / consolidation
    while day <= 5:
        if day == 4:
            action_title = "Day 4: Mixed Assessment & Speed Drill"
            summary = "Practice mixed aptitude and core technical questions under strict placement time constraints."
            skill_name = "Mixed Technical"
            subtopic_name = "Speed Drill"
        else:
            action_title = "Day 5: Placement Readiness Recalculation Assessment"
            summary = "Comprehensive milestone assessment to recalculate placement readiness index and measure gap closure."
            skill_name = "Comprehensive"
            subtopic_name = "Milestone Re-assessment"
            
        roadmap_steps.append({
            "id": f"step_{day}_milestone",
            "day_number": day,
            "skill": skill_name,
            "topic": "Placement Readiness",
            "subtopic": subtopic_name,
            "action_title": action_title,
            "explanation_summary": summary,
            "target_questions_count": 10,
            "is_completed": False,
            "score_achieved": None,
            "recommended_resources": [
                {"title": "Full Length Placement Mock Guide", "url": "https://www.geeksforgeeks.org/"}
            ]
        })
        day += 1
        
    return roadmap_steps
