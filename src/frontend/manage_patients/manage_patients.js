document.getElementById("admissions-btn").addEventListener("click", () => {
    window.electronAPI.navigateTo("manage_patients/admissions/admissions.html"); 
  });

document.getElementById("discharges-btn").addEventListener("click", () => {
window.electronAPI.navigateTo("manage_patients/discharges/discharges.html");
});

document.getElementById("update-phase-btn").addEventListener("click", () => {
window.electronAPI.navigateTo("manage_patients/update_phase/update_phase.html");
});