const urlInput = document.getElementById("urlInput");
const checkBtn = document.getElementById("checkBtn");
const backBtn = document.getElementById("backBtn");

const inputScreen = document.getElementById("inputScreen");
const resultScreen = document.getElementById("resultScreen");
const typoList = document.getElementById("typoList");

function checkUrl() {
  const url = urlInput.value.trim();

  if (!url) {
    alert("Please enter a URL in the form www.example.com.");
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
        favicon.src = "https://www.google.com/s2/favicons?sz=64&domain_url=" + t.domain;
        favicon.className = "preview-favicon";

        const info = document.createElement("div");
        info.className = "preview-info";

        const domainName = document.createElement("h4");
        domainName.textContent = t.domain;

        const table = document.createElement("table");
        table.className = "domain-table";

        const fields = [
          ["Created", t.creation_date || "N/A"],
          ["Registrar", t.registrar || "N/A"],
          ["Name servers", t.name_servers ? t.name_servers.join(", ") : "N/A"],
          ["Similarity", t.similarity || "N/A"],
          ["Flags", t.flags && t.flags.length > 0 ? t.flags.join(", ") : "None"]
        ];

        fields.forEach(([label, value]) => {
          const row = document.createElement("tr");
          const th = document.createElement("th");
          th.textContent = label;
          const td = document.createElement("td");
          td.textContent = value;
          row.appendChild(th);
          row.appendChild(td);
          table.appendChild(row);
        });

        info.appendChild(domainName);
        info.appendChild(table);

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
