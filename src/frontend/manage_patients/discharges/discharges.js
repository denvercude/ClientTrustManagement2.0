document.addEventListener("DOMContentLoaded", () => {
  loadHeader("Discharges");

  const tableBody = document.querySelector("#discharges-table tbody");
  const fields = ["First Name", "Last Name", "Reason for Discharge"];

  for (let i = 0; i < 5; i++) {
    addRow(tableBody, fields);
  }

  document.getElementById("add-row").addEventListener("click", () => {
    addRow(tableBody, fields);
  });

  document.getElementById("discharge-all").addEventListener("click", async () => {
    const rows = Array.from(tableBody.querySelectorAll("tr"));
    const patients = rows.map(row => {
      const inputs = row.querySelectorAll("input");
      return {
        first_name: inputs[0].value.trim(),
        last_name: inputs[1].value.trim(),
        reason_for_discharge: inputs[2].value.trim(),
      };
    });

    await sendPatients(patients, "http://127.0.0.1:8000/discharge-patient/", "PUT");

    rows.forEach(row => {
      const inputs = row.querySelectorAll("input");
      inputs.forEach(input => {
        input.value = "";
      });
    });
  });

  document.getElementById("clear-list").addEventListener("click", async () => {
    clearStatusLists()
  });

});