// ── Auth Guard ────────────────────────────────────────────────────────────────
// If no user is stored in localStorage, redirect to landing page (where login is embedded)
const _storedUserId = localStorage.getItem("placement_user_id");
if (!_storedUserId) {
  window.location.href = "/landing";
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

  // Navigation tabs & Single-Open Accordion Logic
  document.querySelectorAll(".nav-item").forEach(item => {
    item.addEventListener("click", (e) => {
      const tabTarget = item.getAttribute("data-tab");
      const parentGroup = item.closest(".nav-group");

      // Handle accordion groups: ONLY ONE OPEN AT A TIME
      if (item.classList.contains("nav-accordion-toggle") && parentGroup) {
        const wasOpen = parentGroup.classList.contains("open");
        // Close ALL other accordion groups
        document.querySelectorAll(".nav-group").forEach(g => g.classList.remove("open"));
        
        // Toggle the clicked group
        if (!wasOpen) {
          parentGroup.classList.add("open");
        }
      } else if (!parentGroup) {
        // When clicking a non-group nav item, close open accordions
        document.querySelectorAll(".nav-group").forEach(g => g.classList.remove("open"));
      }

      if (tabTarget) {
        switchTab(tabTarget);
      }
    });
  });

  // Navigation Submenu Items Click Listeners
  document.querySelectorAll(".nav-subitem").forEach(subitem => {
    subitem.addEventListener("click", (e) => {
      e.stopPropagation();

      // Highlight active subitem
      document.querySelectorAll(".nav-subitem").forEach(s => s.classList.remove("active"));
      subitem.classList.add("active");

      const action = subitem.getAttribute("data-action");
      const tabTarget = subitem.getAttribute("data-tab");
      const aptCategory = subitem.getAttribute("data-apt-category");

      if (action === "start-drill") {
        switchTab("tab-assessment");
        startQuizSession("adaptive_practice", 8);
      } else if (action === "start-diagnostic") {
        switchTab("tab-assessment");
        startQuizSession("diagnostic", 10);
      } else if (tabTarget === "tab-aptitude" && aptCategory) {
        switchTab("tab-aptitude");
        selectAptitudeCategory(aptCategory);
      } else if (tabTarget) {
        switchTab(tabTarget);
      }
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
      profileSeedBtn.innerHTML = "⏳ Seeding demo...";
      await API.seedDemoData(state.currentUserId);
      await refreshAllViews();
      await renderProfileSliders();
      profileSeedBtn.innerHTML = "⚡ Seed Benchmark Demo";
      showToast("Benchmark demo profile seeded successfully!");
    });
  }

  const clearDataBtn = document.getElementById("clearDataBtn");
  if (clearDataBtn) {
    clearDataBtn.addEventListener("click", async () => {
      if (!confirm("Are you sure you want to clear all test attempts and start fresh with your custom scores?")) return;
      clearDataBtn.innerHTML = "⏳ Clearing data...";
      await API.clearUserData(state.currentUserId);
      await refreshAllViews();
      await renderProfileSliders();
      clearDataBtn.innerHTML = "🧹 Clear Test Logs (Fresh Start)";
      showToast("All test logs cleared! System is now running 100% on your real profile data.");
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

    // 3. Refresh all dashboard widgets and views based on real user data
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
  
  // Update sidebar active class & sync single-open accordion groups
  document.querySelectorAll(".nav-group").forEach(g => g.classList.remove("open"));
  if (tabId === "tab-assessment") {
    const grp = document.getElementById("navGroupAdaptive");
    if (grp) grp.classList.add("open");
  } else if (tabId === "tab-aptitude") {
    const grp = document.getElementById("navGroupAptitude");
    if (grp) grp.classList.add("open");
  }

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
  if (tabId === "tab-aptitude") initAptitudeView();
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

async function renderProfileSliders() {
  const container = document.getElementById("profileSkillSlidersContainer");
  if (!container) return;
  container.innerHTML = "<div style='color:var(--text-muted); font-size:13px;'>Loading skills matrix...</div>";

  let savedPriors = {};
  try {
    savedPriors = await API.getUserSkills(state.currentUserId) || {};
  } catch (e) {
    console.warn("Could not load skill priors:", e);
  }

  container.innerHTML = "";

  SKILL_CATEGORIES.forEach(cat => {
    const currentVal = (savedPriors && savedPriors[cat.id] !== undefined)
      ? Math.round(savedPriors[cat.id])
      : cat.defaultVal;

    const item = document.createElement("div");
    item.className = "profile-slider-item";
    item.innerHTML = `
      <div class="profile-slider-header">
        <span>${cat.icon} ${cat.title}</span>
        <span id="sliderVal_${cat.id}" style="color:var(--accent-cyan); font-weight:700;">${currentVal}%</span>
      </div>
      <input type="range" min="0" max="100" value="${currentVal}" id="range_${cat.id}" class="profile-range-input" oninput="document.getElementById('sliderVal_${cat.id}').innerText = this.value + '%'">
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

  // Collect and persist real slider values
  const skillsPayload = {};
  SKILL_CATEGORIES.forEach(cat => {
    const slider = document.getElementById(`range_${cat.id}`);
    if (slider) {
      skillsPayload[cat.id] = parseFloat(slider.value);
    }
  });

  if (Object.keys(skillsPayload).length > 0) {
    await API.saveUserSkills(state.currentUserId, skillsPayload);
  }

  await refreshAllViews();
  updateUserInfoUI();

  const userBadge = document.getElementById("profileUserRoleBadge");
  if (userBadge) userBadge.innerText = state.roles[newRole]?.title || newRole;

  showToast(`Profile & skill mastery matrix updated successfully for ${newName || "user"}!`);
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
  window.location.href = "/landing";
}


// =========================================================================
// APTITUDE & REASONING HUB MODULE
// =========================================================================

const APTITUDE_DATA = {
  categories: {
    arithmetic: {
      name: "Arithmetic Aptitude",
      icon: "∫",
      subtopics: ["All", "Percentages & Profit Loss", "Simple & Compound Interest", "Ratio & Proportion", "Time & Work", "Speed Distance Time", "Probability & Combinatorics"],
      questions: [
        {
          id: "apt_arith_1",
          subtopic: "Percentages & Profit Loss",
          diff: "Medium",
          prompt: "A retailer marks an item 30% above the cost price and then offers a discount of 15% on the marked price. What is the net profit percentage earned by the retailer?",
          formula: "Net Profit % = [Marked Factor × (1 - Discount)] - 1\n= [1.30 × 0.85] - 1 = 1.105 - 1 = +10.5%",
          options: ["10.5%", "12.0%", "15.0%", "8.5%"],
          correct: 0,
          explanation: "Let CP = 100. Marked Price MP = 100 × 1.30 = 130. Selling Price SP = 130 - (15% of 130) = 130 - 19.5 = 110.5. Net Profit = 110.5 - 100 = 10.5%."
        },
        {
          id: "apt_arith_2",
          subtopic: "Simple & Compound Interest",
          diff: "Hard",
          prompt: "The difference between CI and SI compounded annually on a certain sum for 2 years at 12% per annum is Rs. 144. Find the principal sum.",
          formula: "CI - SI (for 2 yrs) = P × (R / 100)²\nP = Difference / (R / 100)² = 144 / (0.12)²",
          options: ["Rs. 10,000", "Rs. 12,000", "Rs. 9,500", "Rs. 15,000"],
          correct: 0,
          explanation: "Difference = P × (R/100)² => 144 = P × (12/100)² => 144 = P × (144 / 10,000) => P = Rs. 10,000."
        },
        {
          id: "apt_arith_3",
          subtopic: "Time & Work",
          diff: "Medium",
          prompt: "A can complete a software module in 12 days, and B can complete it in 18 days. They work together for 4 days, after which A leaves. How many days will B alone take to finish the remaining work?",
          formula: "Work done in 4 days = 4 × (1/12 + 1/18)\nRemaining Work = 1 - Work Done\nTime for B = Remaining / (1/18)",
          options: ["8 days", "6 days", "10 days", "7.5 days"],
          correct: 0,
          explanation: "Combined rate = 1/12 + 1/18 = 5/36 work/day. In 4 days, work done = 4 × 5/36 = 20/36 = 5/9. Remaining work = 1 - 5/9 = 4/9. Time taken by B alone = (4/9) / (1/18) = (4/9) × 18 = 8 days."
        },
        {
          id: "apt_arith_4",
          subtopic: "Speed Distance Time",
          diff: "Medium",
          prompt: "Two trains 140m and 160m long run on parallel tracks in opposite directions at 60 km/h and 48 km/h. In how many seconds will they completely cross each other?",
          formula: "Relative Speed (Opposite) = S1 + S2 = 60 + 48 = 108 km/h\n108 × (5/18) = 30 m/s\nTime = Total Distance / Relative Speed = (140 + 160) / 30",
          options: ["10 seconds", "12 seconds", "15 seconds", "8 seconds"],
          correct: 0,
          explanation: "Total Distance = 140 + 160 = 300m. Relative speed = 60 + 48 = 108 km/h = 108 × (5/18) = 30 m/s. Time = 300 / 30 = 10 seconds."
        },
        {
          id: "apt_arith_5",
          subtopic: "Ratio & Proportion",
          diff: "Easy",
          prompt: "The ratio of salaries of two software engineers X and Y is 7:9. If each gets a salary increment of Rs. 4,000, the new ratio becomes 4:5. What is the original salary of X?",
          formula: "(7x + 4000) / (9x + 4000) = 4 / 5\n5(7x + 4000) = 4(9x + 4000) => 35x + 20000 = 36x + 16000 => x = 4000",
          options: ["Rs. 28,000", "Rs. 36,000", "Rs. 32,000", "Rs. 24,000"],
          correct: 0,
          explanation: "Let salaries be 7x and 9x. (7x + 4000)/(9x + 4000) = 4/5 => 35x + 20000 = 36x + 16000 => x = 4000. X's salary = 7 × 4000 = Rs. 28,000."
        },
        {
          id: "apt_arith_6",
          subtopic: "Probability & Combinatorics",
          diff: "Medium",
          prompt: "A box contains 5 red, 4 blue, and 3 green marbles. If 2 marbles are drawn at random without replacement, what is the probability that both are red?",
          formula: "P(Both Red) = (5C2) / (12C2)\n5C2 = 10, 12C2 = 66 => 10 / 66 = 5 / 33",
          options: ["5/33", "1/6", "5/36", "10/33"],
          correct: 0,
          explanation: "Total marbles = 5 + 4 + 3 = 12. Ways to pick 2 red marbles = 5C2 = 10. Total ways to pick any 2 marbles = 12C2 = (12 × 11)/2 = 66. Probability = 10/66 = 5/33."
        }
      ]
    },
    di: {
      name: "Data Interpretation",
      icon: "📊",
      subtopics: ["All", "Pie Charts", "Bar Graphs", "Tables", "Line Graphs"],
      questions: [
        {
          id: "apt_di_1",
          subtopic: "Pie Charts",
          diff: "Medium",
          prompt: "In a company budget breakdown of $2,400,000: Cloud Infra (35%), Engineering Salaries (40%), Marketing (15%), Operations (10%). How much more is spent on Engineering Salaries than Marketing?",
          formula: "Difference % = 40% - 15% = 25%\nDollar Difference = 25% of $2,400,000 = 0.25 × 2,400,000",
          options: ["$600,000", "$450,000", "$720,000", "$500,000"],
          correct: 0,
          explanation: "Engineering = 40% ($960,000). Marketing = 15% ($360,000). Difference = $960,000 - $360,000 = $600,000 (which is 25% of total)."
        },
        {
          id: "apt_di_2",
          subtopic: "Tables",
          diff: "Medium",
          prompt: "A tech startup reports users (in thousands): Year 1: 50, Year 2: 80, Year 3: 140. What is the Compound Annual Growth Rate (CAGR) from Year 1 to Year 3?",
          formula: "CAGR = (End / Start)^(1/n) - 1\n= (140 / 50)^(1/2) - 1 = (2.8)^0.5 - 1 ≈ 1.673 - 1 = 67.3%",
          options: ["~67.3%", "~90.0%", "~45.5%", "~80.0%"],
          correct: 0,
          explanation: "CAGR = (140/50)^(1/2) - 1 = sqrt(2.8) - 1 ≈ 1.6733 - 1 = 67.33% per annum."
        },
        {
          id: "apt_di_3",
          subtopic: "Bar Graphs",
          diff: "Easy",
          prompt: "Quarterly server downtime (minutes): Q1: 120, Q2: 90, Q3: 60, Q4: 45. What is the percentage reduction in downtime from Q1 to Q4?",
          formula: "Reduction % = [(Initial - Final) / Initial] × 100\n= [(120 - 45) / 120] × 100 = (75 / 120) × 100",
          options: ["62.5%", "75.0%", "50.0%", "60.0%"],
          correct: 0,
          explanation: "Reduction = 120 - 45 = 75 minutes. Percentage reduction = (75 / 120) × 100 = 62.5%."
        }
      ]
    },
    verbal: {
      name: "Verbal Ability",
      icon: "📝",
      subtopics: ["All", "Spotting Errors", "Synonyms & Antonyms", "Sentence Correction", "Reading Comprehension"],
      questions: [
        {
          id: "apt_verb_1",
          subtopic: "Spotting Errors",
          diff: "Medium",
          prompt: "Find the error part: 'Each of the microservices (A) / deployed on Kubernetes (B) / have their own isolated PostgreSQL database instance (C) / without shared state (D).'",
          formula: "Grammar Rule: 'Each of + Plural Noun' takes a SINGULAR verb ('has its own', not 'have their own').",
          options: ["Part (C) - 'have their own'", "Part (A)", "Part (B)", "Part (D) - No error"],
          correct: 0,
          explanation: "'Each' is singular distributively, requiring 'has its own isolated database instance' instead of 'have their own'."
        },
        {
          id: "apt_verb_2",
          subtopic: "Synonyms & Antonyms",
          diff: "Easy",
          prompt: "Choose the exact ANTONYM of the word: 'OBSOLETE'",
          formula: "Obsolete = Outdated, no longer produced or used.\nAntonym = Contemporary, modern, cutting-edge, state-of-the-art.",
          options: ["Cutting-edge / Contemporary", "Archaic", "Redundant", "Defunct"],
          correct: 0,
          explanation: "'Obsolete' means no longer produced or out of date. Its opposite is 'Cutting-edge' or 'Contemporary'."
        },
        {
          id: "apt_verb_3",
          subtopic: "Sentence Correction",
          diff: "Medium",
          prompt: "Select the best replacement: 'If the distributed cache would have been configured properly, the latency spike would not have crashed the payment gateway.'",
          formula: "Third Conditional Rule: 'If + Past Perfect (had been), ... would have + Past Participle'",
          options: ["If the distributed cache had been configured properly", "If the distributed cache was configured", "Had the cache would configure", "No improvement needed"],
          correct: 0,
          explanation: "In conditional sentences referring to past unfulfilled conditions, use 'If + had been configured' (past perfect), never 'would have been' in the if-clause."
        }
      ]
    },
    logical: {
      name: "Logical Reasoning",
      icon: "🔄",
      subtopics: ["All", "Coding-Decoding", "Blood Relations", "Direction Sense", "Number Series", "Seating Arrangement"],
      questions: [
        {
          id: "apt_log_1",
          subtopic: "Coding-Decoding",
          diff: "Easy",
          prompt: "In a certain placement code, 'SERVER' is written as 'TFWWFS'. How is 'CLIENT' coded in that same pattern?",
          formula: "Pattern: Each letter is shifted forward by +1 position in the alphabet.\nS(+1)T, E(+1)F, R(+1)S, V(+1)W, E(+1)F, R(+1)S",
          options: ["DMJFOU", "DMKFOV", "CLJENU", "DMIENU"],
          correct: 0,
          explanation: "C(+1)D, L(+1)M, I(+1)J, E(+1)F, N(+1)O, T(+1)U -> DMJFOU."
        },
        {
          id: "apt_log_2",
          subtopic: "Blood Relations",
          diff: "Medium",
          prompt: "Introducing a man, a woman says: 'His wife is the only daughter of my mother.' How is the man related to the woman?",
          formula: "Only daughter of woman's mother = The woman herself.\nTherefore, the man's wife = The woman herself => Man is Husband.",
          options: ["Husband", "Brother", "Father-in-law", "Maternal Uncle"],
          correct: 0,
          explanation: "The only daughter of the woman's mother is the woman herself. Since the woman herself is the man's wife, the man is her Husband."
        },
        {
          id: "apt_log_3",
          subtopic: "Number Series",
          diff: "Medium",
          prompt: "Identify the missing term in the sequence: 4, 18, 48, 100, 180, ?",
          formula: "Pattern: n³ - n² or n² × (n - 1) for n = 2, 3, 4, 5, 6, 7...\nn=2: 8-4=4\nn=3: 27-9=18\nn=4: 64-16=48\nn=5: 125-25=100\nn=6: 216-36=180\nn=7: 343-49 = 294",
          options: ["294", "280", "312", "275"],
          correct: 0,
          explanation: "Series pattern is n³ - n² starting from n=2. For n=7: 7³ - 7² = 343 - 49 = 294."
        },
        {
          id: "apt_log_4",
          subtopic: "Direction Sense",
          diff: "Easy",
          prompt: "An engineer walks 20m North, turns Right and walks 30m, turns Right again and walks 20m. How far and in which direction is she from the starting point?",
          formula: "North 20m -> East 30m -> South 20m.\nNet North-South = 20 - 20 = 0m. Net East-West = 30m East.",
          options: ["30m East", "30m West", "50m North-East", "20m East"],
          correct: 0,
          explanation: "The 20m North and 20m South cancel out completely. She is exactly 30m East of her starting location."
        }
      ]
    },
    verbal_reasoning: {
      name: "Verbal Reasoning",
      icon: "ABC",
      subtopics: ["All", "Statement & Assumptions", "Course of Action", "Cause & Effect", "Syllogisms"],
      questions: [
        {
          id: "apt_vr_1",
          subtopic: "Statement & Assumptions",
          diff: "Medium",
          prompt: "Statement: 'The IT company made it mandatory for all junior software engineers to complete a certified cloud security course before promotion.'\nAssumption I: Cloud security proficiency is relevant for higher engineering roles.\nAssumption II: Junior engineers are capable of completing certification courses.",
          formula: "A company mandates training assuming both relevance (I) and candidate capability (II). Both are implicit.",
          options: ["Both I and II are implicit", "Only Assumption I is implicit", "Only Assumption II is implicit", "Neither is implicit"],
          correct: 0,
          explanation: "The company creates this requirement assuming both that cloud security is crucial for promoted engineers (I) and that juniors can pass the certification (II)."
        },
        {
          id: "apt_vr_2",
          subtopic: "Syllogisms",
          diff: "Medium",
          prompt: "Statements:\n1. All microservices are scalable systems.\n2. Some scalable systems are distributed databases.\nConclusions:\nI. Some microservices are distributed databases.\nII. Some scalable systems are microservices.",
          formula: "All A are B -> Some B are A (Conversion holds). Conclusion II is strictly valid. Conclusion I cannot be asserted with certainty.",
          options: ["Only Conclusion II follows", "Only Conclusion I follows", "Both I and II follow", "Neither follows"],
          correct: 0,
          explanation: "From 'All microservices are scalable systems', the immediate conversion 'Some scalable systems are microservices' is definitely true. There is no definite connection given between microservices and distributed databases."
        }
      ]
    },
    nonverbal: {
      name: "Nonverbal Reasoning",
      icon: "▦",
      subtopics: ["All", "Cubes & Dice", "Pattern Completion", "Mirror Images", "Paper Folding"],
      questions: [
        {
          id: "apt_nvr_1",
          subtopic: "Cubes & Dice",
          diff: "Medium",
          prompt: "A wooden cube is painted blue on all 6 faces and then cut into 64 smaller identical cubes (4×4×4). How many small cubes have exactly TWO faces painted blue?",
          formula: "Formula for 2 painted faces = 12 × (n - 2), where n = number of cuts along an edge = 4\n= 12 × (4 - 2) = 12 × 2 = 24",
          options: ["24", "16", "32", "8"],
          correct: 0,
          explanation: "For an n×n×n cube (n=4): Cubes with 2 painted faces lie along the 12 edges (excluding corners) = 12 × (n - 2) = 12 × 2 = 24 cubes."
        },
        {
          id: "apt_nvr_2",
          subtopic: "Cubes & Dice",
          diff: "Easy",
          prompt: "In a standard closed dice, face 1 is opposite 6, face 2 opposite 5, and face 3 opposite 4. If face 4 is on the top and face 5 faces North, which face is on the bottom?",
          formula: "Opposite of Top face (4) = Bottom face (3)",
          options: ["3", "1", "2", "6"],
          correct: 0,
          explanation: "Since opposite of face 4 is face 3, when face 4 is on top, face 3 must be at the bottom."
        }
      ]
    },
    online_tests: {
      name: "Online Mock Tests",
      icon: "⏱️",
      subtopics: ["All", "TCS NQT Full Mock", "Infosys Diagnostic", "Wipro Turbo Test", "Speed Drill"],
      questions: [
        {
          id: "apt_mock_1",
          subtopic: "TCS NQT Full Mock",
          diff: "Hard",
          prompt: "If log₂ x + log₄ x + log₁₆ x = 21/4, what is the exact value of x?",
          formula: "log₄ x = (1/2)log₂ x, log₁₆ x = (1/4)log₂ x\nlog₂ x (1 + 1/2 + 1/4) = log₂ x (7/4) = 21/4 => log₂ x = 3 => x = 2³ = 8",
          options: ["8", "16", "4", "32"],
          correct: 0,
          explanation: "Convert all to base 2: log₂ x + (1/2)log₂ x + (1/4)log₂ x = (7/4)log₂ x. (7/4)log₂ x = 21/4 => log₂ x = 3 => x = 2³ = 8."
        },
        {
          id: "apt_mock_2",
          subtopic: "Infosys Diagnostic",
          diff: "Medium",
          prompt: "Find the unit digit in the expansion of 7^105.",
          formula: "Cyclicity of powers of 7: 7¹=7, 7²=9, 7³=3, 7⁴=1 (Period = 4)\n105 mod 4 = 1 => Unit digit = 7¹ = 7",
          options: ["7", "9", "3", "1"],
          correct: 0,
          explanation: "Powers of 7 cycle in unit digits [7, 9, 3, 1] with period 4. 105 ÷ 4 leaves a remainder of 1. Therefore, unit digit is 7^1 = 7."
        }
      ]
    },
    current_affairs: {
      name: "Current Affairs",
      icon: "🌍",
      subtopics: ["All", "Science & Tech", "AI & Computing", "Economy & Business"],
      questions: [
        {
          id: "apt_ca_1",
          subtopic: "AI & Computing",
          diff: "Easy",
          prompt: "Which AI research milestone introduced the concept of 'Reinforcement Learning from Human Feedback' (RLHF) to align LLMs with user instructions?",
          formula: "Concept: InstructGPT & OpenAI 2022 research popularized RLHF for aligning conversational models safely.",
          options: ["InstructGPT & ChatGPT (OpenAI)", "AlexNet (2012)", "AlphaGo (DeepMind)", "BERT (Google)"],
          correct: 0,
          explanation: "RLHF (Reinforcement Learning from Human Feedback) was pioneered and demonstrated at scale by OpenAI in InstructGPT and ChatGPT to align model outputs with human helpfulness and safety."
        },
        {
          id: "apt_ca_2",
          subtopic: "Science & Tech",
          diff: "Medium",
          prompt: "What is the primary technical distinction of Quantum Computing compared to Classical Computing?",
          formula: "Classical uses Bits (0 or 1); Quantum uses Qubits capable of Superposition and Entanglement.",
          options: ["Qubits exist in superposition of states (0 and 1 simultaneously)", "Quantum computers only execute binary logic 100x faster", "Quantum processors do not generate thermal heat", "Quantum bits cannot be encrypted"],
          correct: 0,
          explanation: "Quantum computers leverage Qubits which, through the quantum mechanical phenomenon of superposition, can represent linear combinations of 0 and 1 simultaneously."
        }
      ]
    },
    gk: {
      name: "General Knowledge",
      icon: "💡",
      subtopics: ["All", "Computer Systems", "Operating Systems Trivia", "Core Science"],
      questions: [
        {
          id: "apt_gk_1",
          subtopic: "Computer Systems",
          diff: "Easy",
          prompt: "Who is widely recognized as the 'Father of Computer Science' and formulated the concept of theoretical Turing Machines?",
          formula: "Historical Foundation: Alan Turing (1912-1954) formulated computation models, Turing completeness, and cryptanalysis.",
          options: ["Alan Turing", "John von Neumann", "Charles Babbage", "Dennis Ritchie"],
          correct: 0,
          explanation: "Alan Turing is considered the father of modern computer science and theoretical artificial intelligence."
        },
        {
          id: "apt_gk_2",
          subtopic: "Operating Systems Trivia",
          diff: "Easy",
          prompt: "Which Linux command displays real-time CPU, memory, and running process utilization metrics interactively?",
          formula: "CLI Tools: 'top' or 'htop' provide dynamic interactive process hierarchy and system health monitoring.",
          options: ["top / htop", "grep", "chmod", "df -h"],
          correct: 0,
          explanation: "'top' (and its enhanced version 'htop') provides real-time interactive process inspection, CPU load average, and RAM memory consumption."
        }
      ]
    },
    hr: {
      name: "HR Interview",
      icon: "👤",
      subtopics: ["All", "STAR Method", "Behavioral Scenarios", "Classic HR"],
      questions: [
        {
          id: "apt_hr_1",
          subtopic: "STAR Method",
          diff: "Easy",
          prompt: "In the STAR interview answering framework, what does 'Result' specifically require the candidate to demonstrate?",
          formula: "STAR: Situation -> Task -> Action -> RESULT (Quantifiable impact, metrics improved, learnings acquired).",
          options: ["Quantifiable positive business/technical outcomes and key learnings", "A list of team members who helped you", "The code repository link", "A description of the company culture"],
          correct: 0,
          explanation: "The Result step must quantify your impact with tangible metrics (e.g. 'reduced latency by 35%', 'resolved 12 critical bugs ahead of sprint deadline') and personal takeaways."
        },
        {
          id: "apt_hr_2",
          subtopic: "Behavioral Scenarios",
          diff: "Medium",
          prompt: "When asked: 'Tell me about a time you had a technical disagreement with a team member', what is the most effective approach?",
          formula: "Best Practice: Ground disagreement in data & test benchmarks, communicate objectively, find consensus, and commit to the team's unified decision.",
          options: ["Explain how you used data/benchmarks objectively, listened to their perspective, and reached a constructive consensus", "Explain that you escalated immediately to senior management", "State that you never have disagreements because you always do what others say", "Insist that your code is always superior and the other person conceded"],
          correct: 0,
          explanation: "Interviewers evaluate emotional intelligence, collaboration, and objective problem-solving through evidence rather than ego."
        }
      ]
    }
  }
};

const aptState = {
  currentCategory: "arithmetic",
  currentSubtopic: "All",
  filteredQuestions: [],
  currentIndex: 0,
  selectedIndex: null,
  isSubmitted: false,
  isHintShown: false,
  timerSeconds: 0,
  timerInterval: null,
  stats: {
    attempted: 0,
    correct: 0,
    totalSeconds: 0
  },
  isMockTest: false
};

function initAptitudeView() {
  bindAptitudeCategoryButtons();
  bindAptitudeActionButtons();
  selectAptitudeCategory("arithmetic");
}

function bindAptitudeCategoryButtons() {
  const catList = document.getElementById("aptitudeCategoryList");
  if (!catList || catList.dataset.bound) return;
  catList.dataset.bound = "true";

  catList.querySelectorAll(".apt-cat-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const catKey = btn.getAttribute("data-category");
      selectAptitudeCategory(catKey);
    });
  });
}

function bindAptitudeActionButtons() {
  const submitBtn = document.getElementById("aptSubmitBtn");
  if (submitBtn && !submitBtn.dataset.bound) {
    submitBtn.dataset.bound = "true";
    submitBtn.addEventListener("click", handleAptitudeSubmit);
  }

  const nextBtn = document.getElementById("aptNextBtn");
  if (nextBtn && !nextBtn.dataset.bound) {
    nextBtn.dataset.bound = "true";
    nextBtn.addEventListener("click", handleAptitudeNext);
  }

  const prevBtn = document.getElementById("aptPrevBtn");
  if (prevBtn && !prevBtn.dataset.bound) {
    prevBtn.dataset.bound = "true";
    prevBtn.addEventListener("click", handleAptitudePrev);
  }

  const hintBtn = document.getElementById("aptHintBtn");
  if (hintBtn && !hintBtn.dataset.bound) {
    hintBtn.dataset.bound = "true";
    hintBtn.addEventListener("click", toggleAptitudeHint);
  }

  const shuffleBtn = document.getElementById("randomAptitudeDrillBtn");
  if (shuffleBtn && !shuffleBtn.dataset.bound) {
    shuffleBtn.dataset.bound = "true";
    shuffleBtn.addEventListener("click", shuffleAptitudeQuestion);
  }

  const mockBtn = document.getElementById("startAptitudeMockBtn");
  if (mockBtn && !mockBtn.dataset.bound) {
    mockBtn.dataset.bound = "true";
    mockBtn.addEventListener("click", startAptitudeMockMode);
  }
}

function selectAptitudeCategory(catKey) {
  const catData = APTITUDE_DATA.categories[catKey];
  if (!catData) return;

  aptState.currentCategory = catKey;
  aptState.currentSubtopic = "All";
  aptState.currentIndex = 0;
  aptState.isMockTest = false;

  // Update active category button in sidebar
  document.querySelectorAll("#aptitudeCategoryList .apt-cat-btn").forEach(btn => {
    if (btn.getAttribute("data-category") === catKey) {
      btn.classList.add("active");
    } else {
      btn.classList.remove("active");
    }
  });

  // Render Subtopics Bar
  renderAptitudeSubtopics(catData.subtopics);

  // Filter and Load Questions
  filterAptitudeQuestions();
}

function renderAptitudeSubtopics(subtopics) {
  const bar = document.getElementById("aptSubtopicsBar");
  if (!bar) return;
  bar.innerHTML = "";

  subtopics.forEach(sub => {
    const pill = document.createElement("button");
    pill.className = `apt-subtopic-pill ${sub === aptState.currentSubtopic ? "active" : ""}`;
    pill.textContent = sub;
    pill.addEventListener("click", () => {
      aptState.currentSubtopic = sub;
      aptState.currentIndex = 0;
      document.querySelectorAll(".apt-subtopic-pill").forEach(p => p.classList.remove("active"));
      pill.classList.add("active");
      filterAptitudeQuestions();
    });
    bar.appendChild(pill);
  });
}

function filterAptitudeQuestions() {
  const catData = APTITUDE_DATA.categories[aptState.currentCategory];
  if (!catData) return;

  if (aptState.currentSubtopic === "All") {
    aptState.filteredQuestions = [...catData.questions];
  } else {
    aptState.filteredQuestions = catData.questions.filter(q => q.subtopic === aptState.currentSubtopic);
  }

  if (aptState.filteredQuestions.length === 0) {
    aptState.filteredQuestions = [...catData.questions];
  }

  renderCurrentAptitudeQuestion();
}

function renderCurrentAptitudeQuestion() {
  const q = aptState.filteredQuestions[aptState.currentIndex];
  if (!q) return;

  aptState.selectedIndex = null;
  aptState.isSubmitted = false;
  aptState.isHintShown = false;
  aptState.timerSeconds = 0;

  // Start question timer
  clearInterval(aptState.timerInterval);
  const timerDisplay = document.getElementById("aptTimerDisplay");
  if (timerDisplay) timerDisplay.textContent = "⏱ 00:00";
  aptState.timerInterval = setInterval(() => {
    aptState.timerSeconds++;
    const m = String(Math.floor(aptState.timerSeconds / 60)).padStart(2, "0");
    const s = String(aptState.timerSeconds % 60).padStart(2, "0");
    if (timerDisplay) timerDisplay.textContent = `⏱ ${m}:${s}`;
  }, 1000);

  // Badges & Meta
  const catBadge = document.getElementById("aptCurrentCatBadge");
  if (catBadge) catBadge.textContent = APTITUDE_DATA.categories[aptState.currentCategory]?.name || "Aptitude";

  const subBadge = document.getElementById("aptCurrentSubtopicBadge");
  if (subBadge) subBadge.textContent = `${q.subtopic} (${aptState.currentIndex + 1}/${aptState.filteredQuestions.length})`;

  const diffBadge = document.getElementById("aptDifficultyBadge");
  if (diffBadge) {
    diffBadge.textContent = q.diff;
    diffBadge.className = `badge ${q.diff === "Easy" ? "badge-success" : q.diff === "Hard" ? "badge-danger" : "badge-warning"}`;
  }

  // Prompt text
  const promptEl = document.getElementById("aptQuestionPrompt");
  if (promptEl) promptEl.textContent = q.prompt;

  // Formula box (hidden initially)
  const formulaBox = document.getElementById("aptFormulaBox");
  const formulaContent = document.getElementById("aptFormulaContent");
  if (formulaBox && formulaContent) {
    formulaBox.style.display = "none";
    formulaContent.textContent = q.formula || "No standard shortcut formula needed for this concept.";
  }

  // Options Grid
  const optionsGrid = document.getElementById("aptOptionsGrid");
  if (optionsGrid) {
    optionsGrid.innerHTML = "";
    const letters = ["A", "B", "C", "D"];
    q.options.forEach((optText, idx) => {
      const btn = document.createElement("button");
      btn.className = "apt-option-btn";
      btn.innerHTML = `
        <span class="apt-option-letter">${letters[idx]}</span>
        <span>${optText}</span>
      `;
      btn.addEventListener("click", () => {
        if (aptState.isSubmitted) return;
        aptState.selectedIndex = idx;
        document.querySelectorAll(".apt-option-btn").forEach(b => b.classList.remove("selected"));
        btn.classList.add("selected");
      });
      optionsGrid.appendChild(btn);
    });
  }

  // Hide solution box
  const solBox = document.getElementById("aptSolutionBox");
  if (solBox) solBox.style.display = "none";

  // Reset Action Buttons
  const submitBtn = document.getElementById("aptSubmitBtn");
  if (submitBtn) submitBtn.style.display = "inline-block";

  const nextBtn = document.getElementById("aptNextBtn");
  if (nextBtn) nextBtn.style.display = "none";

  const prevBtn = document.getElementById("aptPrevBtn");
  if (prevBtn) prevBtn.disabled = (aptState.currentIndex === 0);
}

function handleAptitudeSubmit() {
  if (aptState.selectedIndex === null) {
    showToast("Please select an option before submitting!");
    return;
  }
  if (aptState.isSubmitted) return;

  clearInterval(aptState.timerInterval);
  aptState.isSubmitted = true;

  const q = aptState.filteredQuestions[aptState.currentIndex];
  const isCorrect = (aptState.selectedIndex === q.correct);

  // Update Stats
  aptState.stats.attempted++;
  if (isCorrect) aptState.stats.correct++;
  aptState.stats.totalSeconds += aptState.timerSeconds;

  updateAptitudeStatsUI();

  // Highlight Options
  const optionButtons = document.querySelectorAll(".apt-option-btn");
  optionButtons.forEach((btn, idx) => {
    btn.classList.add("disabled");
    if (idx === q.correct) {
      btn.classList.add("correct");
    } else if (idx === aptState.selectedIndex && !isCorrect) {
      btn.classList.add("wrong");
    }
  });

  // Display Solution Box
  const solBox = document.getElementById("aptSolutionBox");
  const resultStatus = document.getElementById("aptResultStatus");
  const explText = document.getElementById("aptExplanationText");

  if (solBox && resultStatus && explText) {
    resultStatus.textContent = isCorrect ? "✅ Correct Answer!" : "❌ Incorrect (See Step-by-Step Breakdown)";
    resultStatus.style.color = isCorrect ? "var(--accent-emerald)" : "var(--accent-rose)";
    explText.textContent = q.explanation;
    solBox.style.display = "block";
  }

  // Record genuine response to backend
  try {
    API.logDirectResponse({
      user_id: state.currentUserId,
      question_id: q.id || `apt_${aptState.currentCategory}_${aptState.currentIndex}`,
      selected_index: aptState.selectedIndex,
      is_correct: isCorrect,
      response_time_sec: Math.max(4.0, aptState.timerSeconds || 15.0),
      subtopic: q.subtopic || "Aptitude & Probability",
      topic: APTITUDE_DATA.categories[aptState.currentCategory]?.name || "Quantitative Reasoning",
      skill: "Aptitude",
      difficulty: q.difficulty || 2
    }).then(() => {
      refreshAllViews();
    }).catch(err => console.warn("Aptitude backend logging warning:", err));
  } catch (err) {
    console.warn("Aptitude logging failed:", err);
  }

  // Toggle Action Buttons
  const submitBtn = document.getElementById("aptSubmitBtn");
  if (submitBtn) submitBtn.style.display = "none";

  const nextBtn = document.getElementById("aptNextBtn");
  if (nextBtn) nextBtn.style.display = "inline-block";

  showToast(isCorrect ? "🎯 Excellent! Correct answer recorded." : "💡 Solution recorded & explained below.");
}

function handleAptitudeNext() {
  if (aptState.currentIndex < aptState.filteredQuestions.length - 1) {
    aptState.currentIndex++;
    renderCurrentAptitudeQuestion();
  } else {
    showToast("🎉 You reached the end of this subtopic! Shuffling questions...");
    aptState.currentIndex = 0;
    renderCurrentAptitudeQuestion();
  }
}

function handleAptitudePrev() {
  if (aptState.currentIndex > 0) {
    aptState.currentIndex--;
    renderCurrentAptitudeQuestion();
  }
}

function toggleAptitudeHint() {
  const formulaBox = document.getElementById("aptFormulaBox");
  if (!formulaBox) return;
  aptState.isHintShown = !aptState.isHintShown;
  formulaBox.style.display = aptState.isHintShown ? "block" : "none";
}

function shuffleAptitudeQuestion() {
  if (aptState.filteredQuestions.length > 1) {
    let nextIdx = Math.floor(Math.random() * aptState.filteredQuestions.length);
    if (nextIdx === aptState.currentIndex) {
      nextIdx = (nextIdx + 1) % aptState.filteredQuestions.length;
    }
    aptState.currentIndex = nextIdx;
  }
  renderCurrentAptitudeQuestion();
  showToast("🎲 Loaded a random placement aptitude question.");
}

function startAptitudeMockMode() {
  aptState.isMockTest = true;
  // Combine questions across all categories for a 10-Q comprehensive mock
  const allQs = [];
  Object.values(APTITUDE_DATA.categories).forEach(cat => {
    allQs.push(...cat.questions);
  });
  
  // Shuffle array
  for (let i = allQs.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [allQs[i], allQs[j]] = [allQs[j], allQs[i]];
  }

  aptState.filteredQuestions = allQs.slice(0, 10);
  aptState.currentIndex = 0;
  aptState.currentCategory = "online_tests";
  aptState.currentSubtopic = "All";

  document.querySelectorAll("#aptitudeCategoryList .apt-cat-btn").forEach(btn => {
    if (btn.getAttribute("data-category") === "online_tests") {
      btn.classList.add("active");
    } else {
      btn.classList.remove("active");
    }
  });

  renderCurrentAptitudeQuestion();
  showToast("⚡ Starting 10-Question Timed Placement Mock Assessment!");
}

function updateAptitudeStatsUI() {
  const attemptedEl = document.getElementById("aptStatAttempted");
  if (attemptedEl) attemptedEl.textContent = aptState.stats.attempted;

  const accEl = document.getElementById("aptStatAccuracy");
  const accuracy = aptState.stats.attempted > 0 
    ? Math.round((aptState.stats.correct / aptState.stats.attempted) * 100) 
    : 0;
  if (accEl) accEl.textContent = `${accuracy}%`;

  const timeEl = document.getElementById("aptStatAvgTime");
  const avgSeconds = aptState.stats.attempted > 0
    ? Math.round(aptState.stats.totalSeconds / aptState.stats.attempted)
    : 0;
  if (timeEl) timeEl.textContent = `${avgSeconds}s`;

  const boostEl = document.getElementById("aptStatReadiness");
  const boost = (aptState.stats.correct * 0.75).toFixed(1);
  if (boostEl) boostEl.textContent = `+${boost}%`;
}
