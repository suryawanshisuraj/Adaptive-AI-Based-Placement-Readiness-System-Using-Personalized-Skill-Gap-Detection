const API_BASE = window.location.origin;

const API = {
  async getRoles() {
    const res = await fetch(`${API_BASE}/api/profile/roles`);
    return await res.json();
  },

  async getUserProfile(userId) {
    const res = await fetch(`${API_BASE}/api/profile/${userId}`);
    return await res.json();
  },

  async updateTargetRole(userId, targetRole) {
    const res = await fetch(`${API_BASE}/api/profile/${userId}/target-role`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ target_role: targetRole })
    });
    return await res.json();
  },

  async seedDemoData(userId) {
    const res = await fetch(`${API_BASE}/api/analytics/seed-demo-data/${userId}`, {
      method: "POST"
    });
    return await res.json();
  },

  async getReadinessReport(userId, targetRole = null) {
    const url = targetRole 
      ? `${API_BASE}/api/analytics/readiness/${userId}?target_role=${targetRole}`
      : `${API_BASE}/api/analytics/readiness/${userId}`;
    const res = await fetch(url);
    return await res.json();
  },

  async getXAIExplanation(userId, targetRole = null) {
    const url = targetRole 
      ? `${API_BASE}/api/analytics/xai/${userId}?target_role=${targetRole}`
      : `${API_BASE}/api/analytics/xai/${userId}`;
    const res = await fetch(url);
    return await res.json();
  },

  async getSkillGaps(userId) {
    const res = await fetch(`${API_BASE}/api/analytics/skill-gaps/${userId}`);
    return await res.json();
  },

  async getRoleComparison(userId) {
    const res = await fetch(`${API_BASE}/api/analytics/role-comparison/${userId}`);
    return await res.json();
  },

  async startAssessment(userId, sessionType = "diagnostic", numQuestions = 10, targetRole = null) {
    const res = await fetch(`${API_BASE}/api/assessment/start`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_id: userId,
        session_type: sessionType,
        num_questions: numQuestions,
        target_role: targetRole
      })
    });
    return await res.json();
  },

  async submitAnswer(sessionId, userId, questionId, selectedIndex, responseTimeSec) {
    const res = await fetch(`${API_BASE}/api/assessment/submit`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        session_id: sessionId,
        user_id: userId,
        question_id: questionId,
        selected_index: selectedIndex,
        response_time_sec: responseTimeSec
      })
    });
    return await res.json();
  },

  async getSessionSummary(sessionId) {
    const res = await fetch(`${API_BASE}/api/assessment/session/${sessionId}/summary`);
    return await res.json();
  },

  async getRoadmap(userId) {
    const res = await fetch(`${API_BASE}/api/roadmap/generate/${userId}`);
    return await res.json();
  },

  async toggleRoadmapStep(stepId) {
    const res = await fetch(`${API_BASE}/api/roadmap/step/${stepId}/toggle-complete`, {
      method: "POST"
    });
    return await res.json();
  },

  async getResourceDetails(subtopic) {
    const res = await fetch(`${API_BASE}/api/roadmap/resource/${encodeURIComponent(subtopic)}`);
    return await res.json();
  },

  async runResearchExperiment(sampleSize = 50, targetRole = "java_developer", learningDays = 14) {
    const res = await fetch(`${API_BASE}/api/research/simulate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        sample_size_per_group: sampleSize,
        target_role: targetRole,
        learning_days: learningDays
      })
    });
    return await res.json();
  },

  async getInterviewQuestions(roleId) {
    const res = await fetch(`${API_BASE}/api/interview/questions/${roleId}`);
    return await res.json();
  },

  async evaluateInterviewResponse(userId, questionId, candidateAnswer) {
    const res = await fetch(`${API_BASE}/api/interview/evaluate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_id: userId,
        question_id: questionId,
        candidate_answer: candidateAnswer
      })
    });
    return await res.json();
  },

  async analyzeResume(userId, targetRole, resumeText) {
    const res = await fetch(`${API_BASE}/api/resume/analyze`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_id: userId,
        target_role: targetRole,
        resume_text: resumeText
      })
    });
    return await res.json();
  }
};
