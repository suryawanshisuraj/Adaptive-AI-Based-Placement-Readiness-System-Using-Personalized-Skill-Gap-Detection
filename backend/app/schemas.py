from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

# User Schemas
class UserCreate(BaseModel):
    name: str
    email: str
    target_role: str = "java_developer"

class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    target_role: str
    created_at: Optional[str] = None

class TargetRoleUpdate(BaseModel):
    target_role: str

# Question Schemas
class QuestionSchema(BaseModel):
    id: str
    skill: str
    topic: str
    subtopic: str
    difficulty: int
    question_text: str
    options: List[str]
    correct_index: int
    explanation: str
    expected_time_sec: int = 45
    code_snippet: Optional[str] = None
    tags: List[str] = []

class QuestionClientView(BaseModel):
    id: str
    skill: str
    topic: str
    subtopic: str
    difficulty: int
    question_text: str
    options: List[str]
    expected_time_sec: int
    code_snippet: Optional[str] = None
    tags: List[str] = []

# Assessment Session Schemas
class StartAssessmentRequest(BaseModel):
    user_id: str
    session_type: str = "diagnostic" # 'diagnostic', 'adaptive_practice', 'reassessment'
    target_role: Optional[str] = None
    topic_filter: Optional[str] = None
    num_questions: int = 15

class AnswerSubmissionRequest(BaseModel):
    session_id: str
    user_id: str
    question_id: str
    selected_index: int
    response_time_sec: float

class AnswerEvaluationResponse(BaseModel):
    is_correct: bool
    correct_index: int
    explanation: str
    updated_subtopic_mastery: float
    feedback: str
    next_recommended_difficulty: int
    next_question: Optional[QuestionClientView] = None

# Analytics & Skill-Gap Schemas
class SubtopicMasteryDetail(BaseModel):
    subtopic: str
    topic: str
    skill: str
    mastery_score: float # 0 to 100
    attempts: int
    accuracy: float
    avg_latency_sec: float
    status: str # 'Critical Gap', 'Needs Improvement', 'Proficient', 'Mastered'
    gap_severity: float # 0 (no gap) to 1.0 (severe gap)

class SkillCategoryMastery(BaseModel):
    skill: str
    score: float # 0 to 100
    weight_in_role: float # 0 to 1
    subtopics_count: int
    weak_subtopics: List[str]

class PlacementReadinessReport(BaseModel):
    user_id: str
    target_role: str
    target_role_title: str
    overall_readiness_score: float # 0 to 100
    readiness_tier: str # 'Placement Ready (Top Tier)', 'Nearly Ready (Targeted Polish)', 'Moderate Readiness', 'Needs Foundational Preparation'
    consistency_multiplier: float
    confidence_level: float
    skill_breakdown: List[SkillCategoryMastery]
    critical_skill_gaps: List[SubtopicMasteryDetail]
    top_strengths: List[SubtopicMasteryDetail]
    role_alignment_summary: str

# Explainable AI Schemas
class XAIExplanation(BaseModel):
    readiness_score: float
    target_role: str
    executive_summary: str
    main_bottlenecks: List[Dict[str, Any]]
    positive_drivers: List[Dict[str, Any]]
    role_weight_impact: List[Dict[str, Any]]
    recommended_immediate_action: Dict[str, Any]
    diagnostic_reasoning_tree: List[Dict[str, Any]]

# Learning Roadmap Schemas
class RoadmapStepSchema(BaseModel):
    id: str
    day_number: int
    skill: str
    topic: str
    subtopic: str
    action_title: str
    explanation_summary: str
    target_questions_count: int
    is_completed: bool
    score_achieved: Optional[float] = None
    recommended_resources: List[Dict[str, str]] = []

class LearningRoadmapResponse(BaseModel):
    roadmap_id: str
    user_id: str
    target_role: str
    generated_at: str
    steps: List[RoadmapStepSchema]
    completion_percentage: float

# Research Experiment Schemas
class RunExperimentRequest(BaseModel):
    sample_size_per_group: int = 50
    target_role: str = "java_developer"
    learning_days: int = 14
    noise_factor: float = 0.15

class CohortMetrics(BaseModel):
    group_name: str
    group_type: str
    sample_size: int
    pre_test_mean: float
    pre_test_std: float
    post_test_mean: float
    post_test_std: float
    mean_improvement_pct: float
    avg_time_spent_hours: float
    avg_questions_attempted: int
    weak_topic_resolution_rate_pct: float
    readiness_gain_mean: float

class StatisticalComparison(BaseModel):
    t_statistic: float
    p_value: float
    is_statistically_significant: bool
    cohens_d: float
    effect_size_interpretation: str # 'Large Effect (d > 0.8)', etc.
    time_efficiency_gain_pct: float
    weak_gap_recovery_ratio: float
    research_verdict: str

class ExperimentResultResponse(BaseModel):
    experiment_id: str
    target_role: str
    group_a_fixed: CohortMetrics
    group_b_adaptive: CohortMetrics
    statistics: StatisticalComparison
    distribution_data: Dict[str, List[float]] # For charting pre/post distributions
    trajectory_data: Dict[str, List[float]] # For day-by-day learning curve
