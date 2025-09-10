const urlInput = document.getElementById("urlInput");
const checkBtn = document.getElementById("checkBtn");
const backBtn = document.getElementById("backBtn");

const inputScreen = document.getElementById("inputScreen");
const resultScreen = document.getElementById("resultScreen");
const typoList = document.getElementById("typoList");

function checkUrl() {
  const url = urlInput.value.trim();

  if (!url) {
    alert("Please enter a URL.");
    return;
  }

  // 🔮 Placeholder typosquatted results
  const typos = [
    `${url.replace(".com", ".co")}`,
    `${url.replace(".com", ".cm")}`,
    `www-${url}`,
    `${url}123.com`
  ];

  // Clear old list
  typoList.innerHTML = "";

  // Populate list
  typos.forEach(t => {
    const li = document.createElement("li");
    li.textContent = t;
    typoList.appendChild(li);
  });

  // Switch to results screen
  inputScreen.style.display = "none";
  resultScreen.style.display = "block";
}

checkBtn.addEventListener("click", checkUrl);

urlInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    checkUrl();
  }
});

backBtn.addEventListener("click", () => {
  resultScreen.style.display = "none";
  inputScreen.style.display = "block";
  urlInput.value = "";
});
