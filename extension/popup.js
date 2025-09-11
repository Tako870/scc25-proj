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

  API.addTypos({ website: url }, (status, data) => {
    console.log('Status:', status);
    console.log('Data:', data);
    if (status === 200) {
      // Clear old list
      typoList.innerHTML = "";

      // Populate list with preview cards
      data.domains.forEach(t => {
        const card = document.createElement("div");
        card.className = "preview-card";

        const favicon = document.createElement("img");
        // placeholder favicon (real one would use https://www.google.com/s2/favicons)
        favicon.src = "https://www.google.com/s2/favicons?sz=64&domain_url=" + t;

        const info = document.createElement("div");
        info.className = "preview-info";

        const domain = document.createElement("p");
        domain.className = "preview-domain";
        domain.textContent = t;

        const note = document.createElement("p");
        note.textContent = "Registered: placeholder date";

        info.appendChild(domain);
        info.appendChild(note);

        card.appendChild(favicon);
        card.appendChild(info);

        typoList.appendChild(card);
      });

      // Switch to results screen
      inputScreen.style.display = "none";
      resultScreen.style.display = "block";
    } else {
      alert("Error checking URL: " + data.error);
    }
  });
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
