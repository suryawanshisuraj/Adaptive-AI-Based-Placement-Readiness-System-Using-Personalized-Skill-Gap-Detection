// ── Auth Guard ────────────────────────────────────────────────────────────────
// If no user is stored in localStorage, redirect to auth page
const _storedUserId = localStorage.getItem("placement_user_id");
if (!_storedUserId) {
  window.location.href = "/auth";
}

// Application State
const state = {
  currentUserId: _storedUserId || "usr_alex_rivera",

  currentRole: "java_developer",
  roles: {},
  activeTab: "tab-dashboard",
  
  // Assessment state
  activeSession: null,
  currentQuestion: null,
  selectedOptionIndex: null,
  timerInterval: null,
  secondsElapsed: 0,
  isAnswerSubmitted: false,
  sessionQuestionsCount: 0,
  
  // Cache
  readinessReport: null,
  xaiReport: null,
  roadmapData: null
};

// Initialize Application
document.addEventListener("DOMContentLoaded", async () => {
  setupEventListeners();
  await loadInitialData();
});

function updateUserInfoUI() {
  const userName = localStorage.getItem("placement_user_name") || "Student";
  const userEmail = localStorage.getItem("placement_user_email") || "";

  // Derive up to 2 uppercase initials
  const initials = userName
    .trim()
    .split(/\s+/)
    .filter(Boolean)
    .map(word => word[0])
    .slice(0, 2)
    .join("")
    .toUpperCase() || "ST";

  // Topbar user name
  const topbarNameEl = document.getElementById("topbarUserName");
  if (topbarNameEl) topbarNameEl.textContent = `👤 ${userName}`;

  // Sidebar user avatar, name, and account status/email
  const sidebarAvatar = document.getElementById("sidebarUserAvatar");
  if (sidebarAvatar) sidebarAvatar.textContent = initials;
  
  const sidebarName = document.getElementById("sidebarUserName");
  if (sidebarName) sidebarName.textContent = userName;

  const sidebarRole = document.getElementById("sidebarUserRole");
  if (sidebarRole) {
    sidebarRole.textContent = userEmail ? userEmail.split("@")[0] : "Active Candidate";
    sidebarRole.title = userEmail ? `Logged in as: ${userEmail}` : "Logged in candidate";
  }

  // Profile Tab Elements
  const profileAvatar = document.getElementById("profileUserAvatar");
  if (profileAvatar) profileAvatar.textContent = initials;

  const profileNameTitle = document.getElementById("profileUserNameTitle");
  if (profileNameTitle) profileNameTitle.textContent = userName;

  const profileNameInput = document.getElementById("profileNameInput");
  if (profileNameInput && !profileNameInput.matches(":focus")) {
    profileNameInput.value = userName;
  }

  const profileEmail = document.getElementById("profileUserEmail");
  if (profileEmail && userEmail) {
    profileEmail.textContent = userEmail;
  }
}

