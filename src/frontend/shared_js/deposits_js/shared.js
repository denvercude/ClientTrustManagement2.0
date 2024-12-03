function loadHeader(pageTitle) {
    const headerHTML = `
        <div class="header">
        <button onclick="location.href='../../dashboard/dashboard.html'">Dashboard</button>
        <button onclick="location.href='../deposits.html'">Back</button>
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