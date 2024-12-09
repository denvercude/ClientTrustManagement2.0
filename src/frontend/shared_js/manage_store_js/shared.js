function loadHeader(pageTitle) {
    const headerHTML = `
      <div class="header">
        <button onclick="location.href='../../dashboard/dashboard.html'">Dashboard</button>
        <button onclick="location.href='../manage_store.html'">Back</button>
        <div class="title">${pageTitle}</div>
      </div>
    `;
    document.body.insertAdjacentHTML("afterbegin", headerHTML);
  }