function setupEventListeners() {
  // Update user name and avatar across all UI locations
  updateUserInfoUI();

  // Clicking on the sidebar user spot opens the profile tab directly
  const sidebarUserCard = document.getElementById("sidebarUserCard");
  if (sidebarUserCard) {
    sidebarUserCard.addEventListener("click", () => {
      switchTab("tab-profile");
    });
  }

  // Navigation tabs

  document.querySelectorAll(".nav-item").forEach(item => {
    item.addEventListener("click", () => {
      const tabTarget = item.getAttribute("data-tab");
      switchTab(tabTarget);
    });
  });

  // Target role switcher in topbar
  const roleDropdown = document.getElementById("topbarRoleSelect");
  if (roleDropdown) {
    roleDropdown.addEventListener("change", async (e) => {
      state.currentRole = e.target.value;
      await API.updateTargetRole(state.currentUserId, state.currentRole);
      await refreshAllViews();
      // Automatically open the roadmap tab when the role changes
      switchTab("tab-roadmap");
    });
  }

  // Seed demo data button
  const seedBtn = document.getElementById("seedDemoBtn");
  if (seedBtn) {
    seedBtn.addEventListener("click", async () => {
      seedBtn.innerHTML = "⏳ Seeding benchmark profile...";
      await API.seedDemoData(state.currentUserId);
      await refreshAllViews();
      seedBtn.innerHTML = "✨ Reset Benchmark Profile";
      showToast("Diagnostic benchmark data seeded! Showing Alex Rivera's profile.");
    });
  }

  // Quick Action Button in Dashboard Banner
  const quickActionBtn = document.getElementById("quickActionBtn");
  if (quickActionBtn) {
    quickActionBtn.addEventListener("click", () => {
      switchTab("tab-assessment");
      startQuizSession("adaptive_practice", 5);
    });
  }

  // Start Diagnostic Quiz Button
  const startDiagBtn = document.getElementById("startDiagBtn");
  if (startDiagBtn) {
    startDiagBtn.addEventListener("click", () => {
      startQuizSession("diagnostic", 10);
    });
  }

  // Start Adaptive Practice Button
  const startPracticeBtn = document.getElementById("startPracticeBtn");
  if (startPracticeBtn) {
    startPracticeBtn.addEventListener("click", () => {
      startQuizSession("adaptive_practice", 8);
    });
  }

  // Quiz Submit Button
  const submitAnswerBtn = document.getElementById("submitAnswerBtn");
  if (submitAnswerBtn) {
    submitAnswerBtn.addEventListener("click", submitCurrentAnswer);
  }

  // Quiz Next Button
  const nextQuestionBtn = document.getElementById("nextQuestionBtn");
  if (nextQuestionBtn) {
    nextQuestionBtn.addEventListener("click", loadNextAdaptiveQuestion);
  }

  // Research Experiment Simulation Form
  const runSimBtn = document.getElementById("runExperimentBtn");
  if (runSimBtn) {
    runSimBtn.addEventListener("click", executeResearchSimulation);
  }

  // Modal Close Button
  const closeModalBtn = document.getElementById("closeModalBtn");
  if (closeModalBtn) {
    closeModalBtn.addEventListener("click", closeModal);
  }

  // AI Mock Interview listeners
  const loadIntBtn = document.getElementById("loadInterviewQuestionsBtn");
  if (loadIntBtn) loadIntBtn.addEventListener("click", loadInterviewRound);

  const toggleVoiceBtn = document.getElementById("toggleVoiceBtn");
  if (toggleVoiceBtn) toggleVoiceBtn.addEventListener("click", toggleVoiceDictation);

  const evalIntBtn = document.getElementById("evaluateInterviewBtn");
  if (evalIntBtn) evalIntBtn.addEventListener("click", evaluateInterviewResponse);

  const nextIntQBtn = document.getElementById("nextInterviewQBtn");
  if (nextIntQBtn) nextIntQBtn.addEventListener("click", nextInterviewQuestion);

  const intAnswerInput = document.getElementById("interviewAnswerInput");
  if (intAnswerInput) {
    intAnswerInput.addEventListener("input", (e) => {
      const words = e.target.value.trim().split(/\s+/).filter(Boolean).length;
      const countSpan = document.getElementById("answerWordCount");
      if (countSpan) countSpan.innerText = words;
    });
  }

  // Resume ATS Analyzer listeners
  const analyzeResumeBtn = document.getElementById("analyzeResumeBtn");
  if (analyzeResumeBtn) analyzeResumeBtn.addEventListener("click", executeResumeAnalysis);

  const resumeInput = document.getElementById("resumeTextInput");
  if (resumeInput) {
    resumeInput.addEventListener("input", (e) => {
      const words = e.target.value.trim().split(/\s+/).filter(Boolean).length;
      const countSpan = document.getElementById("resumeWordCount");
      if (countSpan) countSpan.innerText = `${words} words`;
    });
  }

  document.querySelectorAll(".sample-resume-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const sampleKey = btn.getAttribute("data-sample");
      loadSampleResume(sampleKey);
    });
  });

  // Profile Page listeners
  const profileSaveBtn = document.getElementById("profileSaveBtn");
  if (profileSaveBtn) profileSaveBtn.addEventListener("click", saveProfileChanges);

  const profileSeedBtn = document.getElementById("profileSeedBtn");
  if (profileSeedBtn) {
    profileSeedBtn.addEventListener("click", async () => {
      await API.seedDemoData(state.currentUserId);
      await refreshAllViews();
      renderProfileSliders();
      showToast("Profile benchmark data reset!");
    });
  }
}

async function loadInitialData() {
  try {
    // 1. Fetch available roles
    state.roles = await API.getRoles();
    populateRoleDropdown();

    // 2. Fetch or create user profile
    const profile = await API.getUserProfile(state.currentUserId);
    state.currentRole = profile.target_role || "java_developer";
    const roleDropdown = document.getElementById("topbarRoleSelect");
    if (roleDropdown) roleDropdown.value = state.currentRole;

    // 3. Automatically seed demo data if fresh session
    const gaps = await API.getSkillGaps(state.currentUserId);
    const hasAttempts = gaps.some(g => g.attempts > 0);
    if (!hasAttempts) {
      await API.seedDemoData(state.currentUserId);
    }

    // 4. Refresh all dashboard widgets and views
    await refreshAllViews();
  } catch (err) {
    console.error("Initialization error:", err);
  }
}

function populateRoleDropdown() {
  const roleDropdown = document.getElementById("topbarRoleSelect");
  if (!roleDropdown) return;

  roleDropdown.innerHTML = "";
  for (const [id, info] of Object.entries(state.roles)) {
    const opt = document.createElement("option");
    opt.value = id;
    opt.innerText = `${info.icon} ${info.title}`;
    if (id === state.currentRole) opt.selected = true;
    roleDropdown.appendChild(opt);
  }
}

function switchTab(tabId) {
  state.activeTab = tabId;
  
  // Update sidebar active class
  document.querySelectorAll(".nav-item").forEach(item => {
    if (item.getAttribute("data-tab") === tabId) {
      item.classList.add("active");
    } else {
      item.classList.remove("active");
    }
  });

  // Show active view
  document.querySelectorAll(".tab-view").forEach(view => {
    if (view.id === tabId) {
      view.classList.add("active");
    } else {
      view.classList.remove("active");
    }
  });

  // Lazy render for specific tabs
  if (tabId === "tab-roadmap") renderRoadmapView();
  if (tabId === "tab-research") executeResearchSimulation();
  if (tabId === "tab-interview") initInterviewView();
  if (tabId === "tab-resume") initResumeView();
  if (tabId === "tab-profile") initProfileView();
}

async function refreshAllViews() {
  try {
    // Fetch readiness report
    state.readinessReport = await API.getReadinessReport(state.currentUserId, state.currentRole);
    // Fetch XAI breakdown
    state.xaiReport = await API.getXAIExplanation(state.currentUserId, state.currentRole);
    // Fetch Role Comparisons
    const comparisons = await API.getRoleComparison(state.currentUserId);

    renderDashboard(state.readinessReport, state.xaiReport, comparisons);
    renderXAIView(state.xaiReport);
    renderRoadmapView();
  } catch (err) {
    console.error("Refresh error:", err);
  }
}

/* =========================================================================
   1. DASHBOARD RENDERING
   ========================================================================= */
