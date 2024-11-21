let currentPage = 1;
const totalPages = 5;

function showPage(page) {
  document
    .querySelectorAll(".form-page")
    .forEach((pageElement) => (pageElement.style.display = "none"));
  document.getElementById(`page-${page}`).style.display = "block";
}

function nextPage() {
  if (currentPage < totalPages) {
    currentPage++;
    showPage(currentPage);
  }
}

function prevPage() {
  if (currentPage > 1) {
    currentPage--;
    showPage(currentPage);
  }
}

function submitSurvey() {
  // Collect responses from all pages (example with first three questions)
  const q1 = parseInt(document.getElementById("q1").value) || 0;
  const q2 = parseInt(document.getElementById("q2").value) || 0;
  const q3 = parseInt(document.getElementById("q3").value) || 0;

  // Determine the stage based on responses
  let stage = 1;

  if (q1 === 2 || q2 === 2 || q3 === 2) {
    stage = 6;
  } else if (q1 === 1 || q2 === 1 || q3 === 1) {
    stage = 4;
  } else {
    stage = 2;
  }

  // Call displayStage to show the visualization
  displayStage(stage);
}

function displayStage(stage) {
  const stageBar = document.getElementById("stage-bar");
  stageBar.innerHTML = ""; // Clear previous stages

  for (let i = 1; i <= 6; i++) {
    const stageDiv = document.createElement("div");
    stageDiv.classList.add("stage", `stage${i}`);
    stageDiv.textContent = `Stage ${i}`;
    stageDiv.style.backgroundColor = i === stage ? "#333" : "#cccccc"; // Highlight only the selected stage
    stageBar.appendChild(stageDiv);
  }

  const stageDescriptions = [
    "Immediate Grief, Shock & Emotion",
    "Navigating Family Relationships",
    "Learning to Process Grief",
    "Moments That Matter",
    "Feeling Immersed, Connected & Seen",
    "New Growth & Purpose",
  ];

  document.getElementById("stage-description").textContent =
    stageDescriptions[stage - 1];
  document.getElementById("grief-stage-visualization").style.display = "block"; // Show the visualization section
}

// Initialize the first page
showPage(currentPage);
