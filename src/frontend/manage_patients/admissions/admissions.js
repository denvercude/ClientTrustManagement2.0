document.addEventListener("DOMContentLoaded", () => {
  loadHeader("Admissions");

  const tableBody = document.querySelector("#admissions-table tbody");
  const successList = document.querySelector("#success-list");
  const errorList = document.querySelector("#error-list");

  const fields = ["First Name", "Last Name", "Contract"];

  for (let i = 0; i < 5; i++) {
    addRow(tableBody, fields);
  }

  document.getElementById("add-row").addEventListener("click", () => {
    addRow(tableBody, fields);
  });

  document.getElementById("add-all").addEventListener("click", async () => {
    const rows = Array.from(tableBody.querySelectorAll("tr"));
    const patients = rows.map(row => {
      const inputs = row.querySelectorAll("input");
      return {
        first_name: inputs[0].value.trim(),
        last_name: inputs[1].value.trim(),
        contract: inputs[2].value.trim(),
      };
    });

    await sendPatients(patients, "http://127.0.0.1:8000/add-patient/");

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
  