function renderDashboard(report, xai, comparisons) {
  if (!report) return;

  // Render Dial
  Charts.renderReadinessDial(report.overall_readiness_score);

  // Update Hero Text
  document.getElementById("heroRoleTitle").innerText = report.target_role_title;
  document.getElementById("heroTierBadge").innerText = report.readiness_tier;
  document.getElementById("heroSummaryText").innerText = report.role_alignment_summary;
  document.getElementById("heroConfidenceVal").innerText = `${Math.round(report.confidence_level * 100)}%`;
  document.getElementById("heroConsistencyVal").innerText = `${Math.round(report.consistency_multiplier * 100)}%`;

  // Update Action Banner
  const action = xai ? xai.recommended_immediate_action : null;
  if (action) {
    document.getElementById("actionTopicTitle").innerText = action.focus_topic;
    document.getElementById("actionStatement").innerText = action.action_statement;
  }

  // Render Skill Bars
  renderSkillBars(report.skill_breakdown);

  // Render Radar Chart
  Charts.renderSkillRadar(report.skill_breakdown);

  // Render Role Comparison Bar Chart
  if (comparisons) {
    Charts.renderRoleComparisonChart(comparisons);
  }
}

function renderSkillBars(skills) {
  const container = document.getElementById("skillBarsContainer");
  if (!container) return;

  container.innerHTML = "";
  skills.forEach(s => {
    let fillClass = "fill-low";
    if (s.score >= 75) fillClass = "fill-high";
    else if (s.score >= 55) fillClass = "fill-med";

    const item = document.createElement("div");
    item.className = "skill-bar-item";
    item.innerHTML = `
      <div class="skill-bar-header">
        <span>${s.skill}</span>
        <div>
          <span class="skill-weight-tag">Weight: ${Math.round(s.weight_in_role * 100)}%</span>
          <strong style="margin-left: 8px;">${s.score}%</strong>
        </div>
      </div>
      <div class="bar-track">
        <div class="bar-fill ${fillClass}" style="width: ${s.score}%;"></div>
      </div>
    `;
    container.appendChild(item);
  });
}

/* =========================================================================
   2. EXPLAINABLE AI (XAI) VIEW
   ========================================================================= */
function renderXAIView(xai) {
  if (!xai) return;

  document.getElementById("xaiExecSummary").innerText = xai.executive_summary;

  // Main Bottlenecks
  const bContainer = document.getElementById("xaiBottlenecksList");
  if (bContainer) {
    bContainer.innerHTML = "";
    if (xai.main_bottlenecks.length === 0) {
      bContainer.innerHTML = `<p style="color: #94a3b8; font-size: 13px;">No critical bottlenecks detected for this role.</p>`;
    } else {
      xai.main_bottlenecks.forEach(b => {
        const div = document.createElement("div");
        div.className = "bottleneck-item";
        div.innerHTML = `
          <div class="bottleneck-details">
            <h5>${b.subtopic} (${b.skill})</h5>
            <p>${b.reason}</p>
            <span style="font-size: 11px; color: #fda4af; font-weight: 600;">Role Impact: ${b.impact_level} (Weight: ${b.role_weight_pct}%)</span>
          </div>
          <div class="bottleneck-score">${b.mastery_score}%</div>
        `;
        bContainer.appendChild(div);
      });
    }
  }

  // Reasoning Tree
  const treeContainer = document.getElementById("xaiReasoningTree");
  if (treeContainer) {
    treeContainer.innerHTML = "";
    xai.diagnostic_reasoning_tree.forEach(step => {
      const node = document.createElement("div");
      node.className = "tree-node";
      node.innerHTML = `
        <h5>${step.step}</h5>
        <p>${step.observation}</p>
      `;
      treeContainer.appendChild(node);
    });
  }
}

/* =========================================================================
   3. ADAPTIVE ASSESSMENT / PRACTICE QUIZ
   ========================================================================= */
async function startQuizSession(sessionType = "diagnostic", numQuestions = 8) {
  try {
    clearInterval(state.timerInterval);
    state.selectedOptionIndex = null;
    state.isAnswerSubmitted = false;
    state.sessionQuestionsCount = 0;

    const data = await API.startAssessment(state.currentUserId, sessionType, numQuestions, state.currentRole);
    state.activeSession = data;
    
    document.getElementById("quizStartCard").style.display = "none";
    document.getElementById("quizActiveCard").style.display = "block";
    document.getElementById("quizCompleteCard").style.display = "none";

    renderQuestion(data.question);
    startQuestionTimer();
  } catch (err) {
    console.error("Start quiz error:", err);
  }
}

function startQuestionTimer() {
  clearInterval(state.timerInterval);
  state.secondsElapsed = 0;
  const timerEl = document.getElementById("quizTimerDisplay");
  
  state.timerInterval = setInterval(() => {
    state.secondsElapsed++;
    const mins = String(Math.floor(state.secondsElapsed / 60)).padStart(2, '0');
    const secs = String(state.secondsElapsed % 60).padStart(2, '0');
    if (timerEl) timerEl.innerText = `⏱ ${mins}:${secs}`;
  }, 1000);
}

