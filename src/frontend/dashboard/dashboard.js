document.getElementById("manage-patients-btn").addEventListener("click", () => {
    window.electronAPI.navigateTo("manage_patients/manage_patients.html"); 
  });

document.getElementById("deposits-btn").addEventListener("click", () => {
  window.electronAPI.navigateTo("deposits/deposits.html"); 
});

document.getElementById("store-btn").addEventListener("click", () => {
  window.electronAPI.navigateTo("manage_store/manage_store.html"); 
});