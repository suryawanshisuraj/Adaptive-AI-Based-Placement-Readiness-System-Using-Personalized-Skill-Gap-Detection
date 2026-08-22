from fastapi import APIRouter
from ..schemas import RunExperimentRequest, ExperimentResultResponse
from ..engine.research_experiment import run_ab_experiment_simulation

router = APIRouter(prefix="/api/research", tags=["Research Lab"])

@router.post("/simulate", response_model=ExperimentResultResponse)
def simulate_research_experiment(payload: RunExperimentRequest):
    results = run_ab_experiment_simulation(
        sample_size_per_group=payload.sample_size_per_group,
        target_role=payload.target_role,
        learning_days=payload.learning_days,
        noise_factor=payload.noise_factor
    )
    return results

@router.get("/quick-summary")
def get_quick_research_summary():
    results = run_ab_experiment_simulation(
        sample_size_per_group=60,
        target_role="java_developer",
        learning_days=14
    )
    return results