function renderQuestion(q) {
  state.currentQuestion = q;
  state.selectedOptionIndex = null;
  state.isAnswerSubmitted = false;

  // Reset feedback & buttons
  const feedbackCard = document.getElementById("quizFeedbackCard");
  feedbackCard.style.display = "none";
  feedbackCard.className = "feedback-card";
  document.getElementById("submitAnswerBtn").style.display = "inline-flex";
  document.getElementById("nextQuestionBtn").style.display = "none";

  // Badges
  document.getElementById("qSkillBadge").innerText = q.skill;
  document.getElementById("qSubtopicBadge").innerText = q.subtopic;
  
  let diffText = "Beginner (Level 1-2)";
  let diffClass = "badge-success";
  if (q.difficulty >= 4) { diffText = `Advanced (Level ${q.difficulty})`; diffClass = "badge-danger"; }
  else if (q.difficulty === 3) { diffText = `Medium (Level 3)`; diffClass = "badge-warning"; }
  
  const diffBadge = document.getElementById("qDifficultyBadge");
  diffBadge.innerText = diffText;
  diffBadge.className = `badge ${diffClass}`;

  // Question Text & Code Snippet
  document.getElementById("qQuestionText").innerText = q.question_text;
  const codeBlock = document.getElementById("qCodeSnippet");
  if (q.code_snippet) {
    codeBlock.innerText = q.code_snippet;
    codeBlock.style.display = "block";
  } else {
    codeBlock.style.display = "none";
  }

  // Options
  const optionsList = document.getElementById("qOptionsList");
  optionsList.innerHTML = "";
  const letters = ["A", "B", "C", "D", "E"];

  q.options.forEach((opt, idx) => {
    const item = document.createElement("div");
    item.className = "option-item";
    item.setAttribute("data-index", idx);
    item.innerHTML = `
      <div class="option-letter">${letters[idx]}</div>
      <div class="option-text">${opt}</div>
    `;
    item.addEventListener("click", () => {
      if (state.isAnswerSubmitted) return;
      document.querySelectorAll(".option-item").forEach(el => el.classList.remove("selected"));
      item.classList.add("selected");
      state.selectedOptionIndex = idx;
    });
    optionsList.appendChild(item);
  });
}

async function submitCurrentAnswer() {
  if (state.selectedOptionIndex === null) {
    showToast("Please select an option first!");
    return;
  }

  clearInterval(state.timerInterval);
  state.isAnswerSubmitted = true;

  const res = await API.submitAnswer(
    state.activeSession.session_id,
    state.currentUserId,
    state.currentQuestion.id,
    state.selectedOptionIndex,
    state.secondsElapsed
  );

  // Show feedback
  const feedbackCard = document.getElementById("quizFeedbackCard");
  feedbackCard.style.display = "block";
  if (res.is_correct) {
    feedbackCard.className = "feedback-card correct";
    feedbackCard.innerHTML = `
      <h4>✅ Correct! (+ Mastery: ${res.updated_subtopic_mastery}%)</h4>
      <p>${res.explanation}</p>
      <div style="margin-top: 8px; font-size: 12px; color: #a7f3d0;">
        Adaptive AI Engine calibrated next difficulty to <strong>Level ${res.next_recommended_difficulty}</strong>.
      </div>
    `;
  } else {
    feedbackCard.className = "feedback-card incorrect";
    feedbackCard.innerHTML = `
      <h4>❌ Incorrect (Subtopic Mastery Adjusted: ${res.updated_subtopic_mastery}%)</h4>
      <p><strong>Explanation:</strong> ${res.explanation}</p>
      <div style="margin-top: 8px; font-size: 12px; color: #fecdd3;">
        Adaptive AI Engine prioritized remedial practice on <strong>${state.currentQuestion.subtopic}</strong>.
      </div>
    `;
  }

  // Highlight options
  const optionItems = document.querySelectorAll(".option-item");
  optionItems.forEach((item, idx) => {
    if (idx === res.correct_index) {
      item.style.borderColor = "#10b981";
      item.style.background = "rgba(16, 185, 129, 0.15)";
    } else if (idx === state.selectedOptionIndex && !res.is_correct) {
      item.style.borderColor = "#f43f5e";
      item.style.background = "rgba(244, 63, 94, 0.15)";
    }
  });

  document.getElementById("submitAnswerBtn").style.display = "none";
  
  if (res.next_question) {
    state.nextQuestionCache = res.next_question;
    document.getElementById("nextQuestionBtn").style.display = "inline-flex";
  } else {
    // Session complete
    const finishBtn = document.getElementById("nextQuestionBtn");
    finishBtn.innerText = "View Final Assessment Results 🎉";
    finishBtn.style.display = "inline-flex";
    finishBtn.onclick = showQuizResults;
  }

  // Background refresh data
  refreshAllViews();
}

function loadNextAdaptiveQuestion() {
  if (state.nextQuestionCache) {
    renderQuestion(state.nextQuestionCache);
    state.nextQuestionCache = null;
    startQuestionTimer();
  }
}

async function showQuizResults() {
  const summary = await API.getSessionSummary(state.activeSession.session_id);
  
  document.getElementById("quizActiveCard").style.display = "none";
  const compCard = document.getElementById("quizCompleteCard");
  compCard.style.display = "block";

  document.getElementById("compTotalQuestions").innerText = summary.total_questions;
  document.getElementById("compCorrectCount").innerText = summary.correct_count;
  document.getElementById("compAccuracy").innerText = `${summary.accuracy}%`;
  document.getElementById("compReadinessScore").innerText = `${summary.readiness_report.overall_readiness_score}%`;
}

/* =========================================================================
   4. LEARNING ROADMAP
   ========================================================================= */
