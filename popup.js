const urlInput = document.getElementById("urlInput");
const result = document.getElementById("result");
const checkBtn = document.getElementById("checkBtn");

function checkUrl() {
  const url = urlInput.value.trim();

  if (!url) {
    result.textContent = "Please enter a URL.";
    return;
  }

  // Placeholder check (later: add typosquatting detection logic here)
  result.textContent = `You entered: ${url}`;
}

checkBtn.addEventListener("click", checkUrl);

// Also handle Enter key
urlInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    checkUrl();
  }
});
