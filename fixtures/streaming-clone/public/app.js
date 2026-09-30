"use strict";

const loginView = document.getElementById("login-view");
const catalogView = document.getElementById("catalog-view");
const logoutBtn = document.getElementById("logout-btn");
const loginForm = document.getElementById("login-form");
const loginError = document.getElementById("login-error");
const rowsEl = document.getElementById("rows");

const modal = document.getElementById("detail-modal");
const closeModalBtn = document.getElementById("close-modal");
const detailTitle = document.getElementById("detail-title");
const detailCategory = document.getElementById("detail-category");
const detailSynopsis = document.getElementById("detail-synopsis");
const detailVideo = document.getElementById("detail-video");
const videoUnavailable = document.getElementById("video-unavailable");

function showCatalog() {
  loginView.classList.add("hidden");
  catalogView.classList.remove("hidden");
  logoutBtn.classList.remove("hidden");
}

function showLogin() {
  catalogView.classList.add("hidden");
  loginView.classList.remove("hidden");
  logoutBtn.classList.add("hidden");
}

async function checkSession() {
  const res = await fetch("/api/session");
  const data = await res.json();
  if (data.loggedIn) {
    showCatalog();
    loadCatalog();
  } else {
    showLogin();
  }
}

loginForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  loginError.classList.add("hidden");
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;
  const res = await fetch("/api/login", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });
  if (res.ok) {
    showCatalog();
    loadCatalog();
  } else {
    loginError.classList.remove("hidden");
  }
});

logoutBtn.addEventListener("click", async () => {
  await fetch("/api/logout", { method: "POST" });
  showLogin();
});

async function loadCatalog() {
  const res = await fetch("/api/catalog");
  if (!res.ok) {
    showLogin();
    return;
  }
  const { rows } = await res.json();
  rowsEl.innerHTML = "";
  for (const row of rows) {
    const section = document.createElement("section");
    section.className = "row";

    const heading = document.createElement("h2");
    heading.textContent = row.category;
    section.appendChild(heading);

    const tiles = document.createElement("div");
    tiles.className = "tiles";
    for (const title of row.titles) {
      const tile = document.createElement("div");
      tile.className = "tile";
      tile.dataset.id = title.id;

      const img = document.createElement("img");
      img.src = title.poster;
      img.alt = title.title;
      tile.appendChild(img);

      const label = document.createElement("div");
      label.className = "tile-title";
      label.textContent = title.title;
      tile.appendChild(label);

      tile.addEventListener("click", () => openDetail(title.id));
      tiles.appendChild(tile);
    }
    section.appendChild(tiles);
    rowsEl.appendChild(section);
  }
}

async function openDetail(id) {
  const res = await fetch(`/api/titles/${id}`);
  if (!res.ok) return;
  const title = await res.json();

  detailTitle.textContent = title.title;
  detailCategory.textContent = title.category;
  detailSynopsis.textContent = title.synopsis;

  videoUnavailable.classList.add("hidden");
  detailVideo.classList.remove("hidden");
  detailVideo.src = title.video;
  detailVideo.onerror = () => {
    detailVideo.classList.add("hidden");
    videoUnavailable.classList.remove("hidden");
  };

  modal.classList.remove("hidden");
}

closeModalBtn.addEventListener("click", () => {
  modal.classList.add("hidden");
  detailVideo.pause();
  detailVideo.removeAttribute("src");
  detailVideo.load();
});

checkSession();