async function renderRoadmapView() {
  try {
    const data = await API.getRoadmap(state.currentUserId);
    state.roadmapData = data;

    document.getElementById("roadmapRoleBadge").innerText = data.target_role.replace("_", " ").toUpperCase();
    document.getElementById("roadmapCompPct").innerText = `${data.completion_percentage}%`;
    document.getElementById("roadmapProgressBar").style.width = `${data.completion_percentage}%`;

    const container = document.getElementById("roadmapTimeline");
    if (!container) return;

    container.innerHTML = "";
    data.steps.forEach(step => {
      const card = document.createElement("div");
      card.className = "roadmap-step-card";
      card.innerHTML = `
        <div class="step-day-badge">
          <span>Day</span>
          <strong>${step.day_number}</strong>
        </div>
        <div class="step-details">
          <h4>
            ${step.action_title}
            <span class="badge ${step.is_completed ? 'badge-success' : 'badge-primary'}">
              ${step.is_completed ? 'Completed' : 'Pending'}
            </span>
          </h4>
          <p>${step.explanation_summary}</p>
          <div class="step-actions">
            <button class="btn-secondary" onclick="openStudyResource('${step.subtopic}')">
              📖 Study Notes & Cheatsheet
            </button>
            <button class="btn-primary" onclick="launchTargetedPractice('${step.subtopic}')">
              🎯 Practice 5 Questions
            </button>
            <button class="btn-secondary" onclick="toggleStep('${step.id}')">
              ${step.is_completed ? '↩ Mark Incomplete' : '✓ Mark Complete'}
            </button>
          </div>
        </div>
      `;
      container.appendChild(card);
    });
  } catch (err) {
    console.error("Roadmap render error:", err);
  }
}

async function toggleStep(stepId) {
  await API.toggleRoadmapStep(stepId);
  renderRoadmapView();
  refreshAllViews();
}

async function openStudyResource(subtopic) {
  const res = await API.getResourceDetails(subtopic);
  const modal = document.getElementById("resourceModal");
  
  document.getElementById("modalTitle").innerText = res.title;
  document.getElementById("modalSkillTopic").innerText = `${res.skill} → ${res.topic}`;
  
  // Key concepts
  const conceptsList = document.getElementById("modalConceptsList");
  conceptsList.innerHTML = "";
  res.key_concepts.forEach(c => {
    const li = document.createElement("li");
    li.innerText = c;
    conceptsList.appendChild(li);
  });

  // Pitfalls
  const pitfallsList = document.getElementById("modalPitfallsList");
  pitfallsList.innerHTML = "";
  res.common_pitfalls.forEach(p => {
    const li = document.createElement("li");
    li.innerText = p;
    pitfallsList.appendChild(li);
  });

  // Code Example
  document.getElementById("modalCodeExample").innerText = res.code_example;

  modal.style.display = "flex";
}

function closeModal() {
  document.getElementById("resourceModal").style.display = "none";
}

function launchTargetedPractice(subtopic) {
  switchTab("tab-assessment");
  startQuizSession("adaptive_practice", 5);
}

/* =========================================================================
   5. RESEARCH EXPERIMENTATION LAB
   ========================================================================= */
async function executeResearchSimulation() {
  const sampleSize = parseInt(document.getElementById("simSampleSize")?.value || "60");
  const simRole = document.getElementById("simTargetRole")?.value || state.currentRole;
  
  const res = await API.runResearchExperiment(sampleSize, simRole, 14);
  
  // Update Stat Boxes
  document.getElementById("statCohensD").innerText = `d = ${res.statistics.cohens_d}`;
  document.getElementById("statPVal").innerText = res.statistics.p_value < 0.001 ? "p < 0.001 (***)" : `p = ${res.statistics.p_value}`;
  document.getElementById("statTimeSaved").innerText = `${res.statistics.time_efficiency_gain_pct}% Faster`;
  document.getElementById("statGapRecovery").innerText = `${res.statistics.weak_gap_recovery_ratio}x Faster`;
  document.getElementById("statResearchVerdict").innerText = res.statistics.research_verdict;

  // Render Table
  const tbody = document.getElementById("researchTableBody");
  if (tbody) {
    const mA = res.group_a_fixed;
    const mB = res.group_b_adaptive;
    tbody.innerHTML = `
      <tr>
        <td><strong>Group A: Fixed Question Bank (Control)</strong></td>
        <td>${mA.sample_size}</td>
        <td>${mA.pre_test_mean}% ± ${mA.pre_test_std}</td>
        <td>${mA.post_test_mean}% ± ${mA.post_test_std}</td>
        <td style="color: #fbbf24;">+${mA.mean_improvement_pct}%</td>
        <td>${mA.avg_time_spent_hours} hrs</td>
        <td>${mA.weak_topic_resolution_rate_pct}%</td>
      </tr>
      <tr>
        <td><strong>Group B: Adaptive AI System (Novel Proposed)</strong></td>
        <td>${mB.sample_size}</td>
        <td>${mB.pre_test_mean}% ± ${mB.pre_test_std}</td>
        <td>${mB.post_test_mean}% ± ${mB.post_test_std}</td>
        <td style="color: #34d399; font-weight: 700;">+${mB.mean_improvement_pct}%</td>
        <td style="color: #34d399; font-weight: 700;">${mB.avg_time_spent_hours} hrs</td>
        <td style="color: #34d399; font-weight: 700;">${mB.weak_topic_resolution_rate_pct}%</td>
      </tr>
    `;
  }

  // Render Charts
  Charts.renderResearchCharts(res);
}

function showToast(msg) {
  // Remove existing toasts
  document.querySelectorAll(".toast-notification").forEach(el => el.remove());

  const toast = document.createElement("div");
  toast.className = "toast-notification";
  toast.innerHTML = `<span>✨</span> <span>${msg}</span>`;
  document.body.appendChild(toast);

  setTimeout(() => {
    toast.classList.add("hide");
    setTimeout(() => toast.remove(), 260);
  }, 3200);
}

/* =========================================================================
   6. AI MOCK TECHNICAL INTERVIEW CONTROLLER
   ========================================================================= */
