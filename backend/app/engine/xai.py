from typing import List, Dict, Any
from ..data.role_profiles import get_role_profile
from .skill_gap import analyze_all_skill_gaps
from .readiness import calculate_placement_readiness

def generate_xai_explanation(
    user_id: str,
    target_role: str,
    responses: List[Dict[str, Any]],
    user_priors: Dict[str, float] = None
) -> Dict[str, Any]:
    """
    Generates human-interpretable explanations and transparent reasoning
    for the student's Placement Readiness Score and AI Recommendations.
    """
    readiness_report = calculate_placement_readiness(user_id, target_role, responses, user_priors)
    role_info = get_role_profile(target_role)
    role_weights = role_info.get("weights", {})
    subtopic_diags = analyze_all_skill_gaps(responses, user_priors)
    
    score = readiness_report["overall_readiness_score"]
    tier = readiness_report["readiness_tier"]
    
    # 1. Identify main bottlenecks
    bottlenecks = []
    for diag in readiness_report["critical_skill_gaps"]:
        subtopic = diag["subtopic"]
        skill = diag["skill"]
        weight = role_weights.get(skill, 0.1)
        mastery = diag["mastery_score"]
        attempts = diag["attempts"]
        accuracy = diag["accuracy"]
        latency = diag["avg_latency_sec"]
        
        # Diagnostic reason
        if attempts == 0:
            reason = f"Unassessed domain. Defaults to baseline prior ({mastery}%)."
        elif accuracy < 50.0 and latency > 50.0:
            reason = f"Low accuracy ({accuracy}%) coupled with high latency ({latency}s) — indicates conceptual hesitation."
        elif accuracy < 50.0 and latency < 20.0:
            reason = f"Low accuracy ({accuracy}%) with rapid response ({latency}s) — indicates careless rushing or blind guessing."
        else:
            reason = f"Accuracy of {accuracy}% across {attempts} attempts falls below the proficiency threshold (70%)."
            
        bottlenecks.append({
            "subtopic": subtopic,
            "skill": skill,
            "mastery_score": mastery,
            "role_weight_pct": round(weight * 100, 1),
            "reason": reason,
            "impact_level": "HIGH" if weight >= 0.20 else "MEDIUM"
        })
        
    # 2. Identify positive drivers
    positive_drivers = []
    for diag in readiness_report["top_strengths"]:
        subtopic = diag["subtopic"]
        skill = diag["skill"]
        weight = role_weights.get(skill, 0.1)
        mastery = diag["mastery_score"]
        
        positive_drivers.append({
            "subtopic": subtopic,
            "skill": skill,
            "mastery_score": mastery,
            "role_weight_pct": round(weight * 100, 1),
            "reason": f"High consistency ({mastery}% mastery) with solid accuracy."
        })
        
    # 3. Role Weight Impact Analysis
    role_weight_impact = []
    for skill_name, wt in role_weights.items():
        role_weight_impact.append({
            "skill": skill_name,
            "weight_pct": round(wt * 100, 1),
            "significance": "Crucial Filter" if wt >= 0.25 else ("Core Competency" if wt >= 0.15 else "Supporting Requirement")
        })
        
    # 4. Immediate Recommended Action
    if bottlenecks:
        top_weakness = bottlenecks[0]
        rec_action = {
            "focus_topic": top_weakness["subtopic"],
            "skill_area": top_weakness["skill"],
            "suggested_questions_count": 5,
            "target_difficulty": "Medium (Difficulty 2-3)",
            "action_statement": f"Practice {top_weakness['subtopic']} → 5 questions → medium difficulty to raise your role score by estimated +4.5%."
        }
    else:
        rec_action = {
            "focus_topic": "Full Length Mock & Speed Drills",
            "skill_area": "Comprehensive",
            "suggested_questions_count": 15,
            "target_difficulty": "Advanced (Difficulty 4-5)",
            "action_statement": "Take a timed full-length placement mock assessment to maintain high consistency."
        }
        
    # 5. Diagnostic Reasoning Tree
    reasoning_tree = [
        {
            "step": "1. Performance Ingestion",
            "observation": f"Aggregated {len(responses)} question responses across {len(subtopic_diags)} unique technical subtopics."
        },
        {
            "step": "2. Subtopic Skill-Gap Detection",
            "observation": f"Detected {len(bottlenecks)} high-priority skill gaps and {len(positive_drivers)} strength areas."
        },
        {
            "step": f"3. Role Calibration ({role_info['title']})",
            "observation": f"Applied career role weighting matrix (Primary weight on {max(role_weights, key=role_weights.get)}: {int(max(role_weights.values())*100)}%)."
        },
        {
            "step": "4. Placement Readiness Index Computation",
            "observation": f"Computed Placement Readiness Score of {score}% ({tier})."
        },
        {
            "step": "5. Adaptive Optimization Loop",
            "observation": f"Recommended dynamic remedial path prioritizing {rec_action['focus_topic']} to maximize placement readiness gain."
        }
    ]
    
    # Executive summary
    exec_summary = (
        f"Your current Placement Readiness Score for {role_info['title']} is {score}% ({tier}). "
    )
    if bottlenecks:
        exec_summary += (
            f"The primary readiness bottlenecks are {bottlenecks[0]['subtopic']} "
            f"and {bottlenecks[1]['subtopic'] if len(bottlenecks) > 1 else 'foundational concepts'}. "
            f"Targeted remediation in these areas will yield the highest readiness gain."
        )
    else:
        exec_summary += "You have demonstrated strong performance across all core skills for this role."
        
    return {
        "readiness_score": score,
        "target_role": target_role,
        "executive_summary": exec_summary,
        "main_bottlenecks": bottlenecks,
        "positive_drivers": positive_drivers,
        "role_weight_impact": role_weight_impact,
        "recommended_immediate_action": rec_action,
        "diagnostic_reasoning_tree": reasoning_tree
    }
