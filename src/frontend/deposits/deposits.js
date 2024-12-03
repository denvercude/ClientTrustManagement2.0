document.getElementById("deposits-sheet-btn").addEventListener("click", () => {
    window.electronAPI.navigateTo("deposits/deposits_sheet/deposits_sheet.html"); 
  });

document.getElementById("add-deposits-btn").addEventListener("click", () => {
window.electronAPI.navigateTo("deposits/add_deposits/add_deposits.html");
});