function initInterviewView() {
  const select = document.getElementById("interviewRoleSelect");
  if (select && select.children.length === 0) {
    for (const [id, info] of Object.entries(state.roles)) {
      const opt = document.createElement("option");
      opt.value = id;
      opt.innerText = `${info.icon} ${info.title}`;
      if (id === state.currentRole) opt.selected = true;
      select.appendChild(opt);
    }
  }
  if (!state.interviewQuestions || state.interviewQuestions.length === 0) {
    loadInterviewRound();
  }
}

async function loadInterviewRound() {
  const roleId = document.getElementById("interviewRoleSelect")?.value || state.currentRole;
  state.interviewQuestions = await API.getInterviewQuestions(roleId);
  state.currentInterviewIdx = 0;
  renderCurrentInterviewQuestion();
}

function renderCurrentInterviewQuestion() {
  const questions = state.interviewQuestions;
  if (!questions || questions.length === 0) return;
  const q = questions[state.currentInterviewIdx];

  const typeBadge = document.getElementById("interviewQTypeBadge");
  if (typeBadge) typeBadge.innerText = q.type || "Technical Core";

  const idxBadge = document.getElementById("interviewQIndexBadge");
  if (idxBadge) idxBadge.innerText = `Question ${state.currentInterviewIdx + 1} of ${questions.length}`;

  const qText = document.getElementById("interviewQText");
  if (qText) qText.innerText = q.question;

  const textarea = document.getElementById("interviewAnswerInput");
  if (textarea) textarea.value = "";

  const wordSpan = document.getElementById("answerWordCount");
  if (wordSpan) wordSpan.innerText = "0";

  const emptyState = document.getElementById("interviewEmptyState");
  if (emptyState) emptyState.style.display = "block";

  const resultsWrap = document.getElementById("interviewResultsWrapper");
  if (resultsWrap) resultsWrap.style.display = "none";
}

function toggleVoiceDictation() {
  const pulse = document.getElementById("voicePulse");
  const label = document.getElementById("micLabel");
  const textarea = document.getElementById("interviewAnswerInput");

  if (!state.isRecordingVoice) {
    state.isRecordingVoice = true;
    if (pulse) pulse.style.display = "flex";
    if (label) label.innerText = "Listening... (Click to Stop)";

    const sampleDictations = [
      "In G1 GC, memory is divided into equal-sized regions (Eden, Survivor, Tenured). To diagnose OutOfMemoryError in production, I enable -XX:+HeapDumpOnOutOfMemoryError and analyze the heap dump using Eclipse MAT to identify humongous allocations and memory leak root causes.",
      "To optimize slow SQL queries with multiple JOINs, I start by executing EXPLAIN ANALYZE to inspect the query plan. Then I build composite B-Tree indexes on foreign keys and rewrite unindexed subqueries into explicit INNER or LEFT JOINs.",
      "Window functions like ROW_NUMBER and RANK compute aggregate values over partitions while maintaining individual row identities, unlike GROUP BY which collapses rows."
    ];
    const sampleDictation = sampleDictations[state.currentInterviewIdx % sampleDictations.length];
    let currentLen = 0;
    const interval = setInterval(() => {
      if (!state.isRecordingVoice || currentLen >= sampleDictation.length) {
        clearInterval(interval);
        state.isRecordingVoice = false;
        if (pulse) pulse.style.display = "none";
        if (label) label.innerText = "Simulate Voice Dictation";
        return;
      }
      currentLen += 12;
      textarea.value = sampleDictation.substring(0, currentLen);
      const words = textarea.value.trim().split(/\s+/).filter(Boolean).length;
      const countSpan = document.getElementById("answerWordCount");
      if (countSpan) countSpan.innerText = words;
    }, 150);
  } else {
    state.isRecordingVoice = false;
    if (pulse) pulse.style.display = "none";
    if (label) label.innerText = "Simulate Voice Dictation";
  }
}

async function evaluateInterviewResponse() {
  const textarea = document.getElementById("interviewAnswerInput");
  const candidateAnswer = textarea ? textarea.value.trim() : "";
  if (!candidateAnswer) {
    showToast("Please type or dictate an answer before submitting for AI evaluation.");
    return;
  }

  const questions = state.interviewQuestions;
  const q = questions[state.currentInterviewIdx];
  const evalBtn = document.getElementById("evaluateInterviewBtn");
  if (evalBtn) evalBtn.innerHTML = "⏳ Evaluating...";

  try {
    const result = await API.evaluateInterviewResponse(state.currentUserId, q.id, candidateAnswer);

    document.getElementById("interviewEmptyState").style.display = "none";
    document.getElementById("interviewResultsWrapper").style.display = "block";

    document.getElementById("interviewOverallScore").innerText = `${result.overall_score}%`;
    document.getElementById("interviewStatusText").innerText = result.status;
    document.getElementById("interviewBoostText").innerText = `Readiness Boost: ${result.readiness_boost}`;
    
    const statusBadge = document.getElementById("interviewHireStatusBadge");
    if (statusBadge) {
      statusBadge.innerText = result.overall_score >= 70 ? "Strong Response" : "Needs Practice";
      statusBadge.className = result.overall_score >= 70 ? "badge badge-success" : "badge badge-warning";
    }

    // Matched keywords
    const matchedCloud = document.getElementById("interviewKeywordsCloud");
    if (matchedCloud) {
      matchedCloud.innerHTML = result.matched_keywords.length > 0 
        ? result.matched_keywords.map(k => `<span class="keyword-pill keyword-pill-matched">✓ ${k}</span>`).join("")
        : `<span style="font-size:12px; color:var(--text-muted);">No key terms matched</span>`;
    }

    // Missing concepts
    const missingCloud = document.getElementById("interviewMissingCloud");
    if (missingCloud) {
      missingCloud.innerHTML = result.missing_key_concepts.length > 0
        ? result.missing_key_concepts.map(k => `<span class="keyword-pill keyword-pill-missing">✕ ${k}</span>`).join("")
        : `<span style="font-size:12px; color:#34d399;">Comprehensive coverage! Zero missing concepts.</span>`;
    }

    // Depth feedback
    const depthFeedback = document.getElementById("interviewDepthFeedback");
    if (depthFeedback) depthFeedback.innerText = result.depth_feedback;

    // Model points
    const pointsList = document.getElementById("interviewIdealPointsList");
    if (pointsList) pointsList.innerHTML = result.ideal_points.map(pt => `<li>${pt}</li>`).join("");

    showToast(`AI Interview Evaluation Complete: ${result.status} (${result.readiness_boost})`);
  } catch (err) {
    console.error("Interview Evaluation error:", err);
    showToast("Error evaluating interview answer.");
  } finally {
    if (evalBtn) evalBtn.innerHTML = "🧠 Evaluate with AI Engine";
  }
}

