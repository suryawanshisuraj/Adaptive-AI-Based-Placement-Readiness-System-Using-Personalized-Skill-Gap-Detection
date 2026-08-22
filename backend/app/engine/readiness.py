from typing import List, Dict, Any
from ..data.role_profiles import get_role_profile
from .skill_gap import analyze_all_skill_gaps

def calculate_placement_readiness(
    user_id: str,
    target_role: str,
    responses: List[Dict[str, Any]],
    user_priors: Dict[str, float] = None
) -> Dict[str, Any]:
    """
    Computes weighted Placement Readiness based on target job role,
    consistency, and granular subtopic skill gaps.
    """
    role_info = get_role_profile(target_role)
    role_weights: Dict[str, float] = role_info.get("weights", {})
    subtopic_diagnostics = analyze_all_skill_gaps(responses, user_priors)
    
    # 1. Group subtopics into high-level skills
    skill_scores: Dict[str, List[float]] = {}
    skill_subtopics: Dict[str, List[Dict[str, Any]]] = {}
    
    for subtopic, diag in subtopic_diagnostics.items():
        skill = diag["skill"]
        if skill not in skill_scores:
            skill_scores[skill] = []
            skill_subtopics[skill] = []
        skill_scores[skill].append(diag["mastery_score"])
        skill_subtopics[skill].append(diag)
        
    skill_breakdown = []
    weighted_sum = 0.0
    total_active_weight = 0.0
    
    for skill, weight in role_weights.items():
        scores = skill_scores.get(skill, [50.0]) # Default 50 if unassessed
        avg_score = sum(scores) / len(scores) if scores else 50.0
        
        weak_subs = [
            s["subtopic"] for s in skill_subtopics.get(skill, [])
            if s["mastery_score"] < 65.0
        ]
        
        skill_breakdown.append({
            "skill": skill,
            "score": round(avg_score, 1),
            "weight_in_role": weight,
            "subtopics_count": len(scores),
            "weak_subtopics": weak_subs
        })
        
        weighted_sum += avg_score * weight
        total_active_weight += weight
        
    base_readiness = weighted_sum / max(0.01, total_active_weight)
    
    # 2. Consistency & Confidence Calculation
    total_attempts = len(responses)
    if total_attempts >= 20:
        confidence = 0.95
    elif total_attempts >= 10:
        confidence = 0.85
    elif total_attempts >= 5:
        confidence = 0.70
    else:
        confidence = 0.50
        
    # Variance penalty on assessed critical subtopics
    critical_subtopics = role_info.get("critical_subtopics", [])
    critical_scores = [
        subtopic_diagnostics[s]["mastery_score"]
        for s in critical_subtopics
        if s in subtopic_diagnostics and subtopic_diagnostics[s]["attempts"] > 0
    ]
    
    if critical_scores and len(critical_scores) > 1:
        mean_c = sum(critical_scores) / len(critical_scores)
        var_c = sum((x - mean_c) ** 2 for x in critical_scores) / len(critical_scores)
        std_c = var_c ** 0.5
        # Higher variation between critical topics slightly dampens placement confidence
        consistency_multiplier = max(0.88, 1.0 - (std_c / 250.0))
    else:
        consistency_multiplier = 0.95
        
    final_readiness_score = round(base_readiness * consistency_multiplier, 1)
    final_readiness_score = max(5.0, min(100.0, final_readiness_score))
    
    # 3. Determine Readiness Tier
    if final_readiness_score >= 80.0:
        tier = "Placement Ready (Tier 1)"
        role_alignment_summary = f"Strong profile alignment with {role_info['title']}. Candidate demonstrates solid command over core weighted skills."
    elif final_readiness_score >= 65.0:
        tier = "Nearly Ready (Targeted Polish)"
        role_alignment_summary = f"Good baseline for {role_info['title']}. Minor remediation required in targeted weak subtopics."
    elif final_readiness_score >= 50.0:
        tier = "Moderate Readiness (In Progress)"
        role_alignment_summary = f"Emerging readiness for {role_info['title']}. Foundational gaps in critical role requirements must be addressed."
    else:
        tier = "Needs Foundational Preparation"
        role_alignment_summary = f"Significant skill gaps detected for {role_info['title']}. Systematic daily roadmap execution recommended."
        
    # 4. Critical Gaps & Top Strengths
    all_diags = list(subtopic_diagnostics.values())
    sorted_by_gap = sorted(all_diags, key=lambda x: x["mastery_score"])
    
    critical_gaps = [d for d in sorted_by_gap if d["mastery_score"] < 65.0][:5]
    top_strengths = [d for d in reversed(sorted_by_gap) if d["mastery_score"] >= 70.0][:5]
    
    return {
        "user_id": user_id,
        "target_role": target_role,
        "target_role_title": role_info["title"],
        "overall_readiness_score": final_readiness_score,
        "readiness_tier": tier,
        "consistency_multiplier": round(consistency_multiplier, 3),
        "confidence_level": confidence,
        "skill_breakdown": skill_breakdown,
        "critical_skill_gaps": critical_gaps,
        "top_strengths": top_strengths,
        "role_alignment_summary": role_alignment_summary
    }
