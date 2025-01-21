document.getElementById("create-store-list-btn").addEventListener("click", () => {
    window.electronAPI.navigateTo("manage_store/create_list/create_list.html"); 
  });

document.getElementById("add-patients-btn").addEventListener("click", () => {
  window.electronAPI.navigateTo("manage_store/add_patients_store/add_patients.html"); 
});

document.getElementById("remove-patients-btn").addEventListener("click", () => {
  window.electronAPI.navigateTo("manage_store/remove_patients_store/remove_patients.html"); 
});