function nextInterviewQuestion() {
  if (!state.interviewQuestions) return;
  state.currentInterviewIdx = (state.currentInterviewIdx + 1) % state.interviewQuestions.length;
  renderCurrentInterviewQuestion();
}

/* =========================================================================
   7. RESUME SKILL-GAP & ATS ANALYZER CONTROLLER
   ========================================================================= */
const SAMPLE_RESUMES = {
  java: `Alex Rivera | Software Engineering Candidate
alex.rivera@campus.edu | GitHub: github.com/arivera | LinkedIn: linkedin.com/in/arivera

SUMMARY
Computer Science Senior specializing in Java backend development, OOP design principles, and enterprise database systems.

TECHNICAL SKILLS
Languages & Frameworks: Java, JVM, Spring Boot, Hibernate, JPA, Python, C++, SQL
Database Management: MySQL, PostgreSQL, ACID Transactions, B-Tree Indexing, Stored Procedures, Normalization
Tools & DevOps: Docker, Git, GitHub, Maven, Gradle, Linux, CI/CD, JUnit, REST API Architecture
Core CS Competencies: Data Structures, Algorithms (DSA), Object-Oriented Programming (OOP), SOLID Principles, Design Patterns, Multithreading

EXPERIENCE & PROJECTS
Enterprise Microservice Backend (Java, Spring Boot, Docker)
• Built RESTful microservices processing 10,000+ daily requests with Spring Boot and Hibernate ORM.
• Optimized relational SQL JOINs and composite indexes, reducing query latency by 45%.
• Managed heap memory and garbage collection tuning using G1 GC parameters.`,

  data: `Jordan Lee | Data Analyst & BI Specialist
jordan.lee@campus.edu | GitHub: github.com/jlee-data

TECHNICAL SKILLS
Analytical Tools: SQL (PostgreSQL, BigQuery), Python (Pandas, NumPy, Scikit-learn), R, Tableau, Excel
Database & Querying: Window Functions (ROW_NUMBER, RANK, DENSE_RANK), GROUP BY, PARTITION BY, Subqueries, Joins
Data Science & ML: Quantitative Aptitude, Statistics, Probability, Cohort Segmentation, A/B Testing, User Churn Analysis`,

  minimal: `Sam Taylor | Computer Science Student
sam@email.com

SKILLS
HTML, CSS, JavaScript, Basic Python.

PROJECTS
Personal Portfolio Website
• Built a personal responsive website using HTML and CSS.`
};

function initResumeView() {
  const select = document.getElementById("resumeRoleSelect");
  if (select && select.children.length === 0) {
    for (const [id, info] of Object.entries(state.roles)) {
      const opt = document.createElement("option");
      opt.value = id;
      opt.innerText = `${info.icon} ${info.title}`;
      if (id === state.currentRole) opt.selected = true;
      select.appendChild(opt);
    }
  }
}

function loadSampleResume(key) {
  const text = SAMPLE_RESUMES[key] || SAMPLE_RESUMES.java;
  const textarea = document.getElementById("resumeTextInput");
  if (textarea) {
    textarea.value = text;
    const countSpan = document.getElementById("resumeWordCount");
    if (countSpan) countSpan.innerText = `${text.split(/\s+/).filter(Boolean).length} words`;
  }
  executeResumeAnalysis();
}

