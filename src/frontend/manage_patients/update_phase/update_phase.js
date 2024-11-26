document.addEventListener("DOMContentLoaded", () => {
    loadHeader("Update Phase");
  
    const tableBody = document.querySelector("#phase-table tbody");
    const successList = document.querySelector("#success-list");
    const errorList = document.querySelector("#error-list");
  
    const fields = ["First Name", "Last Name", "New Phase"];
  
    for (let i = 0; i < 5; i++) {
      addRow(tableBody, fields);
    }
  
    document.getElementById("add-row").addEventListener("click", () => {
      addRow(tableBody, fields);
    });
  
    document.getElementById("update-all").addEventListener("click", async () => {
      const rows = Array.from(tableBody.querySelectorAll("tr"));
      const patients = rows.map(row => {
        const inputs = row.querySelectorAll("input");
        return {
          first_name: inputs[0].value.trim(),
          last_name: inputs[1].value.trim(),
          new_phase: parseInt(inputs[2].value.trim(), 10),
        };
      });
  
      successList.innerHTML = "";
      errorList.innerHTML = "";

      for (const patient of patients) {
        if (patient.first_name && patient.last_name && !isNaN(patient.new_phase)) {
          try {
            const response = await fetch("http://127.0.0.1:8000/update-phase/", {
              method: "PUT",
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
              const li = document.createElement("li");
              li.textContent = `${patient.first_name} ${patient.last_name} - Error: ${result.detail || "Unknown error"}`;
              li.classList.add("error");
              errorList.appendChild(li);
            }
          } catch (error) {
            console.error("Error:", error);
            const li = document.createElement("li");
            li.textContent = `${patient.first_name} ${patient.last_name} - Error: Network or Server Error`;
            li.classList.add("error");
            errorList.appendChild(li);
          }
        }
      }

      rows.forEach(row => {
        const inputs = row.querySelectorAll("input");
        inputs.forEach(input => {
          input.value = "";
        });
      });
    });
  });
  