let skillRadarChart = null;
let roleComparisonChart = null;
let researchTrajectoryChart = null;
let researchDistributionChart = null;

const Charts = {
  renderReadinessDial(score) {
    const dialContainer = document.getElementById("readinessDialSvg");
    if (!dialContainer) return;

    // SVG circular progress bar calculation
    const radius = 52;
    const circumference = 2 * Math.PI * radius;
    const offset = circumference - (score / 100) * circumference;

    let strokeColor = "#f43f5e"; // Rose (<50)
    if (score >= 80) strokeColor = "#10b981"; // Emerald
    else if (score >= 65) strokeColor = "#6366f1"; // Indigo
    else if (score >= 50) strokeColor = "#f59e0b"; // Amber

    dialContainer.innerHTML = `
      <svg width="130" height="130" viewBox="0 0 130 130">
        <circle cx="65" cy="65" r="${radius}" stroke="#1f2937" stroke-width="10" fill="none" />
        <circle cx="65" cy="65" r="${radius}" stroke="${strokeColor}" stroke-width="10" 
                stroke-dasharray="${circumference}" stroke-dashoffset="${offset}" 
                stroke-linecap="round" fill="none"
                style="transition: stroke-dashoffset 1s ease-in-out;"
                transform="rotate(-90 65 65)" />
      </svg>
    `;
    
    const scoreValEl = document.getElementById("heroScoreVal");
    if (scoreValEl) scoreValEl.innerText = `${score}%`;
  },

  renderSkillRadar(skillBreakdown) {
    const ctx = document.getElementById("skillRadarCanvas");
    if (!ctx) return;

    if (skillRadarChart) {
      skillRadarChart.destroy();
    }

    const labels = skillBreakdown.map(s => s.skill);
    const dataScores = skillBreakdown.map(s => s.score);
    const dataWeights = skillBreakdown.map(s => Math.round(s.weight_in_role * 100));

    skillRadarChart = new Chart(ctx, {
      type: "radar",
      data: {
        labels: labels,
        datasets: [
          {
            label: "Candidate Mastery (%)",
            data: dataScores,
            backgroundColor: "rgba(99, 102, 241, 0.25)",
            borderColor: "#6366f1",
            pointBackgroundColor: "#818cf8",
            pointBorderColor: "#fff",
            borderWidth: 2
          },
          {
            label: "Role Importance Weight (%)",
            data: dataWeights,
            backgroundColor: "rgba(6, 182, 212, 0.15)",
            borderColor: "#06b6d4",
            borderDash: [4, 4],
            pointBackgroundColor: "#06b6d4",
            borderWidth: 1.5
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          r: {
            angleLines: { color: "rgba(255, 255, 255, 0.08)" },
            grid: { color: "rgba(255, 255, 255, 0.08)" },
            pointLabels: {
              color: "#94a3b8",
              font: { size: 11, family: "Inter", weight: "600" }
            },
            ticks: {
              backdropColor: "transparent",
              color: "#64748b",
              stepSize: 20
            },
            min: 0,
            max: 100
          }
        },
        plugins: {
          legend: {
            labels: { color: "#cbd5e1", font: { size: 11, family: "Inter" } }
          }
        }
      }
    });
  },

  renderRoleComparisonChart(comparisons) {
    const ctx = document.getElementById("roleComparisonCanvas");
    if (!ctx) return;

    if (roleComparisonChart) {
      roleComparisonChart.destroy();
    }

    const labels = comparisons.map(c => c.role_title);
    const scores = comparisons.map(c => c.readiness_score);
    const backgroundColors = comparisons.map(c => 
      c.is_current_target ? "#6366f1" : "rgba(148, 163, 184, 0.35)"
    );

    roleComparisonChart = new Chart(ctx, {
      type: "bar",
      data: {
        labels: labels,
        datasets: [{
          label: "Readiness Score (%)",
          data: scores,
          backgroundColor: backgroundColors,
          borderRadius: 6,
          borderWidth: 0
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        indexAxis: 'y',
        scales: {
          x: {
            grid: { color: "rgba(255, 255, 255, 0.06)" },
            ticks: { color: "#94a3b8" },
            min: 0,
            max: 100
          },
          y: {
            grid: { display: false },
            ticks: { color: "#cbd5e1", font: { size: 11, weight: "500" } }
          }
        },
        plugins: {
          legend: { display: false }
        }
      }
    });
  },

  renderResearchCharts(experimentData) {
    const trajCtx = document.getElementById("researchTrajectoryCanvas");
    const distCtx = document.getElementById("researchDistributionCanvas");

    if (trajCtx) {
      if (researchTrajectoryChart) researchTrajectoryChart.destroy();
      
      const traj = experimentData.trajectory_data;
      researchTrajectoryChart = new Chart(trajCtx, {
        type: "line",
        data: {
          labels: traj.days,
          datasets: [
            {
              label: "Group B (Adaptive AI System)",
              data: traj.group_b_curve,
              borderColor: "#10b981",
              backgroundColor: "rgba(16, 185, 129, 0.1)",
              fill: true,
              tension: 0.3,
              borderWidth: 3,
              pointRadius: 4
            },
            {
              label: "Group A (Fixed Question Bank)",
              data: traj.group_a_curve,
              borderColor: "#94a3b8",
              borderDash: [5, 5],
              tension: 0.3,
              borderWidth: 2,
              pointRadius: 3
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              title: { display: true, text: "Placement Readiness Score (%)", color: "#94a3b8" },
              grid: { color: "rgba(255, 255, 255, 0.06)" },
              ticks: { color: "#cbd5e1" },
              min: 30,
              max: 100
            },
            x: {
              grid: { color: "rgba(255, 255, 255, 0.06)" },
              ticks: { color: "#94a3b8" }
            }
          },
          plugins: {
            legend: { labels: { color: "#cbd5e1", font: { family: "Inter" } } }
          }
        }
      });
    }

    if (distCtx) {
      if (researchDistributionChart) researchDistributionChart.destroy();

      const mA = experimentData.group_a_fixed;
      const mB = experimentData.group_b_adaptive;

      researchDistributionChart = new Chart(distCtx, {
        type: "bar",
        data: {
          labels: ["Pre-Test Mean", "Post-Test Mean", "Weak Topics Resolved %"],
          datasets: [
            {
              label: "Group A (Control - Fixed)",
              data: [mA.pre_test_mean, mA.post_test_mean, mA.weak_topic_resolution_rate_pct],
              backgroundColor: "rgba(148, 163, 184, 0.5)",
              borderRadius: 6
            },
            {
              label: "Group B (Adaptive AI)",
              data: [mB.pre_test_mean, mB.post_test_mean, mB.weak_topic_resolution_rate_pct],
              backgroundColor: "rgba(16, 185, 129, 0.8)",
              borderRadius: 6
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            y: {
              grid: { color: "rgba(255, 255, 255, 0.06)" },
              ticks: { color: "#94a3b8" },
              min: 0,
              max: 100
            },
            x: {
              grid: { display: false },
              ticks: { color: "#cbd5e1" }
            }
          },
          plugins: {
            legend: { labels: { color: "#cbd5e1" } }
          }
        }
      });
    }
  }
};
