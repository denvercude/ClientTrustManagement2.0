function loadHeader(pageTitle) {
    const headerHTML = `
      <div class="header">
        <button onclick="location.href='../../dashboard/dashboard.html'">Dashboard</button>
        <button onclick="location.href='../manage_patients.html'">Back</button>
        <div class="title">${pageTitle}</div>
      </div>
    `;
    document.body.insertAdjacentHTML("afterbegin", headerHTML);
  }

  function addRow(tableBody, fields, values = []) {
    const row = document.createElement("tr");
    fields.forEach((field, index) => {
      const value = values[index] || "";
      const cell = document.createElement("td");
      cell.innerHTML = `<input type="text" placeholder="${field}" value="${value}" />`;
      row.appendChild(cell);
    });
    tableBody.appendChild(row);
  }

  async function sendPatients(patients, url, method = "POST") {
    const successList = document.querySelector("#success-list");
    const errorList = document.querySelector("#error-list");
  
    for (const patient of patients) {
      if (Object.values(patient).every(value => value.trim())) {
        try {
          const response = await fetch(url, {
            method: method,
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(patient),
          });
          const result = await response.json();
          if (response.ok) {
            const li = document.createElement("li");
            li.textContent = `${patient.first_name} ${patient.last_name}`;
            li.classList.add("success");
            successList.appendChild(li);
          } else {
            handleAPIError(patient, result.detail || "Unknown error");
          }
        } catch (error) {
          console.error("Error:", error);
          handleAPIError(patient, "Network or Server Error");
        }
      }
    }
  }
  
  function handleAPIError(patient, message) {
    const errorList = document.querySelector("#error-list");
    const li = document.createElement("li");
    li.textContent = `${patient.first_name} ${patient.last_name} - Error: ${message}`;
    li.classList.add("error");
    errorList.appendChild(li);
  }
  
  function clearStatusLists() {
    document.querySelector("#success-list").innerHTML = "";
    document.querySelector("#error-list").innerHTML = "";
  }