async function executeResumeAnalysis() {
  const text = document.getElementById("resumeTextInput")?.value.trim() || "";
  if (!text) {
    showToast("Please enter resume text or choose a sample resume.");
    return;
  }

  const roleId = document.getElementById("resumeRoleSelect")?.value || state.currentRole;
  const analyzeBtn = document.getElementById("analyzeResumeBtn");
  if (analyzeBtn) analyzeBtn.innerHTML = "⏳ Scanning Resume...";

  try {
    const res = await API.analyzeResume(state.currentUserId, roleId, text);

    document.getElementById("resumeEmptyState").style.display = "none";
    document.getElementById("resumeResultsWrapper").style.display = "block";

    document.getElementById("statAtsScore").innerText = `${res.ats_score}%`;
    document.getElementById("statRoleMatchPct").innerText = `${res.role_match_percentage}%`;
    
    const matchBadge = document.getElementById("resumeRoleMatchBadge");
    if (matchBadge) {
      matchBadge.innerText = `${res.target_role_title} Match`;
      matchBadge.className = res.role_match_percentage >= 70 ? "badge badge-success" : "badge badge-warning";
    }

    // Detected Skills Breakdown
    const container = document.getElementById("resumeSkillsBreakdownContainer");
    if (container) {
      container.innerHTML = "";
      for (const [cat, skills] of Object.entries(res.detected_skills_breakdown)) {
        const row = document.createElement("div");
        row.className = "profile-slider-item";
        row.innerHTML = `
          <div class="profile-slider-header">
            <span>${cat}</span>
            <span style="color:var(--accent-cyan);">${skills.length} detected</span>
          </div>
          <div style="display:flex; flex-wrap:wrap; gap:4px; margin-top:4px;">
            ${skills.map(s => `<span class="keyword-pill keyword-pill-matched">${s}</span>`).join("")}
          </div>
        `;
        container.appendChild(row);
      }
    }

    // Missing Critical Requirements
    const missingList = document.getElementById("resumeMissingCriticalList");
    if (missingList) {
      missingList.innerHTML = res.missing_critical_gaps.length > 0
        ? res.missing_critical_gaps.map(g => `<span class="keyword-pill keyword-pill-missing">✕ Missing: ${g}</span>`).join("")
        : `<span style="font-size:12px; color:#34d399;">✓ Perfect fit! All critical prerequisites detected.</span>`;
    }

    // Recommendations
    const recsList = document.getElementById("resumeRecommendationsList");
    if (recsList) {
      recsList.innerHTML = res.actionable_recommendations.map(r => `<li>${r}</li>`).join("");
    }

    showToast(`Resume ATS Analysis Complete: ${res.ats_score}% Score against ${res.target_role_title}`);
  } catch (err) {
    console.error("Resume Analysis error:", err);
    showToast("Error analyzing resume.");
  } finally {
    if (analyzeBtn) analyzeBtn.innerHTML = "🔍 Run ATS & Skill-Gap Analysis";
  }
}

/* =========================================================================
   8. STUDENT PROFILE & PROFICIENCY MATRIX CONTROLLER
   ========================================================================= */
const SKILL_CATEGORIES = [
  { id: "Java", title: "Java Core & Ecosystem", icon: "☕", defaultVal: 72 },
  { id: "OOP", title: "Object-Oriented Programming (OOP)", icon: "🧩", defaultVal: 85 },
  { id: "SQL", title: "SQL & Relational Querying", icon: "🗄️", defaultVal: 64 },
  { id: "DBMS", title: "Database Systems & Architecture", icon: "💾", defaultVal: 58 },
  { id: "Coding", title: "Data Structures & Algorithms (DSA)", icon: "⚡", defaultVal: 80 },
  { id: "Aptitude", title: "Quantitative Aptitude & Stats", icon: "📐", defaultVal: 75 },
  { id: "DevOps & Cloud", title: "DevOps, Git & Infrastructure", icon: "🐳", defaultVal: 60 },
  { id: "Communication", title: "Technical Communication & STAR", icon: "🗣️", defaultVal: 82 }
];

function initProfileView() {
  updateUserInfoUI();

  const select = document.getElementById("profileRoleSelect");
  if (select && select.children.length === 0) {
    for (const [id, info] of Object.entries(state.roles)) {
      const opt = document.createElement("option");
      opt.value = id;
      opt.innerText = `${info.icon} ${info.title}`;
      if (id === state.currentRole) opt.selected = true;
      select.appendChild(opt);
    }
  }

  const nameInput = document.getElementById("profileNameInput");
  if (nameInput && !nameInput.dataset.boundEnter) {
    nameInput.dataset.boundEnter = "true";
    nameInput.addEventListener("keydown", (e) => {
      if (e.key === "Enter") saveProfileChanges();
    });
  }

  renderProfileSliders();
}

function renderProfileSliders() {
  const container = document.getElementById("profileSkillSlidersContainer");
  if (!container) return;
  container.innerHTML = "";

  SKILL_CATEGORIES.forEach(cat => {
    const item = document.createElement("div");
    item.className = "profile-slider-item";
    item.innerHTML = `
      <div class="profile-slider-header">
        <span>${cat.icon} ${cat.title}</span>
        <span id="sliderVal_${cat.id}" style="color:var(--accent-cyan); font-weight:700;">${cat.defaultVal}%</span>
      </div>
      <input type="range" min="0" max="100" value="${cat.defaultVal}" class="profile-range-input" oninput="document.getElementById('sliderVal_${cat.id}').innerText = this.value + '%'">
    `;
    container.appendChild(item);
  });
}

async function saveProfileChanges() {
  const nameInput = document.getElementById("profileNameInput");
  const newName = nameInput?.value?.trim();
  if (newName) {
    localStorage.setItem("placement_user_name", newName);
  }

  const newRole = document.getElementById("profileRoleSelect")?.value || state.currentRole;
  state.currentRole = newRole;
  await API.updateTargetRole(state.currentUserId, newRole);
  await refreshAllViews();
  updateUserInfoUI();

  const userBadge = document.getElementById("profileUserRoleBadge");
  if (userBadge) userBadge.innerText = state.roles[newRole]?.title || newRole;

  showToast(`Profile updated successfully for ${newName || "user"}!`);
}

// ── Sign Out ─────────────────────────────────────────────────────────────────
async function handleSignOut() {
  // Sign out from Supabase Auth if the client is available
  try {
    if (typeof supabase !== "undefined") {
      const { createClient } = supabase;
      const sbClient = createClient(
        "https://lxqlvfwubnkvxqkabeag.supabase.co",
        "sb_publishable_Z4CG7DBXYvhZs5lunsOqPA_q3H26mhB"
      );
      await sbClient.auth.signOut();
    }
  } catch (e) { /* ignore */ }

  localStorage.removeItem("placement_user_id");
  localStorage.removeItem("placement_user_name");
  localStorage.removeItem("placement_user_email");
  window.location.href = "/auth";
}
